from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

# Formulario para inicio de sesión
class LoginForm(FlaskForm):
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

# Formulario para registro de usuarios
class RegisterForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired()])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(), 
        EqualTo('password', message='Las contraseñas deben coincidir')
    ])
    
    role = SelectField(
        'Rol',
        choices=[
            ('Lector', 'Lector'),
            ('Bibliotecario', 'Bibliotecario'),
            ('Admin', 'Administrador')
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField('Registrarse')

# Formulario para cambio de contraseña
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Contraseña Actual', validators=[DataRequired()])
    new_password = PasswordField('Nueva Contraseña', validators=[
        DataRequired(), 
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres')
    ])
    confirm_password = PasswordField('Confirmar Nueva Contraseña', validators=[
        DataRequired(), 
        EqualTo('new_password', message='Las contraseñas deben coincidir')
    ])
    submit = SubmitField('Actualizar Contraseña')

# Formulario para gestión de libros
class LibroForm(FlaskForm):
    titulo = StringField('Título', validators=[
        DataRequired(message='El título es obligatorio'),
        Length(max=100, message='Máximo 100 caracteres')
    ])
    
    autor = StringField('Autor', validators=[
        DataRequired(message='El autor es obligatorio'),
        Length(max=100, message='Máximo 100 caracteres')
    ])
    
    isbn = StringField('ISBN', validators=[
        DataRequired(message='El ISBN es obligatorio'),
        Length(min=10, max=13, message='El ISBN debe tener entre 10 y 13 caracteres')
    ])
    
    fecha_publicacion = DateField('Fecha de Publicación', 
        format='%Y-%m-%d',
        validators=[Optional()]
    )
    
    genero = SelectField('Género', 
        choices=[
            ('', 'Seleccione...'),
            ('ficcion', 'Ficción'),
            ('no-ficcion', 'No Ficción'),
            ('ciencia', 'Ciencia'),
            ('historia', 'Historia'),
            ('infantil', 'Infantil')
        ],
        validators=[DataRequired(message='Seleccione un género')]
    )
    
    disponibilidad = BooleanField('Disponible', default=True)
    submit = SubmitField('Guardar')