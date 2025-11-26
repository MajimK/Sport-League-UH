from functools import wraps
from flask import redirect, session, url_for, flash

def manager_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' not in session or session.get('role') not in ['manager', 'admin']:
            flash('You need manager privileges to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrap

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user_id' not in session or not session.get('is_admin'):
            flash('You need to be an admin to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrap

def admin_or_manager_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user_id' not in session or (not session.get('is_admin') and not session.get('is_manager')):
            flash('You need admin or manager privileges to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrap

