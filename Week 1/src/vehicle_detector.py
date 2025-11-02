import cv2
import numpy as np
from ultralytics import YOLO
import os
import json
from lane_detector import LaneDetector

class VehicleDetector:
    def __init__(self, model_path='yolov8n.pt'):
        print("🚦 Initializing Vehicle Detector with Lane Counting...")
        self.model = YOLO(model_path)
        self.vehicle_classes = ['car', 'truck', 'bus', 'motorcycle']
        self.lane_detector = LaneDetector()
        print("✅ Vehicle Detector ready!")
    
    def detect_vehicles_by_lane(self, image_path, intersection_id='default'):
        """Detect vehicles and count them by lane"""
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            return {}, []
        
        try:
            # Run YOLO inference
            results = self.model(image_path)
            
            # Initialize lane counts with all possible lanes
            lane_counts = {
                'north_lane': 0,
                'south_lane': 0, 
                'east_lane': 0,
                'west_lane': 0,
                'unknown': 0,
                'total': 0
            }
            
            vehicle_details = []
            
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    class_id = int(box.cls[0])
                    class_name = self.model.names[class_id]
                    confidence = float(box.conf[0])
                    bbox = box.xyxy[0].tolist()
                    
                    # Count only vehicles
                    if class_name in self.vehicle_classes:
                        # Determine which lane the vehicle is in
                        lane = self.lane_detector.get_vehicle_lane(bbox, intersection_id)
                        lane_counts[lane] += 1
                        lane_counts['total'] += 1
                        
                        vehicle_details.append({
                            'class': class_name,
                            'confidence': round(confidence, 2),
                            'bbox': bbox,
                            'lane': lane
                        })
            
            return lane_counts, vehicle_details
            
        except Exception as e:
            print(f"❌ Error processing {image_path}: {e}")
            # Return empty but properly structured counts
            empty_counts = {
                'north_lane': 0, 'south_lane': 0, 'east_lane': 0, 
                'west_lane': 0, 'unknown': 0, 'total': 0
            }
            return empty_counts, []
    
    def process_intersection_by_lane(self, folder_path, intersection_id):
        """Process all images for a specific intersection with lane counting"""
        print(f"\n🛣️ Processing Intersection {intersection_id} with Lane Analysis...")
        
        # Get absolute path
        abs_folder_path = os.path.abspath(folder_path)
        print(f"   Looking in: {abs_folder_path}")
        
        if not os.path.exists(abs_folder_path):
            print(f"❌ Folder not found: {abs_folder_path}")
            return {}
        
        intersection_data = {}
        
        # Process each image (1.jpg to 9.jpg)
        for i in range(1, 10):
            image_file = f"{i}.jpg"
            image_path = os.path.join(abs_folder_path, image_file)
            
            if os.path.exists(image_path):
                lane_counts, vehicle_details = self.detect_vehicles_by_lane(image_path, f"intersection_{i}")
                intersection_data[image_file] = {
                    'lane_counts': lane_counts,
                    'vehicles': vehicle_details
                }
                
                # Print lane-wise summary
                print(f"   📊 {image_file}:")
                lanes_with_vehicles = False
                for lane, count in lane_counts.items():
                    if lane != 'total' and lane != 'unknown' and count > 0:
                        print(f"      {lane}: {count} vehicles")
                        lanes_with_vehicles = True
                if not lanes_with_vehicles:
                    print(f"      No vehicles detected in defined lanes")
                print(f"      TOTAL: {lane_counts['total']} vehicles")
                
            else:
                print(f"   ❌ Image not found: {image_path}")
        
        return intersection_data

    def save_results(self, data, filename):
        """Save detection results to JSON file"""
        results_dir = 'results'
        os.makedirs(results_dir, exist_ok=True)
        
        filepath = os.path.join(results_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"💾 Results saved to: {filepath}")