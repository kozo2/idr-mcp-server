"""IDR MCP Server using fastmcp.

This module provides MCP tools for interacting with the Image Data Resource (IDR) API.
IDR is a public repository of reference image datasets from published scientific studies.
"""
import json
from typing import Any, Annotated

import httpx
from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("IDR MCP Server")

# Base URL for IDR API
IDR_BASE_URL = "https://idr.openmicroscopy.org"

# HTTP client for making requests
client = httpx.AsyncClient(timeout=30.0)


def format_json_response(data: Any) -> str:
    """Format API response data as JSON string for display."""
    return json.dumps(data, indent=2, default=str)


@mcp.tool()
async def search_studies(
    limit: Annotated[int, "Maximum number of results to return"] = 100,
    offset: Annotated[int, "Offset for pagination"] = 0
) -> str:
    """Search for studies (screens and projects) in IDR.
    
    Returns a list of available screens (high-content screening studies) and 
    projects (non-HCS image datasets) in the Image Data Resource.
    """
    results = {"screens": [], "projects": []}
    
    try:
        # Get screens
        screens_url = f"{IDR_BASE_URL}/api/v0/m/screens/"
        screens_params = {"limit": limit, "offset": offset}
        screens_response = await client.get(screens_url, params=screens_params)
        screens_response.raise_for_status()
        screens_data = screens_response.json()
        results["screens"] = screens_data.get("data", [])
        
        # Get projects
        projects_url = f"{IDR_BASE_URL}/api/v0/m/projects/"
        projects_params = {"limit": limit, "offset": offset}
        projects_response = await client.get(projects_url, params=projects_params)
        projects_response.raise_for_status()
        projects_data = projects_response.json()
        results["projects"] = projects_data.get("data", [])
        
        results["pagination"] = {
            "limit": limit,
            "offset": offset
        }
        
        return format_json_response(results)
        
    except httpx.HTTPError as e:
        return f"Error searching studies: {str(e)}"


@mcp.tool()
async def get_screen_info(
    screen_id: Annotated[int, "The ID of the screen to retrieve"]
) -> str:
    """Get detailed information about a specific screen.
    
    A screen represents a high-content screening study in IDR.
    """
    url = f"{IDR_BASE_URL}/api/v0/m/screens/{screen_id}/"
    
    try:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        return format_json_response(data)
        
    except httpx.HTTPError as e:
        return f"Error getting screen info: {str(e)}"


@mcp.tool()
async def get_project_info(
    project_id: Annotated[int, "The ID of the project to retrieve"]
) -> str:
    """Get detailed information about a specific project.
    
    A project represents a collection of non-HCS image datasets in IDR.
    """
    url = f"{IDR_BASE_URL}/api/v0/m/projects/{project_id}/"
    
    try:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        return format_json_response(data)
        
    except httpx.HTTPError as e:
        return f"Error getting project info: {str(e)}"


@mcp.tool()
async def get_plates(
    screen_id: Annotated[int, "The ID of the screen"],
    limit: Annotated[int, "Maximum number of results to return"] = 100,
    offset: Annotated[int, "Offset for pagination"] = 0
) -> str:
    """List plates in a screen.
    
    Plates are containers for wells in high-content screening studies.
    Each well typically contains multiple images (fields of view).
    """
    url = f"{IDR_BASE_URL}/api/v0/m/screens/{screen_id}/plates/"
    params = {"limit": limit, "offset": offset}
    
    try:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return format_json_response(data)
        
    except httpx.HTTPError as e:
        return f"Error getting plates: {str(e)}"


@mcp.tool()
async def get_datasets(
    project_id: Annotated[int, "The ID of the project"],
    limit: Annotated[int, "Maximum number of results to return"] = 100,
    offset: Annotated[int, "Offset for pagination"] = 0
) -> str:
    """List datasets in a project.
    
    Datasets are containers for images in non-HCS projects.
    """
    url = f"{IDR_BASE_URL}/api/v0/m/projects/{project_id}/datasets/"
    params = {"limit": limit, "offset": offset}
    
    try:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return format_json_response(data)
        
    except httpx.HTTPError as e:
        return f"Error getting datasets: {str(e)}"


@mcp.tool()
async def get_images_in_dataset(
    dataset_id: Annotated[int, "The ID of the dataset"],
    limit: Annotated[int, "Maximum number of results to return"] = 100,
    offset: Annotated[int, "Offset for pagination"] = 0
) -> str:
    """List images in a dataset.
    
    Returns a list of images contained in the specified dataset.
    """
    url = f"{IDR_BASE_URL}/api/v0/m/datasets/{dataset_id}/images/"
    params = {"limit": limit, "offset": offset}
    
    try:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return format_json_response(data)
        
    except httpx.HTTPError as e:
        return f"Error getting images in dataset: {str(e)}"


@mcp.tool()
async def get_plate_grid(
    plate_id: Annotated[int, "The ID of the plate"],
    field: Annotated[int, "Field index (0-based)"] = 0
) -> str:
    """Retrieve plate grid with wells and images.
    
    Returns the grid structure of a plate showing wells and their images.
    The field parameter specifies which field of view to retrieve (typically 0 for the first field).
    """
    url = f"{IDR_BASE_URL}/webgateway/plate/{plate_id}/{field}/"
    
    try:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        return format_json_response(data)
        
    except httpx.HTTPError as e:
        return f"Error getting plate grid: {str(e)}"


@mcp.tool()
async def get_image_metadata(
    image_id: Annotated[int, "The ID of the image"]
) -> str:
    """Get detailed metadata about an image.
    
    Returns comprehensive metadata including dimensions (width, height, z-stacks, 
    channels, timepoints), pixel size, channel information, and acquisition details.
    """
    url = f"{IDR_BASE_URL}/webclient/imgData/{image_id}/"
    
    try:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        return format_json_response(data)
        
    except httpx.HTTPError as e:
        return f"Error getting image metadata: {str(e)}"


@mcp.tool()
async def get_annotations(
    object_type: Annotated[str, "Type of object: 'screen', 'plate', or 'image'"],
    object_id: Annotated[int, "The ID of the object"]
) -> str:
    """Get map annotations for an object.
    
    Map annotations contain key-value pairs with experimental metadata,
    gene information, phenotypes, and other scientific annotations.
    """
    url = f"{IDR_BASE_URL}/webclient/api/annotations/"
    params = {"type": "map", object_type: object_id}
    
    try:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return format_json_response(data)
        
    except httpx.HTTPError as e:
        return f"Error getting annotations: {str(e)}"


@mcp.tool()
async def get_thumbnail_url(
    image_id: Annotated[int, "The ID of the image"]
) -> str:
    """Get thumbnail URL for an image.
    
    Returns a URL that can be used to retrieve a thumbnail preview of the image.
    """
    url = f"{IDR_BASE_URL}/webclient/render_thumbnail/{image_id}/"
    return format_json_response({
        "image_id": image_id,
        "thumbnail_url": url
    })


@mcp.tool()
async def get_image_url(
    image_id: Annotated[int, "The ID of the image"]
) -> str:
    """Get rendered image URL.
    
    Returns a URL that can be used to retrieve a rendered version of the image.
    """
    url = f"{IDR_BASE_URL}/webclient/render_image/{image_id}/"
    return format_json_response({
        "image_id": image_id,
        "image_url": url
    })


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="IDR MCP Server")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    if args.debug:
        import logging
        import sys
        logging.basicConfig(level=logging.DEBUG)
        print("Debug mode enabled", file=sys.stderr)
    
    # Run in stdio mode (default for MCP)
    mcp.run()


def main():
    """Entry point for the MCP server (stdio mode by default)."""
    mcp.run()


def main_debug():
    """Entry point for debug mode."""
    import sys
    import logging
    logging.basicConfig(level=logging.DEBUG)
    print("IDR MCP Server - Debug mode enabled", file=sys.stderr)
    mcp.run()
