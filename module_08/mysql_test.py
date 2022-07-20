import mysql.connector
from mysql.connector import errorcode

# parameters to configure connection to the database
config = {
    'user'             :'pysports_user',
    'password'         :'MySQL8IsGreat!',
    'host'             :'127.0.0.1',
    'database'         :'pysports',
    'raise_on_warnings':True
}

if __name__ == '__main__':
    # attempt to establish the connection
    try:
        db = mysql.connector.connect(**config)
        print('\n Database user {} connected to MySQL on host {} with database {}.'.format(config['user'], config['host'], config['database']))
        input('\n\n Press any key to continue...')
    # provide the error information if the connection fails    
    except mysql.connector.Error as err:
        if err.errorno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('The supplied username or password is invalid.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('The specified database does not exist')
        else:
            print(err)
    # close the connection
    finally:
        db.close()