from collections import deque

def bfs_shortest_path_with_turns(town_map, start, goal):
    """
    Find the shortest path using breadth-first search (BFS), considering turn restrictions
    :param town_map: TownMap object
    :param start: Start node
    :param goal: Goal node
    :return: Shortest path list, or None if unreachable
    """
    if start == goal:
        return [start]
    
    # Queue stores nodes to visit, path to node, and previous node
    queue = deque([(start, [start], None)])
    # Record visited (node, previous node) pairs to handle turn restrictions
    visited = set()
    visited.add((start, None))
    
    while queue:
        current, path, previous = queue.popleft()
        
        # Traverse all neighbors of the current node
        for neighbor in town_map.get_neighbors(current):
            # Check if the turn is allowed
            if previous is not None and not town_map.is_turn_allowed(previous, current, neighbor):
                continue
                
            # Check if we've reached the goal
            if neighbor == goal:
                return path + [neighbor]
            
            # Check if we've visited this state
            if (neighbor, current) not in visited:
                visited.add((neighbor, current))
                queue.append((neighbor, path + [neighbor], current))
    
    # If queue is empty and we haven't found the goal node, there's no path
    return None

# Example usage
if __name__ == "__main__":
    from town_map import TownMap
    town = TownMap('large_map_data.json')
    
    start = '0'
    goal = '99'
    path = bfs_shortest_path_with_turns(town, start, goal)
    print(f"Shortest path from {start} to {goal}: {path}")