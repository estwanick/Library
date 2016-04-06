import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash 
# from flask.ext.login  import LoginManager
from flask.ext.bcrypt import Bcrypt 

#Configuration
DATABASE = 'database/articles.db'
DEBUG = True
SECRET_KEY = 'Development key'
USERNAME = 'admin'
PASSWORD = 'admin'

#create application
app = Flask(__name__)
app.config.from_object(__name__)

#Flask-Login
# login_manager = LoginManager()
# login_manager.init_app(app)

#Flask-Bcrypt
bcrypt = Bcrypt(app) 

# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id) 

@app.route('/inventory/')
@app.route('/inventory/<param>/')
def inventory(param=None):
    context = { 
        'title': param
    }
    print param

    return render_template('inventory.html', context=context)
    
@app.route('/register', methods=['GET','POST'])
def register():
    
    message = ''
    
    if request.method == 'POST':
        if request.form['password1'] != request.form['password2']:
            message = 'Passwords do not match'
        else:
            if request.form['password1'] != '':
                password = request.form['password1']
                pw_hash = bcrypt.generate_password_hash(password)
                print pw_hash
                print bcrypt.check_password_hash(pw_hash, password)
                if bcrypt.check_password_hash(pw_hash, password) == True:
                    g.db.execute('insert into user (username, password) values (?, ?)', [request.form['email'], pw_hash])
                    g.db.commit()
                    print request.form['email'] 
                    print request.form['password1']
                    message = 'Thanks'
            else:
                message = 'Please enter a valid password'
    
    context = {
        'message': message
    } 
    
    return render_template('register.html', context=context)
    
@app.route('/users')
@app.route('/users/<user>/')
def users(user=None):

    if user == None:
        cur = g.db.execute('select * from user')
        entries = [dict(email=row[0], password=row[1]) for row in cur.fetchall()]
        print "Print All"
        print entries
    else:
        cur = g.db.execute('select * from user where username = (?)', [user])
        entries = [dict(email=row[0], password=row[1]) for row in cur.fetchall()]
        print "Print Single" 
        print entries 
    
    return render_template('users.html', entries=entries)
    
@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        print 'POST REQUEST ACCEPTED'
        
        pw_hash = bcrypt.generate_password_hash(  request.form['password'])
        print pw_hash
        print bcrypt.check_password_hash(pw_hash, request.form['password'])
        
        cur = g.db.execute('select * from user where username=(?) and password=(?)', ( request.form['username'], pw_hash) )
        entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
        print entries
       
        if  entries != '': 
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('users'))
            
            
    return render_template('login.html', error=error)
    
@app.route('/logout')
def logout():    
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/')
def show_entries():

    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    print entries
    
    return render_template('show_entries.html')
    
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)', [request.form['title'], request.form['text']])
    g.db.commit()
    #flash('New entry was successfully posted')
    print request.form['title']
    print request.form['text']
    return redirect(url_for('show_entries'))
    
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
