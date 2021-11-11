import re
import sqlite3
import sys
from os.path import exists
import subprocess
from datetime import date

# corrigir select , ASC
class Database:

    conn = None

    def __init__(self):

        self.conn = self.db_connection()

    def db_start(self):

        cursor = sqlite3.connect("accb.sqlite").cursor()
        sql_file = open("schema.sql")
        sql_as_string = sql_file.read()
        cursor.executescript(sql_as_string)
        # subprocess.check_call(["attrib", "+H", "accb.sqlite"])

    def db_connection(self):

        conn = None
        if exists("accb.sqlite"):
            conn = sqlite3.connect("accb.sqlite")
            conn.execute("PRAGMA foreign_keys = ON")
        else:
            self.db_start()
            conn = sqlite3.connect("accb.sqlite")
            conn.execute("PRAGMA foreign_keys = ON")
            self.db_update_city(
                {"city_name": "Ilhéus", "primary_key": "IlhÃ©us"})

        return conn

    def db_save_city(self, name):

        self.conn = self.db_connection()
        cursor = self.conn.cursor()

        sql_query = """INSERT INTO city(city_name) VALUES(?)"""
        cursor = cursor.execute(sql_query, (name))
        self.conn.commit()
        self.db_end_conn()

    def db_save_product(self, product):

        self.conn = self.db_connection()
        cursor = self.conn.cursor()

        sql_query = """INSERT INTO product(product_name, keywords) VALUES(?,?)"""
        cursor = cursor.execute(
            sql_query, (product['product_name'], product['keywords']))
        self.conn.commit()
        self.db_end_conn()

    def db_save_search(self, done):

        self.conn = self.db_connection()
        cursor = self.conn.cursor()

        sql_query = """INSERT INTO search(done, search_date) VALUES(?,?)"""
        cursor = cursor.execute(sql_query, (done, str(date.today()), ))
        self.conn.commit()
        self.db_end_conn()

        return cursor.lastrowid

    def db_save_estab(self, estab):

        self.conn = self.db_connection()
        cursor = self.conn.cursor()
        sql_query = """INSERT INTO estab(city_name, estab_name, adress, web_name) VALUES(?,?,?,?)"""
        cursor = cursor.execute(
            sql_query, (estab["city_name"], estab["estab_name"], estab["adress"], estab["web_name"]))
        self.conn.commit()
        self.db_end_conn()

    def db_save_backup(self, backup):

        self.conn = self.db_connection()
        cursor = self.conn.cursor()

        sql_query = """INSERT INTO backup(active, city, done, estab_info,product_info, search_id ) VALUES(?,?,?,?,?,?)"""
        cursor = cursor.execute(
            sql_query, (backup["active"], backup["city"], backup["done"], backup["estab_info"], backup["product_info"], backup["search_id"]))
        self.conn.commit()
        self.db_end_conn()

    def db_save_search_item(self, search_item):

        self.conn = self.db_connection()
        cursor = self.conn.cursor()

        sql_query = """INSERT INTO search_item(search_id, city_name, product_name, web_name,adress, price) VALUES(?,?,?,?,?,?)"""
        cursor = cursor.execute(
            sql_query, (search_item["search_id"], search_item["city_name"], search_item["product_name"], search_item["web_name"], search_item["adress"], search_item["price"]))
        self.conn.commit()
        self.db_end_conn()

    def db_save_city(self, city):

        self.conn = self.db_connection()
        cursor = self.conn.cursor()
        sql_query = """INSERT INTO city(city_name) VALUES(?)"""
        cursor = cursor.execute(sql_query, (city,))
        self.conn.commit()
        self.db_end_conn()

    # query
    def db_delete(self, table, where, value):

        self.conn = self.db_connection()
        cursor = self.conn.cursor()
        sql_query = """DELETE FROM {} WHERE {} = "{}" """.format(
            table, where, value)
        cursor = cursor.execute(sql_query)
        self.conn.commit()
        self.db_end_conn()

    def db_get_city(self):

        self.conn = self.db_connection()
        cursor = self.conn.cursor()
        cursor = self.conn.execute("SELECT * FROM city ORDER BY city_name ASC")
        cities = cursor.fetchall()
        self.db_end_conn()

        return cities

    # query
    def db_get_search(self, where=None, value=None):

        self.conn = self.db_connection()
        cursor = self.conn.cursor()
        if value != None:
            cursor = self.conn.execute(
                "SELECT * FROM search WHERE {} = '{}' ORDER BY id ASC".format(where, value))
            search = cursor.fetchall()
        else:
            cursor = self.conn.execute("SELECT * FROM search ORDER BY id ASC")
            search = cursor.fetchall()
        self.db_end_conn()

        return search

    # query
    def db_get_search_item(self, search_id=None):

        self.conn = self.db_connection()
        cursor = self.conn.cursor()
        if search_id != None:
            cursor = self.conn.execute(
                "SELECT * FROM search_item WHERE search_id = '{}' ORDER BY search_id ASC".format(search_id))
            search_item = cursor.fetchall()
        else:
            cursor = self.conn.execute(
                "SELECT * FROM search_item ORDER BY search_id ASC")
            search_item = cursor.fetchall()
        self.db_end_conn()

        return search_item

    # query
    def db_get_backup(self, id=None):

        self.conn = self.db_connection()
        cursor = self.conn.cursor()
        if id != None:
            cursor = self.conn.execute(
                "SELECT * FROM backup WHERE search_id = '{}'".format(id))
            backup = cursor.fetchall()
        else:
            cursor = self.conn.execute("SELECT * FROM backup")
            backup = cursor.fetchall()
        self.db_end_conn()

        return backup

    def db_get_product(self):

        self.conn = self.db_connection()
        cursor = self.conn.cursor()
        cursor = self.conn.execute(
            "SELECT * FROM product ORDER BY product_name ASC")
        products = cursor.fetchall()
        self.db_end_conn()

        return products

    def db_get_estab(self):

        self.conn = self.db_connection()
        cursor = self.conn.cursor()
        cursor = self.conn.execute("SELECT * FROM estab")
        estabs = cursor.fetchall()
        self.db_end_conn()

        return estabs

    def db_update_estab(self, estab):

        self.conn = self.db_connection()
        cursor = self.conn.cursor()
        sql_query = """UPDATE estab SET city_name="{}", estab_name="{}", adress="{}", web_name="{}" WHERE estab_name = "{}" """.format(
            estab["city_name"], estab["estab_name"], estab["adress"], estab["web_name"], estab["primary_key"])
        cursor = cursor.execute(sql_query)
        self.conn.commit()
        self.db_end_conn()

    def db_update_product(self, product):

        self.conn = self.db_connection()
        cursor = self.conn.cursor()
        sql_query = """UPDATE product SET product_name="{}", keywords="{}" WHERE product_name = "{}" """.format(
            product['product_name'], product['keywords'], product['primary_key'])
        cursor = cursor.execute(sql_query)
        self.conn.commit()
        self.db_end_conn()

    def db_update_city(self, city):

        self.conn = self.db_connection()
        cursor = self.conn.cursor()
        sql_query = """UPDATE city SET city_name="{}" WHERE city_name = "{}" """.format(
            city['city_name'], city['primary_key'])
        cursor = cursor.execute(sql_query)
        self.conn.commit()
        self.db_end_conn()

    # query
    def db_update_search(self, search):

        self.conn = self.db_connection()
        cursor = self.conn.cursor()
        sql_query = """UPDATE search SET done="{}" WHERE id = "{}" """.format(
            search['done'], search['id'])
        cursor = cursor.execute(sql_query)
        self.conn.commit()
        self.db_end_conn()

    def db_run_query(self, query):

        self.conn = self.db_connection()
        cursor = self.conn.cursor()
        cursor = cursor.execute(query)
        values = cursor.fetchall()
        self.conn.commit()
        self.db_end_conn()

        return values

    def db_end_conn(self):

        if self.conn:
            self.conn.close()


# db = Database()
