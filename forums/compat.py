try:
    from account.decorators import login_required
except ImportError:
    from django.contrib.auth.decorators import login_required  # noqa
