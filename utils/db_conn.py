import sqlalchemy
import sqlalchemy.sql as sql
import sqlalchemy.orm

# Constants setting the configuration of database connection
DB_NAME = 'sandbox_4'
DB_TEST = 'test1'
DB_IP = 'localhost'
DB_PORT = '3306'
DB_USER = 'root'
DB_PASS = ''

# SQLAlchemy engine and python sql connector
# check http://docs.sqlalchemy.org/en/latest/core/engines.html for supported engines and connectors 
SQL_ENGINE = 'mysql'
SQL_CONNECTOR = 'pymysql'
SQL_CHARSET = 'utf8mb4'

# construct sqlalchemy connection string

CONN_STRING = {'production': SQL_ENGINE + '+' + SQL_CONNECTOR + '://' + DB_USER + ':' + DB_PASS + '@' + DB_IP + ':' + DB_PORT + '/' + DB_NAME + '?charset=' + SQL_CHARSET,
               'test': SQL_ENGINE + '+' + SQL_CONNECTOR + '://' + DB_USER + ':' + DB_PASS + '@' + DB_IP + ':' + DB_PORT + '/' + DB_TEST + '?charset=' + SQL_CHARSET,
               }


engine = sqlalchemy.create_engine(CONN_STRING['production'])
test_engine = sqlalchemy.create_engine(CONN_STRING['test'])
