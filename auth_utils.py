from functools import wraps
from flask import session, redirect, url_for, flash

# Definiere die Rollen mit Berechtigungen
ROLES = {
    'Admin': ['create_task', 'delete_task', 'edit_task', 'move_task', 'assign_task', 'view'],
    'Manager': ['create_task', 'delete_task', 'edit_task', 'move_task', 'assign_task', 'view'],
    'Benutzer': ['create_task', 'edit_own_task', 'move_own_task', 'assign_own_task', 'view'],
    'Leser': ['view']
}

# Berechtigungs-Dekorator für geschützte Routen
def requires_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'role' not in session:
                flash("❌ Zugriff verweigert. Bitte anmelden.", "danger")
                return redirect(url_for('login'))

            user_role = session['role']
            allowed_permissions = ROLES.get(user_role, [])

            if permission not in allowed_permissions:
                flash("❌ Zugriff verweigert. Du hast nicht die erforderlichen Rechte.", "danger")
                return redirect(url_for('task_manager.Task_Manager'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator
