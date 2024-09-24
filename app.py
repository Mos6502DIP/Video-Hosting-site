from flask import *
import sqlite3
from emailpy import emails as ep
import random
from datetime import timedelta, datetime
import string
import hashlib
import os
from moviepy.editor import VideoFileClip
import shutil





app = Flask(__name__)




email_address = "< Your Email Address Here >"
app.secret_key = "Lucario"
app.permanent_session_lifetime = timedelta(hours=48)

webserver_address = "http://127.0.0.1:5000" # when hosted change this

auth_codes = {}

forgot_password_codes = {}

UPLOAD_FOLDER_VIDEOS = 'static/videos/'
UPLOAD_FOLDER_THUMBNAILS = 'static/thumbnails/'
UPLOAD_FOLDER_AUTH = 'vomit/'

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER_VIDEOS'] = UPLOAD_FOLDER_VIDEOS
app.config['UPLOAD_FOLDER_THUMBNAILS'] = UPLOAD_FOLDER_THUMBNAILS
app.config['UPLOAD_FOLDER_AUTH'] = UPLOAD_FOLDER_AUTH


ALLOWED_EXTENSIONS_VIDEO = {'mp4', 'mov', 'mkv', 'webm'}
ALLOWED_EXTENSIONS_IMAGE = {'png', 'jpg', 'jpeg', 'gif'}

bitrate = '2M'
quality=2

def get_extension(filename):
    return filename.split('.')[-1]

def get_id(num_chars):
    while True:
        id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(num_chars))
        if colum_check("Videos", "char_id", id):
            return id

def email_password():

    try:
        with open("email_password.txt") as fp:
            lines = fp.readlines()
            for line in lines:
                if line.strip()[0] != "#":
                    setting_line = line.strip().split("=")
                    if setting_line[0] == "password":
                        return setting_line[1]

    except FileNotFoundError:
        print("File not found")
        return "Nah Huh" #


def delete_directory_contents(directory_path):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove the file or symbolic link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove the directory and its contents
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


def convert_to_webm_ffmpeg(input_video_path, output_webm_path, bitrate='4M', crf=23):
    (
        ffmpeg
        .input(input_video_path)
        .output(output_webm_path,
                vcodec='libvpx-vp9',  # VP9 codec for better quality
                video_bitrate=bitrate,  # Target bitrate
                crf=crf,  # Constant Rate Factor, lower means better quality
                acodec='libvorbis',  # Audio codec for WebM
                )
        .run()
    )



def colum_check(table, colum, data):
    conn = sqlite3.connect("os.db")
    cursor = conn.cursor()

    query = f"SELECT * FROM {table} WHERE {colum} = ?"

    # Execute the query, passing the variable as a parameter
    cursor.execute(query, (data,))

    # Fetch all matching rows
    rows = cursor.fetchall()

    if len(rows) == 0:
        return True
    else:
        return False


def change_password(username, password):
    conn = sqlite3.connect("os.db")
    cursor = conn.cursor()
    query = f"UPDATE Users SET password_hash = ? WHERE username = ?"
    cursor.execute(query, (password, username))
    conn.commit()


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def hash_string(password):
    return hashlib.sha256(password.encode()).hexdigest()


def get_day():
    date_time = datetime.now()
    return date_time.strftime("%d/%m/%Y")


def from_now(days):
    now = datetime.now()
    return now + timedelta(days=days)


def register(username, email, password):
    conn = sqlite3.connect("os.db")
    cursor = conn.cursor()
    pfp = "pfp/normi_profile_picture.png"
    date = get_day()

    cursor.execute('''
    INSERT INTO Users (username, password_hash, email, profile_picture_url, created_at) 
    VALUES (?, ?, ?, ?, ?)
    ''', (username, password, email, pfp, date))

    conn.commit()

    # Retrieve and print data
    cursor.execute('SELECT * FROM Users')
    rows = cursor.fetchall()

    for row in rows:
        print(row)


def login(username, password):
    conn = sqlite3.connect("os.db")
    cursor = conn.cursor()

    cursor.execute('SELECT password_hash FROM Users WHERE username = ?', (username,))
    com_pass = cursor.fetchone()

    if com_pass is None:
        print("Invalid Username or Password")
        return False
    else:
        if com_pass[0] == password:
            return True

        else:
            print("Invalid Password")
            return False


def get_username_email(email):
    conn_2 = sqlite3.connect("os.db")
    cursor_2 = conn_2.cursor()
    cursor_2.execute('SELECT username FROM Users WHERE email = ?', (email,))
    result = cursor_2.fetchone()

    if result is None:
        return None  # or some other appropriate value like an error message

    return result[0]


def is_user():
    if 'username' in session:
        return True
    else:
        return False


def get_username():
    if 'username' in session:
        return session['username']
    else:
        return None


def file_allow(filename, extensions):  # checks if the file name is allowed
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

@app.route('/', methods=['GET', 'POST'])
def landing():
    if request.method == 'POST':
        if login(request.form['username'], hash_string(request.form['password'])):
            session['username'] = request.form['username']
            resp = make_response(redirect("/dashboard"))
            resp.set_cookie('Joshua',
                            value=f"{session['username']}|{hash_string(request.form['password'])}",
                            expires=from_now(3))
            return resp
        else:
            return render_template('landing.html', response="Username or Password is incorrect", username=get_username())
    else:
        joshua = request.cookies.get('Joshua', 'David')


        if joshua == "David":
            return render_template('landing.html', response="", username=get_username())

        else:
            username_password = joshua.split("|")
            if login(username_password[0], username_password[1]):
                session['username'] = username_password[0]
                resp = make_response(redirect("/dashboard"))
                resp.set_cookie('Joshua',
                                value=f"{session['username']}|{username_password[1]}",
                                expires=from_now(3))
                return resp

            else:
                return render_template('landing.html', response="Code error - 34", username=get_username())



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('sign_up.html', response='', username=get_username())

    if request.method == 'POST':
        user_name = request.form['Username']
        password = request.form['Password']
        email = request.form['Email']

        if colum_check("users", "username", user_name) and colum_check("users", "email", email):
            while True:
                com_code = get_random_string(12)
                if com_code not in auth_codes:
                    break

            subject = "Confirm your email address - Ocean Space"

            ep.send_email(email_address, email_password(), email, subject,
                          f"""Hi to verify your email for Ocean Space please open the link in the same browser.
(If you did not request this link do not click on it and delete this email)
{webserver_address}/email_verify/{com_code}
-Ocean Space
                          """)

            auth_codes[com_code] = {}
            auth_codes[com_code]['email'] = email
            auth_codes[com_code]['password'] = hash_string(password)
            auth_codes[com_code]['username'] = user_name

            session['auth_code'] = com_code

            return render_template('sign_up.html', response='Email sent', username=get_username())

        else:
            return render_template('sign_up.html', response='Email Or Username in Use', username=get_username())



@app.route('/email_verify/<code>', methods=['GET'])
def email_verify(code):
    if code in auth_codes:
        if 'auth_code' in session:
            register(auth_codes[code]["username"], auth_codes[code]['email'], auth_codes[code]['password'])
            login(auth_codes[code]["username"], auth_codes[code]['password'])

            session['username'] = auth_codes[code]["username"]
            resp = make_response(redirect("/dashboard"))
            resp.set_cookie('Joshua',
                            value=f"{session['username']}|{auth_codes[code]['password']}",
                            expires=from_now(3))

            auth_codes.pop(code)
            return resp
        else:
            return "This code is either expired or not being opened in the same browser!"
    else:
        return "Code Error 628"

@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        if not colum_check("users", "email", request.form['email']):
            while True:
                com_code = get_random_string(12)
                if com_code not in forgot_password_codes:
                    break

            email = request.form["email"]

            subject = "Forgot your email address - Ocean Space"

            user_name = get_username_email(email)

            ep.send_email(email_address, email_password(), email, subject,
                          f"""Hi, {user_name} You have requested to reset your password 
just click on the link in the same browser.
(If you did not request this link do not click on it and delete this email)
            {webserver_address}/password-reset/{com_code}
-Ocean Space
                                      """)

            forgot_password_codes[com_code] = {}
            forgot_password_codes[com_code]['email'] = email
            forgot_password_codes[com_code]['username'] = user_name

            session['auth_code'] = com_code

            return render_template('forgot.html', response='Email sent', username=get_username())

        else:
            return render_template("forgot.html", response='Email Sent!', username=get_username())
    else:
        return render_template("forgot.html", response='', username=get_username())


@app.route('/password-reset/<code>', methods=['GET', 'POST'])
def password_reset(code):
    if code in forgot_password_codes:
        if request.method == 'GET':
            if 'auth_code' in session:
                return render_template("password_reset.html")
            else:
                return "This code is either expired or not being opened in the same browser!"

        else:
            if 'auth_code' in session:
                new_password = hash_string(request.form['password'])
                change_password(forgot_password_codes[code]["username"], new_password)
                forgot_password_codes.pop(code)
                session.clear()
                return redirect("/")

            else:
                return "This code is either expired or not being opened in the same browser!"

    else:
        return "Code Error 1998"  # Lol i am bad


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    resp = make_response(redirect("/"))
    resp.set_cookie('Joshua', '', expires=0)
    return resp


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if is_user():  # check if the browsers session is logged in with a account
        if request.method == 'POST':
            pass
        else:
            return render_template('dashboard.html', username=get_username())

    else:
        return redirect('/') # if not return to sign


@app.route('/upload', methods = ['GET', 'POST'])
def upload_video():
    if is_user():
        if request.method == 'POST':
            # check if the files exist
            if 'video' not in request.files or 'thumbnail' not in request.files:
                return 'Error code - 639'

            video = request.files['video']
            thumbnail = request.files['thumbnail']

            title = request.form['title']
            description = request.form['description']

            if video.filename == '' or thumbnail.filename == '':
                return 'Error code - 739'

            if file_allow(video.filename, ALLOWED_EXTENSIONS_VIDEO):

                video_id = get_id(5)  # id amount of chars this can be moded if for some reason the limit is exced but i doubt this line will be used in that situation
                save_video( )




                video_filename = os.path.join(app.config['UPLOAD_FOLDER_VIDEOS'], secure_filename)









        else:
            return render_template('upload.html', username=get_username())

    else:
        return redirect('/')



if __name__ == '__main__':
    app.run()
