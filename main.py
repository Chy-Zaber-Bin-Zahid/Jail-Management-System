from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import MySQLdb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/jailmanage'
db = SQLAlchemy(app)
app.secret_key = 'jail'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False)

class Prisoner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.String(120), nullable=False)
    birth = db.Column(db.String(120), nullable=False)
    record = db.Column(db.String(120), nullable=False)
    year = db.Column(db.String(120), nullable=False)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    failed = ""
    if request.method == 'POST':
        checkId = request.form.get('id')
        email = request.form.get('email')
        password = request.form.get('password')
        occupation = request.form.get('occupation')
        # Database connect
        conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
        cursor = conn.cursor()
        # Query execute
        cursor.execute('SELECT * FROM user WHERE id = %s AND `email` = %s AND password = %s AND role = %s', (checkId, email, password, occupation))
        # Matched row in 'user'
        user = cursor.fetchone()

        if user is not None:
            session['id'] = user[0]
            session['email'] = user[3]
            if user[2] == "Cleaner":
                return redirect(url_for('cleaner'))
            elif user[2] == "Chef":
                return redirect(url_for('chef'))
            else:
                return redirect(url_for('police'))
        else:
            failed = "Login Failed!"
            # return redirect(url_for('login'))
        
    return render_template('login.html', failed=failed)

@app.route('/admin', methods = ['GET','POST'])
def admin():
    failed = ""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Database connect
        conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
        cursor = conn.cursor()
        # Query execute
        cursor.execute('SELECT * FROM admin WHERE `email` = %s AND password = %s', (email, password))
        # Matched row in 'user'
        user = cursor.fetchone()

        if user is not None:
            session['email'] = user[1]
            return redirect(url_for('adminDash'))
        else:
            failed = "Login Failed!"
            # return redirect(url_for('admin'))
    return render_template('admin.html',failed=failed)

@app.route('/cleaner')
def cleaner():
    return render_template('cleaner.html')

@app.route('/police')
def police():
    return render_template('police.html')

@app.route('/chef')
def chef():
    return render_template('chef.html')

@app.route('/adminDash')
def adminDash():
    return render_template('adminDash.html')

@app.route('/staffDetails', methods = ['GET','POST'])
def staffDetails():
    failed= ""
    # Database connect
    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
    cursor = conn.cursor()
    # Query execute
    cursor.execute('SELECT * FROM user')
    # Matched row in 'user'
    user = cursor.fetchall()

    if request.method == 'POST':
        if 'Add' == request.form.get('btn'):
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            role = request.form.get('occupation')

            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                failed="Email already exists. Please choose a different email!"
            else:
                entry = User(name=name, role=role, password=password, email=email)
                db.session.add(entry)
                db.session.commit()
                # Database connect
                conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
                cursor = conn.cursor()
                # Query execute
                cursor.execute('SELECT * FROM user')
                # Matched row in 'user'
                user = cursor.fetchall()
                failed="Added!"
        elif 'Modify' == request.form.get('btn'):
            email = request.form.get('email')
            user = User.query.filter_by(email=email).first()
            if user:
                user.name = request.form.get('name')
                user.password = request.form.get('password')
                user.role = request.form.get('occupation')
                db.session.commit()
                # Database connect
                conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
                cursor = conn.cursor()
                # Query execute
                cursor.execute('SELECT * FROM user')
                # Matched row in 'user'
                user = cursor.fetchall()
                failed="Changed!"
        else:
            email = request.form.get('email')
            user = User.query.filter_by(email=email).first()
            if user:
                db.session.delete(user)
                db.session.commit()
            # Database connect
            conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
            cursor = conn.cursor()
            # Query execute
            cursor.execute('SELECT * FROM user')
            # Matched row in 'user'
            user = cursor.fetchall()
            failed="Deleted!"

    return render_template('staffDetails.html',user=user,failed=failed)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query')
        results = User.query.filter(User.name.ilike(f'%{query}%')).all()
        prisoner_results = Prisoner.query.filter(Prisoner.name.ilike(f'%{query}%')).all()
        return render_template('search.html', results=results, prisoner_results=prisoner_results)
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)