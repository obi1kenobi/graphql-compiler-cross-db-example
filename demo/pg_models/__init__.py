from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Airport(Base):
    __tablename__ = 'airport'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    city_served = Column(String, nullable=False)
    alpha2_country = Column(String(2), nullable=False, index=True)
    iata_code = Column(String(3), nullable=True, index=True)
    icao_code = Column(String(4), nullable=True, index=True)
    elevation_ft = Column(Integer, nullable=True, index=True)


class Airline(Base):
    __tablename__ = 'airline'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    iata_code = Column(String(2), nullable=True, index=True)
    icao_code = Column(String(3), nullable=True, index=True)
    callsign = Column(String, nullable=True, index=True)
    alpha2_country = Column(String(2), nullable=True, index=True)


class FlightRoute(Base):
    __tablename__ = 'flightroute'

    id = Column(Integer, primary_key=True)
    airline_id = Column(Integer, ForeignKey('airline.id'), nullable=False, index=True)
    source_airport_id = Column(Integer, ForeignKey('airport.id'), nullable=False, index=True)
    destination_airport_id = Column(Integer, ForeignKey('airport.id'), nullable=False, index=True)
    codeshare = Column(Boolean, nullable=False)
    stops = Column(Integer, nullable=False)
