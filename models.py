from sqlalchemy.orm import Mapped, mapped_column
from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Guess(db.Model):
    __tablename__ = "guess"

    # Column(DateTime(timezone=True), server_default=func.now())
    id: Mapped[int] = mapped_column(primary_key=True)
    created: Mapped[datetime] = mapped_column(server_default=func.now())
    image_id: Mapped[int] = mapped_column(ForeignKey("image.id"))

    image: Mapped["Image"] = relationship(back_populates="guesses")


class Image(db.Model):
    __tablename__ = "image"

    id: Mapped[int] = mapped_column(primary_key=True)    
    title: Mapped[str] = mapped_column(default="unknown")
    filename: Mapped[str] = mapped_column(unique=True)

    guesses: Mapped[List["Guess"]] = relationship(back_populates="image")