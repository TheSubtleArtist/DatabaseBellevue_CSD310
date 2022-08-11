# Jennifer Adams
# WhatABook Assignment
# August 8, 2022
#
# Objective: Create a console application for a company called WhatABook.
# The application must allow users to see books in stock, view store hours and
# locations, and add books to their wishlist. 

# Import statements
import sys
import mysql.connector
from mysql.connector import errorcode

# Configuration information
config = {
    "user": "whatabook_user",
    "password": "MySQL8IsGreat!",
    "host": "127.0.0.1",
    "database": "whatabook_adams",
    "raise_on_warnings": True
}

# Method for showing the main menu of the application
def show_menu():

    # Menu Title
    print(' ----------------------')
    print('|  WhatABook Main Menu |')
    print(' ----------------------')
    
    # Menu Options
    print('   1. View Books\n   2. View Store Locations & Hours\n   3. User Account\n   0. Exit Application')

    #try/catch block to notify users of invalid selections
    try:
        main_menu_selection = int(input('      Enter the number for the option you wish to select: '))
               
        return main_menu_selection

    except ValueError:
        print('\n      Invalid option. Please enter a valid option.')

        # if a ValueError is thrown, return to the main menu
        show_menu()

# Method for showing users a list of books belonging to WhatABook
def show_books(_cursor):

    # Cursor object inputs query  
    _cursor.execute('SELECT book_name, details, author FROM Book')

    # Return result from cursor object 
    books = _cursor.fetchall()

    # Introduce the View Books option
    print('\n        ------------------------------------------')
    print('       |  Here are the Titles We Currently Offer  |')
    print('        ------------------------------------------\n')

    # Return data from Book table for each book 
    for book in books:
        print('        Title: {}\n        Details: {}\n        Author: {}\n'.format(book[0], book[1], book[2]))

# Method for showing users a list of locations and hours of operation for WhatABook        
def show_locations(_cursor):

    _cursor.execute('SELECT store_id, locale, hours FROM Store')

    # Introduce the Store Locations & Hours option
    print('\n        ---------------------------')
    print('       |  Store Locations & Hours  |')
    print('        ---------------------------\n')

    # Return result from cursor
    stores = _cursor.fetchall()

    # Return data from Store table for each book
    for store in stores:
        print('        Store Number: {}\n        Location: {}\n        Store Hours: {}'.format(store[0], store[1], store[2]))

# Method for accepting and validating User ID input
def validate_user():
    
    # try/catch block to notify of incorrect inputs and exits application
    try:
        user_id = int(input('\n      Enter your User ID: '))

        if user_id < 1 or user_id > 3:
            print('\n      Invalid User ID. Exiting application.\n')
            
            sys.exit(0)

        return user_id
    except ValueError:
        print('\n  Invalid User ID. Please enter a valid User ID.\n')

        sys.exit(0)

# Method for displaying the user account menu to users        
def show_account_menu():

    # try/catch block to identify incorrect input and return users to the account menu to try again
    try:
        print('\n        -----------------------')
        print('       |  User Account Portal  |')
        print('        -----------------------')
        print('        1. View Wishlist\n        2. Add Book\n        0. Return to Main Menu')
        user_option = int(input('           Enter the number for the option you wish to select: '))

        return user_option
    except ValueError:
        print('\n           Invalid option. Exiting application.')

        sys.exit(0)

# Method using multiple INNER JOIN functions to show users their current wishlist entries        
def show_wishlist(_cursor, _user_id):
    _cursor.execute("SELECT user.user_id, user.first_name, user.last_name, book.book_id, book.book_name, book.details, book.author " + 
                    "FROM wishlist " + 
                    "INNER JOIN user ON wishlist.user_id = user.user_id " + 
                    "INNER JOIN book ON wishlist.book_id = book.book_id " + 
                    "WHERE user.user_id = {}".format(_user_id))
    
    # Returns INNER JOIN result
    user_wishlist = _cursor.fetchall()

    print('\n                 ------------')
    print('                |  Wishlist  |')
    print('                 ------------')
    
    # Displays data for every book in the user's wishlist
    for book in user_wishlist:
        print('\n                Book Title: {}\n                Book Details: {}\n                Book Author: {}'.format(book[4], book[5], book[6]))

# Method to determine which books are already on a users wishlist and return only those that are not on the wishlist for user selection        
def show_books_to_add(_cursor, _user_id):

    # Query asks for all entries in Book that are not already in Wishlist for that User
    identify_new_books = ('SELECT book_id, book_name, details, author FROM Book WHERE book_id NOT IN (SELECT book_id FROM wishlist WHERE user_id = {})'.format(_user_id)) 
    print('\n                --------------------')
    print('               |  New Books to Add  |')
    print('                --------------------')
    _cursor.execute(identify_new_books)
    add_new_books = _cursor.fetchall()

    # Display data for every book that isn't already on the user wishlist
    for book in add_new_books:
        print('\n                Book ID: {}\n                Book Title: {}\n                Book Details: {}\n                Book Author: {}'.format(book[0], book[1], book[2], book[3]))
    
# Method to INSERT a book_id provided by user input into the user's wishlist
def add_book_to_wishlist(_cursor, _user_id, _book_id):

    _cursor.execute('INSERT INTO Wishlist(user_id, book_id) VALUES({}, {})'.format(_user_id, _book_id))

# Try/catch block for potential connection errors 
try:
    db = mysql.connector.connect(**config)
    
    # Introduce the application to the user upon startup
    print('\n -------------------------------------------------')
    print('|  Welcome to the WhatABook Console Application!  |')
    print(' -------------------------------------------------')
   
    # Create a value for MySQL cursor function
    cursor = db.cursor()

    # Call the show_menu() method to present users with a main menu
    user_input = show_menu()

    # If the user has not entered 0 to exit. . .
    while user_input != 0:

        # Call the show_books method to provide users with the list of available books
        if user_input == 1:
            show_books(cursor)

        # Call the show_locations method to provide users with store hours and locations
        if user_input == 2:
            show_locations(cursor)
            print('\n')

        # Call both the validate_user and show_account_menu method to prompt users for a User ID and present them with a user console
        if user_input == 3:

            user_login = validate_user()
            load_user_console = show_account_menu()

            # If the user has not chosen to return to the main menu. . .
            while load_user_console != 0:

                # Call the show_wishlist method to provide users with their wishlist
                if load_user_console == 1:
                    show_wishlist(cursor, user_login)

                # Call the show_books_to_add method to provide users with books that are not on their wishlist. . .
                if load_user_console == 2:
                    show_books_to_add(cursor, user_login)

                    book_id = int(input('\n\n                Enter the Book ID for the book you wish to add: '))

                    if book_id < 1 or book_id > 9:
                        print ('                Invalid Book ID. Exiting application.')
                        sys.exit(0)

                    # Call the add_book_to_wishlist method    
                    add_book_to_wishlist(cursor, user_login, book_id)
                    
                    # And add the user's selection to their wishlist
                    db.commit()

                    print('\n                Book ID {} was added to your wishlist!'.format(book_id))
                
                # If a user responds with an int that isn't listed. . .
                if load_user_console < 0 or load_user_console > 2:
                    print('\n        Invalid menu selection. Please select a valid menu selection.\n')
                
                # Return them to the user console
                load_user_console = show_account_menu() 

        # If a user responds with an int that isn't listed. . .
        if user_input < 0 or user_input > 3:
                print('\n  Invalid menu selection. Please select a valid menu selection.\n')
        # Return them to the main menu
        user_input = show_menu()

    # Notifies users of application close.
    print('\n\nNow exiting. Thank you for using the WhatABook Application!')    


except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid")
    
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print ("The specified database does not exist")
    
    else:
        print(err)

finally:
    db.close()