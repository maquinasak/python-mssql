from flask import Flask, request, jsonify, send_from_directory
import pyodbc

# Configuración de la conexión a SQL Server
server = '.'
port = 7000
database = 'prueba2'
username = 'sa'
password = 'Password12345'
connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes'

# connection_string = f"mssql+pyodbc://{username}:{password}@{server}:{port}/{database}?driver=ODBC+Driver+17+for+SQL+Server"

# connection_string = f"{{SQL Server}};SERVER={server};UID={username};PWD={password}"


app = Flask(__name__,static_folder='static')

def get_db_connection():
    conn = pyodbc.connect(connection_string)
    # Desactivar autocommit para manejar transacciones manualmente
    conn.autocommit = False
    return conn


def get_next_usuario():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "Select isnull(max(id),0) as ultimo from usuarios"
        cursor.execute(query)

        # Recuperar todas las filas
        rows = cursor.fetchall()
        
        # Obtener los nombres de las columnas
        columns = [column[0] for column in cursor.description]

        # Convertir las filas en una lista de diccionarios
        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))

        return results

    except Exception as e:
        raise Exception(f"error: ${e}") 
    


# # Endpoint to create a new usuario
# @app.route('/', methods=['GET'])
# def inicio():
#     return jsonify({'message': 'Inicio correcto'}), 200

@app.route('/')
def serve_index():
    # return jsonify({'message': 'llegué..'}), 200
    return send_from_directory('static', 'index.html')
    # return app.send_static_file('static/index.html')



@app.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.json
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    email = data.get('email')
    contrasenia = data.get('contrasenia')
    fechanac = data.get('fechanac')
    id = get_next_usuario()
    
    if not nombre or not apellido or not email or not contrasenia or not fechanac:
        return jsonify({'error': 'faltan campos'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "insert into usuarios (id,nombre,apellido,email,contrasenia,fechanac) values(?,?,?,?,?,?)"
        cursor.execute(query, (id,nombre,apellido,email,contrasenia,fechanac))
        conn.commit()

        return jsonify({'message': 'Update successful'}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    try:
        results = get_next_usuario()
        return jsonify(results), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# @app.route('/usuarios/<int:id>', methods=['GET'])
# def get_usuario(id):
#     usuario = Usuario.query.get(id)
#     if usuario:
#         return jsonify(usuario.to_dict())
#     else:
#         return jsonify({'message': 'Usuario no encontrado'}), 404

# @app.route('/usuarios/<int:id>', methods=['PUT'])
# def update_usuario(id):
#     usuario = Usuario.query.get(id)
#     if usuario:
#         data = request.get_json()
#         usuario.name = data['name']
#         usuario.email = data['email']
#         usuario.surname = data['surname']
#         db.session.commit()
#         return jsonify({'message': 'Usuario actualizado correctamente'})
#     else:
#         return jsonify({'message': 'Usuario no encontrado'}), 404
    

# @app.route('/usuarios/<int:id>', methods=['DELETE'])
# def delete_usuario(id):
#     usuario = Usuario.query.get(id)
#     if usuario:
#         db.session.delete(usuario)
#         db.session.commit()
#         return jsonify({'message': 'Usuario eliminado correctamente'})
#     else:
#         return jsonify({'message': 'Usuario no encontrado'}), 404
    


# def to_dict(self):
#     return {
#         'id': self.id,
#         'nombre': self.nombre,
#         'apellido': self.apellido,
#         'email': self.email,
#         'contrasenia':self.contrasenia
#     }


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')