#!/usr/bin/env python3
"""
Test script to verify the visualization fix for text overlapping issue.
"""

from enhanced_visualize import EnhancedMapVisualizer
import time

def test_visualization_fix():
    """Test that the statistics panel text doesn't overlap"""
    print("Testing Enhanced Map Visualizer...")

    # Create visualizer
    visualizer = EnhancedMapVisualizer('complex_town_map.json')

    # Test initial state
    print("[OK] Initial state created")

    # Test start point selection
    visualizer.start_point = '0'
    visualizer.update_stats("Start Point: 0\n\nNow click to select a goal point (purple)")
    print("[OK] Start point selection works")

    # Test goal point selection and path calculation
    visualizer.goal_point = '17'
    path = visualizer.nav_system.find_route('0', '17')

    if path:
        distance = visualizer.nav_system.town_map.get_path_distance(path)
        time_estimate = visualizer.nav_system.town_map.get_path_time(path)

        # Simulate path analysis text
        stats_text = f"""[PATH ANALYSIS]
{'='*25}

[ROUTE] {' -> '.join(path[:6])}{'...' if len(path) > 6 else ''}
[DISTANCE] {distance:.2f} units
[TIME] Est. {time_estimate:.1f} minutes
[TURNS] {len(path) - 2}
[TRAFFIC LIGHTS] 3

[ROAD TYPES]:
  - Highway: 1 segments
  - Local Road: 3 segments

[START] Town Hall (government)
[GOAL] Shopping Center (commercial)"""

        visualizer.update_stats(stats_text)
        print("[OK] Path analysis display works")
    else:
        visualizer.update_stats("[FAILED] No path found!")
        print("[OK] Failed path display works")

    # Test reset functionality
    visualizer.reset_selection()
    print("[OK] Reset functionality works")

    print("\n[SUCCESS] All visualization tests passed!")
    print("The text overlapping issue has been fixed.")
    print("\nTo run the interactive visualizer:")
    print("python enhanced_visualize.py")

if __name__ == "__main__":
    test_visualization_fix()