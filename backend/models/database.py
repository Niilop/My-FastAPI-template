# backend/models/database.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from core.database import Base
from datetime import datetime, timezone
import enum

EMBEDDING_DIM = 768  # Google text-embedding-004 default


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    settings = Column(JSON, default={})  # Store user preferences
    
    # Relationships
    data_catalogs = relationship("DataCatalog", back_populates="owner", cascade="all, delete-orphan")
    models = relationship("Model", back_populates="owner", cascade="all, delete-orphan")
    pipelines = relationship("Pipeline", back_populates="owner", cascade="all, delete-orphan")
    document_chunks = relationship("DocumentChunk", back_populates="owner", cascade="all, delete-orphan")


class DataCatalog(Base):
    __tablename__ = "data_catalogs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    description = Column(Text, default="")
    data_metadata = Column(JSON, default={})  # Store shape, columns, data types, etc.
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    owner = relationship("User", back_populates="data_catalogs")


class ModelType(str, enum.Enum):
    LINEAR_REGRESSION = "linear_regression"
    RANDOM_FOREST = "random_forest"
    XGBOOST = "xgboost"
    NEURAL_NETWORK = "neural_network"
    CUSTOM = "custom"


class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    model_type = Column(SQLEnum(ModelType), nullable=False)
    description = Column(Text, default="")
    file_path = Column(String(500), nullable=False)
    dataset_ids = Column(JSON, default=[])  # List of DataCatalog IDs used for training
    metrics = Column(JSON, default={})  # Store accuracy, precision, recall, rmse, etc.
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    owner = relationship("User", back_populates="models")


class PipelineStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    COMPLETED = "completed"
    FAILED = "failed"


class Pipeline(Base):
    __tablename__ = "pipelines"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    pipeline_type = Column(String(100), nullable=False)  # e.g., "news_scraper", "data_processor"
    description = Column(Text, default="")
    status = Column(SQLEnum(PipelineStatus), default=PipelineStatus.INACTIVE)
    schedule = Column(String(100), default="")  # e.g., "0 0 * * *" for cron
    pipeline_config = Column(JSON, default={})  # Store pipeline-specific configuration
    last_run = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    owner = relationship("User", back_populates="pipelines")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    source = Column(String(255), nullable=False)   # filename or label supplied by caller
    content = Column(Text, nullable=False)
    embedding = Column(Vector(EMBEDDING_DIM), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    owner = relationship("User", back_populates="document_chunks")
