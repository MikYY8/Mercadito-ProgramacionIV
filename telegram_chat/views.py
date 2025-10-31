import os
import requests
import json
import threading
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import TelegramMessage
from .forms import MessageForm
from django.views.decorators.csrf import csrf_exempt
from config.settings import TELEGRAM_BOT_TOKEN, CHAT_ID

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

def chat_view(request):
    form = MessageForm()

    # --- POST: enviar mensaje ---
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.cleaned_data.get('message')
            photo = form.cleaned_data.get('photo')
            audio = form.cleaned_data.get('audio')

            # --- Enviar imagen ---
            if photo:
                path = default_storage.save(f"telegram_photos/{photo.name}", photo)
                full_path = os.path.join(settings.MEDIA_ROOT, path)
                with open(full_path, 'rb') as img_file:
                    requests.post(
                        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto",
                        data={"chat_id": CHAT_ID},
                        files={"photo": img_file}
                    )
                TelegramMessage.objects.create(sender='Tú', photo=path)

            # --- Enviar audio ---
            elif audio:
                path = default_storage.save(f"telegram_audios/{audio.name}", audio)
                full_path = os.path.join(settings.MEDIA_ROOT, path)
                with open(full_path, 'rb') as audio_file:
                    requests.post(
                        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendAudio",
                        data={"chat_id": CHAT_ID},
                        files={"audio": audio_file}
                    )
                TelegramMessage.objects.create(sender='Tú', audio=path)

            # --- Enviar texto ---
            elif text:
                    threading.Thread(
                    target=requests.post,
                    args=(
                        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                    ),
                    kwargs={"data": {"chat_id": CHAT_ID, "text": text}},
                    daemon=True
                ).start()
                    TelegramMessage.objects.create(sender='Tú', text=text)

            return render(request, 'chat.html', {'form': MessageForm(), 'messages': TelegramMessage.objects.all().order_by('date')})


    # --- Obtener mensajes del bot de Telegram ---
    last_update_id = request.session.get('last_update_id', 0)

    updates = requests.get(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates").json()

    if updates.get("ok"):
        for update in updates["result"]:
            msg = update.get("message")
            if not msg:
                continue

            sender_name = msg["from"]["first_name"]

            # --- Texto ---
            text = msg.get("text")
            if text and not TelegramMessage.objects.filter(sender=sender_name, text=text).exists():
                TelegramMessage.objects.create(sender=sender_name, text=text)

            # --- Imagen ---
            if "photo" in msg:
                file_id = msg["photo"][-1]["file_id"]
                file_info = requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getFile?file_id={file_id}").json()
                file_path = file_info["result"]["file_path"]
                response = requests.get(f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}")
                file_name = os.path.basename(file_path)
                saved_path = default_storage.save(f"telegram_photos/{file_name}", ContentFile(response.content))
                if not TelegramMessage.objects.filter(sender=sender_name, photo=saved_path).exists():
                    TelegramMessage.objects.create(sender=sender_name, photo=saved_path)

            # --- Audio / Voz ---
            if "voice" in msg or "audio" in msg:
                file_id = msg.get("voice", msg.get("audio"))["file_id"]
                file_info = requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getFile?file_id={file_id}").json()
                file_path = file_info["result"]["file_path"]
                response = requests.get(f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}")
                file_name = os.path.basename(file_path)
                saved_path = default_storage.save(f"telegram_audios/{file_name}", ContentFile(response.content))
                if not TelegramMessage.objects.filter(sender=sender_name, audio=saved_path).exists():
                    TelegramMessage.objects.create(sender=sender_name, audio=saved_path)

            # Actualizar último update_id
            last_update_id = update["update_id"]

    request.session['last_update_id'] = last_update_id

    messages = TelegramMessage.objects.all().order_by('date')

    # --- Si es AJAX, devolver JSON ---
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = []
        for msg in messages:
            data.append({
                'sender': msg.sender,
                'text': msg.text,
                'photo': msg.photo.url if msg.photo else '',
                'audio': msg.audio.url if msg.audio else '',
            })
        return JsonResponse({'messages': data})

    return render(request, 'chat.html', {'form': form, 'messages': messages})

@csrf_exempt
def post_message(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text = data.get("text", "").strip()

            print("🟣 LLEGA POST A DJANGO:", text)

            if text:
                response = requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                    data={"chat_id": CHAT_ID, "text": text},
                )
                print("💬 Enviando a Telegram:", response.text)
                return JsonResponse({"status": "ok", "telegram_response": response.json()})

            return JsonResponse({"status": "error", "message": "sin texto"})

        except Exception as e:
            print("❌ ERROR:", e)
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "método no permitido"})