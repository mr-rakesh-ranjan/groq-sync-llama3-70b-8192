## Configuration of GROQ with llama3-70b-8192

### Step 1 :- create a virtual environment for the running the code.
using this command - $python -m venv .venv

Start your virtual environment using this command - .venv\Scripts\activate

Install the required packages using this command - pip install -r requirements.txt
### Step 2: Adding secret Keys to the .env file

example of .env file
```Python
GROQ_API_KEY=<your_api_key>

# db config
DB_SERVER='<your_server_name>'
DB_NAME='<your_db_name>'
DB_USERNAME='<your_username>'
DB_PWD='<your_pwd>'

SQLALCHEMY_DATABASE_URI='DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ {DB_SERVER}+';DATABASE='+{DB_NAME}+';UID='+{DB_USERNAME}+';PWD='+ {DB_PWD}

```
## Running the code
```command prompt

$system> python app.py

```
