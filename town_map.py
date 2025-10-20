import json

class TownMap:
    def __init__(self, map_file):
        self.intersections = {}
        self.roads = []
        self.road_types = {}
        self.traffic_restrictions = {}
        self.landmarks = {}
        self.metadata = {}
        self._load_map(map_file)

    def _load_map(self, map_file):
        """Load map data from JSON file"""
        with open(map_file, 'r', encoding='utf-8') as f:
            map_data = json.load(f)

        # Load metadata
        self.metadata = map_data.get('metadata', {})

        # Load intersections
        for id, data in map_data['intersections'].items():
            self.intersections[id] = {
                'position': (data['x'], data['y']),
                'turns': data.get('turns', {}),
                'neighbors': [],
                'type': data.get('type', 'intersection'),
                'traffic_light': data.get('traffic_light', False)
            }

            # Build neighbors list from turns
            for direction, neighbor in data.get('turns', {}).items():
                if neighbor not in self.intersections[id]['neighbors']:
                    self.intersections[id]['neighbors'].append(neighbor)

        # Build roads list and load road types
        self.road_types = map_data.get('road_types', {})
        for id, data in self.intersections.items():
            for neighbor in data['neighbors']:
                # Ensure we don't duplicate roads (only add each road once)
                road_key = f"{id}-{neighbor}"
                reverse_key = f"{neighbor}-{id}"
                if (neighbor, id) not in self.roads:
                    self.roads.append((id, neighbor))
                    # Add default road type if not specified
                    if road_key not in self.road_types and reverse_key not in self.road_types:
                        self.road_types[road_key] = {
                            'type': 'local_road',
                            'speed_limit': 30,
                            'lanes': 1,
                            'one_way': False
                        }

        # Load traffic restrictions
        self.traffic_restrictions = map_data.get('traffic_restrictions', {})

        # Load landmarks
        self.landmarks = map_data.get('landmarks', {})
                    
    def get_neighbors(self, intersection):
        """Get neighbors of a specified intersection"""
        return self.intersections[intersection]['neighbors']
    
    def get_all_intersections(self):
        """Get all intersections"""
        return list(self.intersections.keys())
    
    def get_all_roads(self):
        """Get all roads"""
        return self.roads
    
    def get_position(self, intersection):
        """Get the coordinates of an intersection"""
        return self.intersections[intersection]['position']
    
    def is_turn_allowed(self, from_intersection, through_intersection, to_intersection):
        """Check if a turn is allowed at a specified intersection"""
        # Check if the turn is allowed based on the turns definition
        if through_intersection in self.intersections:
            turns = self.intersections[through_intersection]['turns']
            # Check if there's a direct turn from from_intersection to to_intersection
            for direction, neighbor in turns.items():
                if neighbor == to_intersection:
                    # Check if from_intersection is a valid incoming road for this turn
                    if from_intersection in self.intersections[through_intersection]['neighbors']:
                        # Check traffic restrictions
                        turn_key = f"{from_intersection}-{through_intersection}-{to_intersection}"
                        if turn_key in self.traffic_restrictions.get('no_left_turn', []):
                            return False
                        if turn_key in self.traffic_restrictions.get('no_right_turn', []):
                            return False
                        if turn_key in self.traffic_restrictions.get('no_u_turn', []):
                            return False
                        return True
        return False

    def get_road_type(self, from_intersection, to_intersection):
        """Get road type information for a road"""
        road_key = f"{from_intersection}-{to_intersection}"
        reverse_key = f"{to_intersection}-{from_intersection}"

        if road_key in self.road_types:
            return self.road_types[road_key]
        elif reverse_key in self.road_types:
            return self.road_types[reverse_key]
        else:
            return {
                'type': 'local_road',
                'speed_limit': 30,
                'lanes': 1,
                'one_way': False
            }

    def get_intersection_type(self, intersection):
        """Get intersection type"""
        return self.intersections[intersection].get('type', 'intersection')

    def has_traffic_light(self, intersection):
        """Check if intersection has traffic light"""
        return self.intersections[intersection].get('traffic_light', False)

    def get_landmark(self, intersection):
        """Get landmark information for an intersection"""
        return self.landmarks.get(intersection, None)

    def get_road_distance(self, from_intersection, to_intersection):
        """Calculate distance between two intersections"""
        from_pos = self.get_position(from_intersection)
        to_pos = self.get_position(to_intersection)
        return ((from_pos[0] - to_pos[0]) ** 2 + (from_pos[1] - to_pos[1]) ** 2) ** 0.5

    def get_path_distance(self, path):
        """Calculate total distance for a path"""
        if not path or len(path) < 2:
            return 0
        total_distance = 0
        for i in range(len(path) - 1):
            total_distance += self.get_road_distance(path[i], path[i+1])
        return total_distance

    def get_path_time(self, path):
        """Calculate estimated travel time for a path (in minutes)"""
        if not path or len(path) < 2:
            return 0
        total_time = 0
        for i in range(len(path) - 1):
            distance = self.get_road_distance(path[i], path[i+1])
            road_type = self.get_road_type(path[i], path[i+1])
            speed_limit = road_type['speed_limit']  # km/h
            # Convert distance to km and calculate time
            distance_km = distance * 0.1  # assuming 1 unit = 100m
            time_hours = distance_km / speed_limit
            total_time += time_hours * 60  # convert to minutes
        return total_time

# Example usage
if __name__ == "__main__":
    town = TownMap('large_map_data.json')
    print("Intersections:", town.get_all_intersections())
    print("Roads:", town.get_all_roads())