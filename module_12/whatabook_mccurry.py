""" 
    Title: mccurry_whatabook_final.py
    Author: Jules MCCurry
    Date: August 8, 2022
    Description: Final for CYBR410; WhatABook program; Console program that interfaces with a MySQL database
"""

# import statements
import sys
import mysql.connector
from mysql.connector import errorcode

#database config object 
config = {
    "user": "whatabook_user",
    "password": "MySQL8IsGreat!",
    "host": "localhost",
    "database": "whatabook_mccurry",
    "raise_on_warnings": True
}


# METHODS
def show_menu():
    print("\n  -- Main Menu --")

    print("""    
        1. View Books\n    
        2. View Store Locations\n    
        3. My Account\n    
        4. Exit Program""")

    try:
        choice = int(input('Enter an option: '))

        return choice
    except ValueError:
        print("\n  That was an incorrect option choice...\n")

        sys.exit(0)


def show_locations(_cursor):
    #query db for locations
    _cursor.execute("SELECT store_id, locale from store")

    #Get results
    locations = _cursor.fetchall()

    #results
    print("\n  -- DISPLAYING STORE LOCATIONS --")

    for location in locations:
        print("  Locale: {}\n".format(location[1]))


def show_books(_cursor):
    #query DB for books
    _cursor.execute("SELECT book_id, book_name, author, details from book")

    #get results
    books = _cursor.fetchall()

    #display results
    print("\n  -- DISPLAYING BOOK LISTING --")

    for book in books:
        print("""Book Name: {}\n  
        Author: {}\n  
        Details: {}\n""".format(book[0], book[1], book[2]))


def validate_user():
    #Validate the users ID

    try:
        user_id = int(input('\n Enter User ID: '))

        if user_id < 0 or user_id > 3:
            print("\n  That was an incorrect User ID...\n")
            sys.exit(0)

        return user_id
    except ValueError:
        print("\n  That was an incorrect User ID...\n")

        sys.exit(0)


def show_account_menu():
    # display the users account menu

    try:
        print("-- CUstomer Menu --")
        print("""1. View Wishlist \n 
        2. Add Book to Wishlist \n 
        3. Return to the Main Menu""")

        account_option = int(input('Choose an option:'))
        return account_option

    except ValueError:
        print("Invalid option")
        sys.exit(0)


def show_wishlist(_cursor, _user_id):
    #query the database for a list of books added to the users wishlist

    _cursor.execute("SELECT user.user_id, user.first_name, user.last_name, book.book_id, book.book_name, book.author " + 
                    "FROM wishlist " + 
                    "INNER JOIN user ON wishlist.user_id = user.user_id " + 
                    "INNER JOIN book ON wishlist.book_id = book.book_id " + 
                    "WHERE user.user_id = {}".format(_user_id))

    wishlist = _cursor.fetchall()

    print("\n   -- DISPLAYING WISHLIST ITEMS --")

    for book in wishlist:
        print("""Book Name: {}\n 
        Author: {}\n""".format(book[4], book[5]))


def show_books_to_add(_cursor, _user_id):
    #query the database for a list of books not in the users wishlist

    query = ("SELECT book_id, book_name, author, details "
            "FROM book "
            "WHERE book_id NOT IN (SELECT book_id FROM wishlist WHERE user_id = {})".format(_user_id))

    print(query)

    _cursor.execute(query)

    books_to_add = _cursor.fetchall()

    print("\n    -- DISPLAYING AVAILABLE BOOKS --")

    for book in books_to_add:
        print("""Book Id: {}\n 
        Book Name: {}\n""".format(book[0], book[1]))


def add_book_to_wishlist(_cursor, _user_id, _book_id):
    _cursor.execute("INSERT INTO wishlist(user_id, book_id) VALUES({}, {})".format(_user_id, _book_id))


try:
    #for handling errors w/ connecting to DB
    # connect to the WhatABook database

    db = mysql.connector.connect(**config) 
     
     #for queries
    cursor = db.cursor() # cursor for MySQL queries

    print("\n  Welcome to the WhatABook App! ")


#For the main menu
    user_selection = show_menu() 
    # show the main menu 

     # while the user's selection is not 4 - exit option
    while user_selection != 4:


        #show locations
        if user_selection == 1:
            show_locations(cursor)
            

        #Show books
        if user_selection == 2:
            show_books(cursor)


        # go to user menu
        #validate ID
        #show account menu
        if user_selection == 3:
            my_user_id = validate_user()
            account_option = show_account_menu()

            # while account option does not equal 3 - exit option
            while account_option != 3:

                # show wishlist
                if account_option == 1:
                    show_wishlist(cursor, my_user_id)

                # SHow books not in the users wishlist
                if account_option == 2:

                    # show the books not currently configured in the users wishlist
                    show_books_to_add(cursor, my_user_id)

                    # get the entered book_id 
                    book_id = int(input("\n    Enter the id of the book you want to add: "))
                    
                    # add the selected book the users wishlist
                    add_book_to_wishlist(cursor, my_user_id, book_id)

                    # commit the changes
                    db.commit() 

                    print("\n    Book id: {} was added to your wishlist!".format(book_id))

                # if the selected option is less than 0 or greater than 3, display an invalid user selection 
                if account_option < 0 or account_option > 3:
                    print("\n    That was an invalid option...")

                # show the account menu 
                account_option = show_account_menu()
        

        # if the user selection is less than 0 or greater than 4, display an invalid user selection
        if user_selection < 0 or user_selection > 4:
            print("\n   That was not a valid ID...")
            
        # show the main menu
        user_selection = show_menu()

    print("\n  THat was not an option...")


except mysql.connector.Error as err:
    # handle errors

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("One of the supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("database does not exist")

    else:
        print(err)


#finally:
    # close the connection to MySQL
     #db.close()