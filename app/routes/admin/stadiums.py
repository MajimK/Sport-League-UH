from flask import render_template, request, redirect, url_for, flash
from app.database.db import get_db
from app.routes.admin_routes import admin_bp
from app.routes.admin.decorators import admin_required

@admin_bp.route('/manage_stadiums', methods=['GET', 'POST'])
@admin_required
def manage_stadiums():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        try:
            stadium_id = request.form.get('stadium_id')
            name = request.form['name']
            location = request.form['location']
            capacity = request.form['capacity']

            if 'add' in request.form:
                cur.execute('INSERT INTO stadiums (name, location, capacity) VALUES (%s, %s, %s)', 
                            (name, location, capacity))
                flash('Stadium added successfully', 'success')
            elif 'edit' in request.form and stadium_id:
                cur.execute('UPDATE stadiums SET name = %s, location = %s, capacity = %s WHERE stadium_id = %s', 
                            (name, location, capacity, stadium_id))
                flash('Stadium updated successfully', 'success')
            elif 'delete' in request.form and stadium_id:
                cur.execute('DELETE FROM stadiums WHERE stadium_id = %s', (stadium_id,))
                flash('Stadium deleted successfully', 'success')
            db.commit()
        except Exception as e:
            db.rollback()
            flash('An error occurred: ' + str(e), 'error')
        finally:
            cur.close()
        return redirect(url_for('admin.manage_stadiums'))

    cur.execute('SELECT stadium_id, name, location, capacity FROM stadiums')
    stadiums = cur.fetchall()
    cur.close()
    return render_template('manage_stadiums.html', stadiums=stadiums)