from flask import Flask, request, render_template, redirect, session, url_for
import SQLAlchemy
import os
import string
import smtplib
import random
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_credentials.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User('{self.email}')"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_url = db.Column(db.String(200), nullable=False)
    set_price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Product('{self.product_url}', '{self.set_price}')"

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/register', methods=['POST'])
def register():
    error = None
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    session['email'] = email
    if password != confirm_password:
        error = "Passwords do not match. Please re-enter passwords."
    else:
        user = User.query.filter_by(email=email).first()
        if user:
            error = "Email already exists. Please use a different email address."
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/home')

    return render_template('login.html', error=error)


@app.route('/login', methods=['POST'])
def login():
    error = None
    email = request.form['email']
    password = request.form['password']
    session['email'] = email

    user = User.query.filter_by(email=email).first()
    if user:
        hashed_password = user.password
        if bcrypt.check_password_hash(hashed_password, password):
            session['logged_in'] = True
            return redirect('/home')
        else:
            error = "Invalid password. Please try again."
    else:
        error = "Invalid email. Please try again."

    return render_template('login.html', error=error)

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/report', methods=['POST'])
def report():
    if request.method == 'POST':
        search_query = request.form['query']
        amazon_title, amazon_price, amazon_product_url = test.get_amazon_price(search_query)
        flipkart_title, flipkart_price, flipkart_product_url = test.get_flipkart_price(search_query)
    return render_template("report.html", amazon_title=amazon_title,amazon_price=amazon_price, amazon_product_url=amazon_product_url ,flipkart_title=flipkart_title, flipkart_price=flipkart_price, flipkart_product_url=flipkart_product_url)

'''def generate_token(length=6):
    """Generate a random token of specified length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))


def send_email(email, token):
    """Send an email with the password reset token."""
    sender_email = "bharathwaj0910@gmail.com"  
    password = "gogw dojo ldis uiua" 
    reset_link = f"http://localhost:5000/reset_password/{token}"


    message = f"""\
    <html>
      <body>
        <p>Dear User,</p>
        <p>You have requested to reset your password. Please click on the following link to reset your password:</p>
        <p><a href="{reset_link}">Reset Password</a></p>
        <p>If you did not request this change, please ignore this email.</p>
        <p>Regards,<br>Your App Team</p>
      </body>
    </html>
    """

    msg = MIMEMultipart()
    msg.attach(MIMEText(message, 'html'))
    msg['Subject'] = "Password Reset Request"
    msg['From'] = sender_email
    msg['To'] = email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Enter your SMTP server
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, [email], msg.as_string())
        server.quit()
        msg= "Email sent successfully."
        return render_template("Recovery_page.html",msg=msg)
    except Exception as e:
        return f"Error sending email: {str(e)}"

def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            token = generate_token()
            expiry_time = datetime.now() + timedelta(minutes=30)
            new_token = Token(email=email, token=token, expiry_time=expiry_time)
            db.session.add(new_token)
            db.session.commit()
            send_email(email, token)
            return render_template('Recovery_page.html', msg="Email sent successfully.")
        else:
            return render_template('Recovery_page.html', error="This email is not registered.")
    return render_template('Recovery_page.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    return render_template('password_reset.html', token=token)

@app.route('/reset_pass', methods=['GET', 'POST'])
def reset_pass():
    if request.method == 'POST':
        token = request.form['token']
        new_password = request.form['password']
        confirm_password = request.form['confirm_password']
        if token in user_tokens:
            if datetime.now() > user_tokens[token]['expiry_time']:
                del user_tokens[token]  
                error="Token expired. Please request a new password reset link."
                return render_template("Recovery_page.html",error)
            email = user_tokens[token]['email']
            if new_password != confirm_password:
                error = "Passwords do not match. Please re-enter passwords."
                return render_template("password_reset.html", error=error)
            else:
                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                Hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                cursor.execute("UPDATE users SET password = ? WHERE email = ?", (Hashed_password, email))
                conn.commit()
                conn.close()
                
                del user_tokens[token]  
                msg= "Password reset successfully."
                return render_template("login.html",msg=msg)
        else:
            error ="Invalid or expired token."
            return render_template("Recovery_page.html",error=error)   
    return render_template('password_reset.html')'''

@app.route('/notify',methods=['GET', 'POST'])
def notify_page():
    return render_template('notify.html')

@app.route('/notify_form', methods=['GET', 'POST'])
def save():
    if request.method == 'POST':
        product_url = request.form['product_url']
        set_price = float(request.form['set_price'])

        if 'amazon' in product_url or 'flipkart' in product_url:
            new_product = Product(product_url=product_url, set_price=set_price)
            db.session.add(new_product)
            db.session.commit()
            msg = "Successfully added"
            return render_template('notify.html', msg=msg)
        else:
            error_message = "Unsupported app"
            return render_template('notify.html', error_message=error_message)

    return render_template('notify.html')

@app.route('/recovery_page')
def recovery_page():
    return render_template('Recovery_page.html')


if __name__ == '__main__':
    app.run(debug=True)