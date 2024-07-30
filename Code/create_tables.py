from app import *
from db.models import *

app.app_context().push()

db.create_all()