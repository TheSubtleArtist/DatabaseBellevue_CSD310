-- create new database 'whatabook'
CREATE DATABASE whatabook;

-- create whatabook_user and grant them all privileges to the pysports database 
CREATE USER 'whatabook_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'MySQL8IsGreat!';

-- grant all privileges to the pysports database to user pysports_user on localhost 
GRANT ALL PRIVILEGES ON whatabook.* TO'pysports_user'@'localhost';

-- create the store table 
CREATE TABLE store (
    store_id     INT             NOT NULL        AUTO_INCREMENT,
    locale	     VARCHAR(500)    NOT NULL,
    PRIMARY KEY(store_id)
); 
-- create the user table 
CREATE TABLE user_table (
    user_id     INT             NOT NULL        AUTO_INCREMENT,
    first_name   VARCHAR(75)     NOT NULL,
    last_name    VARCHAR(75)     NOT NULL,
    PRIMARY KEY(user_id)
); 

-- create the book table 
CREATE TABLE book (
    book_id     INT             NOT NULL        AUTO_INCREMENT,
    book_name   VARCHAR(200)    NOT NULL,
    book_author VARCHAR(200)    NOT NULL,
    book_detail VARCHAR(500),
    PRIMARY KEY(book_id)
); 

-- create the wishlist table and set the foreign keys
CREATE TABLE wishlist (
    wishlist_id   INT     NOT NULL        AUTO_INCREMENT,
    user_id		  INT     NOT NULL,
    book_id		  INT 	  NOT NULL,
    PRIMARY KEY(wishlist_id),
    CONSTRAINT fk_user 
    FOREIGN KEY(user_id)
        REFERENCES user_table(user_id),
	CONSTRAINT fk_book 
    FOREIGN KEY(book_id)
        REFERENCES book(book_id)
);

-- insert store
INSERT INTO store(locale) values('1776 Mesa Ave, Colorado Springs, CO 80906');

-- insert users
INSERT INTO user_table (first_name, last_name) VALUES
	('jubal', 'harshaw'),
    ('michael', 'smith'),
    ('dawn', 'ardent');
    
INSERT INTO book (book_author, book_name, book_detail) VALUES
	('robert a. heinlein', 'stranger in a string land', 'if you grok it, they will come'),
    ('robert a. heinlein', 'starship troopers', 'service guarantees citizenship'),
    ('robert a. heinlein', 'the moon is a harsh mistress', 'insurrection a-z'),
    ('robert a. heinlein', 'time enough for love', 'earn it to earn it'),
    ('robert a. heinlein', 'job: a comedy of justice', 'never meet your heros or your enemies'),
    ('robert a. heinlein', 'to sail beyond the sunset', 'let me try this again'),
    ('robert a. heinlein', 'i will fear no evil', 'thank you, eunice'),
    ('robert a. heinlein', 'the man who sold the moon ', 'there really is a sucker born every minute'),
    ('robert a. heinlein', 'methusala\'s children', 'it already happened tomorrow');
    
    -- determine primary key values assigned to users and books
    select * from user_table;
    select* from book;
    
-- create wishlist
INSERT INTO wishlist (user_id, book_id) VALUES
	(1, 1),
    (2, 2),
    (3, 3),
    (1, 4),
    (2, 5),
    (3, 6);


    
    


