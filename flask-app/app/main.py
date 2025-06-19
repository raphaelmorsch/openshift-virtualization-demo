from flask import Flask, request, redirect, render_template
import psycopg2

app = Flask(__name__)

# Configure your Postgres VM service here
DB_HOST = "postgres-vm-service.demo.svc.cluster.local"
DB_NAME = "fruits"
DB_USER = "postgres"
DB_PASS = ""

def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM fruits;')
    fruits = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', fruits=fruits)

@app.route('/add', methods=['POST'])
def add_fruit():
    name = request.form['name']
    country = request.form['country']
    taste = request.form['taste']
    season = request.form['season']
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO fruits (name, country_of_origin, taste, season_period) VALUES (%s, %s, %s, %s)",
                (name, country, taste, season))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>', methods=['POST'])
def delete_fruit(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM fruits WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
