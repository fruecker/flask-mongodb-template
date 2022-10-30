
from flask_login import UserMixin
from flask_bcrypt import check_password_hash, generate_password_hash

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

from app.enums import USER_ROLES
from app.utils.times import get_utc_now


class UserBaseDocument(Document):

    meta = {
        # 'abstract': True,
        'collection': 'users',
        'allow_inheritance': True
    }

    username = StringField(unique=True, required=True)
    email = EmailField(required=True)
    password = BinaryField()

    created = DateTimeField()
    validated = BooleanField(default=False)
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

    def is_admin(self) -> bool:
        return bool(self.get_role() == USER_ROLES.ADMIN)

    def is_user(self) -> bool:
        return bool(self.get_role() == USER_ROLES.USER)


    @classmethod
    def load(cls, user_id):
        return cls.objects(username=user_id).first()


   
class User(UserBaseDocument, UserMixin):
    """Representation of database User object"""

    def __init__(self, *args, **kwargs):
        UserBaseDocument.__init__(self, *args, **kwargs)

    @classmethod
    def register(cls, form, **kwargs) -> bool:
        """Registers the user with passed data"""

        kwargs.setdefault('created', get_utc_now())

        user = cls(**kwargs)
        form.populate_obj(user)
        user.set_password(form.password.data)

        if UserBaseDocument.objects(email=user.get_email()).first():
            return False, "That email is already registered!"

        if UserBaseDocument.objects(username=user.get_user_id()).first():
            return False, "That username is already taken!"

        return user.save(), "Successfully registered!"

    def verify_login(self, login_password):
        return self.validate_password(login_password)

    def get_id(self):
        return self.get_user_id()
