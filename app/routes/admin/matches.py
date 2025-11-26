from flask import render_template, request, redirect, url_for, flash
from app.database.db import get_db
from app.routes.admin_routes import admin_bp
from app.routes.admin.decorators import admin_or_manager_required

@admin_bp.route('/manage_matches', methods=['GET', 'POST'])
@admin_or_manager_required
def manage_matches():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        try:
            match_id = request.form.get('match_id')
            date = request.form['date']
            team1_id = request.form['team1_id']
            team2_id = request.form['team2_id']
            season_id = request.form['season_id']
            league_id = request.form['league_id']

            if 'submit' in request.form:
                if match_id:
                    cur.execute('UPDATE matches SET utc_date = %s, home_team_id = %s, away_team_id = %s, season_id = %s, league_id = %s WHERE match_id = %s', 
                                (date, team1_id, team2_id, season_id, league_id, match_id))
                    flash('Match updated successfully', 'success')
                else:
                    cur.execute('INSERT INTO matches (utc_date, home_team_id, away_team_id, season_id, league_id) VALUES (%s, %s, %s, %s, %s)', 
                                (date, team1_id, team2_id, season_id, league_id))
                    flash('Match added successfully', 'success')
            elif 'delete' in request.form:
                match_id = request.form['deleteEntityId']
                cur.execute('DELETE FROM matches WHERE match_id = %s', (match_id,))
                flash('Match deleted successfully', 'success')
            db.commit()
        except Exception as e:
            db.rollback()
            flash('An error occurred: ' + str(e), 'error')
        finally:
            cur.close()
        return redirect(url_for('admin.manage_matches'))

    cur.execute('''
        SELECT m.match_id, m.utc_date, t1.name AS team1, t2.name AS team2, s.year AS season, l.name AS league,
               m.home_team_id, m.away_team_id
        FROM matches m
        JOIN teams t1 ON m.home_team_id = t1.team_id
        JOIN teams t2 ON m.away_team_id = t2.team_id
        JOIN seasons s ON m.season_id = s.season_id
        JOIN leagues l ON m.league_id = l.league_id
    ''')
    matches = cur.fetchall()
    cur.execute('SELECT team_id, name FROM teams')
    teams = cur.fetchall()
    cur.execute('SELECT season_id, year FROM seasons')
    seasons = cur.fetchall()
    cur.execute('SELECT league_id, name FROM leagues')
    leagues = cur.fetchall()
    cur.close()
    return render_template('manage_matches.html', matches=matches, teams=teams, seasons=seasons, leagues=leagues)
