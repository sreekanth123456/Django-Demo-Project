# Django-Demo-Project


## Installation

1. Install Python 3.8

    $ sudo apt-get install python3.8
    
2. Navigate to the project directory and install all the requirements

    $ pip3 install -r /path/to/requirements.txt

3. Create Superuser to manage the project with Djando admin page. (This is optional)

    $ python3 manage.py createsuperuser

4. Run the following commands to run the Django Server
    
    $ python3 manage.py makemigrations
    
    $ python3 manage.py migrate
    
    $ python3 manage.py runserver 8000
    
    Alternatively, you can use the following command to run the server forever in background
    
    $ nohup python3 manage.py runserver &

5. Install Nginx and map the port 8000 to port 80
    
    $ sudo apt update

    $ sudo apt install nginx
