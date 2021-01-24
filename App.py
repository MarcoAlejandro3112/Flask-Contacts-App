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
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
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

@app.route('/update/<user_id>',methods=['POST'])
def edit(user_id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE users 
            SET fullname = %s,
                email = %s,
                phone = %s
            WHERE id = %s
        """,(fullname,email,phone,user_id))
        mysql.connection.commit()
        flash("El contacto ha sido actualizado","info")
        cur.close()
        return redirect(url_for('Index'))

@app.route('/update/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE id = %s',(id))
    u_user = cur.fetchall()
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    return render_template('index.html', u_user=u_user,users=users)

@app.route('/delete/<id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM users WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash("Contacto eliminado satisfactoriamente")
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port = 3000,debug=True)