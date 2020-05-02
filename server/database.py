#!/usr/bin/python
import sqlite3

class database:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.connect()

    def close(self):
        """ Close database connection """
        # Close communication with the sqlite3 database
        self.cur.close()
        self.conn.close()

    def connect(self):
        """ Connect to the sqlite3 database server """

        # connect to the sqlite3 server
        print('Connecting to the sqlite3 database...')
        self.conn = sqlite3.connect('database.db')
        self.cur = self.conn.cursor()


    def create_table(self):
        """ create table in the sqlite3 database"""
        query = """CREATE TABLE products (
                       name varchar(100),
                       category varchar(100)
                   )"""

        print('Creating table "products"...')
        self.cur.execute(query)

    def insert(self, name, category):
        """ insert a new product into the products table """
        query = """INSERT INTO products (name, category)
                     VALUES (?, ?);"""
        try:
            #execute the INSERT statement
            self.cur.execute(query, (name, category))
            # get the generated id back
            id = self.cur.lastrowid
            # commit the changes to the database
            self.conn.commit()
            response = {'result': 'ok', 'id': id}

        except sqlite3.DatabaseError as error:
            response = {'result': 'error', 'error_message': '{}'.format(error)}
        return response


    def update(self, id, name, category):
        """ update product name and category based on the product id """
        query = """UPDATE products
                        SET name = ?, category = ?
                        WHERE rowid = ?"""
        try:
            # execute the UPDATE  statement
            self.cur.execute(query, (name, category, id))
            # commit the changes to the database
            self.conn.commit()
            response = {'result': 'ok'}
        except sqlite3.DatabaseError as error:
            response = {'result': 'error', 'error_message': '{}'.format(error)}
        return response

    def delete(self, id):
        """ delete product by product id """
        query = "DELETE FROM products WHERE rowid = ?"
        try:
            # execute the DELETE  statement
            self.cur.execute(query, (id, ))
            # commit the changes to the database
            self.conn.commit()
            response = {'result': 'ok'}
        except sqlite3.DatabaseError as error:
            response = {'result': 'error', 'error_message': '{}'.format(error)}
        return response

    def get_by_id(self, id):
        """ get product name and category based on the product id """
        query = """SELECT rowid, name, category FROM products WHERE rowid = ?"""
        try:
            # execute the SELECT  statement
            self.cur.execute(query, (id, ))
            # commit the changes to the database
            row = self.cur.fetchone()
            response = {'result': 'ok', 'product':row}
        except sqlite3.DatabaseError as error:\
            response = {'result': 'error', 'error_message': '{}'.format(error)}
        return response

    def get_all(self):
        """ get all products from the products table"""
        query = """SELECT rowid, name, category FROM products;"""
        try:
            products = []
            # execute the SELECT statement
            self.cur.execute(query)
            for row in self.cur:
                products.append(row)
            response = {'result': 'ok', 'products': products}
        except sqlite3.DatabaseError as error:
            response = {'result': 'error', 'error_message': '{}'.format(error)}
        return response