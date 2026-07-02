import os
from PIL import Image

def test_images_generated():
    expected_frames = [f"frame_{i:02d}.png" for i in range(1, 21)]
    for frame in expected_frames:
        path = os.path.join("generated_images", frame)
        assert os.path.exists(path), f"{frame} is missing"
        with Image.open(path) as img:
            assert img.size == (1920, 1080), f"{frame} has wrong size: {img.size}"
            assert img.format == "PNG", f"{frame} is not a PNG"
    print("All 20 images verified successfully.")

if __name__ == "__main__":
    try:
        test_images_generated()
    except AssertionError as e:
        print(f"Test failed: {e}")
        exit(1)
