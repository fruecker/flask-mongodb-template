
import flask
from flask import Blueprint

from flask_login import login_required, current_user, logout_user
import flask_login
from app.database.models.user import User

from app.decorators import admin_only, under_construction
from app.modules.account.forms import AccountDataForm, ForgotPasswordForm, LoginForm, PasswordResetForm, RegisterForm
from app.utils.sites import site_map


# Import module forms
module = Blueprint("account", __name__, url_prefix="/account")

@module.route("/")
@login_required
def home():
    return flask.redirect(flask.url_for('default.home'))

@module.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        flask.flash("You are already logged in.", category="info")
        return flask.redirect(flask.url_for('default.home'))

    form = LoginForm()
    if form.validate_on_submit():

        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data

        user = User.load(email=email)

        if not user or not user.validate_password(password):
            flask.flash("Falsche Email und/oder Passwort.", category="danger")
            return flask.redirect(flask.url_for("account.login"))
        
        # TODO: Maybe check if user is validated so we can prompt them to validate their email
        success = flask_login.login_user(user, remember=remember_me)
        if not success:
            flask.flash("Du scheinst deine Email noch nicht validiert zu haben. Bitte schau in deinem Postfach & Spam-Ordner nach.", category="danger")
            return flask.redirect(flask.url_for("account.login"))

        next = flask.request.args.get('next')

        return flask.redirect(next or flask.url_for('default.home'))
    return flask.render_template("account/login.html", form=form)


@module.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        flask.flash("Du bist bereits eingeloggt.", category="info")
        return flask.redirect(flask.url_for('default.home'))
    
    form = RegisterForm()

    if form.validate_on_submit():

        payload, msg = User.register_from_form(form)

        if payload is False:
            flask.flash(msg, category="danger")
            return flask.redirect(flask.url_for("account.register"))

        if not isinstance(payload, User):
            flask.flash("Etwas ist schief gelaufen. Bitte kontaktiere uns.", category="danger")
            return flask.redirect(flask.url_for("account.register"))
        
        payload.send_validation_email()

        flask.flash("Erfolgreich registriert. Bitte schau in deinem Email-Postfach & Spam-Ordner.", category="success")
        return flask.redirect(flask.url_for("account.login"))

    return flask.render_template("account/register.html", form=form)


@module.route("/validate/<token>")
def validate(token):

    user, msg = User.get_user_by_email_token(token)

    if not user:
        flask.flash(msg, category="danger")
        return flask.redirect(flask.url_for("account.login"))

    if user.validated_at:
        flask.flash("Email bereits validiert.", category="info")
        return flask.redirect(flask.url_for("default.home"))

    user.validate_email()
    flask.flash("Email wurde erfolgreich validiert.", category="success")

    flask_login.login_user(user)

    return flask.redirect(flask.url_for("default.home"))


@module.route("/validate/resend/<user_id>", methods=["GET"])
def validate_resend(user_id):
    
    user = User.load(email=user_id)

    if not user:
        flask.flash("Falls der Nutzer existiert wurde eine Email gesendet.", category="info")
        return flask.redirect(flask.request.referrer or flask.url_for("default.home"))

    if user.validated_at:
        flask.flash("Nutzer wurde bereits validiert.", category="info")
        return flask.redirect(flask.request.referrer or flask.url_for("default.home"))

    user.send_validation_email()
    flask.flash("Falls der Nutzer existiert wurde eine Email gesendet.", category="info")

    return flask.redirect(flask.request.referrer or flask.url_for("default.home"))


@module.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if current_user.is_authenticated:
        flask.flash("Du bist bereits eingeloggt.", category="info")
        return flask.redirect(flask.url_for('default.home'))

    form = ForgotPasswordForm()

    if form.validate_on_submit():

        email = form.email.data

        user = User.load(email=email)

        if not user:
            flask.flash("Wenn dieser Account existiert, haben wir dir eine Email gesendet. Bitte schaue auch in deinem Spam-Ordner.", category="success")
            return flask.redirect(flask.url_for("account.forgot_password"))

        user.send_forgot_password_email()

        flask.flash("Wenn dieser Account existiert, haben wir dir eine Email gesendet. Bitte schaue auch in deinem Spam-Ordner.", category="success")
        return flask.redirect(flask.url_for("account.login"))

    return flask.render_template("account/forgot_password.html", form=form)


@module.route("/reset-password/<token>", methods=["GET", "POST"])
def password_reset(token):

    user, msg = User.get_user_by_email_token(token)

    if not user:
        flask.flash(msg, category="danger")
        return flask.redirect(flask.url_for("account.login"))

    form = PasswordResetForm()
    if form.validate_on_submit():

        password = form.password.data

        user.update_password(password)

        flask.flash("Passwort erfolgreich zurückgesetzt.", category="success")
        return flask.redirect(flask.url_for("account.login"))

    return flask.render_template("account/password_reset.html", form=form)


@module.route("/logon/<user_id>", methods=["GET"])
@login_required
@admin_only
def logon(user_id):

    user = User.load(email=user_id)

    if not user:
        flask.flash("Benutzer existiert nicht.", category="danger")
        return flask.redirect(flask.url_for("default.home"))

    flask_login.login_user(user, force=True)

    return flask.redirect(flask.url_for("default.home"))


@module.route("/logout")
@login_required
def logout():

    logout_user()

    return flask.redirect(flask.url_for("default.home"))


@module.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    form = AccountDataForm()
    if form.validate_on_submit() and form.submit_data.data:

        form.populate_obj(current_user)
        current_user.save()

        flask.flash("Daten erfolgreich aktualisiert.", category="success")
        return flask.redirect(flask.url_for("account.profile"))
    
    form.process(obj=current_user)
    return flask.render_template("account/profile.html", form=form)