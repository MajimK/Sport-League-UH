from flask import render_template, request, redirect, url_for, flash
from app.database.db import get_db
from app.routes.admin_routes import admin_bp
from app.routes.admin.decorators import admin_required

@admin_bp.route('/manage_leagues', methods=['GET', 'POST'])
@admin_required
def manage_leagues():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        try:
            league_id = request.form.get('league_id')
            name = request.form['name']
            country = request.form['country']

            if 'add' in request.form:
                cur.execute('INSERT INTO leagues (name, country) VALUES (%s, %s)', 
                            (name, country))
                flash('League added successfully', 'success')
            elif 'edit' in request.form and league_id:
                cur.execute('UPDATE leagues SET name = %s, country = %s WHERE league_id = %s', 
                            (name, country, league_id))
                flash('League updated successfully', 'success')
            elif 'delete' in request.form and league_id:
                cur.execute('DELETE FROM leagues WHERE league_id = %s', (league_id,))
                flash('League deleted successfully', 'success')
            db.commit()
        except Exception as e:
            db.rollback()
            flash('An error occurred: ' + str(e), 'error')
        finally:
            cur.close()
        return redirect(url_for('admin.manage_leagues'))

    cur.execute('SELECT league_id, name, country FROM leagues')
    leagues = cur.fetchall()
    cur.close()
    return render_template('manage_leagues.html', leagues=leagues)