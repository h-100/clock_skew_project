from app import db
from app.models import Test

tests = Test.query.all()
for test in tests:
    db.session.delete(test)

db.session.commit()
