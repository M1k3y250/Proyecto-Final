from app import create_app, db
from app.models import Role, User, Libro
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Crear roles actualizados
    roles = ['Admin', 'Bibliotecario', 'Lector']
    for role_name in roles:
        existing_role = Role.query.filter_by(name=role_name).first()
        if not existing_role:
            new_role = Role(name=role_name)
            db.session.add(new_role)
            print(f'✅ Rol "{role_name}" creado.')

    db.session.commit()

    # Usuarios de demostración actualizados
    users_data = [
        {
            "username": "Administrador",
            "email": "admin@biblioteca.com",
            "password": "admin123",
            "role_name": "Admin"
        },
        {
            "username": "Ana Sanchez",
            "email": "bibliotecario@biblioteca.com",
            "password": "biblio123",
            "role_name": "Bibliotecario"
        },
        {
            "username": "Carlos Pérez",
            "email": "lector@biblioteca.com",
            "password": "lector123",
            "role_name": "Lector"
        }
    ]

    for user_info in users_data:
        existing_user = User.query.filter_by(email=user_info['email']).first()
        if not existing_user:
            role = Role.query.filter_by(name=user_info['role_name']).first()
            user = User(
                username=user_info['username'],
                email=user_info['email'],
                role=role
            )
            user.set_password(user_info['password'])
            db.session.add(user)
            print(f'✅ Usuario "{user.username}" creado con rol "{role.name}".')
        else:
            print(f'ℹ️ El usuario con email {user_info["email"]} ya existe.')

    db.session.commit()

    # Crear libros de demostración
    bibliotecario = User.query.filter_by(email='bibliotecario@biblioteca.com').first()
    
    libros_data = [
        {
            "titulo": "Cien años de soledad",
            "autor": "Gabriel García Márquez",
            "isbn": "9788437604947",
            "genero": "ficcion",
            "user_id": bibliotecario.id
        },
        {
            "titulo": "Física Universitaria",
            "autor": "Sears Zemansky",
            "isbn": "9786073240154",
            "genero": "ciencia",
            "user_id": bibliotecario.id
        }
    ]

    for libro_info in libros_data:
        existing_libro = Libro.query.filter_by(isbn=libro_info['isbn']).first()
        if not existing_libro:
            libro = Libro(**libro_info)
            db.session.add(libro)
            print(f'✅ Libro "{libro.titulo}" agregado al catálogo.')
        else:
            print(f'ℹ️ El libro con ISBN {libro_info["isbn"]} ya existe.')

    db.session.commit()
    print("✅ Base de datos inicializada con datos de demostración.")