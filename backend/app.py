import os
from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

def connect():
    return psycopg2.connect(os.environ['DATABASE_URL'])

def init_db():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute('CREATE TABLE IF NOT EXISTS tasks (id SERIAL PRIMARY KEY, title VARCHAR(200) NOT NULL)')

@app.get('/api/tasks')
def tasks():
    init_db()
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, title FROM tasks ORDER BY id')
            return jsonify([{'id': row[0], 'title': row[1]} for row in cur.fetchall()])

@app.post('/api/tasks')
def add_task():
    title = str((request.get_json(silent=True) or {}).get('title', '')).strip()
    if not title or len(title) > 200:
        return jsonify({'error': 'Назва має містити від 1 до 200 символів'}), 400
    init_db()
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO tasks (title) VALUES (%s) RETURNING id', (title,))
            task_id = cur.fetchone()[0]
    return jsonify({'id': task_id, 'title': title}), 201

@app.delete('/api/tasks/<int:task_id>')
def delete_task(task_id):
    init_db()
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM tasks WHERE id = %s RETURNING id', (task_id,))
            if cur.fetchone() is None:
                return jsonify({'error': 'Не знайдено'}), 404
    return '', 204
