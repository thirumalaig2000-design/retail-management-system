from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from .models import AuditLog
from .services import log_event


@receiver(user_logged_in)
def audit_login(sender, request, user, **kwargs):
    log_event(
        user=user,
        action=AuditLog.Action.LOGIN,
        module=AuditLog.Module.AUTH,
        record_id=str(user.pk),
        description=f"{user.email} logged in.",
    )


@receiver(user_logged_out)
def audit_logout(sender, request, user, **kwargs):
    if user is None:
        return
    log_event(
        user=user,
        action=AuditLog.Action.LOGOUT,
        module=AuditLog.Module.AUTH,
        record_id=str(user.pk),
        description=f"{user.email} logged out.",
    )
