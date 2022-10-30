from json import loads
from bson.json_util import dumps
from mongoengine.connection import get_db

def generate_backup():
    """Generates a backup of the database. Serves as a generator.
    
    https://stackoverflow.com/questions/24610484/pymongo-mongoengine-equivalent-of-mongodump
    """
    # do not save uploaded files
    EXCEPTION = ['fs.chunks', 'fs.files', 'files']

    database = get_db()

    collection_names = database.list_collection_names()
    # collections = database.list_collections()

    for i, collection_name in enumerate(collection_names):
        if collection_name in EXCEPTION: continue # skip 
        col = getattr(database, collection_names[i])
        # collection = col.find()
        data = dumps([dict(item) for item in col.find()])
        # data = loads(data)
        yield collection_name, loads(data)