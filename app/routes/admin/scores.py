from flask import render_template, request, redirect, url_for, flash
from app.database.db import get_db
from app.routes.admin_routes import admin_bp
from app.routes.admin.decorators import admin_required

@admin_bp.route('/manage_scores', methods=['GET', 'POST'])
@admin_required
def manage_scores():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        try:
            score_id = request.form.get('score_id')
            match_id = request.form['match_id']
            full_time_home = request.form['full_time_home']
            full_time_away = request.form['full_time_away']
            half_time_home = request.form['half_time_home']
            half_time_away = request.form['half_time_away']

            if 'submit' in request.form:
                if score_id:
                    cur.execute('UPDATE scores SET match_id = %s, full_time_home = %s, full_time_away = %s, half_time_home = %s, half_time_away = %s WHERE score_id = %s',
                                (match_id, full_time_home, full_time_away, half_time_home, half_time_away, score_id))
                    flash('Score updated successfully', 'success')
                else:
                    cur.execute('INSERT INTO scores (match_id, full_time_home, full_time_away, half_time_home, half_time_away) VALUES (%s, %s, %s, %s, %s)',
                                (match_id, full_time_home, full_time_away, half_time_home, half_time_away))
                    flash('Score added successfully', 'success')
            elif 'delete' in request.form:
                score_id = request.form['deleteEntityId']
                cur.execute('DELETE FROM scores WHERE score_id = %s', (score_id,))
                flash('Score deleted successfully', 'success')
            db.commit()
        except Exception as e:
            db.rollback()
            flash('An error occurred: ' + str(e), 'error')
        finally:
            cur.close()
        return redirect(url_for('admin.manage_scores'))

    cur.execute('SELECT s.score_id, m.utc_date, s.full_time_home, s.full_time_away, s.half_time_home, s.half_time_away FROM scores s JOIN matches m ON s.match_id = m.match_id')
    scores = cur.fetchall()
    cur.execute('SELECT match_id, utc_date FROM matches')
    matches = cur.fetchall()
    cur.close()
    return render_template('manage_scores.html', scores=scores, matches=matches)
