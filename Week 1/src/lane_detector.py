import cv2
import numpy as np
import json
import os

class LaneDetector:
    def __init__(self):
        # Pre-defined lane regions for each intersection
        self.lane_regions = self.load_lane_regions()
    
    def load_lane_regions(self):
        """Define lane regions for each intersection"""
        # Using more generic regions that should work with most intersection images
        return {
            'default': {
                'north_lane': [200, 0, 400, 150],    # Top region
                'south_lane': [200, 450, 400, 600],  # Bottom region  
                'east_lane': [450, 200, 600, 400],   # Right region
                'west_lane': [0, 200, 150, 400]      # Left region
            },
            'intersection_1': {
                'north_lane': [200, 0, 400, 150],
                'south_lane': [200, 450, 400, 600], 
                'east_lane': [450, 200, 600, 400],
                'west_lane': [0, 200, 150, 400]
            },
            'intersection_2': {
                'north_lane': [200, 0, 400, 150],
                'south_lane': [200, 450, 400, 600],
                'east_lane': [450, 200, 600, 400],
                'west_lane': [0, 200, 150, 400]
            },
            'intersection_3': {
                'north_lane': [200, 0, 400, 150],
                'south_lane': [200, 450, 400, 600],
                'east_lane': [450, 200, 600, 400],
                'west_lane': [0, 200, 150, 400]
            },
            'intersection_4': {
                'north_lane': [200, 0, 400, 150],
                'south_lane': [200, 450, 400, 600],
                'east_lane': [450, 200, 600, 400],
                'west_lane': [0, 200, 150, 400]
            },
            'intersection_5': {
                'north_lane': [200, 0, 400, 150],
                'south_lane': [200, 450, 400, 600],
                'east_lane': [450, 200, 600, 400],
                'west_lane': [0, 200, 150, 400]
            },
            'intersection_6': {
                'north_lane': [200, 0, 400, 150],
                'south_lane': [200, 450, 400, 600],
                'east_lane': [450, 200, 600, 400],
                'west_lane': [0, 200, 150, 400]
            },
            'intersection_7': {
                'north_lane': [200, 0, 400, 150],
                'south_lane': [200, 450, 400, 600],
                'east_lane': [450, 200, 600, 400],
                'west_lane': [0, 200, 150, 400]
            },
            'intersection_8': {
                'north_lane': [200, 0, 400, 150],
                'south_lane': [200, 450, 400, 600],
                'east_lane': [450, 200, 600, 400],
                'west_lane': [0, 200, 150, 400]
            },
            'intersection_9': {
                'north_lane': [200, 0, 400, 150],
                'south_lane': [200, 450, 400, 600],
                'east_lane': [450, 200, 600, 400],
                'west_lane': [0, 200, 150, 400]
            }
        }
    
    def get_vehicle_lane(self, vehicle_bbox, intersection_id='default'):
        """Determine which lane a vehicle is in based on its position"""
        x_center = (vehicle_bbox[0] + vehicle_bbox[2]) / 2
        y_center = (vehicle_bbox[1] + vehicle_bbox[3]) / 2
        
        # Use default if specific intersection not found
        if intersection_id not in self.lane_regions:
            intersection_id = 'default'
            
        lanes = self.lane_regions[intersection_id]
        
        for lane_name, region in lanes.items():
            x1, y1, x2, y2 = region
            if x1 <= x_center <= x2 and y1 <= y_center <= y2:
                return lane_name
        
        return 'unknown'