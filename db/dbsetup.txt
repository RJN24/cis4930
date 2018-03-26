We will use a PostgreSQL db v10.3

To install:
- visit https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
- Select version PostgreSQL version 10.3
- Select operating system
- Run the installer

During installation:
- Select all default values
- When prompted to enter a password, enter 'password'
- I choose not to intall the stack builder, but it is up to you

After installation:
- Run SQL Shell (psql)
- Press enter until prompted to enter a password
- Enter 'password'

You should now be in the PostgreSQL database.

To create the table using my schema, type the following:
\i path/to/schema.sql 

*Obviously, change path/to/ to whatever your local path is.

If successful, PostgreSQL should say back "CREATE TABLE". To check if table
was successfully create, type "\dt" and it should show you a table with the name
"users".

Now that the table is created, you can test filling it with random data.
Type the following command:
\i path/to/insert-random-data.sql

This will add the test values from my insert-random-data.sql file.

To see the updated table, run the command:
SELECT * FROM users;

This will show you the user information currently in the table. 
Feel free to add your own to test it out.
