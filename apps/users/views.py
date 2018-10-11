from django.shortcuts import render
from apps.users.forms import SignUpForm
from django.template.loader import render_to_string


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return render(request, 'registration/user_created.html', {'email': form.cleaned_data.get('email')})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
