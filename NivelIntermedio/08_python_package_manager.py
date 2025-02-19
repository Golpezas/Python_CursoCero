# Clase en vídeo: https://youtu.be/TbcEqkabAWU?t=24010

### Python Package Manager ###

# PIP https://pypi.org

# pip install pip
# pip --version

# pip install numpy

import pandas
try:
	from mypackage import arithmetics
except ImportError:
	print("mypackage is not installed. Please install it to proceed.")
	arithmetics = None
import requests
import numpy

print(numpy.version.version)

numpy_array = numpy.array([35, 24, 62, 52, 30, 30, 17])
print(type(numpy_array))

print(numpy_array * 2)

# pip install pandas

# pip list
# pip uninstall pandas
# pip show numpy

# pip install requests

response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=151")
print(response)
print(response.status_code)
print(response.json())

# Arithmetics Package


print(arithmetics.sum_two_values(1, 4))