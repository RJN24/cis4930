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

print("Goodbye")
db.closeDb()
