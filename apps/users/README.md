# Users APP

In config:
```
LOGIN_REDIRECT_URL = '/'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
AUTH_USER_MODEL = 'persons.ReBaseUser'
DEV_SETTINGS_MODULE = 'OpenAwards.settings.dev'
USER_FIXTURE_FACTORY_CLASS = 'openawards.tests.fixtures.UserFactory'
```