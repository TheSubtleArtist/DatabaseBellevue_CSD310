import mysql.connector

from mysql.connector import errorcode
from time import sleep

wait = 1

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
def allTeams(cursor):
    table = 'team'
    print(f'--DISPLAYING THE {table.upper()} RECORDS--')
    cursor.execute(f'SELECT * FROM {table}')
    for record in cursor:
        print(f'{table.title()} ID: {record[0]}', f'{table.title()} Name: {record[1].title()}', f'{table.title()} Mascot: {record[2].title()}', sep='\n')
        print('\n')

# display all entries in the 'players' table
def allPlayers(cursor):
    table = 'player'
    print(f'--DISPLAYING THE {table.upper()} RECORDS--')
    cursor.execute(f'SELECT * FROM {table}')
    for record in cursor:
        print(f'Player ID: {record[0]}', f'First Name: {record[1].title()}', f'Last Name: {record[2].title()}', f'Team ID: {record[3]}', sep='\n')
        print('\n')

# inner join with players as left table
def players_inner_join(cursor, purpose):
    left_table = 'player'
    right_table = 'team'
    join_field = 'team_id'
    print(f'--DISPLAYING ALL {left_table.upper()} RECORDS AFTER {purpose.upper()}--')
    cursor.execute(f'SELECT * FROM {left_table} INNER JOIN {right_table} ON {left_table}.{join_field}={right_table}.{join_field} ORDER BY player.player_id')
    for record in cursor:
       #print(record)
       print(f'Player ID: {record[0]}', f'First Name: {record[1].title()}', f'Last Name: {record[2].title()}', f'Team Name: {record[5].title()}', sep='\n')
       print('\n')


def insert_player(cursor):
    first_name = 'smeagol'
    last_name = 'shire folk'
    team_id = 1
    insert_statement = """INSERT INTO player (first_name, last_name, team_id) VALUES (%s, %s, %s)"""
    insert_values = (first_name, last_name, team_id)
    cursor.execute(insert_statement, insert_values)
   
def player_trade(cursor):
    new_team_id = 2
    query_field = 'first_name'
    query_value = 'smeagol'
    update_statement = """UPDATE player SET team_id = %s WHERE first_name = %s """
    update_values = (new_team_id, query_value)
    cursor.execute(update_statement, update_values)

def delete_player(cursor):
    delete_criteria = 'smeagol'
    delete_statement ="""DELETE FROM player WHERE first_name = %s"""
    delete_criteria = (delete_criteria,)
    cursor.execute(delete_statement, delete_criteria)
    
    


if __name__ == '__main__':
    #dbConnect(pysportsdb)
    #printTables(pysportscursor)
    #allTeams(pysportscursor)
    #allPlayers(pysportscursor)
    insert_player(pysportscursor)
    sleep(wait)
    players_inner_join(pysportscursor, 'insert')
    sleep(wait)
    player_trade(pysportscursor)
    sleep(wait)
    players_inner_join(pysportscursor, 'update')
    sleep(wait)
    delete_player(pysportscursor)
    sleep(wait)
    players_inner_join(pysportscursor, 'delete')
    sleep(wait)
    pysportsdb.commit()
    input('Press any key to continue...')
    pysportsdb.close()
    exit(0)




