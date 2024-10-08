import psycopg2

def init_database():
    # Aquí puedes poner la lógica de creación de tablas, si es necesario
    conn = psycopg2.connect(database="dashbaord_python",
                            host="localhost",
                            user="postgres",
                            password="Eyeoftiger123",
                            port=5432)
    cursor = conn.cursor()

    # Crear tablas (si no existen)
    cursor.execute('''CREATE TABLE IF NOT EXISTS "user" (
                   id SERIAL PRIMARY KEY,
                   name VARCHAR(100),
                   password VARCHAR(30)
                   );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS document (
                   id SERIAL PRIMARY KEY,
                   name VARCHAR(50),
                   user_id INT,
                   FOREIGN KEY (user_id) REFERENCES "user"(id)
                   );''')

    conn.commit()
    cursor.close()
    conn.close()


def get_connection():
    return psycopg2.connect(
        database="dashbaord_python",
        host="localhost",
        user="postgres",
        password="Eyeoftiger123",
        port=5432
    )
