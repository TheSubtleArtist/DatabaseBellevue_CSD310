from pymongo import MongoClient
from pprint import pprint
mongoUname = 'admin'
mongoPword = 'admin'
client = MongoClient(f'mongodb+srv://{mongoUname}:{mongoPword}@cluster0.qhciunv.mongodb.net/?retryWrites=true&w=majority')
db = client.pytech

print('--Pytech Collection List--', '\n', db.list_collection_names())
if input('End of program, press any key to exit...'): exit(0)


