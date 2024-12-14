from flask import Blueprint, render_template, request, redirect, url_for, flash

auth = Blueprint('auth', __name__)

USER_EMAIL = "test@easybuis.de" 
USER_PASSWORD = "password123"

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        accept = request.form.get('accept')

        if not accept:
            flash("Bitte akzeptieren Sie die Nutzungsbedingungen.", "error")
            return redirect(url_for('auth.login'))

        if email == USER_EMAIL and password == USER_PASSWORD:
            flash("Erfolgreich eingeloggt!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Ungültige E-Mail oder Passwort.", "error")
            return redirect(url_for('auth.login'))

    return render_template('login.html')
