# Research & Development Notes

## Safetly sharing keys
I have been working on changing keys that have been shared in the repo and finding a safe way to refer to them instead on just hard coding it. The API key should be good as all user will have a unique key and the API key used prior also didn't do anything to the code. I changed the Django Key and Simon said to make a Secrets in Github which I've done. This is some notes I have made when trying to figure out how to share this secret now. 
- GitHub Secrets allows sensitive values to be accessed by GitHub Actions workflows without hardcoding them into the repository but there is no command to then give this key out.
- we agreed to then have every user make their own django key and I added instruction on cccsetupinstructions.md

## SETTING UP API's FOR MAP PAGE
- Go to your google cloud, and click the 3 lines on the upper left corner
- Click APIs & Services, and click enable APIs & Services
- Search for and enable
   - Maps JavaScript API	
   - Places API	
   - Geocoding API
- Copy the key for API(should all be the same key)
- Open setting.py and update the GOOGLE_MAPS_API_KEY
- When commiting code make sure to git ignore setting.py to keep your API key private

## Running CCC Website Steps: (After installing everything, just C&P)

cd /home/shared_workspace/ChesapeakeCommunityConnect/cccSite

python3 -m venv .venv
source .venv/bin/activate

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 8080

## Issue Investigation
- Investigated Issue #163 and found that it had already been resolved.
- Commented on GitHub noting it may be environment-specific.

## Environment Setup
- Rebuilt my development environment using terminal instead of VS Code.
- Resolved dependency and setup issues.

## Technical Exploration
- Researched APIs for better understanding of integration.
- Worked with team members to troubleshoot Google Maps issues.

## Outcome
- Successfully ran the Django development server locally.
- Contributed to debugging and collaboration efforts.
