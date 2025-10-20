import random
from town_map import TownMap
from pathfinding import bfs_shortest_path_with_turns

class NavigationSystem:
    def __init__(self, map_file):
        self.town_map = TownMap(map_file)
        
    def find_route(self, start, goal):
        """
        Find the shortest path from start to goal
        :param start: Start point ID
        :param goal: Goal point ID
        :return: Shortest path list
        """
        # Use BFS to find the shortest path, considering turn restrictions
        return bfs_shortest_path_with_turns(self.town_map, start, goal)
    
    def random_route(self):
        """
        Randomly select a start and goal point, and calculate the shortest path
        :return: (start, goal, path)
        """
        intersections = self.town_map.get_all_intersections()
        start = random.choice(intersections)
        goal = random.choice(intersections)
        
        while goal == start:
            goal = random.choice(intersections)
            
        path = self.find_route(start, goal)
        return start, goal, path

# Example usage
if __name__ == "__main__":
    nav = NavigationSystem('large_map_data.json')
    start, goal, path = nav.random_route()
    print(f"Shortest path from {start} to {goal}: {path}")