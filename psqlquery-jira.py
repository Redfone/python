#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python_version  :2.7.6  
#=======================================================================
# MAKE SURE YOUR LOCAL .pgpass IS UP-TO-DATE WITH LOGIN CREDS FOR DBs
# CREATE YOUR JIRA API KEY IN THE JIRA WEBSITE.
#=======================================================================
from __future__ import print_function
from jira import JIRA
import sys, os
import psycopg2
import time

__author__ = 'markwarr'

# Main definition - constants
menu_actions  = {}  

# =======================
#     MENUS FUNCTIONS
# =======================

# 1.) Main menu. Select target DB for query 
def main_menu():
    global choice
    os.system('clear')
    
    print ("===================================================")
    print (" PostgreSQL DB QUERY TOOL")
    print (" Choose the DB where you wish to execute the query ")
    print ("===================================================")
    print ("1. DATABASE ONE")
    print ("2. DATABASE TWO")
    print ("3. DATABASE THREE")
    print ("9. GO BACK IN MENU")
    print ("\n0. Quit")
    choice = raw_input(" >>  ")
    exec_menu(choice)
    
    return

# 2.) Enter JIRA Ticket Info 
def exec_menu_filename():
    global FILE
    print ("===================================================")
    print (" ENTER THE NAME OF JIRA TICKET                ")
    print (" EX. DB-763                                   ")
    print ("===================================================")
    FILE = raw_input(" >> ")
    jira_connect()
    
    return
    

# Execute menu
def exec_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print ("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return

# Back to main menu
def back():
    menu_actions['main_menu']()

# Exit program
def exit():
    sys.exit()

# =======================
#   JIRA CONNECT STUFF
# =======================
def jira_connect():
    user = 'your.name@yourdomain.com'
    apikey = 'yourapikeygoeshere'
    server = 'https://yourdomain.jira.com'
    options = {
     'server': server
    }

    jira = JIRA(options, basic_auth=(user,apikey) )
    ticket = FILE
    issue = jira.issue(ticket, expand="attachment")
    summary = issue.fields.summary

# We query the ticket, print the attachment contents 
# to a file named the same as ex. 'DB-763' and then use that
# same 'ticket' variable when calling our db_connect below.
    for attachment in issue.fields.attachment:
        print("Name: '{filename}', size: {size}".format(
            filename=attachment.filename, size=attachment.size))
        # to read content use `get` method:
        sql_file = open((FILE), 'w')
        print(format(attachment.get()), file=(sql_file))
        sql_file.close()
        db_connect()
        

# =======================
#     DB VAR FUNCTIONS   
# =======================

# 1. DATABASE ONE
def database_one ():
    global DB, USER, DBHOST
    DBHOST = "database_one.com"
    DB = "manager"
    USER = "manager"
    exec_menu_filename()

# 2. DATABASE TWO
def database_two ():
    global DB, USER, DBHOST 
    DBHOST = "database_two.com"
    DB = "db_one"
    USER = "db_one"
    exec_menu_filename()

# 3. PROD LEADFORM
def database_three ():
    global DB, USER, DBHOST
    DBHOST = "dbthree.com"
    DB = "test"
    USER = "test"
    exec_menu_filename()

# 3. Test Function
def test_connect():
    print("TEST PRUEBA")
    
# =======================
#     DB QUERY FUNCTION
# =======================
def db_connect():
    
    conn = None
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(database= (DB), user = (USER), host = (DBHOST))
        # create a cursor
        cur = conn.cursor()

        print('PostgreSQL query output:')
        sql_file = open((FILE), 'r')
        cur.execute(sql_file.read())
        # Example running query directly with cur.execute;
        #cur.execute("UPDATE configuration set value='abcdefghijk12345' where key='SomeKey';")
        conn.commit()
        print('Total number of rows updated'),cur.rowcount

        # Display the PostgreSQL database output from above query
        db_output = cur.fetchall()
        print(db_output)

        # Close the connection with PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
            print('Query complete')
            time.sleep(3)
            main_menu()

# =======================
#    MENUS DEFINITIONS
# =======================
menu_actions = {
    'main_menu': main_menu,
    '1': database_one,
    '2': database_two,
    '3': database_three,
    '9': back,
    '10': test_connect,
    '0': exit,
}

# =======================
#      MAIN PROGRAM
# =======================

# Main Program
if __name__ == "__main__":
    # Launch main menu
    main_menu()
