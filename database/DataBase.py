import csv
import psycopg2
import pandas as pd
import warnings
import os

from sqlalchemy import create_engine
from io import StringIO
from dotenv import load_dotenv

load_dotenv()

warnings.filterwarnings("ignore")

def psql_insert_copy(table, conn, keys, data_iter):
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        columns = ', '.join('"{}"'.format(k) for k in keys)
        if table.schema:
            table_name = '{}.{}'.format(table.schema, table.name)
        else:
            table_name = table.name

        sql = 'COPY {} ({}) FROM STDIN WITH CSV'.format(
            table_name, columns)
        cur.copy_expert(sql=sql, file=s_buf)

        cur.close()

def Execute(path_name, file_name):
    pan = pd.DataFrame(path_name)
    
    nuevasColumnas=[]
    for i in list(pan.columns):
        columna = str(i)
        columna = columna.replace("á","a")
        columna = columna.replace("é","e")
        columna = columna.replace("í","i")
        columna = columna.replace("ó","o")
        columna = columna.replace("ú","u")
        columna = columna.replace("ñ","n")
        columna = columna.replace(" ","_")
        columna = columna.lower()
        nuevasColumnas.append(columna)
    pan.columns = nuevasColumnas

    user = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    db = 'datos_laboratorio'

    engine = create_engine('postgresql://'+user+':'+password+"@"+host+":"+port+"/"+db)
    
    pan.to_sql(file_name, engine, index=False, if_exists='replace' ,method=psql_insert_copy) #,schema="test"

    return True