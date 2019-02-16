import os
import sys
import sqlite3 as lite


def create_database():
    # check if the BUW_items.db file exists; if not create it
    file_path_abs = os.path.abspath(str(sys.argv[0]))
    file_path_dir = os.path.dirname(file_path_abs)
    dir_gathered_data = os.path.join(file_path_dir, "gathered_data/")

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

if __name__ == "__main__":
    create_database()
