from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")  # o a donde quieras
    else:
        form = ProfileForm(instance=profile)

    return render(request, "profile_edit.html", {"form": form})

@login_required
def profile_view(request):
    profile = Profile.objects.create_or_update_user_profile(user=request.user)
    return render(request, "profile.html", {"profile": profile})