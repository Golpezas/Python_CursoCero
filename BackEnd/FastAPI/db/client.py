from pymongo import MongoClient

#base de datos remota
db_client = MongoClient(
    "mongodb+srv://antoniohernandezmm:t1r0l0c0@clusterpcpython.t7ddc.mongodb.net/?retryWrites=true&w=majority&appName=ClusterPCPython")

db = db_client["DBtest"]

#base de datos local
#db_client = MongoClient()