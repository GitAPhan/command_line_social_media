import dbinteractions as db
from getpass import getpass
import traceback as t

# welcome message
print("---------------------------")
print("Welcome to CLI Social Media")
print("---------------------------")

# loop containing login functionality
while True:
    hacker = None
    try:
        # login prompt
        print("------- Login  Page -------")
        username = input("Enter your username: ")
        password = getpass('Enter you password: ')

        # store login_status and hacker_id returned from function
        login_status, hacker = db.attempt_login(username, password)

        # login attempt
        if login_status:
            print('login successful')
            print('Welcome ', username)
            break
        else:
            print('looks like there was an issue with the credentials you have entered')
            print('Please try again!')
    except Exception as e:
        print(e)
        t.print_exc()

# user select options
options = {
    '1': db.submit_exploits,
    '2': db.view_users_exploits,
    '3': db.view_other_expoits,
    '4': exit
}

while True:
    try:
        # propt user to select action
        print('Please select from the following')
        print('press 1: submit an expoit')
        print('press 2: view your submitted exploits')
        print('press 3: view exploits submitted by others')
        print('press 4: exit program')
        selection = input("Please make your selection: ")

        # conditional to add in arguement only if option 4 isnt selected
        if selection == '4':
            print('-------------- Goodbye!! --------------')
            print('Thank you for visiting CLI Social Media')
            print('-------------- Goodbye!! --------------')
            options[selection]()
        else:
            options[selection](hacker[0])
    except KeyError:
        print('---------- Error Message -----------')
        print('The selection you made seems invalid')
        print('-------- Please try again! ---------')