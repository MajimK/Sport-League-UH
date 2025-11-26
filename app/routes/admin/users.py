from flask import render_template, request, redirect, url_for, flash
from app.database.db import get_db
from app.routes.admin_routes import admin_bp
from app.routes.admin.decorators import admin_required
import bcrypt


@admin_bp.route('/manage_users', methods=['GET', 'POST'])
@admin_required
def manage_users():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        try:
            user_id = request.form.get('user_id')
            action = request.form.get('action')
            
            if action == 'toggle_admin':
                is_admin = request.form.get('is_admin') == 'true'
                cur.execute('UPDATE users SET is_admin = %s WHERE user_id = %s', (is_admin, user_id))
                flash('User privileges updated successfully', 'success')
                
            elif action == 'delete':
                cur.execute('DELETE FROM users WHERE user_id = %s', (user_id,))
                flash('User deleted successfully', 'success')
                
            db.commit()
        except Exception as e:
            db.rollback()
            flash('An error occurred: ' + str(e), 'error')
        finally:
            cur.close()
        return redirect(url_for('admin.manage_users'))

    cur.execute('SELECT user_id, username, email, is_admin FROM users ORDER BY username')
    users = cur.fetchall()
    cur.close()

    return render_template('manage_users.html', users=users)

@admin_bp.route('/manage_users/add', methods=['GET', 'POST'])
@admin_required
def add_user():
    if request.method == 'POST':
        try:
            db = get_db()
            cur = db.cursor()
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']  # Nueva contraseña
            confirm_password = request.form['confirm_password']  # Confirmación
            is_admin = 'is_admin' in request.form  # Checkbox
            
            # Verificar que las contraseñas coincidan
            if password != confirm_password:
                flash('Passwords do not match', 'error')
                return redirect(url_for('admin.add_user'))
            
            # Verificar longitud mínima de contraseña
            if len(password) < 6:
                flash('Password must be at least 6 characters long', 'error')
                return redirect(url_for('admin.add_user'))

            # Verificar si el usuario ya existe
            cur.execute('SELECT * FROM users WHERE username = %s', (username,))
            existing_user = cur.fetchone()
            if existing_user:
                flash('Username already exists', 'error')
                return redirect(url_for('admin.add_user'))

            # Verificar si el email ya existe
            cur.execute('SELECT * FROM users WHERE email = %s', (email,))
            existing_email = cur.fetchone()
            if existing_email:
                flash('Email already registered', 'error')
                return redirect(url_for('admin.add_user'))
            
            # Hash de la contraseña
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # Insertar usuario con contraseña hasheada
            cur.execute(
                'INSERT INTO users (username, email, password, is_admin) VALUES (%s, %s, %s, %s)',
                (username, email, hashed_password, is_admin)
            )
            db.commit()
            cur.close()
            flash('User created successfully', 'success')
            return redirect(url_for('admin.manage_users'))
            
        except Exception as e:
            db.rollback()
            print(f"Error creating user: {str(e)}")
            flash('Failed to create user', 'error')
            return redirect(url_for('admin.add_user'))

    return render_template('add_user.html')