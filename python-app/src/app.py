from flask import Flask, request, jsonify, send_from_directory
import mysql.connector

app = Flask(__name__,static_folder='static')


# MySQL connection details
db_host = "mysql"
db_user = "user"
db_password = "password"
db_name = "mydatabase"

# Function to connect to the database
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

# # Endpoint to create a new usuario
# @app.route('/', methods=['GET'])
# def inicio():
#     return jsonify({'message': 'Inicio correcto'}), 200

@app.route('/')
def serve_index():
    # return jsonify({'message': 'llegué..'}), 200
    return send_from_directory('static', 'index.html')
    # return app.send_static_file('static/index.html')



# Endpoint to create a new usuario
@app.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.get_json()
    email = data.get('email')
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    fechanac = data.get('fechanac')

    conn = connect_to_db()
    cursor = conn.cursor()

    sql = "INSERT INTO usuarios (email, nombre, apellido, fechanac) VALUES (%s, %s, %s, %s)"
    val = (email, nombre, apellido, fechanac)

    try:
        cursor.execute(sql, val)
        conn.commit()
        return jsonify({'message': 'Usuario creado correctamente'}), 201
    except mysql.connector.Error as err:
        print(f"Error inserting usuario: {err}")
        return jsonify({'error': 'Error al crear el usuario'}), 500
    finally:
        if conn:
            conn.close()

# Endpoint to get all usuarios
@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    conn = connect_to_db()
    cursor = conn.cursor()

    sql = "SELECT * FROM usuarios"
    cursor.execute(sql)
    usuarios = cursor.fetchall()
    data = {
        "rta":"ok",
        "usuarios": usuarios
    }

    return jsonify(data), 200

# Endpoint to get a usuario by email
@app.route('/usuarios/<string:email>', methods=['GET'])
def get_usuario(email):
    conn = connect_to_db()
    cursor = conn.cursor()

    sql = "SELECT * FROM usuarios WHERE email = %s"
    val = (email,)
    cursor.execute(sql, val)
    usuario = cursor.fetchone()

    data = {
        "rta":"ok",
    }

    if usuario:
        data["usuarios"] = usuario
        return jsonify(data), 200
    else:
        data["error"] = "usuario no encontrado"
        return jsonify(data), 404

# Endpoint to update a usuario
@app.route('/usuarios/<string:email>', methods=['PUT'])
def update_usuario(email):
    data = request.get_json()
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    fechanac = data.get('fechanac')

    conn = connect_to_db()
    cursor = conn.cursor()

    sql = "UPDATE usuarios SET nombre = %s, apellido = %s, fechaNac = %s WHERE email = %s"
    val = (nombre, apellido, fechanac, email)

    try:
        cursor.execute(sql, val)
        conn.commit()
        return jsonify({'message': 'Usuario actualizado correctamente'}), 200
    except mysql.connector.Error as err:
        print(f"Error updating usuario: {err}")
        return jsonify({'error': 'Error al actualizar el usuario'}), 500
    finally:
        if conn:
            conn.close()

# Endpoint to delete a usuario
@app.route('/usuarios/<string:email>', methods=['DELETE'])
def delete_usuario(email):
    conn = connect_to_db()
    cursor = conn.cursor()

    sql = "DELETE FROM usuarios WHERE email = %s"
    val = (email,)

    try:
        cursor.execute(sql, val)
        conn.commit()
        return jsonify({'message': 'Usuario eliminado correctamente'}), 200
    except mysql.connector.Error as err:
        print(f"Error deleting usuario: {err}")
        return jsonify({'error': 'Error al eliminar el usuario'}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')