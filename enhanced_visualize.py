import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np
from navigation import NavigationSystem

class EnhancedMapVisualizer:
    def __init__(self, map_file):
        self.nav_system = NavigationSystem(map_file)
        self.fig, (self.ax_map, self.ax_stats) = plt.subplots(1, 2, figsize=(16, 8))
        self.start_point = None
        self.goal_point = None
        self.path_line = None
        self.setup_plot()

    def setup_plot(self):
        """Set up the enhanced map drawing elements"""
        self.ax_map.set_aspect('equal')
        self.ax_map.grid(True, alpha=0.3)
        self.ax_map.set_title(f"Enhanced Town Navigation: {self.nav_system.town_map.metadata.get('name', 'Unknown Town')}", fontsize=14, fontweight='bold')

        # Draw roads with different styles based on type
        for road in self.nav_system.town_map.get_all_roads():
            start_id, end_id = road
            start_pos = self.nav_system.town_map.get_position(start_id)
            end_pos = self.nav_system.town_map.get_position(end_id)

            road_type = self.nav_system.town_map.get_road_type(start_id, end_id)
            self.draw_road(start_pos, end_pos, road_type)

        # Draw intersections with enhanced styling
        for intersection_id in self.nav_system.town_map.get_all_intersections():
            pos = self.nav_system.town_map.get_position(intersection_id)
            self.draw_intersection(intersection_id, pos)

        # Draw landmarks
        for intersection_id, landmark in self.nav_system.town_map.landmarks.items():
            pos = self.nav_system.town_map.get_position(intersection_id)
            self.draw_landmark(pos, landmark)

        # Set up statistics panel
        self.setup_stats_panel()

        # Initialize with instruction text
        self.update_stats("Click on the map to select a starting point (green)")

        # Connect mouse click event
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)

    def draw_road(self, start_pos, end_pos, road_type):
        """Draw road with style based on type"""
        x_coords = [start_pos[0], end_pos[0]]
        y_coords = [start_pos[1], end_pos[1]]

        # Road styling based on type
        if road_type['type'] == 'highway':
            color = 'red'
            linewidth = 4
            alpha = 0.8
        elif road_type['type'] == 'main_road':
            color = 'blue'
            linewidth = 3
            alpha = 0.7
        elif road_type['type'] == 'secondary_road':
            color = 'green'
            linewidth = 2
            alpha = 0.6
        else:  # local_road
            color = 'gray'
            linewidth = 1.5
            alpha = 0.5

        self.ax_map.plot(x_coords, y_coords, color=color, linewidth=linewidth, alpha=alpha)

        # Draw one-way arrow if applicable
        if road_type.get('one_way', False):
            mid_x = (start_pos[0] + end_pos[0]) / 2
            mid_y = (start_pos[1] + end_pos[1]) / 2
            dx = end_pos[0] - start_pos[0]
            dy = end_pos[1] - start_pos[1]
            self.ax_map.arrow(mid_x - dx*0.1, mid_y - dy*0.1, dx*0.2, dy*0.2,
                            head_width=0.2, head_length=0.1, fc='black', ec='black', alpha=0.7)

    def draw_intersection(self, intersection_id, pos):
        """Draw intersection with enhanced styling"""
        intersection_type = self.nav_system.town_map.get_intersection_type(intersection_id)
        has_traffic_light = self.nav_system.town_map.has_traffic_light(intersection_id)

        # Choose marker based on intersection type
        if intersection_type == 'dead_end':
            marker = 's'
            color = 'orange'
            size = 8
        else:
            marker = 'o'
            color = 'red' if has_traffic_light else 'darkblue'
            size = 10 if has_traffic_light else 8

        self.ax_map.plot(pos[0], pos[1], marker=marker, color=color, markersize=size,
                        markeredgecolor='black', markeredgewidth=1)

        # Add intersection ID label
        self.ax_map.text(pos[0], pos[1]+0.3, intersection_id, fontsize=8, ha='center',
                        fontweight='bold', bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))

        # Add traffic light indicator
        if has_traffic_light:
            circle = plt.Circle((pos[0]+0.3, pos[1]+0.3), 0.1, color='yellow', alpha=0.8)
            self.ax_map.add_patch(circle)

    def draw_landmark(self, pos, landmark):
        """Draw landmark on the map"""
        # Choose marker based on landmark type
        landmark_markers = {
            'government': ('s', 'purple'),
            'commercial': ('D', 'orange'),
            'industrial': ('^', 'brown'),
            'residential': ('v', 'green'),
            'recreation': ('o', 'darkgreen'),
            'transport': ('*', 'red')
        }

        marker, color = landmark_markers.get(landmark['type'], ('h', 'gray'))
        self.ax_map.plot(pos[0]-0.5, pos[1]+0.5, marker=marker, color=color, markersize=8,
                        markeredgecolor='black', markeredgewidth=1)
        self.ax_map.text(pos[0]-0.5, pos[1]+0.8, landmark['name'], fontsize=6, ha='center',
                        style='italic', color='darkgreen', fontweight='bold')

    def setup_stats_panel(self):
        """Set up the statistics panel"""
        self.ax_stats.axis('off')
        self.ax_stats.set_title('Path Analysis', fontsize=12, fontweight='bold')
        self.stats_text = self.ax_stats.text(0.1, 0.9, '', transform=self.ax_stats.transAxes,
                                            fontsize=10, verticalalignment='top', fontfamily='monospace')

        # Add legend
        self.add_legend()

    def add_legend(self):
        """Add legend for road types and symbols"""
        legend_elements = [
            plt.Line2D([0], [0], color='red', linewidth=4, label='Highway (80 km/h)'),
            plt.Line2D([0], [0], color='blue', linewidth=3, label='Main Road (50 km/h)'),
            plt.Line2D([0], [0], color='green', linewidth=2, label='Secondary Road (40 km/h)'),
            plt.Line2D([0], [0], color='gray', linewidth=1.5, label='Local Road (30 km/h)'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=8,
                      markeredgecolor='black', label='Traffic Light', linestyle='None'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='darkblue', markersize=8,
                      markeredgecolor='black', label='Intersection', linestyle='None'),
            plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='orange', markersize=8,
                      markeredgecolor='black', label='Dead End', linestyle='None'),
        ]

        self.ax_stats.legend(handles=legend_elements, loc='lower left', fontsize=8)

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
        if event.inaxes != self.ax_map:
            return

        # Find the nearest intersection
        point_id = self.find_nearest_intersection(event.xdata, event.ydata)
        if point_id is None:
            return

        point_pos = self.nav_system.town_map.get_position(point_id)

        if self.start_point is None:
            # Set start point
            self.start_point = point_id
            self.ax_map.plot(point_pos[0], point_pos[1], 'go', markersize=15,
                           label='Start', markeredgecolor='black', markeredgewidth=2)
            self.ax_map.legend(loc='upper right', fontsize=8)
            self.update_stats(f"Start Point: {point_id}\n\nNow click to select a goal point (purple)")
            self.fig.canvas.draw_idle()
        elif self.goal_point is None and point_id != self.start_point:
            # Set goal point
            self.goal_point = point_id
            self.ax_map.plot(point_pos[0], point_pos[1], 'mo', markersize=15,
                           label='Goal', markeredgecolor='black', markeredgewidth=2)
            self.ax_map.legend(loc='upper right', fontsize=8)
            self.fig.canvas.draw_idle()

            # Calculate and draw path
            self.calculate_and_draw_path()
        else:
            # Reset selection
            self.reset_selection()
            self.start_point = point_id
            self.ax_map.plot(point_pos[0], point_pos[1], 'go', markersize=15,
                           label='Start', markeredgecolor='black', markeredgewidth=2)
            self.ax_map.legend(loc='upper right', fontsize=8)
            self.update_stats(f"Start Point: {point_id}\n\nNow click to select a goal point (purple)")
            self.fig.canvas.draw_idle()

    def calculate_and_draw_path(self):
        """Calculate and draw the path with detailed analysis"""
        if self.start_point is None or self.goal_point is None:
            return

        # Find shortest path
        path = self.nav_system.find_route(self.start_point, self.goal_point)

        if path is None:
            self.update_stats("[FAILED] No path found!\n\nThis could be due to:\n- Turn restrictions\n- One-way streets\n- Disconnected areas")
            return

        # Draw path
        if self.path_line:
            self.path_line.remove()

        x_coords = [self.nav_system.town_map.get_position(point)[0] for point in path]
        y_coords = [self.nav_system.town_map.get_position(point)[1] for point in path]
        self.path_line, = self.ax_map.plot(x_coords, y_coords, 'purple', linewidth=3,
                                         marker='o', markersize=4, alpha=0.8,
                                         markeredgecolor='black', markeredgewidth=1)

        # Calculate path statistics
        distance = self.nav_system.town_map.get_path_distance(path)
        time_estimate = self.nav_system.town_map.get_path_time(path)

        # Analyze path composition
        road_types = {}
        turns = 0
        traffic_lights = 0

        for i in range(len(path) - 1):
            road_type = self.nav_system.town_map.get_road_type(path[i], path[i+1])
            road_type_name = road_type['type']
            road_types[road_type_name] = road_types.get(road_type_name, 0) + 1

            if self.nav_system.town_map.has_traffic_light(path[i+1]):
                traffic_lights += 1

        turns = len(path) - 2  # Number of turns = waypoints - start - end

        # Format statistics
        route_display = ' -> '.join(path[:6])
        if len(path) > 6:
            route_display += '...'

        stats_text = f"""[PATH ANALYSIS]
{'='*25}

[ROUTE] {route_display}
[DISTANCE] {distance:.2f} units
[TIME] Est. {time_estimate:.1f} minutes
[TURNS] {turns}
[TRAFFIC LIGHTS] {traffic_lights}

[ROAD TYPES]:
"""
        for road_type, count in road_types.items():
            stats_text += f"  - {road_type.replace('_', ' ').title()}: {count} segments\n"

        # Add landmark information
        start_landmark = self.nav_system.town_map.get_landmark(self.start_point)
        goal_landmark = self.nav_system.town_map.get_landmark(self.goal_point)

        if start_landmark:
            stats_text += f"\n[START] {start_landmark['name']} ({start_landmark['type']})"
        if goal_landmark:
            stats_text += f"\n[GOAL] {goal_landmark['name']} ({goal_landmark['type']})"

        self.update_stats(stats_text)

    def update_stats(self, text):
        """Update statistics panel"""
        # Clear the statistics axes
        self.ax_stats.clear()
        self.ax_stats.axis('off')
        self.ax_stats.set_title('Path Analysis', fontsize=12, fontweight='bold')

        # Recreate the text object
        self.stats_text = self.ax_stats.text(0.1, 0.9, text, transform=self.ax_stats.transAxes,
                                            fontsize=10, verticalalignment='top', fontfamily='monospace')

        # Re-add legend
        self.add_legend()

        # Redraw
        self.fig.canvas.draw_idle()

    def reset_selection(self):
        """Reset selection"""
        self.start_point = None
        self.goal_point = None

        # Remove path line
        if self.path_line:
            self.path_line.remove()
            self.path_line = None

        # Redraw map
        self.ax_map.clear()
        self.setup_plot()
        self.update_stats("Click on the map to select a starting point (green)")
        self.fig.canvas.draw_idle()

    def show(self):
        """Show the map"""
        plt.tight_layout()
        plt.show()

# Example usage
if __name__ == "__main__":
    # Create enhanced visualization object
    visualizer = EnhancedMapVisualizer('complex_town_map.json')

    # Show map
    visualizer.show()