import mariadb as db
import dbcreds as c
import traceback as t

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

def attempt_login(username, password):
    hacker = None
    conn, cursor = connect_db()

    try:
        cursor.execute("select id from hackers where alias=? and password=?", [username, password])
        hacker = cursor.fetchone()
    except db.OperationalError:
        print("something went wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB Query, please file bug report")
    except:
        print("Something went wrong!")

    disconnect_db(conn, cursor)

    if hacker == None:
        return False, hacker
    else:
        return True, hacker

def submit_exploits(hacker):
    # exploits submission prompt
    content = input('Enter your submission: ')
    conn, cursor = connect_db()

    cursor.execute("insert into exploits (content, hackers_id) values(?,?)", [content, hacker])
    conn.commit()

    disconnect_db(conn, cursor)

def view_users_exploits(hacker):
    # post welcome message
    print('---------------------------------')
    print('- This is what you have posted! -')
    print('---------------------------------')

    exploits = None
    conn, cursor = connect_db()

    cursor.execute("select e.content, h.alias from exploits e inner join hackers h on h.id = e.hackers_id where e.hackers_id = ?", [hacker,])
    exploits = cursor.fetchall()

    disconnect_db(conn, cursor)

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

    cursor.execute("select e.content, h.alias from exploits e inner join hackers h on h.id = e.hackers_id where e.hackers_id != ?", [hacker,])
    exploits = cursor.fetchall()

    disconnect_db(conn, cursor)

    for exploit in exploits:
        print('')
        print("post: ", exploit[0])
        print("author: ", exploit[1])
        print('')
