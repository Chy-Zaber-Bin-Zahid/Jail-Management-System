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

class Request(db.Model):
    email = db.Column(db.String(200), primary_key=True)
    shift = db.Column(db.String(200), nullable=False)
    reason = db.Column(db.String(1000), nullable=False)
    role = db.Column(db.String(1000), nullable=False)

class Schedule(db.Model):
    email = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(1000), nullable=False)
    shift = db.Column(db.String(1000), nullable=False)
    time = db.Column(db.String(1000), nullable=False)
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
    session['email'] = ""
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
                elif user[2] == "Deputy Warden":
                    return redirect(url_for('deputy'))
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
    session['email'] = ""
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

@app.route('/deputy', methods = ['GET','POST'])
def deputy():
    em = session['email']
    info = 'deputy'
    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
    cursor = conn.cursor()
    # Query execute
    if session['email'] != 'czaber49@gmail.com':
        cursor.execute('SELECT * FROM user WHERE email = %s', (session['email'],))
    else:
        cursor.execute('SELECT * FROM admin WHERE email = %s', (session['email'],))
    # Matched row in 'user'
    user = cursor.fetchone()
    if user != None:
        if user[2] == 'Deputy Warden' or session['email'] == 'czaber49@gmail.com':
            failed= ""
            # Database connect
            conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
            cursor = conn.cursor()
            # Query execute
            cursor.execute('SELECT * FROM schedule Where type = %s',('Not Assigned',))
            # Matched row in 'user'
            user = cursor.fetchall()
            if user:
                if request.method == 'POST':
                #     if 'Add' == request.form.get('btn'):
                #         name = request.form.get('name')
                #         email = request.form.get('email')
                #         type = request.form.get('type')
                #         shift = request.form.get('shift')
                #         time = request.form.get('time')

                #         existing_user = Schedule.query.filter_by(email=email).first()
                #         if existing_user:
                #             failed="Email already exists. Please choose a different email!"
                #         else:
                #             entry = Schedule(name=name, shift=shift, type=type, email=email, time=time)
                #             db.session.add(entry)
                #             db.session.commit()
                #             # Database connect
                #             conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
                #             cursor = conn.cursor()
                #             # Query execute
                #             cursor.execute('SELECT * FROM schedule Where type = %s',('Not Assigned',))
                #             # Matched row in 'user'
                #             user = cursor.fetchall()
                #             failed="Added!"
                    if 'Modify' == request.form.get('btn'):
                        email = request.form.get('email')
                        user = Schedule.query.filter_by(email=email).first()
                        if user:
                            user.type = request.form.get('type')
                            user.shift = request.form.get('shift')
                            user.time = request.form.get('time')
                            
                            db.session.commit()
                            # Database connect
                            conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
                            cursor = conn.cursor()
                            # Query execute
                            cursor.execute('SELECT * FROM schedule Where type = %s',('Not Assigned',))
                            # Matched row in 'user'
                            user = cursor.fetchall()
                            if not user:
                                user = "Nothing"
                            failed="Changed!"
                    elif '🍳' == request.form.get('btn'):
                        email = request.form.get('email')
                        user = Schedule.query.filter_by(email=email).first()
                        # Database connect
                        conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
                        cursor = conn.cursor()
                        # Query execute
                        cursor.execute('SELECT * FROM schedule WHERE email = %s', (email,))
                        # Matched row in 'user'
                        user = cursor.fetchall()
                            
                    # else:
                    #     email = request.form.get('email')
                    #     user = Schedule.query.filter_by(email=email).first()
                    #     if user:
                    #         db.session.delete(user)
                    #         db.session.commit()
                    #     # Database connect
                    #     conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
                    #     cursor = conn.cursor()
                    #     # Query execute
                    #     cursor.execute('SELECT * FROM schedule')
                    #     # Matched row in 'user'
                    #     user = cursor.fetchall()
                    #     # failed="Deleted!"
            else:
                user = 'Nothing'

            return render_template('deputy.html',user=user,failed=failed,info=info, em=em)
        else:
            return render_template('error.html')
    else:
        return render_template('error.html')

@app.route('/cleaner', methods = ['GET','POST'])
def cleaner():
    if request.method == 'POST':
        req="Request Send!"
        shift = request.form.get('shift')
        email = session['email']
        reason = request.form.get('reason')
        existing_user = Request.query.filter_by(email=email).first()
        if existing_user:
            req="Already Requested!"
             # Database connect
            conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
            cursor = conn.cursor()
            # Query execute
            cursor.execute('SELECT * FROM schedule WHERE email = %s', (session['email'],))
            # Matched row in 'user'
            user = cursor.fetchall()
            # Create a new tuple with the additional element "Cleaner"
            user = user[0] + ('Cleaner',)
            # Create a double tuple with the inner tuple
            user = (user,)
            return render_template('cleaner.html',user=user,req=req,email=session['email'])
        else:
            entry = Request(shift=shift, email=email, reason=reason,role = 'Cleaner')
            db.session.add(entry)
            db.session.commit()
            # Database connect
            conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
            cursor = conn.cursor()
            # Query execute
            cursor.execute('SELECT * FROM schedule WHERE email = %s', (session['email'],))
            # Matched row in 'user'
            user = cursor.fetchall()
            # Create a new tuple with the additional element "Cleaner"
            user = user[0] + ('Cleaner',)
            # Create a double tuple with the inner tuple
            user = (user,)
            return render_template('cleaner.html',user=user,req=req,email=session['email'])
    else:
        # req = 'You Can Request For Schedule Change Only Once!'
        conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
        cursor = conn.cursor()
        # Query execute
        cursor.execute('SELECT * FROM user WHERE email = %s', (session['email'],))
        # Matched row in 'user'
        user = cursor.fetchone()
        if user != None:
            if user[2] == 'Cleaner': 
                # Database connect
                conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
                cursor = conn.cursor()
                # Query execute
                cursor.execute('SELECT * FROM schedule WHERE email = %s And type = %s' , (session['email'],'Not Assigned'))
                # Matched row in 'user'
                user = cursor.fetchall()
                # Create a new tuple with the additional element "Cleaner"
                if user:
                    cursor.execute('SELECT * FROM user WHERE email = %s', (session['email'],))
                    # Matched row in 'user'
                    user = cursor.fetchall()
                    user = user[0] + ('Cleaner',)
                    # Create a double tuple with the inner tuple
                    user = (user,)
                    return render_template('cleaner.html',user=user,req="Your Work Schedule Will Be Updated Soon!",email=session['email'])
                else:
                    # Database connect
                    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
                    cursor = conn.cursor()
                    # Query execute
                    cursor.execute('SELECT * FROM schedule WHERE email = %s' , (session['email'],))
                    # Matched row in 'user'
                    user = cursor.fetchall()
                    user = user[0] + ('Cleaner',)
                    # Create a double tuple with the inner tuple
                    user = (user,)
                    return render_template('cleaner.html',user=user,req="You Can't Request Again If You Already Have A Pending Request!",email=session['email'])
            else:
                return render_template('error.html')
        else:
            return render_template('error.html')

@app.route('/police', methods = ['GET','POST'])
def police():
    if request.method == 'POST':
        req="Request Send!"
        shift = request.form.get('shift')
        email = session['email']
        reason = request.form.get('reason')
        existing_user = Request.query.filter_by(email=email).first()
        if existing_user:
            req="Already Requested!"
             # Database connect
            conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
            cursor = conn.cursor()
            # Query execute
            cursor.execute('SELECT * FROM schedule WHERE email = %s', (session['email'],))
            # Matched row in 'user'
            user = cursor.fetchall()
            # Create a new tuple with the additional element "Police"
            user = user[0] + ('Police',)
            # Create a double tuple with the inner tuple
            user = (user,)
            return render_template('cleaner.html',user=user,req=req,email=session['email'])
        else:
            entry = Request(shift=shift, email=email, reason=reason,role = 'Police')
            db.session.add(entry)
            db.session.commit()
            # Database connect
            conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
            cursor = conn.cursor()
            # Query execute
            cursor.execute('SELECT * FROM schedule WHERE email = %s', (session['email'],))
            # Matched row in 'user'
            user = cursor.fetchall()
            # Create a new tuple with the additional element "Police"
            user = user[0] + ('Police',)
            # Create a double tuple with the inner tuple
            user = (user,)
            return render_template('cleaner.html',user=user,req=req,email=session['email'])
    else:
        conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
        cursor = conn.cursor()
        # Query execute
        cursor.execute('SELECT * FROM user WHERE email = %s', (session['email'],))
        # Matched row in 'user'
        user = cursor.fetchone()
        if user != None:
            if user[2] == 'Police': 
                    # Database connect
                conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
                cursor = conn.cursor()
                # Query execute
                cursor.execute('SELECT * FROM schedule WHERE email = %s', (session['email'],))
                # Matched row in 'user'
                user = cursor.fetchall()
                # Database connect
                conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
                cursor = conn.cursor()
                # Query execute
                cursor.execute('SELECT * FROM schedule WHERE email = %s And type = %s' , (session['email'],'Not Assigned'))
                # Matched row in 'user'
                user = cursor.fetchall()
                # Create a new tuple with the additional element "Cleaner"
                if user:
                    cursor.execute('SELECT * FROM user WHERE email = %s', (session['email'],))
                    # Matched row in 'user'
                    user = cursor.fetchall()
                    user = user[0] + ('Police',)
                    # Create a double tuple with the inner tuple
                    user = (user,)
                    return render_template('police.html',user=user,req="Your Work Schedule Will Be Updated Soon!",email=session['email'])
                else:
                    # Database connect
                    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
                    cursor = conn.cursor()
                    # Query execute
                    cursor.execute('SELECT * FROM schedule WHERE email = %s' , (session['email'],))
                    # Matched row in 'user'
                    user = cursor.fetchall()
                    user = user[0] + ('Police',)
                    # Create a double tuple with the inner tuple
                    user = (user,)
                    return render_template('police.html',user=user,req="You Can't Request Again If You Already Have A Pending Request!",email=session['email'])
            else:
                return render_template('error.html')
        else:
            return render_template('error.html')

@app.route('/chef', methods = ['GET','POST'])
def chef():
    if request.method == 'POST':
        req="Request Send!"
        shift = request.form.get('shift')
        email = session['email']
        reason = request.form.get('reason')
        existing_user = Request.query.filter_by(email=email).first()
        if existing_user:
            req="Already Requested!"
             # Database connect
            conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
            cursor = conn.cursor()
            # Query execute
            cursor.execute('SELECT * FROM schedule WHERE email = %s', (session['email'],))
            # Matched row in 'user'
            user = cursor.fetchall()
            # Create a new tuple with the additional element "Chef"
            user = user[0] + ('Chef',)
            # Create a double tuple with the inner tuple
            user = (user,)
            return render_template('cleaner.html',user=user,req=req,email=session['email'])
        else:
            entry = Request(shift=shift, email=email, reason=reason,role = 'Chef')
            db.session.add(entry)
            db.session.commit()
            # Database connect
            conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
            cursor = conn.cursor()
            # Query execute
            cursor.execute('SELECT * FROM schedule WHERE email = %s', (session['email'],))
            # Matched row in 'user'
            user = cursor.fetchall()
            # Create a new tuple with the additional element "Chef"
            user = user[0] + ('Chef',)
            # Create a double tuple with the inner tuple
            user = (user,)
            return render_template('cleaner.html',user=user,req=req,email=session['email'])
    else:
        conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
        cursor = conn.cursor()
        # Query execute
        cursor.execute('SELECT * FROM user WHERE email = %s', (session['email'],))
        # Matched row in 'user'
        user = cursor.fetchone()
        if user != None:
            if user[2] == 'Chef': 
                # Database connect
                conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
                cursor = conn.cursor()
                # Query execute
                cursor.execute('SELECT * FROM schedule WHERE email = %s', (session['email'],))
                # Matched row in 'user'
                user = cursor.fetchall()
                # Database connect
                conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
                cursor = conn.cursor()
                # Query execute
                cursor.execute('SELECT * FROM schedule WHERE email = %s And type = %s' , (session['email'],'Not Assigned'))
                # Matched row in 'user'
                user = cursor.fetchall()
                # Create a new tuple with the additional element "Cleaner"
                if user:
                    cursor.execute('SELECT * FROM user WHERE email = %s', (session['email'],))
                    # Matched row in 'user'
                    user = cursor.fetchall()
                    user = user[0] + ('Chef',)
                    # Create a double tuple with the inner tuple
                    user = (user,)
                    return render_template('chef.html',user=user,req="Your Work Schedule Will Be Updated Soon!",email=session['email'])
                else:
                    # Database connect
                    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
                    cursor = conn.cursor()
                    # Query execute
                    cursor.execute('SELECT * FROM schedule WHERE email = %s' , (session['email'],))
                    # Matched row in 'user'
                    user = cursor.fetchall()
                    user = user[0] + ('Chef',)
                    # Create a double tuple with the inner tuple
                    user = (user,)
                    return render_template('chef.html',user=user,req="You Can't Request Again If You Already Have A Pending Request!",email=session['email'])
            else:
                return render_template('error.html')
        else:
            return render_template('error.html')

@app.route('/adminDash')
def adminDash():
    if session['email'] != 'czaber49@gmail.com':
        return render_template('error.html')
    else:
        # Database connect
        conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
        cursor = conn.cursor()
        # Query execute
        cursor.execute('SELECT role, COUNT(*) as role_count FROM user WHERE role IN (%s, %s, %s) GROUP BY role', ('Cleaner', 'Chef', 'Police'))
        # Matched row in 'user'
        user = cursor.fetchall()
        cursor.execute('SELECT COUNT(*) as row_count FROM prisoner')
        prisoner = cursor.fetchone()
        cursor.execute('''
    SELECT roles.role, COALESCE(COUNT(request.role), 0) as role_count
    FROM (
        SELECT 'Cleaner' as role
        UNION ALL
        SELECT 'Chef' as role
        UNION ALL
        SELECT 'Police' as role
    ) as roles
    LEFT JOIN request ON roles.role = request.role
    GROUP BY roles.role
''')
        req = cursor.fetchall()
        return render_template('adminDash.html',user=user,prisoner=prisoner,req=req)

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

                    if role != "Deputy Warden":
                        entry = Schedule(name=name, email=email, type='Not Assigned', shift='Not Assigned', time='Not Assigned',role = role)
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
                    if role != 'Deputy Warden':
                         user = Schedule.query.filter_by(email=email).first()
                         user.name = request.form.get('name')
                         user.role = request.form.get('role')
                    else:
                        user = Schedule.query.filter_by(email=email).first()
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
                    user = Schedule.query.filter_by(email=email).first()
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
                # failed="Deleted!"

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
                cell1=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
                name = request.form.get('name')
                age = request.form.get('age')
                birth = request.form.get('birth')
                record = request.form.get('record')
                # cell = request.form.get('cell')
                year = request.form.get('year')
                cell=''
                for i in cell1:
                    for j in range(1,11):
                        cellCheck = str(j)+i
                        existing_user = Prisoner.query.filter_by(cell=cellCheck).first()
                        if existing_user:
                            continue
                        else:
                            break
                    if existing_user:
                        continue
                    else:
                        cell = cellCheck
                        break
                if cell == '':
                    failed="Prison Is Full!"
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
                # failed="Deleted!"

        return render_template('prisonerInfo.html',user=user,failed=failed,info=info)

@app.route('/req', methods = ['GET','POST'])
def req():
    param1 = request.args.get('param1')
    if session['email'] != 'czaber49@gmail.com':
        return render_template('error.html')
    elif request.method == 'POST':
        btn = request.form.get('btn')
        email = request.form.get('email')
        shift = request.form.get('shift')
        staff = request.form.get('staff')
        if btn == 'accept':
            user = Schedule.query.filter_by(email=email).first()
            if user:
                user.shift = request.form.get('shift')
                if shift == 'Day':
                    user.time = '8AM - 3PM'
                else:
                    user.time = '9PM - 12AM' 
                db.session.commit()
            user = Request.query.filter_by(email=email).first()
            if user:
                db.session.delete(user)
                db.session.commit()
            if param1 == "Guard" or staff == "Police":
                # Database connect
                conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
                cursor = conn.cursor()
                # Query execute
                cursor.execute('SELECT * FROM request Where role = %s', ('Police',))
                # Matched row in 'user'
                user = cursor.fetchall()
                return render_template('request.html',user=user)
            elif param1 == "Chef" or staff == 'Chef':
                # Database connect
                conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
                cursor = conn.cursor()
                # Query execute
                cursor.execute('SELECT * FROM request Where role = %s', ('Chef',))
                # Matched row in 'user'
                user = cursor.fetchall()
                return render_template('request.html',user=user)
            else:
                # Database connect
                conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
                cursor = conn.cursor()
                # Query execute
                cursor.execute('SELECT * FROM request Where role = %s', ('Cleaner',))
                # Matched row in 'user'
                user = cursor.fetchall()
                return render_template('request.html',user=user)
        else:
            user = Request.query.filter_by(email=email).first()
            if user:
                db.session.delete(user)
                db.session.commit()
            if param1 == "Guard" or staff == "Police":
                # Database connect
                conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
                cursor = conn.cursor()
                # Query execute
                cursor.execute('SELECT * FROM request Where role = %s', ('Police',))
                # Matched row in 'user'
                user = cursor.fetchall()
                return render_template('request.html',user=user)
            elif param1 == "Chef" or staff == "Chef":
                # Database connect
                conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
                cursor = conn.cursor()
                # Query execute
                cursor.execute('SELECT * FROM request Where role = %s', ('Chef',))
                # Matched row in 'user'
                user = cursor.fetchall()
                return render_template('request.html',user=user)
            else:
                # Database connect
                conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
                cursor = conn.cursor()
                # Query execute
                cursor.execute('SELECT * FROM request Where role = %s', ('Cleaner',))
                # Matched row in 'user'
                user = cursor.fetchall()
                return render_template('request.html',user=user)
    else:
        if param1 == "Guard":
            # Database connect
            conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
            cursor = conn.cursor()
            # Query execute
            cursor.execute('SELECT * FROM request Where role = %s', ('Police',))
            # Matched row in 'user'
            user = cursor.fetchall()
            return render_template('request.html',user=user)
        elif param1 == "Chef":
            # Database connect
            conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
            cursor = conn.cursor()
            # Query execute
            cursor.execute('SELECT * FROM request Where role = %s', ('Chef',))
            # Matched row in 'user'
            user = cursor.fetchall()
            return render_template('request.html',user=user)
        else:
            # Database connect
            conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='jailmanage')
            cursor = conn.cursor()
            # Query execute
            cursor.execute('SELECT * FROM request Where role = %s', ('Cleaner',))
            # Matched row in 'user'
            user = cursor.fetchall()
            return render_template('request.html',user=user)
       

if __name__ == '__main__':
    app.run(debug=True)