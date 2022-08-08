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
        print(f"Book ID: {record[0]}", f"Title: {record[1].title()}", f"Author: {record[2].title()}", f"Book Detail: {record[3].title()}", f"Location: {record[6]}", sep='\n' )
        print('\n')
    print('\n')


# show all stores
def show_stores(cursor):
    print('\n', '--DISPLAYING STORE LOCATIONS--')
    cursor.execute('SELECT * FROM store')
    for record in cursor:
        print(f"Store {record[0]}: {record[1].title()}")
    print('\n')


# Requested user_id, validate the user_id
def get_user(cursor):
    # Set a flag to create a loop to go through User ID until a valid User ID is input
    flag = False
    # Enter the while loop
    while flag == False:
        print('\n','--DISPLAYING ALL USERS-- ')
        # query the database for all entries in the user table
        cursor.execute('SELECT * FROM user_table')
        user_list = cursor.fetchall()
        # print all the entries in the user table
        for u in user_list:
            print(f"User ID: {u[0]}", f"Name: {u[1].title()} {u[2].title()}", sep="  ")  
        # request user input which matches one of the displayed users 
        requested_user = input('Enter a valid user ID: ')
        # test if the input supplied matches one of the user id's 
        if int(requested_user) < 1 or int(requested_user) > 3:
            print('Invalid User ID. Please try again', '\n')
        else:
            # exit the while loop if input is a match
            flag = True
    # return the acceptable user id
    return requested_user

# Show specific user information
def display_user(cursor):
    # call the "get_user function to identify acceptable input"
    requested_user = get_user(cursor)
    user_request = 'SELECT * FROM user_table WHERE user_id = %s'
    cursor.execute(user_request, (requested_user,))
    # fetch the only record which is returned
    u = cursor.fetchone()
    print('---User Details---')
    print(f"User ID: {u[0]}", f"Name: {u[1].title()} {u[2].title()}", sep="  ")
    
def display_wishlist(cursor):
    # find an acceptable user id
    requested_user = get_user(cursor)
    # form the SQL statement
    wishlist_request = ("SELECT * FROM user_table INNER JOIN wishlist ON user_table.user_id = wishlist.user_id INNER JOIN book ON wishlist.book_id = book.book_id WHERE user_table.user_id = %s")
    # send the SQL statement and the acceptable user ID to the database
    cursor.execute(wishlist_request, (requested_user,))
    # fetch all records returned by the cursor
    wishlist = cursor.fetchall()
    print('\n', '--- User Wishlist---')
    # print the user wishlist
    for r in wishlist:
        print(f"Title: {r[7].title()}",f"Author: {r[8].title()}", f"Book Detail: {r[9].title()}", sep='\n')
        print('\n')

def books_to_add(cursor):
    # local list 
    # will contain all book_id in the collection of available books
    all_book_id = []
    # flag to validate user input
    flag = False
    # obtain an acceptable user ID
    requested_user = get_user(cursor)
    # format the SQL query
    available_books_request = ("SELECT book_id, book_name, book_author FROM book WHERE book_id NOT IN (SELECT book_id FROM wishlist WHERE user_id = %s)")
    # send query and the user ID to the database
    cursor.execute(available_books_request, (requested_user,))
    available_books = cursor.fetchall()
    print('\n', '--Books available for addition to the user wishlist--')
    for r in available_books:
        all_book_id.append(r[0])
        print(f"Book ID: {r[0]}", f"Book Title: {r[1].title()}", f"Author: {r[2].title()}", sep="\n")
        print('\n')
    print(all_book_id)
    while flag == False:
        requested_book = input("Select Book ID for addition to wishlist: ")
        if int(requested_book) not in all_book_id:
            print('Invalid Selection. Try Again')
        else:
            flag = True
    cursor.execute("INSERT INTO wishlist(user_id, book_id) VALUES ({}, {})".format(requested_user, requested_book))

#def add_to_wishlist(cursor, user, book):
#    cursor.execute("INSERT INTO wishlist(user_id, book_id) VALUES ({}, {})".format(user, book))

# Exit the program
def exit_program(cursor):
    print('All Hail Google!')
    whatabookdb.commit()
    whatabookdb.close()
    exit(0)

# Show a menu
def show_menu(menu):
    print('\n', 'Action Menu')
    for key, value in menu.items():
        print(f'{key}: {value.title()}')

def main(cursor):
    show_menu(main_menu)
    flag = False
    while flag == False:
        main_option = input("Please select an option: ")
        if int(main_option) < 1 or int(main_option) > 4:
            print("Invalid Option. Please Try Again")
        else:
            flag = True
    function_list[main_option](whatabookcursor)

def user(cursor):
    flag = False
    # display the user account options menu
    show_menu(user_menu)
    while flag == False:
        user_option = input('Enter an option: ')
        if int(user_option) < 5 or int(user_option) > 8:
            print("Invalid Input. Please try again")
        else: 
            flag = True
    function_list[user_option](cursor)

main_menu = {
    "1": "show books",
    "2": "show store locations",
    "3": "User Account",
    "4": "exit"
}

user_menu = {
    '5': 'show user data',
    '6': "show user wishlist",
    '7': "add book to wishlist",
    '8': "return to main menu"
}

function_list = {
    '1': show_books,
    '2': show_stores,
    '3': user,
    '4': exit_program,
    '5': display_user,
    '6': display_wishlist,
    '7': books_to_add,
    '8': main
}


if __name__ == '__main__':
    print('\n', 'Welcome to What a Book')
    while True:
        main(whatabookcursor)
