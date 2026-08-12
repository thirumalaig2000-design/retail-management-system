from __future__ import annotations

from .models import AuditLog


def log_event(*, user=None, action: str, module: str, record_id: str = "", description: str) -> AuditLog:
    return AuditLog.objects.create(
        user=user if getattr(user, "is_authenticated", False) else None,
        action=action,
        module=module,
        record_id=record_id,
        description=description,
    )
