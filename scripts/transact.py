from dbfpy3 import dbf
from dbfread import DBF
import pymysql.cursors
from django.db import transaction, DatabaseError
import yaml

# This script is used to integrate EOC's foxpro database file TRANSACT.DBF with our mySQL database

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

# Create Empty Array to put extracted database in #
itemList = []

# Declare Drop Statement #
sql_drop = "Truncate TABLE transact2;"

# Declare Create Statement #
sql_create = '''CREATE TABLE `transact2` (
`CLIENTID` varchar(11) DEFAULT NULL,
`TRANSACTID` varchar(11) DEFAULT NULL,
`SS_NO` varchar(11) DEFAULT NULL,
`HOUSEID` varchar(9) DEFAULT NULL,
`DATER` date DEFAULT NULL,
`SITE` varchar(2) DEFAULT NULL,
`UNITS` float DEFAULT NULL,
`COST` float DEFAULT NULL,
`CSBG` varchar(1) DEFAULT NULL,
`ONE` varchar(1) DEFAULT NULL,
`STAFF` varchar(2) DEFAULT NULL,
`VENCODE` varchar(30) DEFAULT NULL,
`FUELCODE` varchar(1) DEFAULT NULL,
`BATCHCODE` varchar(8) DEFAULT NULL,
`DATE_ADDED` date DEFAULT NULL,
`CHECKNO` varchar(6) DEFAULT NULL,
`SUBCATEG` varchar(1) DEFAULT NULL,
`COL1` varchar(2) DEFAULT NULL,
`COL2` varchar(2) DEFAULT NULL,
`COL3` varchar(2) DEFAULT NULL,
`HOUSING` varchar(1) DEFAULT NULL,
`HOUSEINC` float DEFAULT NULL,
`TARGDATE` date DEFAULT NULL,
`GOALMADE` varchar(1) DEFAULT NULL,
`POVERTY` varchar(1) DEFAULT NULL,
`HANDICAP` varchar(5) DEFAULT NULL,
`HOMELESREA` varchar(5) DEFAULT NULL,
`REFREASON` varchar(2) DEFAULT NULL,
`REAS4AISSU` varchar(1) DEFAULT NULL,
`PARTORFULL` varchar(1) DEFAULT NULL,
`STARTSALA` float DEFAULT NULL,
`ALLFAMILY` tinyint(1) DEFAULT NULL,
`WASEDITED` tinyint(1) DEFAULT NULL,
`REFER` varchar(3) DEFAULT NULL,
`REASON` varchar(1) DEFAULT NULL,
`ACCOUNT_NO` varchar(22) DEFAULT NULL,
`TOWNSHIP` varchar(2) DEFAULT NULL,
`EARNED` float DEFAULT NULL,
`EARNHOUSE` float DEFAULT NULL,
`UNMET` varchar(1) DEFAULT NULL,
`REFERRAL` varchar(1) DEFAULT NULL,
`INTERVIEWE` varchar(2) DEFAULT NULL,
`ADDR` varchar(70) DEFAULT NULL,
`CITY` varchar(17) DEFAULT NULL,
`ZIP` varchar(10) DEFAULT NULL,
`TELEPHONE` varchar(12) DEFAULT NULL,
`PICKTIME` varchar(5) DEFAULT NULL,
`PICKAMFM` varchar(2) DEFAULT NULL,
`DESTADDR` varchar(70) DEFAULT NULL,
`DESTCITY` varchar(17) DEFAULT NULL,
`RIDETYPE` varchar(1) DEFAULT NULL,
`TAXI` varchar(2) DEFAULT NULL,
`INSTRUCT` varchar(256) DEFAULT NULL,
`PICKUPTIME` varchar(8) DEFAULT NULL,
`REFERENCE` varchar(6) DEFAULT NULL,
`TANF` varchar(1) DEFAULT NULL,
`POSTED` tinyint(1) DEFAULT NULL,
`POSTDATE` date DEFAULT NULL,
`REFERTO` varchar(3) DEFAULT NULL,
`DESTZIP` varchar(5) DEFAULT NULL,
`CHRONIC` tinyint(1) DEFAULT NULL,
`FLAGDATE` date DEFAULT NULL,
`FLAG` tinyint(1) DEFAULT NULL,
`WARNING` varchar(128) DEFAULT NULL,
`APPTTYPE` varchar(2) DEFAULT NULL,
`VERIFY` tinyint(1) DEFAULT NULL,
`AIDSID` varchar(10) DEFAULT NULL,
`FUND1` varchar(1) DEFAULT NULL,
`FUND2` varchar(1) DEFAULT NULL,
`FEE1` float DEFAULT NULL,
`FEE2` float DEFAULT NULL
);'''

# Connect To DBF File #
transact = dbf.DBF('/var/sftp/eoc/TRANSACT.DBF')

# Loop DBF Data into Your Empty Array #
for rec in transact:
    itemList.append((
        rec['CLIENTID'],
        rec['TRANSACTID'],
        rec['SS_NO'],
        rec['HOUSEID'],
        rec['DATER'],
        rec['SITE'],
        rec['UNITS'],
        rec['COST'],
        rec['CSBG'],
        rec['ONE'],
        rec['STAFF'],
        rec['VENCODE'],
        rec['FUELCODE'],
        rec['BATCHCODE'],
        rec['DATE_ADDED'],
        rec['CHECKNO'],
        rec['SUBCATEG'],
        rec['COL1'],
        rec['COL2'],
        rec['COL3'],
        rec['HOUSING'],
        rec['HOUSEINC'],
        rec['TARGDATE'],
        rec['GOALMADE'],
        rec['POVERTY'],
        rec['HANDICAP'],
        rec['HOMELESREA'],
        rec['REFREASON'],
        rec['REAS4AISSU'],
        rec['PARTORFULL'],
        rec['STARTSALA'],
        rec['ALLFAMILY'],
        rec['WASEDITED'],
        rec['REFER'],
        rec['REASON'],
        rec['ACCOUNT_NO'],
        rec['TOWNSHIP'],
        rec['EARNED'],
        rec['EARNHOUSE'],
        rec['UNMET'],
        rec['REFERRAL'],
        rec['INTERVIEWE'],
        rec['ADDR'],
        rec['CITY'],
        rec['ZIP'],
        rec['TELEPHONE'],
        rec['PICKTIME'],
        rec['PICKAMFM'],
        rec['DESTADDR'],
        rec['DESTCITY'],
        rec['RIDETYPE'],
        rec['TAXI'],
        rec['INSTRUCT'],
        rec['PICKUPTIME'],
        rec['REFERENCE'],
        rec['TANF'],
        rec['POSTED'],
        rec['POSTDATE'],
        rec['REFERTO'],
        rec['DESTZIP'],
        rec['CHRONIC'],
        rec['FLAGDATE'],
        rec['FLAG'],
        rec['WARNING'],
        rec['APPTTYPE'],
        rec['VERIFY'],
        rec['AIDSID'],
        rec['FUND1'],
        rec['FUND2'],
        rec['FEE1'],
        rec['FEE2']
    ))

# Pepare Insert Statement # 
s = ""
s += "INSERT INTO transact2"
s += "("
s += " CLIENTID"
s += ", TRANSACTID"
s += ", SS_NO"
s += ", HOUSEID"
s += ", DATER"
s += ", SITE"
s += ", UNITS"
s += ", COST"
s += ", CSBG"
s += ", ONE"
s += ", STAFF"
s += ", VENCODE"
s += ", FUELCODE"
s += ", BATCHCODE"
s += ", DATE_ADDED"
s += ", CHECKNO"
s += ", SUBCATEG"
s += ", COL1"
s += ", COL2"
s += ", COL3"
s += ", HOUSING"
s += ", HOUSEINC"
s += ", TARGDATE"
s += ", GOALMADE"
s += ", POVERTY"
s += ", HANDICAP"
s += ", HOMELESREA"
s += ", REFREASON"
s += ", REAS4AISSU"
s += ", PARTORFULL"
s += ", STARTSALA"
s += ", ALLFAMILY"
s += ", WASEDITED"
s += ", REFER"
s += ", REASON"
s += ", ACCOUNT_NO"
s += ", TOWNSHIP"
s += ", EARNED"
s += ", EARNHOUSE"
s += ", UNMET"
s += ", REFERRAL"
s += ", INTERVIEWE"
s += ", ADDR"
s += ", CITY"
s += ", ZIP"
s += ", TELEPHONE"
s += ", PICKTIME"
s += ", PICKAMFM"
s += ", DESTADDR"
s += ", DESTCITY"
s += ", RIDETYPE"
s += ", TAXI"
s += ", INSTRUCT"
s += ", PICKUPTIME"
s += ", REFERENCE"
s += ", TANF"
s += ", POSTED"
s += ", POSTDATE"
s += ", REFERTO"
s += ", DESTZIP"
s += ", CHRONIC"
s += ", FLAGDATE"
s += ", FLAG"
s += ", WARNING"
s += ", APPTTYPE"
s += ", VERIFY"
s += ", AIDSID"
s += ", FUND1"
s += ", FUND2"
s += ", FEE1"
s += ", FEE2"
s += ") VALUES ("
s += "(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ",(%s)"
s += ")"

# Declare Update Statement #
update = 'UPDATE transact2 SET SS_NO = replace(SS_NO, "-", "")'

# Execute SQL Statements #
try:        
    with db.cursor() as cur:
        cur.execute(sql_drop)
except DatabaseError:
    transaction.rollback()

finally:
    cur.close()

#try:        
 #   with db.cursor() as cur:
  #      cur.execute(sql_create)
#except DatabaseError:
 #   transaction.rollback()

#finally:
 #   cur.close()    

try:
     with db.cursor() as cur:
        cur.executemany(s, itemList)
        db.commit()
        print(cur.rowcount, "records inserted.")
except DatabaseError:
    transaction.rollback()

finally:
    cur.close()    

try:
    with db.cursor() as cur:
        cur.execute(update)
        db.commit()
except DatabaseError:
    transaction.rollback()    

except Exception as E:
    print('Error : ', E)

# Close Connection #  
finally:
    cur.close()
    db.close()