import pyodbc
import pandas as pd 
from sqlalchemy.engine import URL, create_engine

server = 'chatbotserver456.database.windows.net'
database = 'chatdb'
username = 'sqlserver'
password = 'chatbot@123'
driver = '{ODBC Driver 18 for SQL Server}'  # Update the driver as necessary
# Connection string
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": conn_str})

db_engine=create_engine(connection_url)


def execute_query_df_json(sql_in):
    with db_engine.begin() as conn:
        df =pd.read_sql(sql_in, conn)
        pd.set_option('display.max_columns', None)
        # print(f'Dataframe \n\n {df}')
        data = df.to_json(indent=4, date_format='iso' ,index=False, orient='records')
        # print(data)
    return df.to_json(indent=4, date_format='iso' ,index=False, orient='records')

def execute_query_df_no_json(sql_in):
    with db_engine.begin() as conn:
        df =pd.read_sql(sql_in, conn)
        pd.set_option('display.max_columns', None)
        # print(f'Dataframe \n\n {df}')
    return df.to_markdown(index=False)


# For direct db Connection 
import pyodbc
import pandas as pd
from dotenv import load_dotenv, find_dotenv
import os

# load dotenv 
load_dotenv(find_dotenv())

con_string = 'DRIVER=ODBC Driver 18 for SQL Server;'+'SERVER='+os.getenv('DB_SERVER') +';'+'Database='+os.getenv('DB_NAME') +';'+'UID='+os.getenv('DB_USERNAME') +';' +'PWD='+os.getenv('DB_PWD') +';'
# print(con_string) #for debugging only
global conn 
conn = pyodbc.connect(con_string)

# Only works on sql query
def get_data(sql:str):
    df = pd.read_sql(sql=sql, con=conn)
    # print(df)
    return df.to_json(indent=4, date_format='iso' ,index=False, orient='records')
