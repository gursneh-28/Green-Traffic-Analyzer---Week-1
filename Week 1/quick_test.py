import os

print("🔍 Checking Dataset Contents...")
print("=" * 40)

# Check each folder
folders = ['data/0', 'data/5', 'data/predicted0', 'data/predicted5']

for folder in folders:
    print(f"\n📁 {folder}:")
    if os.path.exists(folder):
        files = os.listdir(folder)
        image_files = [f for f in files if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        other_files = [f for f in files if not f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        
        print(f"   ✅ Found {len(image_files)} images")
        if image_files:
            print(f"   Sample: {image_files[:3]}")  # Show first 3 images
        if other_files:
            print(f"   Other files: {other_files}")
    else:
        print("   ❌ Folder not found")

print("\n" + "=" * 40)
print("📊 Summary:")
total_images = sum([len([f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]) 
                   for folder in folders if os.path.exists(folder)])
print(f"   Total images across all folders: {total_images}")