# 1º Step
Open terminal or cmd.<br />
Install virtualenv.

	$ pip install virtualenv

# 2º Step
Create a virtual environment with python3x.<br />
Check out python version installed in your system.

  in my case

	$ python -V
	Python 3.7.2

	$ python2 -V
	Python 2.7.15

Then...

	$ virtualenv test --no-site-packages -p python

# 3º Step
Enter in test folder.

	$ cd test

# 4º Step
Clone git repository into.

	$ git clone 

# 5º Step
Activate the environment.

	$ source bin/activate

# 6º Step
Install whole needed packages.

	$ pip install -r requirements.txt

# 7º Step
Install and configure a database service (create an user, set a password and then create a database).<br />
In my case, I'm using MariaDB.

	$ mysql -u root -p
  
	MariaDB [(none)]> create user if not exists 'user'@localhost identified by 'password';
	MariaDB [(none)]> create database your_db;
	MariaDB [(none)]> grant all privileges on your_db.* to user@localhost identified by 'password';
	MariaDB [(none)]> flush privileges;
	MariaDB [(none)]> exit;
  
	$ mysql -u user -p

	MariaDB [(none)]> use your_db;
	Database changed
	MariaDB [your_db]>

# 8º Step
Open test/config.py file and change user, password and database.<br />
NOTE: If you have trouble with the connection, it's because you need to install pymysql and add "+pymysql" as you can see in the code.

	$ pip install pymysql

# 9º Step
Open test/app/_ _init_ _.py file and change the IP to your (and the port if you wants).

# 10º Step
Initialize the database, make the migration and upgrade and then initialize the application.<br />
Run:

	$ python run.py db init
	$ python run.py db migrate
	$ python run.py db upgrade
	$ python run.py runserver

You'll see the application running.
Just copy the url and paste on browser.

NOTE: In some systems, the python3x is called by command "python3". In this case you'll make "virtualenv test --no-site-packages -p python3". So after activate the environment, you don't need to make "python3 run.py", just make "python run.py" that it'll work. And for "pip install package", you don't need of "sudo".
