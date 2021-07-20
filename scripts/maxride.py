from dbfpy3 import dbf
from dbfread import DBF
import pymysql.cursors
from django.db import transaction, DatabaseError
import yaml

# This script is used to integrate EOC's foxpro database file MAXRIDE.DBF with our mySQL database

# Import Database Credentials #
with open('scripts/defines.yml') as file:
    conf = yaml.full_load(file)

host2 = conf['db']['host2']
user2=conf['db']['user2']
password2=conf['db']['password2']
database2=conf['db']['database2']

# Create database connection #

db = pymysql.connect(host=host2,
                            user=user2,
                            password=password2,
                            database=database2,
                            cursorclass=pymysql.cursors.DictCursor)
#cur = db.cursor()


    # Create Empty Array to put extracted database in #
itemList = []

# Declare Drop Table #
sql_drop = "DROP TABLE IF EXISTS maxride2;"

# Delcare Create New Table #
sql_create = '''CREATE TABLE `maxride2`(`CODE` char(2) DEFAULT NULL,`DESCRIP` char(70) DEFAULT NULL, `COLID` char(20) DEFAULT NULL, `LIMIT` int DEFAULT NULL )'''

# Connect To DBF File #
maxride = dbf.DBF('/var/sftp/eoc/MAXRIDE.DBF')

# Loop DBF Data into Your Empty Array #
for rec in maxride:
    itemList.append((
        rec['CODE'], 
        rec['DESCRIP'], 
        rec['COLID'],
        rec['LIMIT']
    ))

# Declare Insert Statement #    
s = ""
s += "INSERT INTO `maxride2`"
s += "("
s += " `CODE`"
s += ", `DESCRIP`"
s += ", `COLID`"
s += ", `LIMIT`"
s += ")VALUES("
s += "(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ")"
    
try:        
    with db.cursor() as cur:
        cur.execute(sql_drop)
except Exception as E:
    print('Error : ', E)   
cur.close()  

try:
     with db.cursor() as cur:                 
        cur.execute(sql_create)
except Exception as E:
    print('Error : ', E)   
cur.close()  

try:
    with db.cursor() as cur:            
        cur.executemany(s, itemList)
        db.commit()
        print(cur.rowcount, "record inserted.")
except Exception as E:
    print('Error : ', E)           
        
finally:    
    cur.close()        
    db.close() 

# Close Connection #            

