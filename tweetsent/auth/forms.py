from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from tweetsent.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired('Este campo es obligatorio.'), 
                                                Email('Ingresa un correo válido')])
    password = PasswordField('Contraseña', validators=[DataRequired('Este campo es obligatorio.')])
    remember_me = BooleanField('Recordarme?')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired('Este campo es obligatorio.'),
                                                  Length(max=32, message='Escoge un nombre de usuario más corto.')])
    email = StringField('Email', validators=[DataRequired('Este campo es obligatorio.'), 
                                            Email('Ingresa un correo válido')])
    password = PasswordField('Contraseña', validators=[DataRequired('Este campo es obligatorio.')])
    confirm_password = PasswordField('Repita la Contraseña',
                                                validators=[DataRequired('Este campo es obligatorio.'),
                                                EqualTo('password', 'Las contraseña no coincide.')])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Ese nombre de usuario ya ha sido tomado. Por favor elige otro.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Ya existe una cuenta registrada con ese correo.")


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired('Este campo es obligatorio.'), 
                                            Email('Ingresa un correo válido')])
    submit = SubmitField('Reestablecer Contraseña')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Contraseña', validators=[DataRequired('Este campo es obligatorio.')])
    confirm_password = PasswordField('Repita la Contraseña',
                                                validators=[DataRequired('Este campo es obligatorio.'),
                                                EqualTo('password', 'Las contraseña no coincide.')])
    submit = SubmitField('Cambiar la Contraseña')
