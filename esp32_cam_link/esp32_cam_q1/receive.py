import serial
import struct
import numpy as np
from PIL import Image

PORT = "COM4"
BAUD = 921600

WIDTH = 96
HEIGHT = 96

ser = serial.Serial(
    PORT,
    BAUD,
    timeout=5,
    dsrdtr=False,
    rtscts=False
)

ser.setDTR(False)
ser.setRTS(False)

img_count = 0
print("Receiving binary images... Press Ctrl+C to stop.")

try:
    while True:
        # Sync
        if ser.read(1) != b'\xAA':
            continue
        if ser.read(1) != b'\x55':
            continue

        # Length
        size_bytes = ser.read(4)
        size = struct.unpack("<I", size_bytes)[0]

        # Data
        data = ser.read(size)
        if len(data) != size:
            print("Incomplete frame")
            continue

        img = np.frombuffer(data, dtype=np.uint8)
        img = img.reshape((HEIGHT, WIDTH))

        image = Image.fromarray(img, mode='L')
        filename = f"binary.png"
        image.save(filename)

        print(f"Saved {filename}")
        img_count += 1

except KeyboardInterrupt:
    print("\nStopped by user.")
    ser.close()
