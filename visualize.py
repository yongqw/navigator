import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
from navigation import NavigationSystem

class InteractiveMapVisualizer:
    def __init__(self, map_file):
        self.nav_system = NavigationSystem(map_file)
        self.fig, self.ax = plt.subplots(1, 1, figsize=(10, 10))
        self.start_point = None
        self.goal_point = None
        self.path_line = None
        self.setup_plot()
        
    def setup_plot(self):
        """Set up the basic map drawing elements"""
        # Draw roads
        for road in self.nav_system.town_map.get_all_roads():
            start_id, end_id = road
            start_pos = self.nav_system.town_map.get_position(start_id)
            end_pos = self.nav_system.town_map.get_position(end_id)
            x_coords = [start_pos[0], end_pos[0]]
            y_coords = [start_pos[1], end_pos[1]]
            self.ax.plot(x_coords, y_coords, 'black', linewidth=2)
            
        # Draw intersections
        for intersection_id in self.nav_system.town_map.get_all_intersections():
            pos = self.nav_system.town_map.get_position(intersection_id)
            self.ax.plot(pos[0], pos[1], 'ro', markersize=8)
            # Add intersection ID label
            self.ax.text(pos[0], pos[1]+0.2, intersection_id, fontsize=12, ha='center')
            
        # Set up axes
        self.ax.set_aspect('equal')
        self.ax.grid(True)
        self.ax.set_title("Interactive Town Navigation Map")
        
        # Connect mouse click event
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        
    def find_nearest_intersection(self, x, y):
        """Find the nearest intersection to the click position"""
        min_dist = float('inf')
        nearest_point = None
        
        for intersection_id in self.nav_system.town_map.get_all_intersections():
            pos = self.nav_system.town_map.get_position(intersection_id)
            dist = (pos[0] - x) ** 2 + (pos[1] - y) ** 2
            if dist < min_dist:
                min_dist = dist
                nearest_point = intersection_id
                
        return nearest_point
    
    def on_click(self, event):
        """Handle mouse click events"""
        if event.inaxes != self.ax:
            return
            
        # Find the nearest intersection
        point_id = self.find_nearest_intersection(event.xdata, event.ydata)
        if point_id is None:
            return
            
        point_pos = self.nav_system.town_map.get_position(point_id)
            
        if self.start_point is None:
            # Set start point
            self.start_point = point_id
            self.ax.plot(point_pos[0], point_pos[1], 'go', markersize=15, label='Start')
            self.ax.legend()
            plt.draw()
        elif self.goal_point is None and point_id != self.start_point:
            # Set goal point
            self.goal_point = point_id
            self.ax.plot(point_pos[0], point_pos[1], 'mo', markersize=15, label='Goal')
            plt.draw()
            
            # Calculate and draw path
            self.calculate_and_draw_path()
        else:
            # Reset selection
            self.reset_selection()
            self.start_point = point_id
            self.ax.plot(point_pos[0], point_pos[1], 'go', markersize=15, label='Start')
            self.ax.legend()
            plt.draw()
            
    def calculate_and_draw_path(self):
        """Calculate and draw the path"""
        if self.start_point is None or self.goal_point is None:
            return
            
        # Find shortest path
        path = self.nav_system.find_route(self.start_point, self.goal_point)
        
        if path is None:
            print("Cannot find a path")
            return
            
        # Draw path
        if self.path_line:
            self.path_line.remove()
            
        x_coords = [self.nav_system.town_map.get_position(point)[0] for point in path]
        y_coords = [self.nav_system.town_map.get_position(point)[1] for point in path]
        self.path_line, = self.ax.plot(x_coords, y_coords, 'b-', linewidth=3, marker='o', markersize=6)
        plt.draw()
        
    def reset_selection(self):
        """Reset selection"""
        self.start_point = None
        self.goal_point = None
        
        # Remove path line
        if self.path_line:
            self.path_line.remove()
            self.path_line = None
            
        # Redraw map
        self.ax.clear()
        self.setup_plot()
        plt.draw()
        
    def show(self):
        """Show the map"""
        plt.show()

# Example usage
if __name__ == "__main__":
    # Create interactive visualization object
    visualizer = InteractiveMapVisualizer('large_map_data.json')
    
    # Show map
    visualizer.show()