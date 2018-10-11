from django.shortcuts import render, redirect
from apps.users.forms import SignUpForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.contrib.auth import login


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            subject = 'Activate Your MySite Account'
            message = render_to_string('emails/user_registration.html', {
                'domain': get_current_site(request).domain,
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
        return redirect('/')
    else:
        return render(request, 'registration/user_activation_invalid.html')
