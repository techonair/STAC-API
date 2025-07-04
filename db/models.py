from sqlalchemy import Column, String, DateTime, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry

Base = declarative_base()

class STACItem(Base):
    __tablename__ = 'stacitem'

    id = Column(String, primary_key=True)
    datetime = Column(DateTime, nullable=False)
    bbox = Column(Geometry(geometry_type='POLYGON', srid=4326), nullable=False)
    collection = Column(String, nullable=False)
    properties = Column(String)

    def __repr__(self):
        return f"<STACItem(id={self.id}, datetime={self.datetime}, collection={self.collection})>"