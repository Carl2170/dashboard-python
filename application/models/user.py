from database import get_connection

class User:
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password
    
    def __repr__(self):
        return f"<User {self.name}>"
    

    # Función para insertar un nuevo usuario
    def create_user(name, password):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO \"user\" (name, password) VALUES (%s, %s) RETURNING id", (name, password))
        user_id = cursor.fetchone()[0]

        conn.commit()
        cursor.close()
        conn.close()
        
        return User(id=user_id, name=name, password=password)