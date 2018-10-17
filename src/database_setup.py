from sqlalchemy import Column, ForeignKey, Integer, String, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class CruiseLine(Base):
    """
    Contain all information about a cruise line
    """
    __tablename__ = 'cruiseline'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    ships = relationship("Ship", back_populates="line")

class Ship(Base):
    """
    Contain all information about a single cruise ship
    """
    __tablename__ = 'ship'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    line_id = Column(Integer, ForeignKey('cruiseline.id'))
    line = relationship("CruiseLine", back_populates="ships")
    build_year = Column(Integer)
    refurbished_year = Column(Integer)
    crew = Column(Integer)
    passagers = Column(Integer)
    bars = Column(Integer)
    pools = Column(Integer)
    casinos = Column(Integer)

class Port(Base):
    """
    Contain all information about a Port
    """
    __tablename__ = "port"
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)

class Day(Base):
    """
    Days contains the information about each day of the cruise
    """
    __tablename__ = 'day'
    id = Column(Integer, primary_key=True)
    cruise_id = Column(Integer, ForeignKey('cruise.id'))
    cruise = relationship("Cruise", back_populates="days")
    day = Column(Integer)
    date = Column(Date)
    port_id = Column(Integer, ForeignKey('port.id'))
    port = relationship(Port)
    arrival = Column(Time)
    Departure = Column(Time)

class Cruise(Base):
    """
    Contain all the information about a single cruise
    """
    __tablename__ = 'cruise'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    line_id = Column(Integer, ForeignKey('cruiseline.id'))
    line = relationship(CruiseLine)
    ship_id = Column(Integer, ForeignKey('ship.id'))
    ship = relationship(Ship)
    destination = Column(String(256))
    departs_id = Column(Integer, ForeignKey('port.id'))
    departs = relationship(Port)
    nights = Column(Integer)
    price = Column(Integer)
    days = relationship("Day", back_populates="cruise")

engine = create_engine('sqlite:///db.db')
Base.metadata.create_all(engine)