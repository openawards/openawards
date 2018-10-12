from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        # TODO: This should be placed into a global app, meanwhile having it here is (more-or-less) fine
        # This ensures the SECRET_KEY has not been published on a git repo by checking the dev key
        from django.conf import settings
        from importlib import import_module
        assert hasattr(settings, 'DEV_SETTINGS_MODULE'), 'Please add DEV_SETTINGS_MODULE value to your settings.'
        dev_module = import_module(settings.DEV_SETTINGS_MODULE)
        is_debug = settings.DEBUG
        dev_secret = dev_module.SECRET_KEY
        current_secret = settings.SECRET_KEY
        assert is_debug or current_secret != dev_secret, '\nIt seems the DEBUG flag is False; however, ' \
                                                         'the secret key remains the same as it is at dev settings.\n' \
                                                         'If you were in production it would be a serious security ' \
                                                         'issue.\nPlease, change the SECRET_KEY value at settings.'
