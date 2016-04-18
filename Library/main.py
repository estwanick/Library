import sqlite3, time, datetime
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash 
# from flask.ext.login  import LoginManager


#Configuration
DATABASE = 'database/library.db'
DEBUG = True
SECRET_KEY = 'Development key'
USERNAME = 'admin'
PASSWORD = 'admin'


#create application
app = Flask(__name__)
app.config.from_object(__name__)


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
            g.db.execute('insert into Reader (reader_id,reader_name, reader_type, password) values (?, ?, ?, ?)', 
                [ request.form['reader_id'], request.form['reader_name'], request.form['reader_type'], request.form['password'] ])
            g.db.commit()
            g.db.execute('insert into Member_of (reader_id, lib_id) values (?, ?)', 
                [ request.form['reader_id'], request.form['lib_id'] ])
            g.db.commit()
            return redirect( url_for('login', username=request.form['reader_id'], type="Reader") )
        except:
            print "could not commit to db"      
    else:
        pass
    
    return redirect( url_for('signup_reader') )
    
    
@app.route('/reader_home')
def reader_home():
    # show a list of all books the reader has checked out
    query = ''' select b.lib_id, b.doc_id, b.doc_copy, b.borrow_date, b.exp_return, d.doc_title, b.borrow_id 
                from borrow as b
                inner join document as d
                   on b.doc_id = d.doc_id
                where b.reader_id = (?)
                  and not exists( select * 
                                  from return as r
                                    where r.return_id = b.borrow_id )
            '''
    
    cur = g.db.execute( query, [session['reader_id']] ) 
    # cur = g.db.execute('select lib_id, doc_id, doc_copy, borrow_date, exp_return from borrow where reader_id = (?)', [session['reader_id']] )
    rows = [dict(lib_id=row[0], doc_id=row[1], doc_copy=row[2], borrow_date=row[3], exp_return=row[4], doc_title=row[5], borrow_id=row[6]) for row in cur.fetchall()]
    todays_date = time.strftime("%Y-%m-%d")
    for row in rows:
        if row['exp_return'] < todays_date:
            row['doc_status'] = 'Overdue'
        else:
            row['doc_status'] = 'Good'
            
    # show a list of all books the reader has returned
    returnquery = ''' select r.lib_id, r.doc_id, r.doc_copy, r.actual_return, d.doc_title, r.return_id 
                from return as r
                inner join document as d
                    on r.doc_id = d.doc_id
                where r.reader_id = (?) 
            '''
    
    returncur = g.db.execute( returnquery, [session['reader_id']] ) 
    returnrows = [dict(lib_id=row[0], doc_id=row[1], doc_copy=row[2], actual_return=row[3], doc_title=row[4], return_id=row[5]) for row in returncur.fetchall()]
    
    
    return render_template('reader_home.html', rows=rows, returnrows=returnrows)

@app.route('/doc_return/<borrow_id>')
def doc_return(borrow_id=None):
    
    if borrow_id:
        query = ''' select d.doc_title, b.lib_id, b.doc_id, b.doc_copy, b.borrow_id
            from borrow as b
            inner join document as d 
            on b.doc_id = d.doc_id 
            where b.borrow_id = (?) 
            '''
        cur = g.db.execute( query, [borrow_id] )
        rows = [dict( doc_name=row[0], lib_id=row[1], doc_id=row[2], doc_copy=row[3], borrow_id=row[4] ) for row in cur.fetchall()]
        print rows
    else:
        pass

    return render_template('return.html', context=rows)
    
@app.route('/dreturn', methods=['POST'])
def dreturn():
    todays_date = time.strftime("%Y-%m-%d")
       
    g.db.execute('insert into return (return_id, reader_id, lib_id, doc_id, doc_copy, actual_return) values (?, ?, ?, ?, ?, ?)', 
                    [ request.form['borrow_id'], session['reader_id'], request.form['return_to'], request.form['doc_id'], request.form['doc_copy'], todays_date ])
    g.db.commit()
    
    g.db.execute('delete from borrow where borrow_id = (?)', [ request.form['borrow_id'] ] )
    g.db.commit()
    
    g.db.execute('update history set returned_to = (?), return_date = (?) where borrow_id = (?)', [ request.form['return_to'], todays_date, request.form['borrow_id'] ] )
    g.db.commit()
    
    g.db.execute('update inventory set curr_location = (?) where doc_id = (?) and doc_copy = (?)', [ request.form['return_to'], request.form['doc_id'], request.form['doc_copy'] ] )
    g.db.commit()
     
    return redirect( url_for('reader_home') )
            
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
                
                #TODO: Get users preferred library
                
                return redirect( url_for('reader_home') )
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
    cur = g.db.execute('select * from inventory where lib_id = (?)', [session['lib_id']])
    rows = [dict(lib_id=row[0], doc_id=row[1], doc_copy=row[2], curr_location=row[3], doc_status=row[4]) for row in cur.fetchall()]
    # print rows[0]['lib_id']
       
    return render_template('library_home.html', rows=rows)

@app.route('/inventory')
def inventory():
    # show a list of all books in inventory of this library and their status, location etc.. 
    query = ''' select d.doc_title, i.doc_copy, i.doc_status, i.curr_location, i.doc_id
            from inventory as i
            inner join document as d 
            on i.doc_id = d.doc_id
            where not exists(
                select *
                from borrow as b
                where b.doc_id   = i.doc_id
                  and b.doc_copy = i.doc_copy
            ) 
            '''
    
    cur = g.db.execute( query )
    rows = [dict( doc_name=row[0], doc_copy=row[1], doc_status=row[2], curr_location=row[3], doc_id=row[4]) for row in cur.fetchall()]
    
    return render_template('inventory.html', rows=rows)

@app.route('/doc_info/<doc_id>')
def doc_info(doc_id=None):
    
    if doc_id:
        query = 'select * from document where doc_id = (?)'
        cur = g.db.execute( query, [doc_id] )
        rows = [dict( doc_name=row[1], doc_desc=row[3] ) for row in cur.fetchall()]
    else:
        pass

    return render_template('doc_info.html', context=rows)

  
@app.route('/borrow/<doc_id>/<doc_copy>')
def borrow(doc_id=None, doc_copy=None):
    
    if doc_id and doc_copy:
        query = ''' select d.doc_title, i.doc_copy, d.doc_type, i.curr_location, i.doc_id, i.lib_id
            from inventory as i
            inner join document as d 
            on i.doc_id = d.doc_id 
            where i.doc_id   = (?) 
              and i.doc_copy = (?)
            '''
        cur = g.db.execute( query, [doc_id, doc_copy] )
        rows = [dict( doc_name=row[0], doc_copy=row[1], doc_desc=row[2], curr_location=row[3], doc_id=row[4], lib_id=row[5] ) for row in cur.fetchall()]
    else:
        pass

    return render_template('borrow.html', context=rows)
    
@app.route('/borrow_doc/<lib_id>/<doc_id>/<doc_copy>')
def borrow_doc(lib_id=None,doc_id=None, doc_copy=None):

    todays_date = time.strftime("%Y-%m-%d")
    date = datetime.datetime.strptime(todays_date, "%Y-%m-%d").date()
    expected_return = date + datetime.timedelta(days=10)
       
    #Insert into borrow 
    g.db.execute('insert into borrow (reader_id, lib_id, doc_id, doc_copy, borrow_date, exp_return) values (?, ?, ?, ?, ?, ?)', 
                    [ session['reader_id'], lib_id, doc_id, doc_copy, todays_date, expected_return ])
    g.db.commit()
    
    #Select current row to get borrow id
    query = ''' select borrow_id
            from borrow
            where doc_id   = (?) 
              and doc_copy = (?)
            '''
    cur = g.db.execute( query, [doc_id, doc_copy] )
    rows = [dict( borrow_id=row[0] ) for row in cur.fetchall()]
        
    #Track borrow History  
    g.db.execute('insert into history (borrow_id, reader_id, borrowed_from, doc_id, doc_copy, borrow_date) values (?, ?, ?, ?, ?, ?)', 
                    [ rows[0]['borrow_id'], session['reader_id'], lib_id, doc_id, doc_copy, todays_date ])
    g.db.commit()
    
    return redirect(url_for('inventory'))
    
    
#Sign out of session
@app.route('/signout')
def signout():
    session.pop('lib_logged_in', None)
    session.pop('reader_logged_in', None)
    return redirect(url_for('index'))
    
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
