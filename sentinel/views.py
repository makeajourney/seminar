from datetime import datetime, timedelta

from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.conf import settings
from django.views import View

from .models import EmailToken, EmailUser
from .forms import EmailLoginForm, ProfileForm

from django.core.mail import send_mail

@login_required
class ProfileView(View):
    template_name = 'profile.html'
    form_class = ProfileForm
    success_url = '/sentinel/profile/'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    form_class = EmailLoginForm
    template_name = 'login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Remove previous tokens
            email = form.cleaned_data['email']
            EmailToken.objects.filter(email=email).delete()

            # Create new
            token = EmailToken(email=email)
            token.save()

            self.send_email_token(request, token, email)
            return render(request, 'mail_sent.html')
        else:
            return render(request, self.template_name, {'form': form})

    def send_email_token(self, request, token, email):
        html = render_to_string('mail/email_token.html', {'token': token}, request)
        send_mail(
            "파이콘 세미나 일회용 로그인 토큰",
            html,
            settings.EMAIL_HOST_USER,
            [email],
            html_message=html,
        )


class CheckTokenView(View):

    def get(self, request, token):
        time_threshold = datetime.now() - timedelta(hours=1)
        try:
            token = EmailToken.objects.get(token=token, created_at__gte=time_threshold)
        except EmailToken.DoesNotExist:
            return render(request, 'invalid_token.html')

        email = token.email
        try:
            user = EmailUser.objects.get(email=email)
        except EmailUser.DoesNotExist:
            user = EmailUser.objects.create_user(email)

        login(request, user)
        token.delete()

        return redirect(reverse('index'))


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))
