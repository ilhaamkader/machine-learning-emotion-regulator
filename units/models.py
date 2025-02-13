# models.py
from datetime import date
from typing import List
from units.db_init import db
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

class EmotionColour(db.Model):
    __tablename__ = 'emotioncolour'
    
    emotion_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    emotion_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    
    black: Mapped[float] = mapped_column(nullable=False)
    red: Mapped[float] = mapped_column(nullable=False)
    gray: Mapped[float] = mapped_column(nullable=False)
    yellow: Mapped[float] = mapped_column(nullable=False)
    light_purple: Mapped[float] = mapped_column(nullable=False)
    sky_blue: Mapped[float] = mapped_column(nullable=False)
    jade: Mapped[float] = mapped_column(nullable=False)
    green: Mapped[float] = mapped_column(nullable=False)
    aqua: Mapped[float] = mapped_column(nullable=False)
    indigo: Mapped[float] = mapped_column(nullable=False)
    blue: Mapped[float] = mapped_column(nullable=False)
    bright_pink: Mapped[float] = mapped_column(nullable=False)
    chocolate: Mapped[float] = mapped_column(nullable=False)
    dark_yellow: Mapped[float] = mapped_column(nullable=False)
    light_green: Mapped[float] = mapped_column(nullable=False)
    
    sample_size:Mapped[int] = mapped_column(nullable=False)
    
    records: Mapped[List["Record"]] = relationship("Record", back_populates="emotioncolour")

    __table_args__ = (
        CheckConstraint('black >= 0 AND black <= 10', name='check_black'),
        CheckConstraint('red >= 0 AND red <= 10', name='check_red'),
        CheckConstraint('gray >= 0 AND gray <= 10', name='check_gray'),
        CheckConstraint('yellow >= 0 AND yellow <= 10', name='check_yellow'),
        CheckConstraint('light_purple >= 0 AND light_purple <= 10', name='check_light_purple'),
        CheckConstraint('sky_blue >= 0 AND sky_blue <= 10', name='check_sky_blue'),
        CheckConstraint('jade >= 0 AND jade <= 10', name='check_jade'),
        CheckConstraint('green >= 0 AND green <= 10', name='check_green'),
        CheckConstraint('aqua >= 0 AND aqua <= 10', name='check_aqua'),
        CheckConstraint('indigo >= 0 AND indigo <= 10', name='check_indigo'),
        CheckConstraint('blue >= 0 AND blue <= 10', name='check_blue'),
        CheckConstraint('bright_pink >= 0 AND bright_pink <= 10', name='check_bright_pink'),
        CheckConstraint('chocolate >= 0 AND chocolate <= 10', name='check_chocolate'),
        CheckConstraint('dark_yellow >= 0 AND dark_yellow <= 10', name='check_dark_yellow'),
        CheckConstraint('light_green >= 0 AND light_green <= 10', name='check_light_green'),
    )

class Record(db.Model):
    __tablename__ = 'records'
    
    record_id: Mapped[int] = mapped_column(primary_key=True)
    emotion_name: Mapped[str] = mapped_column(db.ForeignKey("emotioncolour.emotion_name"), nullable=False)
    likelihood_score: Mapped[float] = mapped_column(nullable=False)
    colour_displayed: Mapped[str] = mapped_column(nullable=False)
    record_date: Mapped[date] = mapped_column(nullable=False)
    colour_match: Mapped[bool] = mapped_column(nullable=False)
    
    emotioncolour: Mapped["EmotionColour"] = relationship("EmotionColour", back_populates="records")
