from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, ForeignKey, DateTime
from datetime import datetime, timezone

# This is the base class all models will inherit from
class Base(DeclarativeBase):
    pass

class Plant(Base):
    __tablename__ = "plants"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(100))
    
    # Relationship: A plant has many zones
    zones: Mapped[list["Zone"]] = relationship("Zone", back_populates="plant")

class Zone(Base):
    __tablename__ = "zones"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    risk_level: Mapped[str] = mapped_column(String(20), default="LOW")
    plant_id: Mapped[int] = mapped_column(ForeignKey("plants.id"))
    
    plant: Mapped["Plant"] = relationship("Plant", back_populates="zones")
    sensors: Mapped[list["Sensor"]] = relationship("Sensor", back_populates="zone")

class Sensor(Base):
    __tablename__ = "sensors"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sensor_type: Mapped[str] = mapped_column(String(50)) # e.g., "gas", "temperature", "camera"
    status: Mapped[str] = mapped_column(String(20), default="ACTIVE")
    last_reading: Mapped[float] = mapped_column(Float, nullable=True)
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    zone_id: Mapped[int] = mapped_column(ForeignKey("zones.id"))
    zone: Mapped["Zone"] = relationship("Zone", back_populates="sensors")