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
    
    # show a list of all books the reader is waiting for
    waitquery = ''' select d.doc_title, l.doc_id, l.doc_copy, l.order_date, l.delivery_date, l.status
                    from lend as l 
                    inner join document as d
                        on l.doc_id = d.doc_id
                    where l.for_reader = (?)
                      and l.status = "processing"
            '''
    
    waitcur = g.db.execute( waitquery, [session['reader_id']] ) 
    waitrows = [dict(doc_title=row[0], doc_id=row[1], doc_copy=row[2], wait_date=row[3], delivery_date=row[4], status=row[5]) for row in waitcur.fetchall()]
    
    #When user logs in and the delivery_date >= todays date then create a lineitem in Borrow for that reader/document/copy
    #Libraries will hold documents until readers log in 
    for row in waitrows:
        if row['delivery_date'] <= todays_date:
            #Move to borrow 
            print 'move to borrow!'
    
    return render_template('reader_home.html', rows=rows, returnrows=returnrows, waitrows=waitrows)

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
    
@app.route('/add_to_inventory/<doc_id>/')
def add_to_inventory(doc_id=None):

    get_doc_copy = g.db.execute('select max(doc_copy) from inventory where doc_id = (?)', [ doc_id ])
    doc_copy = get_doc_copy.fetchone()[0]
    print doc_copy
    
    get_max_copies = g.db.execute('select number_copies from document where doc_id = (?)', [ doc_id ])
    max_copy = get_max_copies.fetchone()[0]
    print max_copy
    
    if doc_copy == None:
        doc_copy = 0
    
    #Needs to be tested and fixed
    if int(max_copy) == int(doc_copy):
        flash('No more copies available','error')
        return redirect( url_for('document') )
    else:
        insert_as_copy = doc_copy + 1
        g.db.execute('insert into inventory (lib_id, doc_id, doc_copy, curr_location) values (?, ?, ?, ? )', 
                    [ session['lib_id'], doc_id, insert_as_copy, session['lib_id'] ])
        g.db.commit()
        flash('Document added to inventory!','success')
        return redirect( url_for('document') )
    

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
    query = ''' select i.lib_id, i.doc_id, i.doc_copy, i.curr_location, i.doc_status, d.doc_title
                from inventory as i
                inner join document as d 
                    on d.doc_id = i.doc_id
                where lib_id = (?) and curr_location = (?)
            '''
    cur = g.db.execute( query, [ session['lib_id'], session['lib_id'] ])
    rows = [dict(lib_id=row[0], doc_id=row[1], doc_copy=row[2], curr_location=row[3], doc_status=row[4], doc_title=row[5]) for row in cur.fetchall()]
    #Documents at other libraries
    query = ''' select * 
                from inventory as i
                where lib_id = (?) and curr_location != (?)
                  and not exists (
                      select * from borrow as b where b.doc_id = i.doc_id and b.doc_copy = i.doc_copy
                  )
            '''
    acur = g.db.execute( query, [ session['lib_id'], session['lib_id'] ])
    arows = [dict(lib_id=row[0], doc_id=row[1], doc_copy=row[2], curr_location=row[3], doc_status=row[4]) for row in acur.fetchall()]
    #Documents being borrowed
    bcur = g.db.execute('select * from borrow where lib_id = (?)', [ session['lib_id'] ])
    brows = [dict(borrow_id=row[0], reader_id=row[1], lib_id=row[2], doc_id=row[3], doc_copy=row[4], borrow_date=row[5], exp_return=row[6]) for row in bcur.fetchall()]
    
    todays_date = time.strftime("%Y-%m-%d")
    for row in brows:
        if row['exp_return'] < todays_date:
            row['doc_status'] = 'Overdue'
        else:
            row['doc_status'] = 'Good'
            
     #Orders Placed
    query = ''' select from_lib, order_date, delivery_date, doc_id, doc_copy, status, lend_id
                from lend
                where to_lib = (?)
            '''
    ocur = g.db.execute( query, [ session['lib_id'] ])
    orders = [dict(from_lib=row[0], order_date=row[1], delivery_date=row[2], doc_id=row[3], doc_copy=row[4], doc_status=row[5], lend_id=row[6]) for row in ocur.fetchall()]
    
    #Process Orders
    for row in orders:
        if row['delivery_date'] <= todays_date:
            row['doc_status'] = 'Complete'
            g.db.execute('update lend set status = ("complete") where lend_id = (?)', [ row['lend_id'] ])
            g.db.commit()
            #Once status is complete delivery to reader in waiting queue 
            

    return render_template('library_home.html', rows=rows, arows=arows, brows=brows, orders=orders)

@app.route('/retrieve/<doc_id>/<doc_copy>')    
def retrieve(doc_id=None,doc_copy=None):
    g.db.execute('update inventory set curr_location = (?) where doc_id = (?) and doc_copy = (?)', [ session['lib_id'], doc_id, doc_copy ])
    g.db.commit()
    return redirect( url_for('library_home') );

@app.route('/inventory')
def inventory():
    # show a list of all books in inventory of this library and their status, location etc.. 
    query = ''' select d.doc_title, i.doc_copy, i.doc_status, i.curr_location, i.doc_id
            from inventory as i
            inner join document as d 
            on i.doc_id = d.doc_id
            where i.lib_id = (?)
              and not exists(
                select *
                from borrow as b
                where b.doc_id   = i.doc_id
                  and b.doc_copy = i.doc_copy
            ) 
            '''
    
    cur = g.db.execute( query, [ session['lib_id'] ] )
    rows = [dict( doc_name=row[0], doc_copy=row[1], doc_status=row[2], curr_location=row[3], doc_id=row[4]) for row in cur.fetchall()]
    
    #Unavailble documents
    query = ''' 
            select d.doc_title, d.doc_id
            from document as d
            where not exists(
                select i.doc_id
                from inventory as i 
                where i.lib_id = (?)
                and i.doc_id = d.doc_id 
            )
            and exists
            (
                select i.doc_id
                from inventory as i 
                where i.lib_id <> "library1"
                and i.doc_id = d.doc_id 
            )and not exists
            (
                select *
                from waiting as w
                where w.reader_id = (?)
                  and w.doc_id = d.doc_id
            ) 
            '''
    
    cur = g.db.execute( query, [ session['lib_id'], session['reader_id'] ] )
    uarows = [dict( doc_name=row[0], doc_id=row[1] ) for row in cur.fetchall()]
   
    return render_template('inventory.html', rows=rows, uarows=uarows)

@app.route('/wait/<doc_id>/')
def wait(doc_id=None):
    todays_date = time.strftime("%Y-%m-%d")
    date = datetime.datetime.strptime(todays_date, "%Y-%m-%d").date()
    delivery_date = date + datetime.timedelta(days=5)
    
    #Insert into waiting queue 
    g.db.execute('insert into waiting (reader_id, doc_id, wait_date) values (?, ?, ?)', [ session['reader_id'], doc_id, todays_date ])
    g.db.commit()
    
    #Find a document that is available 
    query = '''
            select i.lib_id, i.doc_id, max( i.doc_copy )
            from inventory as i
            where i.lib_id <> (?)
            and i.doc_id = (?)
            and not exists(
                select *
                from borrow as b
                where b.doc_id = i.doc_id
                    and b.doc_copy = i.doc_copy );
            '''
    cur = g.db.execute( query, [ session['lib_id'], doc_id ])
    rows = [dict( lib_id=row[0], doc_id=row[1], doc_copy=row[2] ) for row in cur.fetchall()]
    
    print "Waiting for ", rows 
    
    #Create lend entry using available document 
    g.db.execute('insert into lend (to_lib, from_lib, order_date, delivery_date, doc_id, doc_copy, status, for_reader) values (?, ?, ?, ?, ?, ?, ?, ?)', 
                    [ session['lib_id'], rows[0]['lib_id'], todays_date, delivery_date, rows[0]['doc_id'], rows[0]['doc_copy'], "processing" , session['reader_id'] ])
    g.db.commit()
    
    #Document/Copy being delivered as unavailable until it is delivered
    g.db.execute('update inventory set doc_status = ("unavailable") where doc_id = (?) and doc_copy = (?)', [ rows[0]['doc_id'], rows[0]['doc_copy'] ])
    g.db.commit()

    return redirect( url_for('reader_home') )
@app.route('/library_lend')   
def library_lend():

     # show a list of all books in inventory of this library and their status, location etc.. 
    query = ''' select d.doc_title, i.doc_copy, i.doc_status, i.curr_location, i.doc_id, i.lib_id
            from inventory as i
            inner join document as d 
            on i.doc_id = d.doc_id
            where i.lib_id <> (?)
              and i.lib_id = i.curr_location
              and not exists(
                select *
                from borrow as b
                where b.doc_id   = i.doc_id
                  and b.doc_copy = i.doc_copy
            ) 
            '''
    
    cur = g.db.execute( query, [ session['lib_id' ] ])
    rows = [dict( doc_name=row[0], doc_copy=row[1], doc_status=row[2], curr_location=row[3], doc_id=row[4], lib_id=row[5]) for row in cur.fetchall()]
    
    #Unavailble documents
    query = ''' select d.doc_title, i.doc_copy, i.doc_status, i.curr_location, i.doc_id, i.lib_id
        from inventory as i
        inner join document as d 
        on i.doc_id = d.doc_id
        where i.lib_id <> (?)
          and exists(
            select *
            from borrow as b
            where b.doc_id    = i.doc_id
              and b.doc_copy  = i.doc_copy
        ) or i.lib_id <> i.curr_location
        '''
    
    cur = g.db.execute( query, [ session['lib_id'] ] )
    uarows = [dict( doc_name=row[0], doc_copy=row[1], doc_status=row[2], curr_location=row[3], doc_id=row[4], lib_id=row[5] ) for row in cur.fetchall()]

    return render_template('library_lend.html', rows=rows, uarows=uarows)

@app.route('/lend/<doc_id>/<doc_copy>/')
def lend(doc_id=None, doc_copy=None):

    todays_date = time.strftime("%Y-%m-%d")
    date = datetime.datetime.strptime(todays_date, "%Y-%m-%d").date()
    delivery_date = date + datetime.timedelta(days=5)

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
        rows[0]['deliver_to'] = session['lib_id']
        rows[0]['order_date'] = todays_date
        rows[0]['delivery_date'] = delivery_date
        
    else:
        pass

    return render_template('confirm_lend.html', context=rows)

@app.route('/confirm_lend', methods=['POST'])
def confirm_lend():
    
    #Insert into lend
    g.db.execute('insert into lend (to_lib, from_lib, order_date, delivery_date, doc_id, doc_copy, status) values (?, ?, ?, ?, ?, ?, ?)', 
                    [ request.form['to_lib'], request.form['from_lib'], request.form['order_date'], request.form['delivery_date'], request.form['doc_id'], request.form['doc_copy'], "In Process" ])
    g.db.commit()

    return redirect(url_for('library_home'))
    
@app.route('/waitlist')
def waitlist():
    return redirect( url_for('reader_home') )

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

@app.route('/author') 
def author():
    cur = g.db.execute( 'select * from author' )
    rows = [dict( author_id=row[0], author_name=row[1] ) for row in cur.fetchall()]

    return render_template('author.html', rows=rows)
    
@app.route('/add_author', methods=['POST']) 
def add_author():
    g.db.execute('insert into author (author_name) values (?)', 
                    [ request.form['author_name'] ])
    g.db.commit()
    
    return redirect(url_for('author'))
    
@app.route('/document') 
def document():
    query = '''
                select d.doc_id, d.doc_title, d.doc_type, d.number_copies, u.author_name, max(i.doc_copy)
                from document as d
                inner join authoring as a
                    on d.doc_id = a.doc_id
                inner join author as u
                    on a.author_id = u.author_id
                left join inventory as i
                    on d.doc_id = i.doc_id
                group by i.doc_id
            '''
    cur = g.db.execute( query )
    rows = [dict( doc_id=row[0], doc_title=row[1], doc_type=row[2], number_copies=row[3], author_name=row[4], copies_out=row[5] ) for row in cur.fetchall()]
    
    for row in rows:
        if row['copies_out'] is not None:
            row['copies_remaining'] = int( row['number_copies'] ) - int( row['copies_out'] )
        else:
            row['copies_remaining'] = int( row['number_copies'] )
    
    cur = g.db.execute( 'select * from author' )
    options = [dict( author_id=row[0], author_name=row[1] ) for row in cur.fetchall()]
    
    return render_template('document.html', rows=rows, options=options)
    
@app.route('/add_document', methods=['POST']) 
def add_document():
    g.db.execute('insert into document (doc_title, doc_type, number_copies) values (?, ?, ?)', 
                    [ request.form['doc_title'], request.form['doc_type'], request.form['number_copies'] ])
    get_doc_id = g.db.execute('select last_insert_rowid()')
    doc_id = get_doc_id.fetchone()[0]
    g.db.commit()

    g.db.execute('insert into authoring (author_id, doc_id) values (?, ?)', 
                    [ request.form['authors'], doc_id ])
    g.db.commit()
    
    return redirect(url_for('document'))
    
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
