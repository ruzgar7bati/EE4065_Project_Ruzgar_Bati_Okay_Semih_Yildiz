import serial
import struct

PORT = "COM4"
BAUD = 921600

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
print("Waiting for frames...")

while True:
    # Find sync word
    if ser.read(1) != b'\xAA':
        continue
    if ser.read(1) != b'\x55':
        continue

    # Read image size
    size_bytes = ser.read(4)
    if len(size_bytes) != 4:
        continue

    size = struct.unpack("<I", size_bytes)[0]

    # Read image
    data = ser.read(size)
    if len(data) != size:
        print("Incomplete frame")
        continue

    img_count += 1
    filename = f"image_{img_count:03}.jpg"
    with open(filename, "wb") as f:
        f.write(data)

    print(f"Saved {filename} ({size} bytes)")
