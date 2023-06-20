from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    signups = db.relationship('Signup', back_populates='activities')

    serialize_only = ('id', 'name', 'difficulty')

    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'
    
class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    signups = db.relationship('Signup', back_populates='campers')

    serialize_only = ('id', 'name', 'age')

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("must have a name")
        return name

    @validates('age')
    def validate_age(self, key, age):
        if not 8<= age <=18:
            raise ValueError("must be between 8-18")
        return age
            

    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'
    
class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    @validates('time')
    def validate_time(self, key, time):
        if time not in range(0, 24):
            raise ValueError
        return time

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))
    campers = db.relationship('Camper', back_populates='signups')
    activities = db.relationship('Activity', back_populates='signups')


    def __repr__(self):
        return f'<Signup {self.id}>'


# add any models you may need. 