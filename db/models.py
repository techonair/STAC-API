from sqlalchemy import Column, String, DateTime, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry

Base = declarative_base()

class SatelliteImage(Base):
    __tablename__ = 'satellite_images'

    id = Column(String, primary_key=True)
    datetime = Column(DateTime, nullable=False)
    bbox = Column(Geometry(geometry_type='POLYGON', srid=4326), nullable=False)
    collection = Column(String, nullable=False)
    properties = Column(String)  # JSON or string representation of additional properties

    def __repr__(self):
        return f"<SatelliteImage(id={self.id}, datetime={self.datetime}, collection={self.collection})>"