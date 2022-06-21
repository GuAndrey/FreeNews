from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from config.db import DB_USER, DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT

ENGINE = create_engine(
    f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}', 
    client_encoding='utf8',
    echo=False
)

