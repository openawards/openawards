from django.shortcuts import render, redirect, reverse
from apps.users.forms import SignUpForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from urllib.parse import urljoin
from django.contrib.auth.views import LoginView
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from .tokens import AccountActivationTokenGenerator


def get_activate_url(request, user):
    _id = urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8')
    token = AccountActivationTokenGenerator().make_token(user)
    url = reverse('users_activate', args=(_id, token,))
    domain = get_current_site(request).domain
    protocol = 'https' \
        if request.is_secure and not (domain.startswith('127.0.0.1') or domain.startswith('localhost')) \
        else 'http'
    return urljoin(f'{protocol}://{domain}', url)


def signup(request):
    if request.user and request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            subject = 'Activate Your Account'
            message = render_to_string('emails/user_registration.html', {
                'url': get_activate_url(request, user),
                'user': user
            })
            user.email_user(subject, message)
            return render(request, 'registration/user_registered.html', {'email': form.cleaned_data.get('email')})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uuid, token):
    try:
        _id = force_text(urlsafe_base64_decode(uuid))
        user = get_user_model().objects.get(pk=_id)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None \
            and not user.is_active \
            and not user.is_confirmed \
            and AccountActivationTokenGenerator().check_token(user, token):
        user.is_active = True
        user.is_confirmed = True
        user.save()
        login(request, user)
        # TODO: Add successful activation message
        # TODO: Redirect properly (should we take it from settings?)
        return redirect('/')
    else:
        return render(request, 'registration/user_activation_invalid.html')


class UsersLoginView(LoginView):
    redirect_authenticated_user = True
