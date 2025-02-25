Log into Google cloud using the project manager email [smcmmapmanager@gmail.com](mailto:smcmmapmanager@gmail.com)

Find your way to the cloud shell and then run these commands in the cloud command prompt:

**Reclone repository and recreate venv:**

rm \-rf ChesapeakeCommunityConnect  
rm \-rf .venv  
Git clone https://www.github.com/SamAlby/ChesapeakeCommunityConnect  
Python \-m venv .venv

**Activate venv:**  
source .venv/bin/activate

**Switch to cccSite directory and install requirements**  
Cd ChesapeakeCommunityConnect/cccSite  
pip install \-r requirements.txt

**Make Django migrations and static**  
python manage.py makemigrations  
python manage.py migrate  
python manage.py collect static

**Deploy the app to the app engine**  
gcloud app deploy  
