from application import app
from flask import render_template,request,redirect,session,url_for,json
from werkzeug.utils import secure_filename
import os
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Required,Email,Length,EqualTo
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy






mysql=MySQL()

app.secret_key ='A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['ALLOWED_EXTENSIONS'] = set(['mp3', 'mp4'])
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

app.config['SECRET_KEY'] = 'spodifuyggdjkslfjihugweyftshdjkflnkjgfehgudiyegvcbhjv'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:duncan@localhost/myfilesers'

#app.config['DATA']='/home/duncan/databases'

db = SQLAlchemy(app)



name="Login/register"







# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']




music_dir='/home/duncan/Documents/static/music'
music_dir='/home/duncan/Documents/Music_option/application/static/files'
music_readvideo='/home/duncan/Videos/Music videos'


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(200))

    def __init__(self,name,email,passwd):
        self.name = name
        self.email = email
        self.password = hash_pass(passwd)

class Register(Form):
    name = StringField('Name', validators=[Required()])
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required(),Length(min=6),EqualTo('confirm', message="Password must match")])
    confirm=PasswordField('Repeat password')
    submit = SubmitField('Submit')


class Login(Form):
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required(),Length(min=6)])
    submit = SubmitField('Submit')


@app.route('/')
def index():
    return render_template("index.html")



@app.route('/login',methods=['GET','POST'])
def login():
    error=None
    formlogin = Login()
    if request.method == 'POST':
        if formlogin.validate_on_submit():
            if formlogin.Email.data != "duncan@gmail.com":
                error = 'Invalid username'
            elif formlogin.Password != "password":
                error = 'Invalid username'
            else:
                session[ logged_in ] = True
                flash( 'You were logged in' )
                return redirect(url_for( index ))
    return render_template('login.html',form=formlogin,error=error)

@app.route('/register', methods=['GET','POST'])
def register():
    formregister=Register()
    if request.method == "GET":
        return render_template('register.html', form=formregister)

    elif request.method == "POST":
        if formregister.validate_on_submit():
            name = formregister.name.data
            email  = formregister.email.data
            password = formregister.password.data
            kamau = Users(name,email,password)
            db.session.add(kamau)
            db.session.commit()

            return redirect(url_for('login'))

        else:
            return render_template('register.html' ,form=formregister)



@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404



@app.route('/uploads',methods=[ 'GET' ,'POST'])
def uploads():
    """Handle the upload of a file."""
    if request.method == 'GET':
    	return render_template('upload.html')
    else:
    	form = request.form

    	# Is the upload using Ajax, or a direct POST by the form?
    	is_ajax = False
    	if form.get("__ajax", None) == "true":
        	is_ajax = True

    	# Target folder for these uploads.
    	target = music_dir
    	for upload in request.files.getlist("file"):
        	filename = upload.filename.rsplit("/")[0]
        	destination = "/".join([target, filename])
        	print "Accept incoming file:", filename
        	print "Save it to:", destination
        	upload.save(destination)

    	if is_ajax:
        	return ajax_response(True, upload_key)
    	else:
        	return redirect(url_for("upload_complete"))








@app.route('/myfiles')
def myfiles():
    music_files=[f for f in os.listdir(music_dir) if f.endswith('mp3')]
    music_video=[f for f in os.listdir(music_dir) if f.endswith('mp4')]
    photo_file=[f for f in os.listdir(music_dir) if f.endswith('jpg')]
    pdf_file=[f for f in os.listdir(music_dir) if f.endswith('pdf')]
    photo_file_png=[f for f in os.listdir(music_dir) if f.endswith('png')]

    music_files_number=len(music_files)
    music_video_number=len(music_video)

    return render_template("myfiles.html",music_files_number=music_files_number,
                                          music_video_number=music_video_number,
                                          music_files=music_files,
                                          music_video=music_video,
                                          photo_file=photo_file,
                                          pdf_file=pdf_file,
                                          photo_file_png=photo_file_png

                                        )






@app.route('/song')
def song():
    music_files=[f for f in os.listdir(music_dir) if f.endswith('mp3')]
    music_files=[f for f in os.listdir(music_dir) if f.endswith('mp4')]
    music_files_number=len(music_files)

    return render_template("play.html",music_files_number=music_files_number,
                                          music_files=music_files)





def ajax_response(status, msg):
    status_code = "ok" if status else "error"
    return json.dumps(dict(
        status=status_code,
        msg=msg,
    ))
