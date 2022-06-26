
from pymongo import InsertOne, MongoClient
from pprint import pprint
mongoUname = 'ViktorS'
mongoPword = 'D3adFr0g2'
client = MongoClient(f'mongodb+srv://{mongoUname}:{mongoPword}@cluster0.qhciunv.mongodb.net/?retryWrites=true&w=majority')
#db = client.pytech
pydb = client['pytech']
pycol = pydb['students']

stu_id=[1007, 1008, 1009]
fnames = ['thorin', 'bilbo', 'frodo']
lnames = ['oakenshield', 'baggins', 'baggins']

print('---Insert Statements---')
for i in range(len(stu_id)):
    doc = pycol.insert_one({'stu_id':stu_id[i], 'stu_fname':fnames[i], 'stu_lname':lnames[i]})
    print(f'Inserted student record {fnames[i].title()} {lnames[i].title()} into the students collection with document_id {doc.inserted_id}')
if input('End of program, press any key to exit...'): exit(0)

