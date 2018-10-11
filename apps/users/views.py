from django.shortcuts import render, redirect, reverse
from apps.users.forms import SignUpForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from urllib.parse import urljoin
from django.contrib.auth.views import LoginView


def get_activate_url(request, user):
    url = reverse('users_activate', args=(user.token,))
    domain = get_current_site(request).domain
    protocol = 'https' \
        if request.is_secure and not (domain.startswith('127.0.0.1') or domain.startswith('localhost')) \
        else 'http'
    return urljoin(f'{protocol}://{domain}', url)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            subject = 'Activate Your MySite Account'
            message = render_to_string('emails/user_registration.html', {
                'url': get_activate_url(request, user),
                'user': user,
                'token': user.token
            })
            user.email_user(subject, message)
            return render(request, 'registration/user_registered.html', {'email': form.cleaned_data.get('email')})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, token):
    try:
        user = get_user_model().objects.get(token=token)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and not user.is_active:
        user.is_active = True
        user.save()
        login(request, user)
        # TODO: Add successful activation message
        # TODO: Redirect properly (should we take it from settings?)
        return redirect('/')
    else:
        return render(request, 'registration/user_activation_invalid.html')


class UsersLoginView(LoginView):
    redirect_authenticated_user = True
