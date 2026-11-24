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
on subsequent runs. If `cccSite/.env` is missing, setup creates it from the
template. Internet access is needed to download packages.

If the system packages are already installed, use `bash setup.sh --skip-system-packages`.
The script still installs the Python requirements. The packages needed to build
`mysqlclient` must already be available when you use this flag.

After setup, start the server from the repository root.

```bash
bash runserver.sh
```

Open [CCC on port 8080](http://127.0.0.1:8080/). The launcher uses
`CCCSITE_MODE` from `cccSite/.env` when you omit `--production`. The default,
`development`, uses SQLite with Django debug mode enabled.

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
	-	sudo apt install build-essential python3-dev default-libmysqlclient-dev pkg-config
	-	sudo apt install libapache2-mod-wsgi-py3
		-	Y to Continue
	-	For MariaDB, follow [Running the production server](#running-the-production-server).

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
	-	If you have changed Django models and need new migrations, run `python manage.py makemigrations` from `cccSite` before starting the server.
	-	From the repository root, run `bash runserver.sh`. The launcher applies pending migrations before starting Django.
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
	- Open `cccSite/.env`. For a manual installation, copy `cccSite/.env.example` to that path if the file is missing.
	- Set `GOOGLE_API_KEY` to your Maps API key.
	- Keep the gitignored `cccSite/.env` file private.
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

Start the site with the launcher for the database you want to administer. The
launcher applies migrations before starting Django. If the launcher started
MariaDB, keep that terminal open during the next step.

In a second terminal, run the command for your database from the repository root.

- SQLite

	```bash
	CCCSITE_MODE=development cccSite/.venv/bin/python cccSite/manage.py createsuperuser
	```

- MariaDB

	```bash
	CCCSITE_MODE=production cccSite/.venv/bin/python cccSite/manage.py createsuperuser
	```

Enter a username, email address, and password when prompted. Then open the
[Django admin page](http://127.0.0.1:8080/DJadmin/) and sign in. If you use a
forwarded development URL, append `/DJadmin/` to that URL.

This account uses Django's admin login at `/DJadmin/`. The website's regular
login and custom admin area at `/admin/` use separate accounts.

## Running the production server

### Install and provision MariaDB

To install MariaDB on the same VM, run this command from the repository root.

```bash
bash setup.sh --install-mariadb
```

Setup provisions the `chesapeakeconnect` database and the local `cccapp` user by
default. It saves the connection settings in `cccSite/.env` and reuses the
database and credentials on subsequent runs. Setup restores the service's
previous running and boot settings after provisioning. If MariaDB and the
system prerequisites are already installed, run
`bash setup.sh --skip-system-packages --install-mariadb`.

For an existing MariaDB server, run regular `bash setup.sh`. It installs the
driver from `cccSite/requirements.txt`. Create a database with the `utf8mb4`
character set and give the application user permission to run Django migrations
and read and write data in that database. Use that server's connection details
in the next step.

### Configure `cccSite/.env`

Open `cccSite/.env` and set the mode and connection settings. For a local
installation, keep the MariaDB values that setup wrote, including the generated
password. The example shows the default local host, database, and user.

```dotenv
CCCSITE_MODE=production
MARIADB_HOST=127.0.0.1
MARIADB_PORT=3306
MARIADB_NAME=chesapeakeconnect
MARIADB_USER=cccapp
MARIADB_PASSWORD=your_database_password
DJANGO_SECRET_KEY=your_generated_secret_key
GOOGLE_API_KEY=your_google_maps_api_key
```

`production` selects MariaDB and disables Django debug mode. `MARIADB_PORT`
defaults to `3306`. Django gives process environment variables precedence over
`cccSite/.env`. Set the secret key and Maps key as described under
[Setup for Keys](#setup-for-keys), and keep `cccSite/.env` private.

### Start the server with `runserver.sh`

Run this command from the repository root.

```bash
bash runserver.sh --production
```

`--production` selects production mode for this launch. The launcher starts
the local MariaDB service if needed, applies Django migrations to MariaDB, and
starts Django's development server on port 8080. Open
[CCC on port 8080](http://127.0.0.1:8080/) or use your forwarded port.
Starting or stopping the service may prompt for `sudo`. Press **Ctrl+C** to
stop the site. MariaDB stops if the launcher started it, and an already-running
service stays up.

For a remote MariaDB host, the same command uses the configured connection.
If `CCCSITE_MODE=production` is already set, you can run `bash runserver.sh`
while MariaDB is running. Automatic local service startup requires the flag.

For a public deployment, use a production WSGI or ASGI server with
`CCCSITE_MODE=production` and manage MariaDB separately. Add the public hostname
to Django's `ALLOWED_HOSTS`. From the repository root, apply migrations and run
the deployment checks. [Django deployment checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)

```bash
CCCSITE_MODE=production cccSite/.venv/bin/python cccSite/manage.py migrate --noinput
CCCSITE_MODE=production cccSite/.venv/bin/python cccSite/manage.py check --deploy
```
