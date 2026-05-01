from sqlalchemy import create_engine
from src import config

connection_url = config.get_settings().POSTGRES_URI
engine = create_engine(connection_url, pool_pre_ping=True)
