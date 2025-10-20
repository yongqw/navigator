#!/usr/bin/env python3
"""
Demonstration script for the Complex Town Navigation System

This script showcases the capabilities of the enhanced navigation system
including complex traffic patterns, turn restrictions, and detailed path analysis.
"""

from navigation import NavigationSystem
import json

def demo_complex_navigation():
    """Demonstrate the complex navigation system capabilities"""
    print("="*60)
    print("COMPLEX TOWN NAVIGATION SYSTEM DEMO")
    print("="*60)

    # Initialize the navigation system with complex map
    nav_system = NavigationSystem('complex_town_map.json')
    town_map = nav_system.town_map

    # Display map information
    print(f"\n[MAP] {town_map.metadata.get('name', 'Unknown Town')}")
    print(f"   {town_map.metadata.get('description', 'No description')}")
    print(f"   Intersections: {town_map.metadata.get('intersections_count', len(town_map.get_all_intersections()))}")
    print(f"   Roads: {town_map.metadata.get('roads_count', len(town_map.get_all_roads()))}")

    # Show landmarks
    print(f"\n[LANDMARKS] ({len(town_map.landmarks)}):")
    for intersection_id, landmark in town_map.landmarks.items():
        pos = town_map.get_position(intersection_id)
        print(f"   - {landmark['name']} ({landmark['type']}) - Intersection {intersection_id} at {pos}")

    # Test different route scenarios
    test_routes = [
        ('0', '44', 'Town Hall to Riverside Park'),
        ('5', '17', 'Highway to Shopping Center'),
        ('28', '33', 'Residential North to Residential South'),
        ('22', '40', 'Industrial Zone to Park Entrance'),
        ('6', '42', 'Central Area Route')
    ]

    print(f"\n[ROUTE ANALYSIS]:")
    print("-"*60)

    for start, goal, description in test_routes:
        print(f"\n[ROUTE] {description}")
        print(f"   From: {start} ({town_map.get_landmark(start)['name'] if town_map.get_landmark(start) else 'Unknown'})")
        print(f"   To: {goal} ({town_map.get_landmark(goal)['name'] if town_map.get_landmark(goal) else 'Unknown'})")

        # Find path
        path = nav_system.find_route(start, goal)

        if path:
            distance = town_map.get_path_distance(path)
            time_estimate = town_map.get_path_time(path)

            print(f"   [SUCCESS] Path found: {' -> '.join(path[:8])}{'...' if len(path) > 8 else ''}")
            print(f"   [DISTANCE] {distance:.2f} units")
            print(f"   [TIME] Estimated time: {time_estimate:.1f} minutes")
            print(f"   [COMPLEXITY] Route complexity: {len(path)} intersections")

            # Analyze road types
            road_types = {}
            for i in range(len(path) - 1):
                road_type = town_map.get_road_type(path[i], path[i+1])
                road_type_name = road_type['type']
                road_types[road_type_name] = road_types.get(road_type_name, 0) + 1

            print(f"   [ROAD TYPES] Used:")
            for road_type, count in road_types.items():
                print(f"      - {road_type.replace('_', ' ').title()}: {count} segments")

        else:
            print(f"   [FAILED] No path found!")
            print(f"      This could be due to turn restrictions or one-way streets")

    # Show traffic restriction examples
    print(f"\n[TRAFFIC RESTRICTIONS]:")
    print("-"*60)

    restrictions = town_map.traffic_restrictions
    if restrictions.get('no_left_turn'):
        print(f"   [NO LEFT] {len(restrictions['no_left_turn'])} locations")
        for i, turn in enumerate(restrictions['no_left_turn'][:3]):
            print(f"      {i+1}. {turn}")

    if restrictions.get('no_right_turn'):
        print(f"   [NO RIGHT] {len(restrictions['no_right_turn'])} locations")
        for i, turn in enumerate(restrictions['no_right_turn'][:3]):
            print(f"      {i+1}. {turn}")

    if restrictions.get('no_u_turn'):
        print(f"   [NO U-TURN] {len(restrictions['no_u_turn'])} locations")
        for i, turn in enumerate(restrictions['no_u_turn'][:3]):
            print(f"      {i+1}. {turn}")

    # Demonstrate random route generation
    print(f"\n[RANDOM ROUTE GENERATION]:")
    print("-"*60)

    for i in range(3):
        start, goal, path = nav_system.random_route()
        if path is None:
            print(f"\n   Random Route {i+1}:")
            print(f"   From {start} to {goal}")
            print(f"   No path found!")
            continue

        distance = town_map.get_path_distance(path)
        time_estimate = town_map.get_path_time(path)

        print(f"\n   Random Route {i+1}:")
        print(f"   From {start} to {goal}")
        print(f"   Path: {' -> '.join(path[:5])}{'...' if len(path) > 5 else ''}")
        print(f"   Distance: {distance:.2f} units, Time: {time_estimate:.1f} minutes")

    print(f"\n" + "="*60)
    print("[COMPLETE] Demo completed! Run 'python enhanced_visualize.py' for interactive map.")
    print("="*60)

def analyze_connectivity():
    """Analyze the connectivity of the complex town map"""
    print("\n[CONNECTIVITY ANALYSIS]:")
    print("-"*60)

    nav_system = NavigationSystem('complex_town_map.json')
    town_map = nav_system.town_map

    # Count intersection types
    intersection_types = {}
    traffic_lights = 0

    for intersection_id in town_map.get_all_intersections():
        intersection_type = town_map.get_intersection_type(intersection_id)
        intersection_types[intersection_type] = intersection_types.get(intersection_type, 0) + 1

        if town_map.has_traffic_light(intersection_id):
            traffic_lights += 1

    print(f"   Intersection Types:")
    for intersection_type, count in intersection_types.items():
        print(f"      - {intersection_type.replace('_', ' ').title()}: {count}")

    print(f"   Traffic Lights: {traffic_lights}")

    # Count road types
    road_types = {}
    one_way_roads = 0

    for road in town_map.get_all_roads():
        start, end = road
        road_type = town_map.get_road_type(start, end)
        road_type_name = road_type['type']
        road_types[road_type_name] = road_types.get(road_type_name, 0) + 1

        if road_type.get('one_way', False):
            one_way_roads += 1

    print(f"\n   Road Types:")
    for road_type, count in road_types.items():
        print(f"      - {road_type.replace('_', ' ').title()}: {count} segments")

    print(f"   One-way roads: {one_way_roads}")

if __name__ == "__main__":
    demo_complex_navigation()
    analyze_connectivity()