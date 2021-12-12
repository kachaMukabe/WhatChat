from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth import login
from django.views import View
from users.forms import CustomUserCreationForm 
from analyzer.models import Conversation


# def dashboard(request):
    # return render(request, 'users/dashboard.html')

class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        conversations = Conversation.objects.filter(owner=request.user)
        return render(request, "users/dashboard.html", {"conversations": conversations})


class Register(View):
    def get(self, request):
        return render(request, "users/register.html", {"form": CustomUserCreationForm})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.backend = "django.contrib.auth.backends.ModelBackend"
            user.save()
            login(request, user)
            return redirect(reverse("dashboard"))


