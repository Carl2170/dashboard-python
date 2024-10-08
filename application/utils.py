from database import get_connection

 
def create_document(name, user_id):
    """
    Inserta un nuevo documento en la base de datos.

    Parámetros:
    name (str): El nombre del documento.
    user_id (int): El ID del usuario que crea el documento.

    Retorna:
    int o None: El ID del documento recién creado si la inserción fue exitosa, 
                o None si hubo un error.
    """
    try:
        # Conexión a la base de datos
        conn = get_connection() 
        cursor = conn.cursor()

        # Inserción del nuevo documento y retorno del ID
        cursor.execute(
            "INSERT INTO document (name, user_id) VALUES (%s, %s) RETURNING id",
            (name, user_id)
        )
        # Obtiene el ID retornado
        document_id = cursor.fetchone()[0]  
        conn.commit()
        
        # Retorna el ID del documento creado
        return document_id 
     
    except Exception as e:
        print(f"Error al crear el documento: {e}")
        # Si ocurre un error, se revierte los cambios
        conn.rollback()  
        return None

    finally:
        cursor.close()
        conn.close()

def name_document_exists(name):
    """
    Verifica si el nombre del documento dado ya existe en la tabla 'document'.
    
    Parámetros:
    name (str): El nombre del documento a verificar.

    Retorna:
    bool: True si el nombre del documento existe, False si no existe.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Consulta para verificar si existe un documento con el mismo nombre
        cursor.execute("SELECT 1 FROM \"user\" WHERE name = %s LIMIT 1;", (name,))
        result = cursor.fetchone()  # Recupera el primer resultado

        # Retorna True si encontró el registro, False si no
        return result is not None  

    except Exception as e:
        print(f"Error al verificar si hay nombre duplicado: {e}")
        return False

    finally:
        cursor.close()
        conn.close()

