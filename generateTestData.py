from main import db
from models import Priority

db.session.add(Priority(text="Priority 1"))
db.session.commit()
db.session.add(Priority(text="Priority 2"))
db.session.commit()
db.session.add(Priority(text="Priority 3"))
db.session.commit()
db.session.add(Priority(text="Priority 4"))
db.session.commit()
