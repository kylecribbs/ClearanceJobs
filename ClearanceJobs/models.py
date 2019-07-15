import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class People(Base):
    __tablename__ = "people"
    id = sa.Column('id', sa.Integer, primary_key=True)
    member_id = sa.Column('member_id',sa.Integer)
    profile_pic_url = sa.Column('profile_pic_url', sa.String)
    name = sa.Column('name', sa.String)
    professional_title = sa.Column('professional_title', sa.String)
    location = sa.Column('location', sa.String)
    phone_verified = sa.Column('phone_verified', sa.Boolean)
    has_notes = sa.Column('has_notes', sa.Boolean)
    on_hotlist = sa.Column('on_hotlist', sa.Boolean)
    online = sa.Column('online', sa.Boolean)
    can_chat = sa.Column('can_chat', sa.Boolean)
    can_voip = sa.Column('can_voip', sa.Boolean)
    connection_status = sa.Column('connection_status', sa.String)
    updated_at = sa.Column('updated_at', sa.DateTime)
    last_viewed_at = sa.Column('last_viewed_at', sa.DateTime)
    clearance = sa.Column('clearance', sa.String)
    career_level = sa.Column('career_level', sa.String)
    relocate = sa.Column('relocate', sa.String)
    desired_salary = sa.Column('desired_salary', sa.Integer)
    score = sa.Column('score', sa.Float)
    resume = sa.Column('resume', sa.Text)

    def __repr__(self):
        return "<Author(name={self.name!r})>".format(self=self)