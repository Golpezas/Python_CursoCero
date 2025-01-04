#Variables
'''
mi_variable = "Hola, Mundo"
numero = 42
pi = 3.14159
es_verdadero = True
lista = [1, 2, 3, 4, 5]
diccionario = {"clave": "valor", "edad": 30}

# Convertir la variable 'numero' de int a str
numero_str = str(numero)
print(numero_str)

# Convertir la variable 'pi' de float a int
pi_int = int(pi)
print(pi_int)

# ¿Forzamos el tipo?
address: str = "Mi dirección"
address = True
address = 5
address = 1.2
print(type(address))

# Variables en una sola línea. ¡Cuidado con abusar de esta sintaxis!
name, surname, alias, age = "Brais", "Moure", 'MoureDev', 35
print("Me llamo:", name, surname, ". Mi edad es:", age, ". Y mi alias es:", alias)

# Inputs
name = input('¿Cual es tu nombre? ')
age = input('¿Cuántos años tienes? ')
print(name)
print(age)
'''
# Validar que 'name' no contenga números
name = input('¿Cual es tu nombre? ')
while any(char.isdigit() for char in name):
    print("El nombre no debe contener números.")
    name = input('¿Cual es tu nombre? ')

# Validar que 'age' solo contenga números
age = input('¿Cuántos años tienes? ')
while not age.isdigit():
    print("La edad debe ser un número.")
    age = input('¿Cuántos años tienes? ')

print(name)
print(age)

