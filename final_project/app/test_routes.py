from flask import Blueprint, request, jsonify
from app.models import db, Libro  # Cambiado Curso por Libro

# Blueprint para endpoints de prueba de libros
main = Blueprint('main', __name__)

@main.route('/')
@main.route('/dashboard')
def index():
    return '<h1>Sistema de Biblioteca - Modo Pruebas</h1>'

@main.route('/libros', methods=['GET'])  # Cambiado cursos por libros
def listar_libros():
    """
    Retorna lista de libros en JSON
    """
    libros = Libro.query.all()
    
    data = [
        {
            'id': libro.id,
            'titulo': libro.titulo,
            'autor': libro.autor,
            'isbn': libro.isbn,
            'genero': libro.genero,
            'disponibilidad': libro.disponibilidad,
            'user_id': libro.user_id
        }
        for libro in libros
    ]
    return jsonify(data), 200

@main.route('/libros/<int:id>', methods=['GET'])  # Actualizada ruta
def listar_un_libro(id):
    """
    Retorna un libro por ID
    """
    libro = Libro.query.get_or_404(id)
    
    data = {
        'id': libro.id,
        'titulo': libro.titulo,
        'autor': libro.autor,
        'isbn': libro.isbn,
        'fecha_publicacion': str(libro.fecha_publicacion) if libro.fecha_publicacion else None,
        'genero': libro.genero,
        'disponibilidad': libro.disponibilidad,
        'user_id': libro.user_id
    }
    return jsonify(data), 200

@main.route('/libros', methods=['POST'])  # Nueva ruta para crear libros
def crear_libro():
    """
    Crea un libro sin validaciones
    Requiere JSON con: titulo, autor, isbn, user_id
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Datos requeridos'}), 400
    
    libro = Libro(
        titulo=data.get('titulo'),
        autor=data.get('autor'),
        isbn=data.get('isbn'),
        genero=data.get('genero', ''),
        user_id=data.get('user_id')
    )
    
    db.session.add(libro)
    db.session.commit()
    
    return jsonify({
        'message': 'Libro creado',
        'id': libro.id,
        'isbn': libro.isbn
    }), 201

@main.route('/libros/<int:id>', methods=['PUT'])  # Ruta actualizada
def actualizar_libro(id):
    """
    Actualiza un libro sin validaciones
    """
    libro = Libro.query.get_or_404(id)
    data = request.get_json()
    
    # Campos actualizables
    updatable_fields = ['titulo', 'autor', 'isbn', 'genero', 'disponibilidad']
    for field in updatable_fields:
        if field in data:
            setattr(libro, field, data[field])
    db.session.commit()
    return jsonify({'message': 'Libro actualizado'}), 200
@main.route('/libros/<int:id>', methods=['DELETE'])  # Ruta actualizada
def eliminar_libro(id):
    """
    Elimina un libro por ID
    """
    libro = Libro.query.get_or_404(id)
    
    db.session.delete(libro)
    db.session.commit()
    
    return jsonify({'message': 'Libro eliminado'}), 200
@main.route('/libros/<int:id>/disponibilidad', methods=['PATCH'])  # Nueva ruta
def cambiar_disponibilidad(id):
    """
    Cambia la disponibilidad de un libro por ID
    """
    libro = Libro.query.get_or_404(id)
    
    # Cambiar disponibilidad
    libro.disponibilidad = not libro.disponibilidad
    db.session.commit()
    
    return jsonify({
        'message': 'Disponibilidad actualizada',
        'disponibilidad': libro.disponibilidad
    }), 200
@main.route('/libros/<int:id>/prestamo', methods=['POST'])  # Nueva ruta
def prestar_libro(id):
    """
    Presta un libro por ID
    """
    libro = Libro.query.get_or_404(id)
    
    if not libro.disponibilidad:
        return jsonify({'error': 'El libro no está disponible'}), 400
    
    # Cambiar disponibilidad a False
    libro.disponibilidad = False
    db.session.commit()
    
    return jsonify({
        'message': 'Libro prestado',
        'disponibilidad': libro.disponibilidad
    }), 200
@main.route('/libros/<int:id>/devolucion', methods=['POST'])  # Nueva ruta
def devolver_libro(id):
    """
    Devuelve un libro por ID
    """
    libro = Libro.query.get_or_404(id)
    
    if libro.disponibilidad:
        return jsonify({'error': 'El libro ya está disponible'}), 400
    
    # Cambiar disponibilidad a True
    libro.disponibilidad = True
    db.session.commit()
    
    return jsonify({
        'message': 'Libro devuelto',
        'disponibilidad': libro.disponibilidad
    }), 200
    db.session.commit()
#     print(f'✅ Libro "{libro.titulo}" creado.')
#         else:
#             print(f'ℹ️ El libro con ISBN {libro_info["isbn"]} ya existe.')
#     db.session.commit()