from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from app.database.db import get_db
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def landing():
    if 'user_id' in session:
        session.clear()
    return render_template('landing.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        print(f"🔐 Attempting login for: {username}")
        
        db = get_db()
        cur = db.cursor()
        
        # Buscar usuario en la base de datos
        cur.execute(
            'SELECT user_id, username, password, is_admin, is_manager FROM users WHERE username = %s',
            (username,)
        )
        user = cur.fetchone()
        cur.close()
        
        if user:
            print(f"🎪 User found in database: {username}")
            # Verificar contraseña
            if bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
                print(f"✅ Authentication successful for: {username}")
                # Autenticación exitosa
                session['user_id'] = user[0]
                session['username'] = user[1]
                session['is_admin'] = user[3]
                session['is_manager'] = user[4]  # Nuevo campo de manager
                
                print(f"🎭 User roles - Admin: {user[3]}, Manager: {user[4]}")
                
                # Redirigir según permisos
                if session.get('is_admin'):
                    return redirect(url_for('auth.admin'))
                elif session.get('is_manager'):
                    return redirect(url_for('auth.manager'))  # O donde quieras que vayan los managers
                else:
                    return redirect(url_for('user.user_dashboard'))
            else:
                print(f"❌ Authentication failed for: {username}")
                flash('Invalid password', 'error')
                return redirect(url_for('login'))
        else:
            print(f"❌ User not found: {username}")
            flash('Invalid username', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.landing'))

@auth_bp.route('/home')
def home():
    if 'user_id' in session:
        if session.get('is_admin'):
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('user'))
    else:
        return redirect(url_for('login'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    cur = db.cursor()
    user_id = session['user_id']

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if the username already exists
        cur.execute(
            'SELECT * FROM users WHERE username = %s AND user_id != %s',
            (username, user_id))
        existing_user = cur.fetchone()
        if existing_user:
            flash('Username already taken', 'error')
            return redirect(url_for('profile'))

        # Check if the email already exists
        cur.execute('SELECT * FROM users WHERE email = %s AND user_id != %s',
                    (email, user_id))
        existing_email = cur.fetchone()
        if existing_email:
            flash('Email already registered', 'error')
            return redirect(url_for('profile'))

        # Hash the password if it is updated
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        cur.execute(
            'UPDATE users SET username = %s, email = %s, password = %s WHERE user_id = %s',
            (username, email, hashed_password, user_id))
        db.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('profile'))

    cur.execute('SELECT username, email FROM users WHERE user_id = %s',
                (user_id, ))
    user = cur.fetchone()
    cur.close()

    return render_template('profile.html', user=user)


@auth_bp.route('/about')
def about():
    return render_template('about.html')

@auth_bp.route('/search', methods=['GET', 'POST'])
def search():
    if 'user_id' not in session:
        flash('You need to log in to search', 'error')
        return redirect(url_for('login'))

    results = []
    query = ""
    if request.method == 'POST':
        query = request.form['query']
        db = get_db()
        cur = db.cursor()

        # Search in teams
        cur.execute(
            "SELECT team_id, name, 'team' AS source FROM teams WHERE name ILIKE %s",
            ('%' + query + '%', ))
        results.extend(cur.fetchall())

        # Search in coaches
        cur.execute(
            "SELECT coach_id, name, 'coach' AS source FROM coaches WHERE name ILIKE %s",
            ('%' + query + '%', ))
        results.extend(cur.fetchall())

        # Search in players
        cur.execute(
            "SELECT player_id, name, 'player' AS source FROM players WHERE name ILIKE %s",
            ('%' + query + '%', ))
        results.extend(cur.fetchall())

        # Search in stadiums
        cur.execute(
            "SELECT stadium_id, name, 'stadium' AS source FROM stadiums WHERE name ILIKE %s",
            ('%' + query + '%', ))
        results.extend(cur.fetchall())

        # Search in leagues
        cur.execute(
            "SELECT league_id, name, 'league' AS source FROM leagues WHERE name ILIKE %s",
            ('%' + query + '%', ))
        results.extend(cur.fetchall())

        cur.close()

    return render_template('search.html', results=results, query=query)

@auth_bp.route('/admin')
def admin():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    return render_template('admin.html')

@auth_bp.route('/manager')
def manager():
    if 'user_id' not in session or not session.get('is_manager'):
        return redirect(url_for('login'))
    return render_template('manager.html')