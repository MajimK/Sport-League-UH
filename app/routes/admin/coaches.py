from flask import render_template, request, redirect, url_for, flash
from app.database.db import get_db
from app.routes.admin_routes import admin_bp
from app.routes.admin.decorators import admin_required

@admin_bp.route('/manage_coaches', methods=['GET', 'POST'])
@admin_required
def manage_coaches():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        try:
            coach_id = request.form.get('coach_id')
            name = request.form['name']
            nationality = request.form['nationality']
            team_id = request.form['team_id']

            if 'add' in request.form:
                cur.execute('INSERT INTO coaches (name, nationality, team_id) VALUES (%s, %s, %s)', 
                            (name, nationality, team_id))
                flash('Coach added successfully', 'success')
            elif 'submit' in request.form and coach_id:
                cur.execute('UPDATE coaches SET name = %s, nationality = %s, team_id = %s WHERE coach_id = %s', 
                            (name, nationality, team_id, coach_id))
                flash('Coach updated successfully', 'success')
            elif 'delete' in request.form:
                coach_id = request.form['deleteEntityId']
                cur.execute('DELETE FROM coaches WHERE coach_id = %s', (coach_id,))
                flash('Coach deleted successfully', 'success')
            db.commit()
        except Exception as e:
            db.rollback()
            flash('An error occurred: ' + str(e), 'error')
        finally:
            cur.close()
        return redirect(url_for('admin.manage_coaches'))

    cur.execute('''
        SELECT c.coach_id, c.name, c.team_id, c.nationality, t.name AS team_name
        FROM coaches c
        JOIN teams t ON c.team_id = t.team_id
    ''')
    coaches = cur.fetchall()
    cur.execute('SELECT team_id, name FROM teams')
    teams = cur.fetchall()
    cur.close()
    return render_template('manage_coaches.html', coaches=coaches, teams=teams)
