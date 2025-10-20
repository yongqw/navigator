# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based town navigation system that provides pathfinding capabilities with turn restrictions. The system can find shortest paths between intersections on a map while respecting traffic rules and provides interactive visualization.

## Core Architecture

The project consists of four main modules:

1. **TownMap (`town_map.py`)** - Map data structure and graph representation
   - Loads intersection and road data from JSON files
   - Manages turn restrictions and connectivity
   - Provides methods to query neighbors, positions, and turn permissions

2. **Pathfinding (`pathfinding.py`)** - Graph traversal algorithms
   - Implements BFS shortest path algorithm with turn restriction awareness
   - Tracks state as (current_node, previous_node) to handle turn rules
   - Returns path as list of intersection IDs or None if unreachable

3. **NavigationSystem (`navigation.py`)** - High-level navigation interface
   - Coordinates map operations and pathfinding
   - Provides convenience methods for finding routes and random route generation
   - Main API for other components to use navigation features

4. **InteractiveMapVisualizer (`visualize.py`)** - GUI for interactive pathfinding
   - Matplotlib-based interactive map with click-to-select functionality
   - Visual representation of roads, intersections, and calculated paths
   - Real-time path calculation between selected points

## Map Data Format

The system uses JSON files for map data:
- **`large_map_data.json`** - 10x10 grid with turn restrictions (main test map)
- **`map_data.json`** - Simple 3x3 grid without turn restrictions (basic example)

Intersection format:
```json
"intersection_id": {
  "x": coordinate,
  "y": coordinate,
  "turns": {
    "direction": "neighbor_id",
    ...
  }
}
```

## Common Commands

### Running the System
```bash
# Interactive map visualization
python visualize.py

# Command-line route finding
python navigation.py

# Test pathfinding directly
python pathfinding.py

# Explore map structure
python town_map.py
```

### Dependencies
```bash
# Install required packages
pip install -r requirements.txt

# Current dependencies:
# - numpy==2.3.4
# - matplotlib==3.10.7
```

## Development Guidelines

### Key Design Patterns
- **State-aware pathfinding**: The BFS algorithm tracks both current and previous nodes to handle turn restrictions correctly
- **Separation of concerns**: Clear distinction between map data structure, pathfinding algorithms, and user interface
- **JSON configuration**: Map data is externalized for easy modification and testing

### Important Implementation Details
- Turn restrictions are enforced by checking if a turn from `prev → current → next` is allowed in `TownMap.is_turn_allowed()`
- The BFS queue stores tuples of `(current, path, previous)` to maintain turn context
- Interactive visualization uses matplotlib event handling for click-based point selection
- Map loading automatically builds neighbor lists from turn definitions

### Testing Maps
- Use `map_data.json` for basic functionality testing (3x3 grid, simple connections)
- Use `large_map_data.json` for comprehensive testing (10x10 grid with complex turn restrictions)
- The system gracefully handles unreachable destinations by returning `None`

### Common Extension Points
- Add new pathfinding algorithms alongside the existing BFS implementation
- Extend the visualization with additional features like route statistics or alternative paths
- Modify the map data format to support weighted edges or one-way streets
- Add support for real-time traffic conditions or dynamic routing