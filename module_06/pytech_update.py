from pymongo import MongoClient

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

def findAll():
    find_students = pycol.find()
    for each in find_students:
        print('Student ID: '+ str(each['sid']), 'First Name: ' + each['sfname'].title(), 'Last Name: ' + each['slname'].title(), sep='\n')
        print('\n')
        
def findOne(fsid):
    fnd1 = pycol.find_one({'sid':fsid},{'_id':0, 'sid':1, 'sfname':1, 'slname': 1})
    print('Student ID: '+ str(fnd1['sid']), 'First Name: ' + fnd1['sfname'].title(), 'Last Name: ' + fnd1['slname'].title(), sep='\n')

def insertRecords(i):
    doc = pycol.insert_one({'sid':stu_id[i], 'sfname':fnames[i], 'slname':lnames[i]})
    #print(f'Inserted student record {fnames[i].title()} {lnames[i].title()} into the students collection with document id {doc.inserted_id}')

def updateOne(fsid):
    print(f'--- DISPLAYING STUDENT RECORD {fsid} ---')
    qryValue = {'sid':fsid}
    newValue = {'$set': {'slname':'broakenshield'}}
    pycol.update_one(qryValue, newValue)


if __name__ == '__main__':
    with client:
        preclean()
        for i in range(len(stu_id)):
            insertRecords(i)
        print('--DISPLAYING STUDENTS DOCUMENTS FROM find() QUERY--')
        findAll()
        updateOne(fsid = 1007)
        findOne(fsid = 1007)
        print('\n'+'End of program...')
        exit(0)

        #fsid=int(input('Input a student id number (1007, 1008, or 1009), or any other key to exit '))
        #while fsid in fsids:
            #print('--DISPLAYING STUDENTS DOCUMENTS FROM find_one() QUERY--')
            #findOne(fsid)
            #fsid=int(input('Input a student id number (1007, 1008, or 1009), or any other key to exit '))
        #if input('\n'+'End of program, press any key to exit...'): exit(0)

    


