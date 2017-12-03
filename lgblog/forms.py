from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo
from lgblog.models import User


class CommentForm(FlaskForm):
    """Form vaildator for comment."""

    # Set some field(InputBox) for enter the data.
    # patam validators: setup list of validators
    name = StringField(
        'Name',
        validators=[DataRequired(), Length(max=255)])

    text = TextAreaField(u'Comment', validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired()])

    def validate(self):
        """Validator for check the account information."""
        check_validata = super(LoginForm, self).validate()

        # If validator no pass
        if not check_validata:
            return False

        # Check the user whether exist.
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('Invalid username or password.')
            return False

        # Check the password whether right.
        if not user.check_password(self.password.data):
            self.username.errors.append('Invalid username or password.')
            return False

        return True


class RegisterForm(FlaskForm):
    """Register Form."""

    username = StringField('Username', validators=[DataRequired(), Length(max=255)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    comfirm = PasswordField('Comfirm Password', validators=[DataRequired(), EqualTo('password')])

    # recaptcha = RecaptchaField()

    def validate(self):
        check_validate = super(RegisterForm, self).validate()

        # If validator no pass
        if not check_validate:
            return False

        # Check the user whether already exist.
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('User with that name already exists.')
            return False
        return True
