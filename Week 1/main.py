import os
import sys
import json

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from vehicle_detector import VehicleDetector

def main():
    print("🚦 Starting Green Traffic Analyzer - LANE-BASED ANALYSIS")
    print("=" * 60)
    
    # Initialize and run detector
    detector = VehicleDetector()
    
    # Process both timeframes with lane counting
    all_results = {}
    
    for timeframe in ['0', '5']:
        print(f"\n{'='*60}")
        print(f"⏰ PROCESSING TIMEFRAME: {timeframe} seconds - LANE ANALYSIS")
        print(f"{'='*60}")
        
        folder_path = f"data/{timeframe}"
        results = detector.process_intersection_by_lane(folder_path, f"time_{timeframe}")
        all_results[f"time_{timeframe}"] = results
    
    # Save results
    results_dir = 'results'
    os.makedirs(results_dir, exist_ok=True)
    
    results_file = os.path.join(results_dir, 'lane_vehicle_detection_results.json')
    with open(results_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"💾 Results saved to: {results_file}")
    
    # Print intelligent summary
    print(f"\n🎯 INTELLIGENT TRAFFIC ANALYSIS:")
    print(f"{'='*50}")
    
    for timeframe, data in all_results.items():
        print(f"\n📈 {timeframe} SUMMARY:")
        
        # Find which direction has most traffic on average
        lane_totals = {'north_lane': 0, 'south_lane': 0, 'east_lane': 0, 'west_lane': 0}
        total_vehicles = 0
        
        for image_file, image_data in data.items():
            if 'lane_counts' in image_data:
                lane_counts = image_data['lane_counts']
                for lane in lane_totals.keys():
                    lane_totals[lane] += lane_counts[lane]
                total_vehicles += lane_counts['total']
        
        if total_vehicles > 0:
            # Find busiest lane
            busiest_lane = max(lane_totals, key=lane_totals.get)
            print(f"   🚦 Busiest direction: {busiest_lane} ({lane_totals[busiest_lane]} vehicles)")
            print(f"   📊 Lane distribution:")
            for lane, total in lane_totals.items():
                percentage = (total / total_vehicles) * 100 if total_vehicles > 0 else 0
                print(f"      {lane}: {total} vehicles ({percentage:.1f}%)")
            print(f"   🚗 Total vehicles: {total_vehicles}")
        else:
            print("   ❌ No vehicles detected")

if __name__ == "__main__":
    main()