from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from xhtml2pdf import pisa
import io
from .models import QuoteRequest
from market.models import Product

def request_quote(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        email = request.POST.get("email")
        message = request.POST.get("message", "")
        qr = QuoteRequest.objects.create(product=product, requester=request.user if request.user.is_authenticated else None, email=email, message=message)
        # render PDF from template
        html = render_to_string("quotes/quote_pdf.html", {"product": product, "request": qr})
        result = io.BytesIO()
        pisa_status = pisa.CreatePDF(src=html, dest=result)
        if not pisa_status.err:
            pdf = result.getvalue()
            mail = EmailMessage(
                subject=f"Presupuesto para {product.title}",
                body="Adjuntamos el presupuesto solicitado.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
            )
            mail.attach(f"presupuesto_{qr.id}.pdf", pdf, "application/pdf")
            mail.send()
        # redirigir con mensaje
        return HttpResponseRedirect("/gracias-presupuesto/")
    return render(request, "quotes/request_quote.html", {"product": product})