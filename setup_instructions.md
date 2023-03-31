# [DEPRECATED] Use [Setup and Installation](https://github.com/aaman007/MUOJ/wiki/Installation-Guidelines) instead

## Installation and Setup

### 1. Create .env file
Run the following command
```cp .env.example .env```         
Environment [DEVELOPMENT, STAGING, PRODUCTION] and SECRET could be changed optionally.      
Changing the Environment Mode to anything else would require PostgreSQL db configuration to be updated as well.        
In DEVELOPMENT mode, sqlite is used as db which is why this is not required
      

### 2. Creating virtual environment
Run ```virtualenv venv``` command inside the project directory       
Run ```source venv/bin/activate``` to activate the environment          
If you are using PyCharm, you can do the same thing using GUI

### 3. Installing Dependencies
All the dependencies are in ```requirements.txt``` file. Run the following command to install them -             
``` pip install -r requirements.txt ```
In Linux this might fail in case you don't have the package `libpq-dev`. To fix that run the following command
```sudo apt-get install libpq-dev``` \
In DEVELOPMENT mode, psycopg-binary is not required. So removing that from requirements.txt also should
solve this issue.

### 4. Create Migration Files
By default the migration files are not created. To create them
run the following command:
```python manage.py makemigrations```


### 5. Database Migration
Run the following command to migrate changes to the db           
``` python manage.py migrate ```


### 6. Running the application
``` python manage.py runserver ```         
or    
``` python manage.py runserver 0:PORT ``` [This requires the BASE_URL in the frontend to be changed]
