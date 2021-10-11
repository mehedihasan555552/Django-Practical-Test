# Django-Practical-Test

# Installation
1. Create a Folder where you want to save the project

2. Create a Virtual Environment and Activate

# Install Virtual Environment First

$  pip install virtualenv
Create Virtual Environment

# For Windows

$  python -m venv venv
# For Mac

$  python3 -m venv venv
Activate Virtual Environment

# For Windows

$  source venv/scripts/activate
# For Mac

$  source venv/bin/activate
3. Clone this project

$  git clone https://github.com/mehedihasan555552/Django-Practical-Test.git
# Then, Enter the project

$  cd Django-Practical-Test

4. Install Requirements from 'requirements.txt'

$  pip install -r requirements.txt
5. Add the hosts

Got to settings.py file
Then, On allowed hosts, Add [‘*’].
ALLOWED_HOSTS = ['*']
No need to change on Mac.

6. Now Run Server

Command for PC:

$ python manage.py runserver
Command for Mac:

$ python3 manage.py runserver
7. Login Credentials

# Create Super User (HOD)

$  python manage.py createsuperuser
Then Add Email, Username and Password
