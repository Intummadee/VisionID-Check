from pymongo import MongoClient
def get_db_handle(db_name, host, port, username, password):

 client = MongoClient(host=host,
                      port=int(port),
                      username=username,
                      password=password
                     )
 db_handle = client['CardCheck'] # Use the variable db_name instead of 'db_name'
 return db_handle, client