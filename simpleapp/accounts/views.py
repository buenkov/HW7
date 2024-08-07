from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .forms import RegistrationForm
from .models import MyUser
import random
import string

def generate_confirmation_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            confirmation_code = generate_confirmation_code()
            request.session['confirmation_code'] = confirmation_code
            request.session['user_id'] = user.id

            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'confirmation_code': confirmation_code,
            })
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()
            return redirect('confirm_registration')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def confirm_registration(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        if code == request.session.get('confirmation_code'):
            user_id = request.session.get('user_id')
            user = MyUser.objects.get(id=user_id)
            user.is_active = True
            user.save()
            return redirect('login')
    return render(request, 'confirm_registration.html')
