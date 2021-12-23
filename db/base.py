from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from config import BASE_DIR


engine = create_engine(f'sqlite:///{BASE_DIR}\\db.db')
BaseModel = declarative_base()