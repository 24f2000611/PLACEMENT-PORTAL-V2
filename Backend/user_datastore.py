from flask_security import SQLAlchemyUserDatastore
from Backend.models import User,Role

from Backend.database import db

user_datastore = SQLAlchemyUserDatastore(db,User,Role)


