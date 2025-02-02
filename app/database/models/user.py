
import flask
from flask_login import UserMixin
from flask_bcrypt import check_password_hash, generate_password_hash

import jinja2
from mongoengine import (
    Document,
    StringField,
    EmailField,
    BinaryField,
    BooleanField,
    EnumField,
    MapField,
    DateTimeField,
    ListField,
    LazyReferenceField,
    DictField,
    IntField,
    EmbeddedDocumentField
)

from app import TEMPLATES_DIR
from app.enums import USER_ROLES
from app.utils.email import send_email
from app.utils.times import get_utc_now
from app.utils.tokens import generate_token, verify_token


class User(Document, UserMixin):

    meta = {
        # 'abstract': True,
        'collection': 'users',
        'allow_inheritance': True,
        'indexes': [
            {
                'fields': ['$email', '$username', '$firstname', '$lastname'],
                'default_language': 'german',
                'weights': {'email': 10, 'username': 10, 'firstname': 5, 'lastname': 5,}
            }
    ]}

    EMAIL_REGEX_PATTERN = r"^[a-z0-9!#$%&'*+/=?^_`{|}~.-]+@[a-z0-9.-]+\.[a-z]{2,}$"

    username = StringField(unique=True, required=True)
    email = StringField(required=True, regex=EMAIL_REGEX_PATTERN)
    password = BinaryField()

    firstname = StringField()
    lastname = StringField()

    created_at = DateTimeField()
    validated_at = DateTimeField()
    role = EnumField(USER_ROLES, default=USER_ROLES.USER)


    def get_user_id(self):
        return self.username

    def get_username(self):
        return self.username

    def set_password(self, new_password):
        self.password = generate_password_hash(new_password)
        return True

    def update_password(self, new_password):
        return self.modify(password=generate_password_hash(new_password))

    def validate_password(self, password_to_check):
        return check_password_hash(self.get_password(), password_to_check)

    def get_password(self):
        return self.password

    def get_email(self) -> str:
        return self.email

    def set_role(self, value: USER_ROLES):
        return self.modify(status=value)

    def get_role(self):
        return self.role
    
    def validate_email(self):
        return self.modify(validated_at=get_utc_now())

    def is_admin(self) -> bool:
        return bool(self.get_role() == USER_ROLES.ADMIN)

    def is_user(self) -> bool:
        return bool(self.get_role() == USER_ROLES.USER)
    
    def verify_login(self, login_password):
        return self.validate_password(login_password)

    def get_id(self):
        return self.get_user_id()
    
    # Functions required by flask-login
    @property
    def is_active(self):
        return bool(self.validated_at)
    
    @classmethod
    def register_from_form(cls, form, **kwargs) -> bool:
        """Registers the user with passed data"""

        kwargs.setdefault('created_at', get_utc_now())

        user = cls(**kwargs)
        # Caution: Make sure to set email and/or username to small letters
        form.populate_obj(user)
        user.set_password(form.password.data)


        if cls.objects(email__iexact=user.get_email()).first():
            return False, "That email is already registered!"

        if cls.objects(username=user.get_user_id()).first():
            return False, "That username is already taken!"

        return user.save(), "Successfully registered!"

    @classmethod
    def load(cls, user_id):
        """Loads the user with the given username"""
        return cls.objects(username=user_id).first()
    
    @classmethod
    def get_user_by_email_token(cls, token):

        payload = verify_token(token)
        
        if payload is None:
            return None, "Token has expired."
        if payload is False:
            return None, "Token is invalid."
        
        email = payload.get('email')
        if not email:
            return None, "No email attribute found in token."
        
        user = cls.load(email=email)
        if not user:
            return None, "No user found with that email."
        
        return user, "User found"
    
    def send_validation_email(self):
        
        TEMPLATE = '/emails/validation_email.html'

        # Encode the email and generate a token to retrieve it later
        token = generate_token(email=self.email)

        subject = 'Bestätige jetzt deine Emailadresse!'
        context = {
            'token': token,
            'url': flask.url_for('account.validate', token=token, _external=True)
        }

        env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATES_DIR))

        # Load a specific template
        template = env.get_template(TEMPLATE)
        # Render the template with the data
        body = template.render(context)
        # body = flask.render_template(TEMPLATE, **context)

        to_address = self.email
        result = send_email(subject, body, to_address)

        return result

    def send_forgot_password_email(self):

        TEMPLATE = '/emails/password_reset_email.html'

        # Encode the email and generate a token to retrieve it later
        token = generate_token(email=self.email)

        subject = 'Passwort zurücksetzen - Flask Template'
        context = {
            'token': token,
            'url': flask.url_for('account.password_reset', token=token, _external=True)
        }

        env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATES_DIR))

        # Load a specific template
        template = env.get_template(TEMPLATE)
        # Render the template with the data
        body = template.render(context)
        # body = flask.render_template(TEMPLATE, **context)

        to_address = self.email
        result = send_email(subject, body, to_address)

        return result