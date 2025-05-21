from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.forms import ChangePasswordForm, LibroForm
from app.models import db, User, Libro  # Removido Curso
from flask_security import roles_accepted

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('Contraseña actual incorrecta')
            return render_template('cambiar_password.html', form=form)
        
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('✅ Contraseña actualizada correctamente')
        return redirect(url_for('main.dashboard'))
    
    return render_template('cambiar_password.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    # Actualizado para usar Libro y nuevos roles
    if current_user.role.name == 'Lector':
        libros = Libro.query.all()
    else:
        libros = Libro.query.filter_by(user_id=current_user.id).all()
    
    return render_template('dashboard.html', libros=libros)

@main.route('/libros')
@login_required
def libros():
    libros = Libro.query.all()
    return render_template('libros.html', libros=libros)

@main.route('/agregar_libro', methods=['GET', 'POST'])
@login_required
@roles_accepted('Bibliotecario', 'Admin')
def agregar_libro():
    form = LibroForm()
    if form.validate_on_submit():
        try:
            libro = Libro(
                titulo=form.titulo.data,
                autor=form.autor.data,
                isbn=form.isbn.data,
                fecha_publicacion=form.fecha_publicacion.data,
                genero=form.genero.data,
                user_id=current_user.id
            )
            db.session.add(libro)
            db.session.commit()
            flash('Libro agregado exitosamente', 'success')
            return redirect(url_for('main.libros'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar libro: {str(e)}', 'danger')
    
    return render_template('libro_form.html', form=form)

@main.route('/editar_libro/<int:id>', methods=['GET', 'POST'])
@login_required
@roles_accepted('Bibliotecario', 'Admin')
def editar_libro(id):
    libro = Libro.query.get_or_404(id)
    
    # Verificar permisos: Bibliotecario solo puede editar sus propios libros
    if current_user.role.name == 'Bibliotecario' and libro.user_id != current_user.id:
        flash('No tienes permiso para editar este libro', 'danger')
        return redirect(url_for('main.libros'))
    
    form = LibroForm(obj=libro)
    if form.validate_on_submit():
        try:
            form.populate_obj(libro)
            db.session.commit()
            flash('Libro actualizado exitosamente', 'success')
            return redirect(url_for('main.libros'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar libro: {str(e)}', 'danger')
    
    return render_template('libro_form.html', form=form, libro=libro)

@main.route('/eliminar_libro/<int:id>', methods=['POST'])
@login_required
@roles_accepted('Admin')
def eliminar_libro(id):
    libro = Libro.query.get_or_404(id)
    try:
        db.session.delete(libro)
        db.session.commit()
        flash('Libro eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar libro: {str(e)}', 'danger')
    
    return redirect(url_for('main.libros'))

@main.route('/usuarios')
@login_required
@roles_accepted('Admin')
def listar_usuarios():
    usuarios = User.query.join(User.role).all()
    return render_template('usuarios.html', usuarios=usuarios)