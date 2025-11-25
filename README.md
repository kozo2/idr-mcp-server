# IDR MCP Server

This repository contains a Model Context Protocol (MCP) server providing access to the [Image Data Resource (IDR)](https://idr.openmicroscopy.org/) API. IDR is a public repository of reference image datasets from published scientific studies.

This server enables AI assistants to explore and query imaging data, including high-content screening studies, microscopy datasets, and associated scientific annotations.

## Features

The IDR MCP Server provides the following tools:

- **🔍 Search Studies**: Search for screens and projects in IDR
- **📊 Get Screen Info**: Retrieve detailed information about specific screens
- **📁 Get Project Info**: Retrieve detailed information about specific projects
- **🧫 Get Plates**: List plates in a screen with pagination support
- **📂 Get Datasets**: List datasets in a project
- **🖼️ Get Images in Dataset**: List images contained in a dataset
- **🔲 Get Plate Grid**: Retrieve plate grid structure with wells and images
- **📋 Get Image Metadata**: Get comprehensive image metadata (dimensions, channels, pixel size)
- **🏷️ Get Annotations**: Retrieve map annotations (key-value metadata) for objects
- **🖼️ Get Thumbnail URL**: Generate thumbnail URLs for images
- **🌐 Get Image URL**: Generate rendered image URLs

## Installation

### Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager

### Install uv (if not already installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Install the IDR MCP Server

```bash
# Clone the repository
git clone https://github.com/kozo2/idr-mcp-server.git
cd idr-mcp-server

# Install dependencies
uv sync

# Install as a tool (optional)
uv tool install .
```

## Configuration

### Claude Desktop Configuration

To use this server with Claude Desktop, add the following configuration to your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "idr-mcp-server": {
      "command": "uv",
      "args": [
        "tool",
        "run",
        "idr-mcp-server"
      ],
      "env": {}
    }
  }
}
```

### Alternative Configuration (if installed as tool)

If you installed the server as a uv tool, you can use this simpler configuration:

```json
{
  "mcpServers": {
    "idr-mcp-server": {
      "command": "idr-mcp-server",
      "args": [],
      "env": {}
    }
  }
}
```

## Usage Examples

Once configured with Claude Desktop, you can use natural language to interact with the IDR API:

### Exploring Studies

> "List all available screens in IDR"

> "Show me the projects available in the Image Data Resource"

### Getting Study Details

> "Get information about screen 102"

> "Tell me about project 51"

### Browsing Data Structure

> "Show me the plates in screen 1201"

> "List datasets in project 101"

> "What images are in dataset 369"

### Image Analysis

> "Get metadata for image 1884807"

> "What are the dimensions of image 1920093?"

### Accessing Annotations

> "What annotations are associated with image 1884807?"

> "Show me the metadata annotations for screen 102"

### Getting Image URLs

> "Get a thumbnail URL for image 1884807"

> "Generate a rendered image URL for image 1920093"

## API Documentation

The server interacts with the IDR API. For more information, see:

- [IDR API Documentation](https://idr.openmicroscopy.org/about/api.html)
- [IDR Website](https://idr.openmicroscopy.org/)

## Development Setup

### Setting up the Development Environment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kozo2/idr-mcp-server.git
   cd idr-mcp-server
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate  # macOS/Linux
   # or
   .venv\Scripts\activate     # Windows
   ```

### Code Quality

```bash
# Format code
uv run ruff format

# Lint code
uv run ruff check

# Type checking
uv run mypy src/
```

### Adding New Features

1. **Add new tools** in `src/idr_mcp_server/server.py` using the `@mcp.tool()` decorator
2. **Create models** in `src/idr_mcp_server/models.py` for structured responses
3. **Update tests** to cover new functionality
4. **Update documentation** as needed

## Troubleshooting

### Common Issues

1. **Server not found**: Ensure the path to the server is correct in your Claude config
2. **Permission errors**: Make sure the server script is executable
3. **Network errors**: Check your internet connection and firewall settings
4. **Python version**: Ensure you're using Python 3.12 or higher

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `uv run pytest`
5. Format code: `uv run ruff format`
6. Submit a pull request

## Acknowledgments

- [Image Data Resource (IDR)](https://idr.openmicroscopy.org/) for providing access to reference image datasets
- [Open Microscopy Environment (OME)](https://www.openmicroscopy.org/) for developing the OMERO platform and IDR
- [FastMCP](https://github.com/jlowin/fastmcp) for the MCP framework
- The scientific imaging community for contributing valuable reference datasets
