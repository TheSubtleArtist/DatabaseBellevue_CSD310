from pymongo import MongoClient
mongoUname = 'admin'
mongoPword = 'admin'
fsids = [1007, 1008, 1009]
client = MongoClient(f'mongodb+srv://{mongoUname}:{mongoPword}@cluster0.qhciunv.mongodb.net/?retryWrites=true&w=majority')
pydb = client['pytech']
pycol = pydb['students']

def findAll():
    find_students = pycol.find()
    for each in find_students:
        print('Student ID: '+ str(each['sid']), 'First Name: ' + each['sfname'].title(), 'Last Name: ' + each['slname'].title(), sep='\n')
        print('\n')
        
def findOne(fsid):
    fnd1 = pycol.find_one({'sid':fsid},{'_id':0, 'sid':1, 'sfname':1, 'slname': 1})
    print('Student ID: '+ str(fnd1['sid']), 'First Name: ' + fnd1['sfname'].title(), 'Last Name: ' + fnd1['slname'].title(), sep='\n')

if __name__ == '__main__':
    with client:
        print('--DISPLAYING STUDENTS DOCUMENTS FROM find() QUERY--')
        findAll()
        fsid=int(input('Input a student id number (1007, 1008, or 1009), or any other key to exit '))
        while fsid in fsids:
            print('--DISPLAYING STUDENTS DOCUMENTS FROM find_one() QUERY--')
            findOne(fsid)
            fsid=int(input('Input a student id number (1007, 1008, or 1009), or any other key to exit '))
        if input('\n'+'End of program, press any key to exit...'): exit(0)

    


