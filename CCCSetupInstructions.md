# Setting up Chesapeake Community Connect (CCC) on your Google Cloud VM
## Automated first-time setup

After cloning the repository, run this from the repository root as your normal user:

```bash
bash setup.sh
```

The script targets Ubuntu/Debian VMs. It installs the required system packages
(using `sudo`, which may prompt for your password), creates `cccSite/.venv`, installs
the Python requirements, and applies the existing migrations to SQLite. Python 3.10+
is required. It reuses the virtual environment and preserves existing database data
on subsequent runs. Internet access is needed to download packages.

To also start the development server on port 8080:

```bash
bash setup.sh --runserver
```

If the system packages are already installed, use `bash setup.sh --skip-system-packages`.
The script prints commands for activating the environment and starting the server
in future terminals; it cannot activate the environment in your current shell.

## Run CCC with MariaDB

To install MariaDB on the same VM, run these commands from the repository root.

```bash
bash setup.sh --install-mariadb
bash runserver.sh --production
```

The first command installs the server and driver, starts the service, and creates
the `chesapeakeconnect` database and the local `cccapp` user by default. The
installer saves the connection settings in `cccSite/.env` and reuses the database
and credentials on subsequent runs. If the system packages are already installed,
add `--skip-system-packages` to the setup command.

To use an existing MariaDB server, complete the regular setup and install the
driver's build prerequisites and production requirements.

```bash
sudo apt-get install build-essential python3-dev default-libmysqlclient-dev pkg-config
cccSite/.venv/bin/python -m pip install -r cccSite/requirements-production.txt
```

Set `MARIADB_HOST`, `MARIADB_NAME`, `MARIADB_USER`, and `MARIADB_PASSWORD` in
`cccSite/.env` or the process environment. Set `MARIADB_PORT` if the server
uses a port other than `3306`. Create the database with the `utf8mb4` character
set and grant the application user access to that database. Then run
`bash runserver.sh --production` to apply migrations and start the development
server with MariaDB.

Use `bash runserver.sh` to start the development server with SQLite. For direct
Django commands or WSGI and ASGI deployments, set `CCCSITE_MODE=production` to
select MariaDB. Before deploying to a live host, configure the production web
server and run Django's deployment checks.

## CCC Installation
-	**Configuring your Virtual Machine for git, python, and other dependencies**W
	-	sudo apt update
	-	sudo apt upgrade -y
	-	sudo apt install git
	-	git config --global user.name `github-username`
		-	Put in your GitHub username
	-	git config --global user.email `github-email`
		-	Put in your GitHub email
	-	git init
	-	git clone https://github.com/drsimonread/ChesapeakeCommunityConnect 
	-	sudo apt install python3 python3-venv python3-pip libmagic1
	-	sudo apt install libapache2-mod-wsgi-py3
		-	Y to Continue
	-	For MariaDB, follow [Run CCC with MariaDB](#run-ccc-with-mariadb).

-	**Creating and activating your Python virtual environment**
	-	cd cccSite
	-	python3 -m venv .venv
	-	source .venv/bin/activate
	-	Your terminal prompt should now show `(.venv)`. Keep this environment active while installing requirements and running Django commands.
	-	python -m pip install --upgrade pip
	-	Create the environment only once. In each new terminal, return to the `cccSite` directory and run `source .venv/bin/activate` again.

-	**Installing your CCC Requirements**
	-	Make sure you are still in your cccSite directory.
	-	Make sure your virtual environment is active before running these commands. Do not use `sudo` with pip.
	-	python -m pip install -r requirements.txt
-	**Running the CCC Website**
	-	In the cccSite directory.
	-	python manage.py migrate
	-	If you have changed Django models and need new migrations, run `python manage.py makemigrations`, then run `python manage.py migrate` again.
	-	python manage.py runserver 8080
		-	If you’re using Visual Studio Code, this should give you a prompt that says “Your application running on port 8080 is available”. Click on “Open in Browser”
		-	Alternatively, enter “http://127.0.0.1:8080/” in your browser
	-	Press **Ctrl+C** to stop the server. Run `deactivate` when you are finished using the virtual environment.
## Setup for Keys
- API KEY
	- Go to your Google Cloud, and click the 3 lines on the upper left corner
	- Click APIs & Services, and click enable APIs & Services
	- Search for and enable
		- Maps JavaScript API	
		- Places API	
		- Geocoding API
	- Save the key for API (should all have the same key)
	- Double click the cccSite and create a new file called .env 
	- Open .env.example and copy the line where we initalize the Google API key
	- Paste it into your own .env and for the place holder put your API key from earlier
	- This file should automatically be ignored when commiting as it is in the .gitignore file, keeping your key safe
- DJANGO KEY
	- Make sure you are in the cccSite directory (the same directory where manage.py is located).
	- Run the following command to generate your own Django secret key:
		```bash
		python3 -c "import secrets; print(secrets.token_urlsafe(50))"
		```
	- Copy the generated key and keep it private.
	- If you have not already created a .env file, create one inside the cccSite directory.
	- Open .env.example and copy the line where the Django secret key is initialized.
	- Paste it into your .env file and replace the placeholder with your generated key. It should look like this:
		```bash
		DJANGO_SECRET_KEY=your_generated_key_here
		```

## Create a Django admin account

Complete the automated or manual installation before creating the account.
If the development server is running in your terminal, press **Ctrl+C** to stop it.

1. From the repository root, enter the Django project directory:

	```bash
	cd cccSite
	```

2. Activate the virtual environment:

	```bash
	source .venv/bin/activate
	```

3. Apply any pending database migrations:

	```bash
	python manage.py migrate
	```

4. Create the administrator account:

	```bash
	python manage.py createsuperuser
	```

5. Enter a username, an email address, and a password when prompted. Enter the
	password again to confirm it. Password characters do not appear as you type.
	When the command succeeds, Django prints `Superuser created successfully.`

6. Start the development server:

	```bash
	python manage.py runserver 8080
	```

7. Open [the Django admin page](http://127.0.0.1:8080/DJadmin/) in your browser.
	If you use a forwarded development URL, add `/DJadmin/` to that URL instead.
	Sign in with the username and password you just created.

This account uses Django's admin login at `/DJadmin/`. The website's regular
login and custom admin area at `/admin/` use separate accounts.
