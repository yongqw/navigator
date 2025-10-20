import json

class TownMap:
    def __init__(self, map_file):
        self.intersections = {}
        self.roads = []
        self._load_map(map_file)
        
    def _load_map(self, map_file):
        """Load map data from JSON file"""
        with open(map_file, 'r', encoding='utf-8') as f:
            map_data = json.load(f)
            
        # Load intersections
        for id, data in map_data['intersections'].items():
            self.intersections[id] = {
                'position': (data['x'], data['y']),
                'turns': data.get('turns', {}),
                'neighbors': []
            }
            
            # Build neighbors list from turns
            for direction, neighbor in data.get('turns', {}).items():
                if neighbor not in self.intersections[id]['neighbors']:
                    self.intersections[id]['neighbors'].append(neighbor)
                    
        # Build roads list
        for id, data in self.intersections.items():
            for neighbor in data['neighbors']:
                # Ensure we don't duplicate roads (only add each road once)
                if (neighbor, id) not in self.roads:
                    self.roads.append((id, neighbor))
                    
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
                    # This is a simplified check - in a more complex system, we might need
                    # to store more detailed turn information
                    if from_intersection in self.intersections[through_intersection]['neighbors']:
                        return True
                        
        return False

# Example usage
if __name__ == "__main__":
    town = TownMap('large_map_data.json')
    print("Intersections:", town.get_all_intersections())
    print("Roads:", town.get_all_roads())