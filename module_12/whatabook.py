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

# print all books
def show_books(cursor):
    print('--DISPLAYING ALL BOOKS--')
    cursor.execute('SELECT * FROM book INNER JOIN store ON book.store_id')
    for record in cursor:
        #print(record)
        print(f"Book ID: {record[0]}", f"Title: {record[1].title()}", f"Author: {record[2].title()}", f"Book Detail: {record[3].title()}", f"Location: {record[6]}", sep='\n' )
        print('\n')
    print('\n')

# Requested user_id, validate the user_id
def get_user(cursor):
    # Set a flag to create a loop to go through User ID until a valid User ID is input
    flag = False
    # Enter the while loop
    while flag == False:
        print('\n','--DISPLAYING ALL USERS-- ')
        cursor.execute('SELECT * FROM user_table')
        for u in cursor:
            #print(record)
            print(f"User ID: {u[0]}", f"Name: {u[1].title()} {u[2].title()}", sep="  ")
            #print('\n')
        # request user id input    
        requested_user = input('Enter a valid user ID: ')
        if int(requested_user) < 0 or int(requested_user) >3:
            print('Invalid User ID. Please try again', '\n')
        else:
            flag = True
        return requested_user

# Show specific user information
def display_user(cursor):
    requested_user = get_user(cursor)
    user_request = 'SELECT * FROM user_table WHERE user_id = %s'
    cursor.execute(user_request, (requested_user,))
    u = cursor.fetchone()
    print('---User Details---')
    print(f"User ID: {u[0]}", f"Name: {u[1].title()} {u[2].title()}", sep="  ")
    return requested_user
    
def display_wishlist(cursor):
    requested_user = display_user(cursor)
    #print(requested_user)
    wishlist_request = ("SELECT * FROM user_table INNER JOIN wishlist ON user_table.user_id = wishlist.user_id INNER JOIN book ON wishlist.book_id = book.book_id WHERE user_table.user_id = %s")
    cursor.execute(wishlist_request, (requested_user,))
    wishlist = cursor.fetchall()
    print('\n', '--- User Wishlist---')
    for r in wishlist:
        print(f"Title: {r[7].title()}",f"Author: {r[8].title()}", f"Book Detail: {r[9].title()}", sep='\n')
        print('\n')

def books_to_add(cursor):
    requested_user = get_user(cursor)
    available_books_request = ("SELECT book_id, book_name, book_author FROM book WHERE book_id NOT IN (SELECT book_id FROM wishlist WHERE user_id = %s)")
    cursor.execute(available_books_request, (requested_user,))
    available_books = cursor.fetchall()
    print('\n', '--Books available for addition to the user wishlist--')
    #print(available_books)
    for r in available_books:
        print(f"Book ID: {r[0]}", f"Book Title: {r[1].title()}", f"Author: {r[2].title()}", sep="\n")
        print('\n')

def add_to_wishlist(cursor, user, book):
    add_statement = ("INSERT INTO wishlist(user_id, book_id) VALUES(%s, %s )")
    cursor.execute(add_statement, user, book)
    

# show all stores
def show_stores(cursor):
    print('\n', '--DISPLAYING STORE LOCATIONS--')
    cursor.execute('SELECT * FROM store')
    for record in cursor:
        print(f"Store {record[0]}: {record[1].title()}")
    print('\n')

# Exit the program
def exit_program(cursor):
    print('All Hail The Google!')
    exit(0)

# Show a menu
def show_menu(menu):
    print('\n', 'Action Menu')
    for key, value in menu.items():
        print(f'{key}: {value.title()}')

def main(cursor):
    show_menu(main_menu)
    main_option = input("Please select an option: ")
    function_list[main_option](whatabookcursor)

def user(cursor):
    # display the user account options menu
    show_menu(user_menu)
    user_option = input('Enter an option: ')
    function_list[user_option](cursor)

main_menu = {
    "1": "show books",
    "2": "show store locations",
    "3": "User Account",
    "0": "exit"
}

function_list = {
    '1': show_books,
    '2': show_stores,
    '3': user,
    '4': display_user,
    '5': display_wishlist,
    '6': books_to_add,
    '9': main,
    '0': exit_program
}

user_menu = {
    '4': 'show user data',
    '5': "show user wishlist",
    '6': "add book to wishlist",
    '9': "return to main menu"
}

if __name__ == '__main__':
    print('Welcome to What a Book', '\n')
    while True:
        main(whatabookcursor)





