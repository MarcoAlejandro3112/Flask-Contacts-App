from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
from flask_mysqldb import MySQL
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'contacts'
mysql = MySQL(app)

app.secret_key = 'superr'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT fullname,email,phone FROM users')
    users = cur.fetchall()
    print(users)
    return render_template('index.html',users=users)

@app.route('/add_contact',methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO users(fullname,phone,email) VALUES (%s,%s,%s)',
                    (fullname,phone,email))
        mysql.connection.commit()
        flash("El contacto ha sido agregado","info")
        cur.close()
        return redirect(url_for('Index'))

@app.route('/edit')
def edit():
    return 'add contact'

@app.route('/delete')
def delete():
    return 'add contact'

if __name__ == '__main__':
    app.run(port = 3000,debug=True)