import os
import cv2
from ultralytics import YOLO

print("🚦 Testing YOLO Vehicle Detection...")
print("=" * 50)

try:
    # 1. Initialize YOLO
    print("1. Loading YOLO model...")
    model = YOLO('yolov8n.pt')
    print("   ✅ YOLO model loaded successfully!")
    
    # 2. Test on one sample image
    print("\n2. Testing on sample image...")
    test_image_path = "data/0/1.jpg"
    
    if os.path.exists(test_image_path):
        print(f"   📷 Testing on: {test_image_path}")
        
        # Run detection
        results = model(test_image_path)
        
        # Count vehicles
        vehicle_count = 0
        vehicle_types = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                
                # Count only vehicles
                if class_name in ['car', 'truck', 'bus', 'motorcycle']:
                    vehicle_count += 1
                    vehicle_types.append(class_name)
        
        print(f"   🎯 Detection Results:")
        print(f"      - Total vehicles detected: {vehicle_count}")
        print(f"      - Vehicle types: {list(set(vehicle_types))}")
        
        # 3. Show what YOLO can detect
        print(f"\n3. All objects detected:")
        all_objects = {}
        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                all_objects[class_name] = all_objects.get(class_name, 0) + 1
        
        for obj, count in all_objects.items():
            print(f"      - {obj}: {count}")
            
    else:
        print(f"   ❌ Test image not found: {test_image_path}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 Troubleshooting:")
    print("   - Make sure ultralytics is installed: pip install ultralytics")
    print("   - This will download yolov8n.pt automatically (~6MB)")