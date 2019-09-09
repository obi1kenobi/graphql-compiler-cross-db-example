from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Airport(Base):
    __tablename__ = 'Airport'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    city_served = Column(String, nullable=True)
    alpha2_country = Column(String(2), nullable=True, index=True)
    iata_code = Column(String(3), nullable=True, index=True)
    icao_code = Column(String(4), nullable=True, index=True)
    elevation_ft = Column(Integer, nullable=True, index=True)


class Airline(Base):
    __tablename__ = 'Airline'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    iata_code = Column(String(2), nullable=True, index=True)
    icao_code = Column(String(3), nullable=True, index=True)
    callsign = Column(String, nullable=True, index=True)
    alpha2_country = Column(String(2), nullable=True, index=True)


class FlightRoute(Base):
    __tablename__ = 'FlightRoute'

    id = Column(Integer, primary_key=True)
    airline_id = Column(Integer, ForeignKey('Airline.id'), nullable=False, index=True)
    source_airport_id = Column(Integer, ForeignKey('Airport.id'), nullable=False, index=True)
    destination_airport_id = Column(Integer, ForeignKey('Airport.id'), nullable=False, index=True)
    codeshare = Column(Boolean)
    stops = Column(Integer, nullable=False, index=True)
