from flask import render_template, request, redirect, url_for, flash
from app.database.db import get_db
from app.routes.admin_routes import admin_bp
from app.routes.admin.decorators import admin_required

@admin_bp.route('/manage_referees', methods=['GET', 'POST'])
@admin_required
def manage_referees():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        try:
            referee_id = request.form.get('referee_id')
            name = request.form['name']
            nationality = request.form['nationality']

            if 'submit' in request.form:
                if referee_id:
                    cur.execute('UPDATE referees SET name = %s, nationality = %s WHERE referee_id = %s', 
                                (name, nationality, referee_id))
                    flash('Referee updated successfully', 'success')
                else:
                    cur.execute('INSERT INTO referees (name, nationality) VALUES (%s, %s)', 
                                (name, nationality))
                    flash('Referee added successfully', 'success')
            elif 'delete' in request.form:
                referee_id = request.form['deleteEntityId']
                cur.execute('DELETE FROM referees WHERE referee_id = %s', (referee_id,))
                flash('Referee deleted successfully', 'success')
            db.commit()
        except Exception as e:
            db.rollback()
            flash('An error occurred: ' + str(e), 'error')
        finally:
            cur.close()
        return redirect(url_for('admin.manage_referees'))

    cur.execute('SELECT referee_id, name, nationality FROM referees')
    referees = cur.fetchall()
    cur.close()
    return render_template('manage_referees.html', referees=referees)
