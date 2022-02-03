import mariadb as db
import dbcreds as c
import traceback as t

# connect to database function
def connect_db():
    conn = None
    cursor = None
    try:
        conn = db.connect(user=c.user,
                          password=c.password,
                          host=c.host,
                          port=c.port,
                          database=c.database)
        cursor = conn.cursor()
    except db.OperationalError:
        print("something went wrong with the DB, please try again in 5 minutes")
    except Exception as e:
        print(e)
        print("Something went wrong!")
    return conn, cursor  

# disconnect from database function
def disconnect_db(conn, cursor):
    try:
        cursor.close()
    except Exception as e:
        print(e)
        print('cursor close error: what happened?')

    try:
        conn.close()
    except Exception as e:
        print(e)
        print('connection close error')

# function to attempt login 
def attempt_login(username, password):
    hacker = None
    conn, cursor = connect_db()

    try:
        # select statement to see if alias and password match, returning the hackers_id to be used later
        cursor.execute("select id from hackers where alias=? and password=?", [username, password])
        hacker = cursor.fetchone()
    except db.OperationalError:
        print("something went wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB Query, please file bug report")
    except:
        print("Something went wrong!")

    disconnect_db(conn, cursor)

    # to return True and hacker_id to be used in future functions
    if hacker == None:
        return False
    else:
        return True, hacker

def submit_exploits(hacker):
    # post welcome message
    print('---------------------------------')
    print("-------- submission page --------")
    print('---------------------------------')
    # exploits submission prompt
    content = input('Enter your submission: ')
    conn, cursor = connect_db()

    try:
        # insert statement to submit exploit content and hackers_id
        cursor.execute("insert into exploits (content, hackers_id) values(?,?)", [content, hacker])
        conn.commit()
    except db.OperationalError:
        print("something went wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB Query, please file bug report")
    except:
        print("Something went wrong!")

    disconnect_db(conn, cursor)

def view_users_exploits(hacker):
    # post welcome message
    print('---------------------------------')
    print('- This is what you have posted! -')
    print('---------------------------------')

    exploits = None
    conn, cursor = connect_db()

    try:
        # select statement to view all exploits submitted by the user
        cursor.execute("select e.content, h.alias from exploits e inner join hackers h on h.id = e.hackers_id where e.hackers_id = ?", [hacker,])
        exploits = cursor.fetchall()
    except db.OperationalError:
        print("something went wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB Query, please file bug report")
    except:
        print("Something went wrong!")

    disconnect_db(conn, cursor)

    # loop to print exploits
    for exploit in exploits:
        print('')
        print("post: ", exploit[0])
        print("author: ", exploit[1])
        print('')

def view_other_expoits(hacker):
    # post welcome message
    print('---------------------------------')
    print('-This is what others have posted-')
    print('---------------------------------')
    exploits = None
    conn, cursor = connect_db()

    try:
        # select statement to view all exploits not submitted by the user
        cursor.execute("select e.content, h.alias from exploits e inner join hackers h on h.id = e.hackers_id where e.hackers_id != ?", [hacker,])
        exploits = cursor.fetchall()
    except db.OperationalError:
        print("something went wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB Query, please file bug report")
    except:
        print("Something went wrong!")

    disconnect_db(conn, cursor)

    # loop to print exploits
    for exploit in exploits:
        print('')
        print("post: ", exploit[0])
        print("author: ", exploit[1])
        print('')
