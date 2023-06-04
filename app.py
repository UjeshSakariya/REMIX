
# for the databse 
import sqlite3
connection = sqlite3.connect('users.db', check_same_thread=False)
cursor = connection.cursor()
connection.commit()

# importing os library to sotre the images
import os

# flask to run server
from flask import Flask, flash, flash, render_template, request, redirect, session, url_for
# import sessions
from flask_session import Session
SESSION_PERMANENT = False

# to make the file to store the API
from tempfile import mkdtemp
# to hash the password 
from werkzeug.security import check_password_hash, generate_password_hash

# allows a secure file to be returned
from werkzeug.utils import secure_filename

# configure application 

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies) 
# session cookies are a temporary memory location which is deleted after the session ends. 
# they are never stored on your device 

# It makes the session for the user end when the browser is closed 
SESSION_PERMANENT = False

#  It will store in the hard drive (these files are stored under a /flask_session folder in your config directory.) or any online ide account, and it is an alternative to using a Database or something else like that.
SESSION_TYPE ='filesysem'
app.config['SECRET_KEY'] = 'name'
app.config['ADMIN'] = 'admin'
app.config['SESSION_TYPE'] = 'filesystem'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'feed/'
app.config['UPLOAD_FILE'] = UPLOAD_FOLDER





#creates a session which has key value pairs for session variables and associated values 
Session(app)


@app.after_request
# allows code to run after the request had been served
def after_request(response):
    # used to give more detail about the response
    # ensure that no response is cached  (no data is to be stored and unsed later therefore faster response)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route('/')
def index():
    return render_template('login.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    if request.method == 'POST':

        session.clear()

        username = request.form.get('username')      
        password = request.form.get('password')
      
        cursor.execute("SELECT * FROM accounts WHERE username = ?",(username,))
        x = cursor.fetchall()
        if len(x) > 0:
            
            session["name"] = x[0][0]
            app.config.update(SECRET_KEY=session['name'])
            return redirect("/")
        else:
            return render_template('login.html', success = 'failure')
    else:
            return render_template('login.html')

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == 'POST':
         
        username = request.form.get('name')
        password = request.form.get('psswd')

        cursor.execute("SELECT * FROM accounts WHERE username = ? AND password = ?",(username, password))
        x = cursor.fetchall()
        if len(x) > 0:
             return render_template('login.html', success = 'username is already in use, try again')
        else:
                cursor.execute("INSERT INTO accounts(username,password) VALUES (?,?)",(username,password))
                connection.commit()
                return render_template('/login.html')

    else:
         return render_template('/register.html')
    
@app.route("/about")
def about():
     
     return render_template('/about.html')

@app.route("/logout")
def logout():
     
     session.clear()
     return redirect("/")

@app.route("/discussion")
def discussion():
    cursor.execute('SELECT * FROM feed')
    data = cursor.fetchall()
    
    user = []
    title =[]
    caption = []
    
    for i in range(len(data)):
         
         user.append(data[i][1])
         title.append(data[i][4])
         caption.append(data[i][3])
        
    cursor.execute('SELECT * FROM comments')
    data2 = cursor.fetchall()

    comments = []
    for i in range(len(data2)):
         tmp =[]
         tmp.append(data2[i][1])
         tmp.append(data2[i][2])
         tmp.append(data2[i][3])
         comments.append(tmp)
    
    print(comments)
    
    images = os.listdir(os.path.join("static/feed"))
    return render_template('/discussion.html', user = user, images = images, caption = caption, comments = comments)

@app.route("/admin", methods=["GET", "POST"]) 
def admin():
    if request.method == 'POST':
        password = request.form.get('admin')
        if password == 'YEREMIX2023':  
            id = session['name']
            session["admin"] = id
            app.config.update(ADMIN=session['admin'])
            x = session['admin']
            return render_template('/admin.html', success = 'correct') 
        else:
            return render_template('/admin.html', success = 'incorrect') 
    else:
         return render_template('/admin.html')
    
@app.route("/upload", methods=["POST","GET"])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/image', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return render_template('/admin.html', success = 'not right type')
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return render_template('/admin.html', success = 'no file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('static/feed', filename))
            caption = request.form.get('caption')

            id = session['name']
            id = int(id)

            cursor.execute('SELECT username FROM accounts WHERE id = ?',(id,))
            name = cursor.fetchone()
            name = name[0]
            name = str(name)
            blobData = None

            with open(f'static/feed/{filename}','rb') as file:
                 blobData = file.read()
                             
            cursor.execute('INSERT INTO feed (name,photo,caption,title) VALUES(?,?,?,?)',(name,blobData,caption,filename))
            connection.commit()
            
        return redirect('/discussion')

@app.route('/comment', methods=['GET', 'POST'])
def comment():
     if request.method == 'POST':
          comment = request.form.get('comment')
          
@app.route('/process-data', methods=['POST'])
def process_data():
    data = request.json['data']
    comment = data[0]
    postnum = data[1]
    print(comment)
    print(postnum)

    id = session['name']
    id = int(id)

    cursor.execute('SELECT username FROM accounts WHERE id = ?',(id,))
    name = cursor.fetchone()
    name = name[0]
    name = str(name)
    cursor.execute('INSERT INTO comments(post_id,user,comment) VALUES(?,?,?)',(postnum,name,comment))
    connection.commit()
    return render_template('/discussion.html')


    

  


    