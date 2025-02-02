
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, EmailField, DateTimeField
from wtforms.validators import InputRequired, EqualTo, Length

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me', default=False)
    submit = SubmitField('Login')

    def validate(self):
        # Preprocess email before validation
        if self.email.data:
            self.email.data = self.email.data.strip().lower()

        # Proceed with default validation
        return super().validate()


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, message="Passwort muss mindestens 6 Zeichen haben.")])
    password_confirm = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message='Passwörter müssen übereinstimmen.')])
    submit = SubmitField('Registrieren')

    def validate(self):
        # Preprocess email before validation
        if self.email.data:
            self.email.data = self.email.data.strip().lower()

        # Proceed with default validation
        return super().validate()


class ForgotPasswordForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired()])
    submit = SubmitField('Passwort zurücksetzen')

    def validate(self):
        # Preprocess email before validation
        if self.email.data:
            self.email.data = self.email.data.strip().lower()

        # Proceed with default validation
        return super().validate()


class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, message="Passwort muss mindestens 6 Zeichen haben.")])
    password_confirm = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message='Passwörter müssen übereinstimmen.')])
    submit = SubmitField('Passwort zurücksetzen')


class AccountDataForm(FlaskForm):
    email = EmailField('Email', render_kw={'readonly': True})
    firstname = StringField('Vorname', validators=[InputRequired()])
    lastname = StringField('Nachname', validators=[InputRequired()])
    phone = StringField('Telefonnummer')
    created_at = DateTimeField('Erstellt am', render_kw={'readonly': True}, format="%d.%m.%Y %H:%M:%S")
    validated_at = DateTimeField('Email validiert am', render_kw={'readonly': True}, format="%d.%m.%Y %H:%M:%S")
    submit_data = SubmitField('Speichern')