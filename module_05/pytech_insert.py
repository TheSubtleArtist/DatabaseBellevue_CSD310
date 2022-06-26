'''

'''



from pymongo import MongoClient
from pprint import pprint
mongoUname = 'ViktorS'
mongoPword = 'D3adFr0g2'
client = MongoClient(f'mongodb+srv://{mongoUname}:{mongoPword}@cluster0.qhciunv.mongodb.net/?retryWrites=true&w=majority')
#db = client.pytech
pydb = client['pytech']
pycol = pydb['students']
stuList = [
{'stu_id': 1007, 'fname':'thorin', 'lname':'oakenshield' },
{'stu_id': 1008, 'fname':'frodo', 'lname':'baggins' },
{'stu_id': 1009, 'fname':'bilbo', 'lname':'baggins' }
]

print('---Insert Statements---')
print(f'Inserted student record {fname.title()} {lname.title()} into the students collection with document_id {doc_id}')
print('End of program, press any key to exit')

