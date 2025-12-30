from functools import wraps

from flask import redirect, abort
from flask_login import current_user

from TruongMauGiao.models import UserRole


def anonymous_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect('/login')

        if not hasattr(current_user, "role") or current_user.role != UserRole.ADMIN:
            abort(403)

        return f(*args, **kwargs)
    return decorated


def staff_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated

