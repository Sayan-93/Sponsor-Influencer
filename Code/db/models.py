from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer,String,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column,relationship
from datetime import datetime
from typing import List

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


class Influencer(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    industry: Mapped[str] = mapped_column(nullable=True)
    followers: Mapped[int] = mapped_column(nullable=True)

class Sponsor(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    campaign: Mapped[List['Campaign']] = relationship(back_populates='sponsor')

class Admin(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

class Campaign(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    industry: Mapped[str]
    start_date: Mapped[datetime]
    end_date: Mapped[datetime]
    budget: Mapped[int]
    private: Mapped[str] = mapped_column(nullable=True)
    flag: Mapped[bool] = mapped_column(nullable=True)
    sponsor_id = mapped_column(ForeignKey('sponsor.id'))
    sponsor: Mapped['Sponsor'] = relationship(back_populates='campaign')

class Ad_requests(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    sponsor_id = mapped_column(ForeignKey('sponsor.id'))
    sponsor_name: Mapped[str] = mapped_column(ForeignKey('sponsor.name'))
    campaign_id = mapped_column(ForeignKey('campaign.id'))
    influencer_id = mapped_column(ForeignKey('influencer.id'))
    influencer_name: Mapped[str] = mapped_column(ForeignKey('influencer.name'))
    request_type: Mapped[str]
    request_status: Mapped[str]


