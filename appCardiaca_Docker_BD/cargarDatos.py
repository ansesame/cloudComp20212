# -*- coding: utf-8 -*-

import pandas as pd
import psycopg2
import psycopg2.extras as extras
import os

# Importar datos
os.system('kaggle datasets download ronitf/heart-disease-uci')
os.system('unzip heart-disease-uci.zip')

# Obtener datos
data = pd.read_csv('heart.csv')
data = data.reset_index()
print(data.shape)

# Conexión BD
conn = psycopg2.connect(
    dbname="deteccion_temprana",
    user="postgres",
    password="postgres",
    host="db",
    port="5432"
)
cur = conn.cursor()

# Crear tabla
crearTablaScript = open("crearTabla.sql", "r").read()
cur.execute(crearTablaScript)

# LLenar tabla
tuples = list(data.itertuples(index=False, name=None))
query = '''
INSERT INTO heart_obs
VALUES %s
ON CONFLICT (index)
DO NOTHING;
'''
try:
    extras.execute_values(cur, query, tuples)
except (Exception, psycopg2.DatabaseError) as error:
    print("ERROR: %s" % error)
    conn.rollback()

# Probar llenado
cur.execute('SELECT COUNT(*) FROM heart_obs;')
print( cur.fetchone() )

# Guardar y cerrar conexión
conn.commit()
cur.close()
conn.close()
