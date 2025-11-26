from flask import Blueprint
from app.database.db import get_db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def get_existing_data(table_name):
    db = get_db()
    cur = db.cursor()
    cur.execute(f'SELECT * FROM {table_name}')
    data = cur.fetchall()
    cur.close()
    return data



