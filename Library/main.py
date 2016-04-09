import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash 
# from flask.ext.login  import LoginManager
from flask.ext.bcrypt import Bcrypt 

#Configuration
DATABASE = 'database/library.db'
DEBUG = True
SECRET_KEY = 'Development key'
USERNAME = 'admin'
PASSWORD = 'admin'

#create application
app = Flask(__name__)
app.config.from_object(__name__)

#Flask-Bcrypt
bcrypt = Bcrypt(app) 

#Home Page
@app.route('/')
def index():
    return render_template('home.html')

#Navigate to Reader signup or Library Signup
@app.route('/signup')
def signup():
    return render_template('signup.html')

#display reader sign up form   
@app.route('/signup_reader')
def signup_reader():    
    return render_template('signup_reader.html')
    
@app.route('/add_reader', methods=['POST'])
def add_reader():

    if request.method == 'POST':
        try:
            g.db.execute('insert into Reader (reader_id, lib_id, reader_name, reader_type, password) values (?, ?, ?, ?, ?)', 
                [ request.form['reader_id'], request.form['lib_id'], request.form['reader_name'], request.form['reader_type'], request.form['password'] ])
            g.db.commit()
            return redirect( url_for('login', username=request.form['reader_id'], type="Reader") )
        except:
            print "could not commit to db"      
    else:
        pass
    
    return redirect( url_for('signup_reader') )
    
    
@app.route('/reader_home')
def reader_home():

    # show a list of all books the reader currently has checked out.. 

    return render_template('library_home.html')
        
#display library sign up form   
@app.route('/signup_library')
def signup_library():
    return render_template('signup_library.html')
    
@app.route('/add_library', methods=['POST'])
def add_library():

    if request.method == 'POST':
        try:
            g.db.execute('insert into Library (lib_id, lib_name, state, city, zip_code, password) values (?, ?, ?, ?, ?, ?)', 
                    [ request.form['lib_id'], request.form['lib_name'], request.form['lib_state'], request.form['lib_city'], request.form['lib_zip_code'], request.form['password'] ])
            g.db.commit()
            return redirect( url_for('login', username=request.form['lib_id'], type="Library") )
        except:
            print "could not commit to db"        
    else:
        pass
    
    return redirect( url_for('signup_library') )

#display login form
@app.route('/login/')
@app.route('/login/<username>/')
@app.route('/login/<username>/<type>/')
def login(username=None, type=None):

    context = {
        "username": username,
        "type": type
    }

    return render_template('login.html', context=context)
    
@app.route('/user_login', methods=['POST'])
def user_login():

    if request.method == 'POST':
        entries = ''
        
        if request.form['radios'] == 'reader':
            try:
                cur = g.db.execute('select reader_id, password from reader where reader_id = (?) and password = (?)', 
                    [ request.form['username'], request.form['password']  ])
                entries = [dict(username=row[0], password=row[1]) for row in cur.fetchall()]
                session['reader_logged_in'] = True
                session['reader_id'] = request.form['username']
            except:
                print "could not find reader in DB"  
        elif request.form['radios'] == 'library':
            try:
                cur = g.db.execute('select lib_id, password from library where lib_id = (?) and password = (?)', 
                    [ request.form['username'], request.form['password']  ])
                entries = [dict(username=row[0], password=row[1]) for row in cur.fetchall()]
                session['lib_logged_in'] = True
                session['lib_id'] = request.form['username']
                return redirect( url_for('library_home') )
            except:
                print "could not find library in DB"  
        else:
            print "Request is not valid"
        
        print 'User: '
        print entries
        
        if entries:
            print "Login as :" + request.form['radios']
        else:
            print "Invalid login"
    
    else:
        pass
    
    return redirect( url_for('login') )
    
@app.route('/library_home')
def library_home():

    # show a list of all books in inventory of this library and their status, location etc.. 

    return render_template('library_home.html')
    
@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

if __name__ == "__main__":
    app.run()
    
# @app.route('/inventory/')
# @app.route('/inventory/<param>/')
# def inventory(param=None):
#     context = { 
#         'title': param
#     }
#     print param

#     return render_template('inventory.html', context=context)
    
# @app.route('/register', methods=['GET','POST'])
# def register():
    
#     message = ''
    
#     if request.method == 'POST':
#         if request.form['password1'] != request.form['password2']:
#             message = 'Passwords do not match'
#         else:
#             if request.form['password1'] != '':
#                 password = request.form['password1']
#                 pw_hash = bcrypt.generate_password_hash(password)
#                 print pw_hash
#                 print bcrypt.check_password_hash(pw_hash, password)
#                 if bcrypt.check_password_hash(pw_hash, password) == True:
#                     g.db.execute('insert into user (username, password) values (?, ?)', [request.form['email'], pw_hash])
#                     g.db.commit()
#                     print request.form['email'] 
#                     print request.form['password1']
#                     message = 'Thanks'
#             else:
#                 message = 'Please enter a valid password'
    
#     context = {
#         'message': message
#     } 
    
#     return render_template('register.html', context=context)
    
# @app.route('/users')
# @app.route('/users/<user>/')
# def users(user=None):

#     if user == None:
#         cur = g.db.execute('select * from user')
#         entries = [dict(email=row[0], password=row[1]) for row in cur.fetchall()]
#         print "Print All"
#         print entries
#     else:
#         cur = g.db.execute('select * from user where username = (?)', [user])
#         entries = [dict(email=row[0], password=row[1]) for row in cur.fetchall()]
#         print "Print Single" 
#         print entries 
    
#     return render_template('users.html', entries=entries)
    
# @app.route('/login', methods=['GET','POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         print 'POST REQUEST ACCEPTED'
        
#         pw_hash = bcrypt.generate_password_hash(  request.form['password'])
#         print pw_hash
#         print bcrypt.check_password_hash(pw_hash, request.form['password'])
        
#         cur = g.db.execute('select * from user where username=(?) and password=(?)', ( request.form['username'], pw_hash) )
#         entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
#         print entries
       
#         if  entries != '': 
#             session['logged_in'] = True
#             flash('You were logged in')
#             return redirect(url_for('users'))
            
            
#     return render_template('login.html', error=error)
    
# @app.route('/logout')
# def logout():    
#     session.pop('logged_in', None)
#     flash('You were logged out')
#     return redirect(url_for('show_entries'))
    
# @app.route('/add', methods=['POST'])
# def add_entry():
#     if not session.get('logged_in'):
#         abort(401)
#     g.db.execute('insert into entries (title, text) values (?, ?)', [request.form['title'], request.form['text']])
#     g.db.commit()
#     #flash('New entry was successfully posted')
#     print request.form['title']
#     print request.form['text']
#     return redirect(url_for('show_entries'))
