from flask import Flask, request, render_template, redirect,session,url_for
import sqlite3
import os
import string
import smtplib
import random
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from apscheduler.schedulers.background import BackgroundScheduler
import test
from Amazon_price_tracker import amazon_price_tracker
from Flipkart_price_tracker import flipkart_price_tracker
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.secret_key = os.urandom(24)
DB_FILE = 'users_credentials.db'
bcrypt=Bcrypt(app)
scheduler = BackgroundScheduler()


if not os.path.exists(DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    CREATE_TABLE_QUERY = """
    CREATE TABLE users (
    email TEXT,
    password TEXT,
    product_url TEXT,
    set_price TEXT,
    token TEXT,
    expiry_time TIME
    notify boolean
    )
    """
    cursor.execute(CREATE_TABLE_QUERY)
    conn.commit()
    conn.close()


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
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        Hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        if user:
            error = "Email already exists. Please use a different email address."
        else:
            cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, Hashed_password))
            conn.commit()
            conn.close()
            return redirect('/home')
    
   
    return render_template('login.html',error=error)


@app.route('/login', methods=['POST'])
def login():
    error = None
    email = request.form['email']
    password = request.form['password']
    session['email'] = email
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=? ", (email,))
    user = cursor.fetchone()
    if user:
        hashed_password=user[1]
        if  bcrypt.check_password_hash(hashed_password,password):
            session['logged_in'] = True
            conn.close()
            return redirect('/home')
        else:
            error = "Invalid password Please try again."
            conn.close()
            return render_template('login.html' ,error=error)

    else:
        error = "Invalid email Please try again."
        conn.close()
        return render_template('login.html' ,error=error)

@app.route('/home')
def home():
    email=session['email']
    return render_template("home.html",email=email)



@app.route('/report', methods=['POST'])
def report():
    if request.method == 'POST':
        search_query = request.form['query']
        amazon_title, amazon_price, amazon_product_url = test.get_amazon_price(search_query)
        flipkart_title, flipkart_price, flipkart_product_url = test.get_flipkart_price(search_query)
    return render_template("report.html", amazon_title=amazon_title,amazon_price=amazon_price, amazon_product_url=amazon_product_url ,flipkart_title=flipkart_title, flipkart_price=flipkart_price, flipkart_product_url=flipkart_product_url)


def generate_token(length=6):
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


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        if user:
            token = generate_token()
            expiry_time = datetime.now() + timedelta(minutes=30)
            cursor.execute("UPDATE users SET token=?, expiry_time=? WHERE email=?", (token, expiry_time, email))
            conn.commit()
            conn.close()
            return send_email(email, token)
        conn.close()
        error = "This email is not registered"
        return render_template('Recovery_page.html', error=error)
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
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE token=?", (token,))
        user = cursor.fetchone()
        print(user)
        if user:
            expiry_time_str = user[5]  # Assuming expiry_time is at index 5
            # Modify format string to handle extra characters
            expiry_time_str_clean = expiry_time_str.split('.')[0]  # Remove milliseconds
            expiry_time = datetime.strptime(expiry_time_str_clean, '%Y-%m-%d %H:%M:%S')
            if datetime.now() > expiry_time:
                conn.close()
                error = "Token expired. Please request a new password reset link."
                return render_template("Recovery_page.html", error=error)
            email = user[0]
            if new_password != confirm_password:
                conn.close()
                error = "Passwords do not match. Please re-enter passwords."
                return render_template("password_reset.html", error=error)
            else:
                hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                cursor.execute("UPDATE users SET password=? WHERE email=?", (hashed_password, email))
                conn.commit()
                conn.close()
                msg = "Password reset successfully."
                return render_template("login.html", msg=msg)
        else:
            conn.close()
            error = "Invalid or expired token."
            return render_template("Recovery_page.html", error=error)
    return render_template('password_reset.html')

@app.route('/notify',methods=['GET', 'POST'])
def notify_page():
    email = request.form['email']
    return render_template('notify.html',email=email)

@app.route('/notify_form', methods=['GET', 'POST'])
def save():
    if request.method == 'POST':
        product_url = request.form['product_url']
        set_price = float(request.form['set_price'])
        email = request.form['email']
        if 'amazon' in product_url or 'flipkart' in product_url or 'amzn' in product_url:
            con = sqlite3.connect('users_credentials.db')
            cur = con.cursor()
            cur.execute("UPDATE users SET product_url = ?, set_price = ?, notify = ? WHERE email = ?", (product_url, set_price, True, email))
            con.commit()
            con.close()
            msg="successfully added"
            return render_template('notify.html',msg=msg)
        else:
            error = "Unsupported app"
            return render_template('notify.html', error=error)

    return render_template('notify.html') 


def send_alert_email(receiver_email, product_url, current_price):
    sender_email = "bharathwaj0910@gmail.com"  # Change this
    sender_password = "gogw dojo ldis uiua"  # Change this
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Price Alert: {} is now under your set price!".format(product_url)

    body = "The price of {} is now {}!".format(product_url, current_price)
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()

def check_price_and_send_email(email, product_url, set_price):
    # Scrape price from Amazon and Flipkart
    if "amazon" in product_url or "amzn" in product_url:
        current_price = amazon_price_tracker(product_url)[0].replace(',', '')
    else:
        current_price = flipkart_price_tracker(product_url)[0].replace(',', '') 
        current_price = ''.join(filter(str.isdigit, current_price))
    
    if float(current_price) <= float(set_price):
        conn = sqlite3.connect('users_credentials.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET notify = ? WHERE email = ?", ( False , email))
        conn.commit()
        conn.close()
        send_alert_email(email, product_url, current_price)


def check_prices():
    conn = sqlite3.connect('users_credentials.db')
    cursor = conn.cursor()
    cursor.execute("SELECT email, product_url, set_price FROM users WHERE notify = 1")
    users = cursor.fetchall()
    
    # List to store processed emails
    processed_emails = []

    for user in users:
        email, product_url, set_price = user
        # Check if the email has already been processed
        if email not in processed_emails:
            check_price_and_send_email(email, product_url, set_price)
            processed_emails.append(email)  # Add the email to the processed list

    conn.close()

    return "Price check completed."



@app.route('/recovery_page')
def recovery_page():
    return render_template('Recovery_page.html')

scheduler.add_job(check_prices, 'interval', hours=2)
if __name__ == '__main__':
    scheduler.start()
    app.run(debug=True)

'''
)
'''


