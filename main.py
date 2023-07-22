from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import MySQLdb
import hashlib

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
    cell = db.Column(db.String(120), nullable=False)

@app.route('/')
@app.route('/home')
def home():
    session['email'] = ""
    return render_template('home.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    failed = ""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Database connect
        conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
        cursor = conn.cursor()
        # Query execute
        cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
        # Matched row in 'user'
        user = cursor.fetchone()
        if user is not None:
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            cursor.execute('SELECT * FROM user WHERE password = %s And email = %s', (hashed_password,email))
            user1 = cursor.fetchone()
            if user1 is not None:
                session['id'] = user[0]
                session['email'] = user[3]
                if user[2] == "Cleaner":
                    return redirect(url_for('cleaner'))
                elif user[2] == "Chef":
                    return redirect(url_for('chef'))
                else:
                    return redirect(url_for('police'))
            else:
                failed = "Password Does Not Match!"
        else:
            failed = "Email Not Found!"
        
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
        cursor.execute('SELECT * FROM admin WHERE `email` = %s', (email,))
        # Matched row in 'user'
        user = cursor.fetchone()

        if user is not None:
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            cursor.execute('SELECT * FROM admin WHERE password = %s And email = %s', (hashed_password,email))
            user1 = cursor.fetchone()
            if user1 is not None:
                session['email'] = user[1]
                return redirect(url_for('adminDash'))
            else:
                failed = "Password Does Not Matched!"
                # return redirect(url_for('admin'))
        else:
            failed = "Email Not Found!"
    return render_template('admin.html',failed=failed)

@app.route('/cleaner')
def cleaner():
    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
    cursor = conn.cursor()
    # Query execute
    cursor.execute('SELECT * FROM user WHERE email = %s', (session['email'],))
    # Matched row in 'user'
    user = cursor.fetchone()
    if user != None:
        if user[2] == 'Cleaner': 
            return render_template('cleaner.html')
        else:
            return render_template('error.html')
    else:
        return render_template('error.html')

@app.route('/police')
def police():
    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
    cursor = conn.cursor()
    # Query execute
    cursor.execute('SELECT * FROM user WHERE email = %s', (session['email'],))
    # Matched row in 'user'
    user = cursor.fetchone()
    if user != None:
        if user[2] == 'Police': 
            return render_template('police.html')
        else:
            return render_template('error.html')
    else:
        return render_template('error.html')

@app.route('/chef')
def chef():
    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
    cursor = conn.cursor()
    # Query execute
    cursor.execute('SELECT * FROM user WHERE email = %s', (session['email'],))
    # Matched row in 'user'
    user = cursor.fetchone()
    if user != None:
        if user[2] == 'Chef': 
            return render_template('chef.html')
        else:
            return render_template('error.html')
    else:
        return render_template('error.html')

@app.route('/adminDash')
def adminDash():
    if session['email'] != 'czaber49@gmail.com':
        return render_template('error.html')
    else:
        return render_template('adminDash.html')

@app.route('/staffDetails', methods = ['GET','POST'])
def staffDetails():
    info = 'staff'
    if session['email'] != 'czaber49@gmail.com':
        return render_template('error.html')
    else:
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
                    #hashed password
                    hashedPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()

                    entry = User(name=name, role=role, password=hashedPassword, email=email)
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
                    user.password = hashlib.sha256(request.form.get('password').encode('utf-8')).hexdigest()
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
            elif '🍳' == request.form.get('btn'):
                email = request.form.get('email')
                user = User.query.filter_by(email=email).first()
                # Database connect
                conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
                cursor = conn.cursor()
                # Query execute
                cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
                # Matched row in 'user'
                user = cursor.fetchall()
                    
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

        return render_template('staffDetails.html',user=user,failed=failed,info=info)
    
@app.route('/prisonerInfo', methods = ['GET','POST'])
def prisonerInfo():
    info = 'prisoner'
    if session['email'] != 'czaber49@gmail.com':
        return render_template('error.html')
    else:
        failed= ""
        # Database connect
        conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
        cursor = conn.cursor()
        # Query execute
        cursor.execute('SELECT * FROM prisoner')
        # Matched row in 'user'
        user = cursor.fetchall()

        if request.method == 'POST':
            if 'Add' == request.form.get('btn'):
                name = request.form.get('name')
                age = request.form.get('age')
                birth = request.form.get('birth')
                record = request.form.get('record')
                cell = request.form.get('cell')
                year = request.form.get('year')

                existing_user = Prisoner.query.filter_by(cell=cell).first()
                if existing_user:
                    failed="Cell already full. Please choose a different cell!"
                else:
                    entry = Prisoner(name=name, age=age, birth=birth, record=record, cell=cell, year=year)
                    db.session.add(entry)
                    db.session.commit()
                    # Database connect
                    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
                    cursor = conn.cursor()
                    # Query execute
                    cursor.execute('SELECT * FROM prisoner')
                    # Matched row in 'user'
                    user = cursor.fetchall()
                    failed="Added!"
            elif 'Modify' == request.form.get('btn'):
                cell = request.form.get('cell')
                user = Prisoner.query.filter_by(cell=cell).first()
                if user:
                    user.name = request.form.get('name')
                    user.age = request.form.get('age')
                    user.birth = request.form.get('birth')
                    user.record = request.form.get('record')
                    user.cell = request.form.get('cell')
                    user.year = request.form.get('year')
                    db.session.commit()
                    # Database connect
                    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
                    cursor = conn.cursor()
                    # Query execute
                    cursor.execute('SELECT * FROM prisoner')
                    # Matched row in 'user'
                    user = cursor.fetchall()
                    failed="Changed!"
            elif '🍳' == request.form.get('btn'):
                cell = request.form.get('cell')
                user = Prisoner.query.filter_by(cell=cell).first()
                # Database connect
                conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
                cursor = conn.cursor()
                # Query execute
                cursor.execute('SELECT * FROM prisoner WHERE cell = %s', (cell,))
                # Matched row in 'user'
                user = cursor.fetchall()
                    
            else:
                cell = request.form.get('cell')
                user = Prisoner.query.filter_by(cell=cell).first()
                if user:
                    db.session.delete(user)
                    db.session.commit()
                # Database connect
                conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
                cursor = conn.cursor()
                # Query execute
                cursor.execute('SELECT * FROM prisoner')
                # Matched row in 'user'
                user = cursor.fetchall()
                failed="Deleted!"

        return render_template('prisonerInfo.html',user=user,failed=failed,info=info)

if __name__ == '__main__':
    app.run(debug=True)