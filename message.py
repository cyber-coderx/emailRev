from flask import Flask, request, render_template
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Replace with your mail server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'obanryebb@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'bimzqntrjimquesc'  # Replace with your email password

mail = Mail(app)

# Set upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('contact.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    file = request.files['file']

    msg = Message('New Message from ' + name,
                  sender = email,
                  recipients=['obanryebb@gmail.com'])  # Replace with your email
    msg.body = message

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        with app.open_resource(filepath) as fp:
            msg.attach(filename, file.content_type, fp.read())

    mail.send(msg)

    return 'Email sent successfully!'

if __name__ == '__main__':
    app.run(debug=True)
