import os
import sys
import sqlite3 as lite

# following variables are used by different functions
file_path_abs = os.path.abspath(str(sys.argv[0]))
file_path_dir = os.path.dirname(file_path_abs)
dir_gathered_data = os.path.join(file_path_dir, "gathered_data/")

def create_database():
    # check if the BUW_items.db file exists; if not create it
    if os.path.exists(os.path.join(dir_gathered_data, 'BUW_items.db')):
        print("Database already exists.")
    else:
        try:
            os.chdir(dir_gathered_data)
        except FileNotFoundError:
            os.mkdir(dir_gathered_data)
            os.chdir(dir_gathered_data)

        open("BUW_items.db", "w").close() # create file

        print("Database file has been created")

def establish_connection_db():
    con = None
    try:
        con = lite.connect('BUW_items.db')

        cur = con.cursor() #used to move inside the db
        cur.execute('SELECT SQLITE_VERSION()')

        data = cur.fetchone() #gets the first row

        print("SQLite version : {}".format(data))
        return con

    except lite.Error as e:
        print("Error {}:".format(e.args[0]))
        sys.exit(1)

def create_table(con, table_name='items'):
    cursor = con.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS {} (
                        id INTEGER PRIMARY KEY,
                        date TEXT,
                        name TEXT,
                        type TEXT);""".format(table_name))
    con.commit() #commit must be executed on a database object

def list_tables(con):
    cursor = con.cursor()
    cursor.execute("""select name from sqlite_master where type = 'table';
    """)
    existing_tables_tmp = cursor.fetchall() #returns a list of names of existing tables
    return (item[0] for item in existing_tables_tmp)


def insert_into_table(con, row, table_name='items'):
    # check if the table exists
    cursor = con.cursor()
    for name in list_tables(con=con):
        if table_name == name:
            break
    else:
        # no such table; create it
        create_table(con=con, table_name=table_name)

    # insert contents into the table
    # assumption: the row argument is a list [date, name, type]
    date, name, type = row
    print(date + " " + name + " " + type)
    sql_code = """INSERT INTO {}(date, name, type)
                    VALUES('{}', '{}', '{}')
    """.format(table_name, date, name, type)
    print(sql_code)
    cursor.execute(sql_code)
    con.commit()
    print(cursor.lastrowid)
    return cursor.lastrowid

def delete_rows(con, table_name='items'):
    cursor = con.cursor()
    sql_code = """DELETE FROM {};
    """.format(table_name)
    print(sql_code)
    cursor.execute(sql_code)
    con.commit()
    print(cursor.lastrowid)

def select_all(con, table_name='items'):
    cursor = con.cursor()
    sql_code = """SELECT * from {};""".format(table_name)
    print(sql_code)
    cursor.execute(sql_code)
    con.commit()
    print(cursor.lastrowid)

def terminate_connection(con):
    # terminates connection with db
    con.close()

def accept_row(row):
    #this function is exposed in other .py files
    create_database()
    create_table(establish_connection_db())
    insert_into_table(establish_connection_db(), row)
    print("Row has been successfully entered into the database.")
    terminate_connection(establish_connection_db())

if __name__ == "__main__":
    create_database()
    create_table(establish_connection_db())
    # insert_into_table(establish_connection_db(), ['dzisiaj', 'klucz1', 'inne'])
    # select_all(establish_connection_db())
    delete_rows(establish_connection_db())
    # select_all(establish_connection_db())
