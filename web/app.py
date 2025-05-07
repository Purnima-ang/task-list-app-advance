from flask import Flask, render_template, request, redirect, url_for
import redis
import os
import psycopg2

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['REDIS_HOST'] = os.environ.get('REDIS_HOST', 'cache')
    app.config['REDIS_PORT'] = int(os.environ.get('REDIS_PORT', 6379))
    app.config['DB_HOST'] = os.environ.get('DB_HOST', 'db')
    app.config['DB_NAME'] = os.environ.get('DB_NAME', 'tasksdb')
    app.config['DB_USER'] = os.environ.get('DB_USER', 'postgres')
    app.config['DB_PASSWORD'] = os.environ.get('DB_PASSWORD', 'postgres')

    r = redis.Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'])

    def get_db_connection():
        conn = psycopg2.connect(
            host=app.config['DB_HOST'],
            database=app.config['DB_NAME'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD']
        )
        return conn

    def init_db():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                description TEXT NOT NULL
            )
        """)
        conn.commit()
        cur.close()
        conn.close()

    @app.route('/', methods=['GET', 'POST'])
    def index():
        init_db()
        message = None
        if request.method == 'POST':
            task = request.form['task']
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO tasks (description) VALUES (%s)", (task,))
            conn.commit()
            cur.close()
            conn.close()
            r.delete('tasks')  # Invalidate cache
            message = f"Task '{task}' added!"

        # Retrieve tasks from Redis or DB
        cached_tasks = r.get('tasks')
        if cached_tasks:
            tasks = eval(cached_tasks.decode('utf-8'))  # Deserialize cached tasks
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT description FROM tasks")
            tasks = [row[0] for row in cur.fetchall()]
            r.set('tasks', str(tasks))  # Cache the tasks
            conn.close()

        return render_template('index.html', tasks=tasks, message=message)

    @app.route('/clear', methods=['POST'])
    def clear_tasks():
        # Clear tasks from DB
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM tasks")
        conn.commit()
        cur.close()
        conn.close()

        # Invalidate Redis cache
        r.delete('tasks')

        return redirect(url_for('index'))

    @app.route('/health')
    def health():
        return 'OK', 200

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
