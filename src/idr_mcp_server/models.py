"""Pydantic models for IDR MCP Server responses."""

from pydantic import BaseModel, Field
from typing import Optional, Any


class PaginationMeta(BaseModel):
    """Pagination metadata for paginated responses."""
    limit: int = Field(default=100, description="Maximum number of results per page")
    offset: int = Field(default=0, description="Starting offset for results")
    total_count: Optional[int] = Field(default=None, description="Total number of results available")


class ScreenInfo(BaseModel):
    """Information about a screen in IDR."""
    id: int = Field(..., description="Unique identifier for the screen")
    name: str = Field(..., description="Name of the screen")
    description: Optional[str] = Field(default=None, description="Description of the screen")
    
    class Config:
        extra = "allow"


class ProjectInfo(BaseModel):
    """Information about a project in IDR."""
    id: int = Field(..., description="Unique identifier for the project")
    name: str = Field(..., description="Name of the project")
    description: Optional[str] = Field(default=None, description="Description of the project")
    
    class Config:
        extra = "allow"


class PlateInfo(BaseModel):
    """Information about a plate in a screen."""
    id: int = Field(..., description="Unique identifier for the plate")
    name: str = Field(..., description="Name of the plate")
    
    class Config:
        extra = "allow"


class DatasetInfo(BaseModel):
    """Information about a dataset in a project."""
    id: int = Field(..., description="Unique identifier for the dataset")
    name: str = Field(..., description="Name of the dataset")
    description: Optional[str] = Field(default=None, description="Description of the dataset")
    
    class Config:
        extra = "allow"


class ImageInfo(BaseModel):
    """Information about an image in IDR."""
    id: int = Field(..., description="Unique identifier for the image")
    name: str = Field(..., description="Name of the image")
    
    class Config:
        extra = "allow"


class ImageMetadata(BaseModel):
    """Detailed metadata for an image."""
    id: int = Field(..., description="Image ID")
    meta: Optional[dict[str, Any]] = Field(default=None, description="Image metadata")
    size: Optional[dict[str, int]] = Field(default=None, description="Image dimensions (width, height, z, c, t)")
    pixel_size: Optional[dict[str, Any]] = Field(default=None, description="Pixel size information")
    channels: Optional[list[dict[str, Any]]] = Field(default=None, description="Channel information")
    
    class Config:
        extra = "allow"


class MapAnnotation(BaseModel):
    """A map annotation containing key-value pairs."""
    id: int = Field(..., description="Annotation ID")
    values: list[list[str]] = Field(default_factory=list, description="Key-value pairs")
    
    class Config:
        extra = "allow"


class AnnotationsResponse(BaseModel):
    """Response containing annotations for an object."""
    annotations: list[MapAnnotation] = Field(default_factory=list, description="List of map annotations")


class PlateGrid(BaseModel):
    """Plate grid structure with well information."""
    grid: list[list[Optional[dict[str, Any]]]] = Field(default_factory=list, description="2D grid of wells")
    collabels: list[str] = Field(default_factory=list, description="Column labels")
    rowlabels: list[str] = Field(default_factory=list, description="Row labels")
    
    class Config:
        extra = "allow"


class StudiesSearchResult(BaseModel):
    """Combined search result for screens and projects."""
    screens: list[ScreenInfo] = Field(default_factory=list, description="List of screens")
    projects: list[ProjectInfo] = Field(default_factory=list, description="List of projects")
    pagination: PaginationMeta = Field(default_factory=PaginationMeta, description="Pagination metadata")