from flask import render_template, request, redirect, url_for, flash
from app.database.db import get_db
from app.routes.admin_routes import admin_bp
from app.routes.admin.decorators import admin_required

@admin_bp.route('/manage_countries', methods=['GET', 'POST'])
@admin_required
def manage_countries():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        try:
            country_id = request.form.get('country_id')
            name = request.form['name']
            flag_url = request.form['flag_url']

            if 'submit' in request.form:
                if country_id:
                    cur.execute('UPDATE countries SET name = %s, flag_url = %s WHERE country_id = %s', 
                                (name, flag_url, country_id))
                    flash('Country updated successfully', 'success')
                else:
                    cur.execute('INSERT INTO countries (name, flag_url) VALUES (%s, %s)', 
                                (name, flag_url))
                    flash('Country added successfully', 'success')
            elif 'delete' in request.form:
                country_id = request.form['deleteEntityId']
                cur.execute('DELETE FROM countries WHERE country_id = %s', (country_id,))
                flash('Country deleted successfully', 'success')
            db.commit()
        except Exception as e:
            db.rollback()
            flash('An error occurred: ' + str(e), 'error')
        finally:
            cur.close()
        return redirect(url_for('admin.manage_countries'))

    cur.execute('SELECT country_id, name, flag_url FROM countries')
    countries = cur.fetchall()
    cur.close()
    return render_template('manage_countries.html', countries=countries)

