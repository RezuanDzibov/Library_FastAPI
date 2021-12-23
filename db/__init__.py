from sqlalchemy.orm import sessionmaker

from db.base import BaseModel, engine
from db.models import *


BaseModel.metadata.create_all(engine)


Session = sessionmaker()
Session.configure(bind=engine)
session = Session()