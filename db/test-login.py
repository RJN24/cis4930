# This program will test the functions used in the db.py file
# Enter y when asked to wipe the db to clear useless test data
# Leave data in db if you want data to persist between tests

import db

dbfile = "users.db"
db.createDbConnection(dbfile)
db.createTable()

exit = 0

print("Welcome to the db login test")
print("Enter 'exit' at any time to exit the test.\n")
while(exit == 0):
	check_login = input("Do you have an account (y/n)?: ")
	if check_login == "y" or check_login == "Y":
		user = input("username: ")
		if user == "exit":
			exit = 1
			break
		pw = input("password: ")
		if pw == "exit":
			exit = 1
			break
		if db.verifyLogin(user, pw):
			print("Successfully logged in. Welcome, {}!".format(user))
			break
		else:
			print("Invalid username or password\n")


	elif check_login == "n" or check_login == "N":
		print("Let's create an account then.")
		setUID = input("Enter a username: ")
		if setUID == "exit":
			exit = 1
			break
		setPW = input("Enter a password: ")
		if setPW == "exit":
			exit = 1
			break
		while db.insertUser(setUID, setPW) == False:
			print("Username taken, please choose a different username")
			setUID = input("Enter a username: ")
			if setUID == "exit":
				exit = 1
				break
			setPW = input("Enter a password: ")
			if setPW == "exit":
				exit = 1
				break
			db.insertUser(setUID, setPW)
		print("Account created, try loggin in!\n")


	elif check_login == "exit":
		exit = 1
		break

	else:
		print("Invalid input. Please enter y, n, or exit.\n")

print("\nNow the test for updating user scores")
print("Enter 'exit' at any time to exit")
exit = 0
while exit == 0:
	user = input("\nEnter user to update score for: ")
	if user == "exit":
		exit = 1
		break
	
	if db.findUser(user):
		level = input("Enter level to update (1, 2, 3): ")
		if level == "exit":
			exit = 1
			break
		while int(level) != 1 and int(level) != 2 and int(level) != 3:
			print("\nInvalid input, please input a level number from 1 to 3")
			level = input("Enter level to update (1, 2, 3): ")
			if level == "exit":
				exit = 1
				break
		correct = input("\nEnter number correct out of 10: ")
		if correct == "exit":
			exit = 1
			break
		while int(correct) > 10 or int(correct) < 0:
			print("\nInvalid input, please enter a number from 1 to 10")
			correct = input("Enter number correct out of 10: ")
		db.updateUserScore(user, int(level), int(correct))
		print("\nThe average for {user} for level {lvl} is {av}".format(user = user, lvl = level, av = db.getUserAverage(user, int(level))))
		print(db.getUserInfo(user))

	else:
		print("No user found under that username\n")
		cont = input("continue (y/n)?: ")
		if cont != 'y' or cont != 'y':
			exit = 1
			break


delete = input("\nEnter y to wipe database, enter anything else to terminate test: ")
if delete == "y" or delete == "Y":
	db.deleteUsers()
	print("Database wiped")
print("Goodbye")
db.closeDb()
