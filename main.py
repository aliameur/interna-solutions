from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
import smtplib
import os
from dotenv import load_dotenv
from flask_talisman import Talisman
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email
import uuid

load_dotenv()
app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = uuid.uuid4().hex
csrf = CSRFProtect(app)


csp = {
    'default-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        'stackpath.bootstrapcdn.com',
        'code.jquery.com',
        'cdn.jsdelivr.net',
        'unpkg.com/popper.js/',
        'fonts.googleapis.com',
        'fonts.gstatic.com',
        'kit.fontawesome.com',
        'ka-f.fontawesome.com'
    ]
}

talisman = Talisman(app, content_security_policy=csp)


class ContactForm(FlaskForm):
    name = StringField('My name is', [DataRequired()], render_kw={'placeholder': 'Full Name'})
    email = StringField('Full Name', [Email()], render_kw={'placeholder': 'name@example.com'})
    message = TextAreaField('Your message', [DataRequired()], render_kw={'placeholder': 'I want to say that...'})


def email_admin(name, email, message):
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=120) as connection:
        connection.starttls()
        server_email = os.getenv('EMAIL')
        server_pass = os.getenv('PASSWORD')
        admin_email = os.getenv('ADMIN_EMAIL')
        connection.login(server_email, server_pass)
        connection.sendmail(from_addr=server_email,
                            to_addrs=admin_email,
                            msg="Subject: New Message From Business Website\n\n"
                                f"Name: {name}\n"
                                f"Email: {email}\n"
                                f"Message: {message}\n")


@app.route('/', methods=["POST", "GET"])
def home():
    form = ContactForm()
    for i in form:
        print(i)
    if form.validate_on_submit():
        email_admin(name=form.name, email=form.email, message=form.message)
    if request.method == "POST":
        data = request.form
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=120) as connection:
            connection.starttls()
            server_email = os.getenv('EMAIL')
            server_pass = os.getenv('PASSWORD')
            admin_email = os.getenv('ADMIN_EMAIL')
            connection.login(server_email, server_pass)
            connection.sendmail(from_addr=server_email,
                                to_addrs=admin_email,
                                msg="Subject: New Message From Business Website\n\n"
                                    f"Name: {data['name']}\n"
                                    f"Email: {data['email']}\n"
                                    f"Message: {data['message']}\n")
    return render_template("home.html", form=form)


if __name__ == '__main__':
    app.run()
