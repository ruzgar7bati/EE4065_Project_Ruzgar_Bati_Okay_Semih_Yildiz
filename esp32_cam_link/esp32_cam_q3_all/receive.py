import serial
import struct
import os

PORT = "COM4"
BAUD = 921600

# Receiver for ESP32 CAM all-in-one mode
# Receives original, downsampled, and upsampled images from same frame

ser = serial.Serial(
    PORT,
    BAUD,
    timeout=5,
    dsrdtr=False,
    rtscts=False
)

ser.setDTR(False)
ser.setRTS(False)

# Image type names
IMG_TYPES = {
    0: "original",
    1: "downsampled",
    2: "upsampled"
}

frame_count = 0
print("Waiting for frames from ESP32 CAM (all-in-one mode)...")
print("Will receive: original, downsampled, upsampled from each frame")
print("=" * 60)

while True:
    # Find sync word (0xAA 0x55)
    if ser.read(1) != b'\xAA':
        continue
    if ser.read(1) != b'\x55':
        continue

    # Read image type (1 byte)
    img_type_bytes = ser.read(1)
    if len(img_type_bytes) != 1:
        continue
    
    img_type = img_type_bytes[0]
    img_name = IMG_TYPES.get(img_type, f"unknown_{img_type}")

    # Read image size (4 bytes, little-endian)
    size_bytes = ser.read(4)
    if len(size_bytes) != 4:
        continue

    size = struct.unpack("<I", size_bytes)[0]

    # Read image data
    data = ser.read(size)
    if len(data) != size:
        print(f"Incomplete frame for {img_name}")
        continue

    # Save image with appropriate name
    if img_type == 0:  # Original - start of new frame set
        frame_count += 1
        print(f"\n--- Frame Set #{frame_count} ---")
    
    filename = f"{img_name}_{frame_count:03d}.jpg"
    with open(filename, "wb") as f:
        f.write(data)

    print(f"  Saved: {filename} ({size} bytes) - {img_name}")
    
    # If we received all three images, print summary
    if img_type == 2:  # Upsampled is the last one
        print(f"  ✓ Complete frame set #{frame_count} received")
        print("=" * 60)

