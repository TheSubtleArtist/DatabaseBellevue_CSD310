import mysql.connector
from mysql.connector import errorcode

# parameter to establish the connection
config = {
    'user'             :'whatabook_user',
    'password'         :'MySQL8IsGreat!',
    'host'             :'127.0.0.1',
    'database'         :'whatabook',
    'raise_on_warnings':True
}

# create the connection
whatabookdb = mysql.connector.connect(**config)

# create the cursor
whatabookcursor = whatabookdb.cursor()


def dbConnect(connect):
    try:
        whatabookdb
        print('\n Database user {} connected to MySQL on host {} with database {}.'.format(config['user'], config['host'], config['database']))
    except mysql.connector.Error as err:
        if err.errorno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('The supplied username or password is invalid.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('The specified database does not exist')
        else:
            print(err)