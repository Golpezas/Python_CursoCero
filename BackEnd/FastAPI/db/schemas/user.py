def user_schema(user) -> dict:
    return {
        "id": str(user["_id"]),
        "Nombre": user["Nombre"],
        "Apellido": user["Apellido"],
        "Edad": user["Edad"],
        "email": user["email"]
    }

def users_schema(users) -> dict:
    return [user_schema(user) for user in users]

