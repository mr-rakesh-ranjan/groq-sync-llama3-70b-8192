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


def execute_query_df(sql_in):
    with db_engine.begin() as conn:
        df =pd.read_sql(sql_in, conn)
        pd.set_option('display.max_columns', None)
        # print(f'Dataframe \n\n {df}')
        data = df.to_json(indent=4, date_format='iso' ,index=False, orient='records')
        # print(data)
    # return df.to_markdown(index=False)
    return df.to_json(indent=4, date_format='iso' ,index=False, orient='records')

def execute_query_df_no_json(sql_in):
    with db_engine.begin() as conn:
        df =pd.read_sql(sql_in, conn)
        pd.set_option('display.max_columns', None)
        # print(f'Dataframe \n\n {df}')
    return df.to_markdown(index=False)
