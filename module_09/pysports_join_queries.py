import mysql.connector
from mysql.connector import errorcode

# parameter to establish the connection
config = {
    'user'             :'pysports_user',
    'password'         :'MySQL8IsGreat!',
    'host'             :'127.0.0.1',
    'database'         :'pysports',
    'raise_on_warnings':True
}

# create the connection
pysportsdb = mysql.connector.connect(**config)

# create the cursor
pysportscursor = pysportsdb.cursor()


def dbConnect(connect):
    try:
        pysportsdb
        print('\n Database user {} connected to MySQL on host {} with database {}.'.format(config['user'], config['host'], config['database']))
    except mysql.connector.Error as err:
        if err.errorno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('The supplied username or password is invalid.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('The specified database does not exist')
        else:
            print(err)

# print all tables
def printTables(cursor):
    cursor.execute('show tables')
    for record in cursor:
        print(record)

# display all entries in the "teams" table
def allTeams(cursor, table):
    print(f'--DISPLAYING THE {table.upper()} RECORDS--')
    cursor.execute(f'SELECT * FROM {table}')
    for record in cursor:
        print(f'{table.title()} ID: {record[0]}', f'{table.title()} Name: {record[1]}', f'{table.title()} Mascot: {record[2]}', sep='\n')
        print('\n')

# display all entries in the 'players' table
def allPlayers(cursor, table):
    print(f'--DISPLAYING THE {table.upper()} RECORDS--')
    cursor.execute(f'SELECT * FROM {table}')
    for record in cursor:
        print(f'Player ID: {record[0]}', f'First Name: {record[1]}', f'Last Name: {record[2]}', f'Team ID: {record[3]}', sep='\n')
        print('\n')

# left join with players as left table
def players_left_join(cursor, left_table, right_table, join_field):
    print(f'--DISPLAYING ALL {left_table.upper()} RECORDS--')
    cursor.execute(f'SELECT * FROM {left_table}, {right_table} WHERE {left_table}.{join_field}={right_table}.{join_field}')
    for record in cursor:
       #print(record)
       print(f'Player ID: {record[0]}', f'First Name: {record[1]}', f'Last Name: {record[2]}', f'Team Name: {record[5]}', sep='\n')
       print('\n')




if __name__ == '__main__':
    #dbConnect(pysportsdb)
    #printTables(pysportscursor)
    #tblName = 'team'
    #allTeams(pysportscursor, tblName)
    #tblName = 'player'
    #allPlayers(pysportscursor, tblName)
    left_table = 'player'
    right_table = 'team'
    join_field = 'team_id'
    players_left_join(pysportscursor, left_table, right_table, join_field)
    input('Press any key to continue...')
    #pysportsdb.close()
    exit(0)




