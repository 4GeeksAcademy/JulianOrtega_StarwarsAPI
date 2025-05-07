from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional

db = SQLAlchemy()

user_has_planets = db.Table(
    'User_has_Planets',
    db.Column('User_id', db.Integer, ForeignKey('User.id'), primary_key=True),
    db.Column('Planets_id', db.Integer, ForeignKey('Planets.id'), primary_key=True)
)

user_has_people = db.Table(
    'User_has_People',
    db.Column('User_id', db.Integer, ForeignKey('User.id'), primary_key=True),
    db.Column('People_id', db.Integer, ForeignKey('People.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'User'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[Optional[str]] = mapped_column(String(30))

    planets: Mapped[List["Planets"]] = relationship(secondary=user_has_planets, back_populates="users")
    people: Mapped[List["People"]] = relationship(secondary=user_has_people, back_populates="users")
    favorites: Mapped[List["Favorites"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "email": self.email
        }

class Planets(db.Model):
    __tablename__ = 'Planets'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(45))
    diameter: Mapped[Optional[int]] = mapped_column()
    rotation_period: Mapped[Optional[str]] = mapped_column(String(45))
    terrain: Mapped[Optional[str]] = mapped_column(String(45))
    gravity: Mapped[Optional[int]] = mapped_column()
    orbital_period: Mapped[Optional[str]] = mapped_column(String(45))
    population: Mapped[Optional[str]] = mapped_column(String(45))
    climate: Mapped[Optional[str]] = mapped_column(String(45))
    surface_water: Mapped[Optional[str]] = mapped_column(String(45))

    users: Mapped[List["User"]] = relationship(secondary=user_has_planets, back_populates="planets")
    favorites: Mapped[List["Favorites"]] = relationship(back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "terrain": self.terrain,
            "gravity": self.gravity,
            "orbital_period": self.orbital_period,
            "population": self.population,
            "climate": self.climate,
            "surface_water": self.surface_water
        }

class People(db.Model):
    __tablename__ = 'People'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(45), nullable=False)
    gender: Mapped[str] = mapped_column(String(45), nullable=False)
    skin_color: Mapped[str] = mapped_column(String(45), nullable=False)
    hair_color: Mapped[str] = mapped_column(String(45), nullable=False)
    height: Mapped[str] = mapped_column(String(45), nullable=False)
    eye_color: Mapped[str] = mapped_column(String(45), nullable=False)

    users: Mapped[List["User"]] = relationship(secondary=user_has_people, back_populates="people")
    favorites: Mapped[List["Favorites"]] = relationship(back_populates="people")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "skin_color": self.skin_color,
            "hair_color": self.hair_color,
            "height": self.height,
            "eye_color": self.eye_color
        }

class Favorites(db.Model):
    __tablename__ = 'Favorites'

    id: Mapped[int] = mapped_column(primary_key=True)
    User_id: Mapped[int] = mapped_column(ForeignKey('User.id'), nullable=False)
    People_id: Mapped[Optional[int]] = mapped_column(ForeignKey('People.id'))
    Planets_id: Mapped[Optional[int]] = mapped_column(ForeignKey('Planets.id'))

    user: Mapped["User"] = relationship(back_populates="favorites")
    people: Mapped[Optional["People"]] = relationship(back_populates="favorites")
    planet: Mapped[Optional["Planets"]] = relationship(back_populates="favorites")
    
    def serialize(self):
        return {
            "id": self.id,
            "User_id": self.User_id,
            "People_id": self.People_id,
            "Planets_id": self.Planets_id
        }