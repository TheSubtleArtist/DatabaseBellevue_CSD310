
from bson import ObjectId
from pymongo import MongoClient
from pprint import pprint
mongoUname = 'admin'
mongoPword = 'admin'
client = MongoClient(f'mongodb+srv://{mongoUname}:{mongoPword}@cluster0.qhciunv.mongodb.net/?retryWrites=true&w=majority')
pydb = client['pytech']
pycol = pydb['students']

stu_id=[1007, 1008, 1009]
fnames = ['thorin', 'bilbo', 'frodo']
lnames = ['oakenshield', 'baggins', 'baggins']

def preclean():
    pycol.delete_many({})

def searchRecords():
        print(f'Student record {fnames[i].title()} {lnames[i].title()} already exists with document id {ObjectId()}')
        

def insertRecords():
    doc = pycol.insert_one({'sid':stu_id[i], 'sfname':fnames[i], 'slname':lnames[i]})
    print(f'Inserted student record {fnames[i].title()} {lnames[i].title()} into the students collection with document id {doc.inserted_id}')


if __name__ == '__main__':
    #preclean()
    print('---Insert Statements---')
    for i in range(len(stu_id)):
        fnd1 = pycol.find_one({'sid':stu_id[i]},{'_id':1, 'sid':1, 'sfname':1, 'slname': 1})
        if fnd1:
            searchRecords()
        else: 
            insertRecords()
    if input('End of program, press any key to exit...'): exit(0)
    