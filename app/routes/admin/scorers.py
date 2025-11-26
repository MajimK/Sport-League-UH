from flask import render_template, request, redirect, url_for, flash
from app.database.db import get_db
from app.routes.admin_routes import admin_bp
from app.routes.admin.decorators import admin_required

@admin_bp.route('/manage_scorers', methods=['GET', 'POST'])
@admin_required
def manage_scorers():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        try:
            scorer_id = request.form.get('scorer_id')
            player_id = request.form['player_id']
            season_id = request.form['season_id']
            league_id = request.form['league_id']
            goals = request.form['goals']
            assists = request.form['assists']
            penalties = request.form['penalties']

            if 'submit' in request.form:
                if scorer_id:
                    cur.execute('UPDATE scorers SET player_id = %s, season_id = %s, league_id = %s, goals = %s, assists = %s, penalties = %s WHERE scorer_id = %s',
                                (player_id, season_id, league_id, goals, assists, penalties, scorer_id))
                    flash('Scorer updated successfully', 'success')
                else:
                    cur.execute('INSERT INTO scorers (player_id, season_id, league_id, goals, assists, penalties) VALUES (%s, %s, %s, %s, %s, %s)',
                                (player_id, season_id, league_id, goals, assists, penalties))
                    flash('Scorer added successfully', 'success')
            elif 'delete' in request.form:
                scorer_id = request.form['deleteEntityId']
                cur.execute('DELETE FROM scorers WHERE scorer_id = %s', (scorer_id,))
                flash('Scorer deleted successfully', 'success')
            db.commit()
        except Exception as e:
            db.rollback()
            flash('An error occurred: ' + str(e), 'error')
        finally:
            cur.close()
        return redirect(url_for('admin.manage_scorers'))

    cur.execute('''
        SELECT s.scorer_id, p.name, se.year, l.name, s.goals, s.assists, s.penalties 
        FROM scorers s 
        JOIN players p ON s.player_id = p.player_id 
        JOIN seasons se ON s.season_id = se.season_id 
        JOIN leagues l ON s.league_id = l.league_id
    ''')
    scorers = cur.fetchall()
    cur.execute('SELECT player_id, name FROM players')
    players = cur.fetchall()
    cur.execute('SELECT season_id, year FROM seasons')
    seasons = cur.fetchall()
    cur.execute('SELECT league_id, name FROM leagues')
    leagues = cur.fetchall()
    cur.close()
    return render_template('manage_scorers.html', scorers=scorers, players=players, seasons=seasons, leagues=leagues)

