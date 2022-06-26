from pymongo import MongoClient
from pprint import pprint
mongoUname = 'ViktorS'
mongoPword = 'D3adFr0g2'
cluster = MongoClient(f'mongodb+srv://{mongoUname}:{mongoPword}@cluster0.qhciunv.mongodb.net/?retryWrites=true&w=majority')
db = cluster.pytech
print('--Pytech Collection List--', '\n', db.list_collection_names())


