from flask import render_template, request, redirect, url_for, flash
from app.database.db import get_db
from app.routes.admin_routes import admin_bp
from app.routes.admin.decorators import admin_or_manager_required

@admin_bp.route('/manage_teams', methods=['GET', 'POST'])
@admin_or_manager_required
def manage_teams():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        try:
            team_id = request.form.get('team_id')
            name = request.form['name']
            founded_year = request.form['founded_year']
            stadium_id = request.form['stadium_id']
            league_id = request.form['league_id']
            coach_id = request.form['coach_id']

            if 'add' in request.form:
                cur.execute('INSERT INTO teams (name, founded_year, stadium_id, league_id, coach_id) VALUES (%s, %s, %s, %s, %s)', 
                            (name, founded_year, stadium_id, league_id, coach_id))
                flash('Team added successfully', 'success')
            elif 'edit' in request.form and team_id:
                cur.execute('UPDATE teams SET name = %s, founded_year = %s, stadium_id = %s, league_id = %s, coach_id = %s WHERE team_id = %s', 
                            (name, founded_year, stadium_id, league_id, coach_id, team_id))
                flash('Team updated successfully', 'success')
            elif 'delete' in request.form and team_id:
                cur.execute('DELETE FROM teams WHERE team_id = %s', (team_id,))
                flash('Team deleted successfully', 'success')
            db.commit()
        except Exception as e:
            db.rollback()
            flash('An error occurred: ' + str(e), 'error')
        finally:
            cur.close()
        return redirect(url_for('admin.manage_teams'))

    cur.execute('SELECT team_id, name, founded_year, stadium_id, league_id, coach_id FROM teams')
    teams = cur.fetchall()
    cur.execute('SELECT stadium_id, name FROM stadiums')
    stadiums = cur.fetchall()
    cur.execute('SELECT league_id, name FROM leagues')
    leagues = cur.fetchall()
    cur.execute('SELECT coach_id, name FROM coaches')
    coaches = cur.fetchall()
    cur.close()
    return render_template('manage_teams.html', teams=teams, stadiums=stadiums, leagues=leagues, coaches=coaches)
