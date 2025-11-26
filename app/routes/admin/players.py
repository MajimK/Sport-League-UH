from flask import render_template, request, redirect, url_for, flash
from app.database.db import get_db
from app.routes.admin_routes import admin_bp
from app.routes.admin.decorators import admin_or_manager_required

@admin_bp.route('/manage_players', methods=['GET', 'POST'])
@admin_or_manager_required
def manage_players():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        try:
            player_id = request.form.get('player_id')
            team_id = request.form['team_id']
            name = request.form['name']
            position = request.form['position']
            date_of_birth = request.form['date_of_birth']
            nationality = request.form['nationality']

            if 'submit' in request.form:
                if player_id:
                    cur.execute('UPDATE players SET team_id = %s, name = %s, position = %s, date_of_birth = %s, nationality = %s WHERE player_id = %s', 
                                (team_id, name, position, date_of_birth, nationality, player_id))
                    flash('Player updated successfully', 'success')
                else:
                    cur.execute('INSERT INTO players (team_id, name, position, date_of_birth, nationality) VALUES (%s, %s, %s, %s, %s)', 
                                (team_id, name, position, date_of_birth, nationality))
                    flash('Player added successfully', 'success')
            elif 'delete' in request.form:
                player_id = request.form['deleteEntityId']
                cur.execute('DELETE FROM players WHERE player_id = %s', (player_id,))
                flash('Player deleted successfully', 'success')
            db.commit()
        except Exception as e:
            db.rollback()
            flash('An error occurred: ' + str(e), 'error')
        finally:
            cur.close()
        return redirect(url_for('admin.manage_players'))

    cur.execute('SELECT p.player_id, t.name AS team, p.name, p.position, p.date_of_birth, p.nationality, p.team_id FROM players p JOIN teams t ON p.team_id = t.team_id')
    players = cur.fetchall()
    cur.execute('SELECT team_id, name FROM teams')
    teams = cur.fetchall()
    cur.close()
    return render_template('manage_players.html', players=players, teams=teams)
