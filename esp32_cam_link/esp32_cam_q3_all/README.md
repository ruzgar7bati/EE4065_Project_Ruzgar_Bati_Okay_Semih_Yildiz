# ESP32 CAM Q3 All-in-One Version

This version captures **one frame** and sends **three versions**:
1. **Original** (160×120)
2. **Downsampled** (106×80, 2/3 scale)
3. **Upsampled** (240×180, 1.5x scale)

All three images come from the **exact same moment**, making comparison easier.

## Advantages

- ✅ All images from same frame (no camera movement issues)
- ✅ Better for side-by-side comparison
- ✅ Demonstrates complete pipeline in one cycle
- ✅ No need to keep camera perfectly stable

## Protocol

Each image is sent with:
- Sync bytes: `0xAA 0x55`
- Image type: 1 byte (0=original, 1=downsampled, 2=upsampled)
- Size: 4 bytes (little-endian)
- JPEG data: variable size

## Usage

### ESP32 Side
1. Upload `esp32_cam_q3_all.ino` to ESP32 CAM
2. Open Serial Monitor (921600 baud)
3. Wait for initialization message

### PC Side
1. Run `receive.py`:
   ```bash
   python receive.py
   ```
2. Update `PORT = "COM4"` if needed (check your COM port)

### Output Files

For each frame set, you'll get:
- `original_001.jpg` - Original 160×120 image
- `downsampled_001.jpg` - Downsampled 106×80 image
- `upsampled_001.jpg` - Upsampled 240×180 image

Files are numbered sequentially (001, 002, 003, ...)

## Memory Usage

- Original buffer: ~38 KB
- Downsampled buffer: ~17 KB
- Upsampled buffer: ~86 KB
- **Total: ~141 KB** (fits in ESP32 RAM)

## Timing

- Frame capture: ~20ms
- Processing: ~50-100ms
- Transmission: ~200-500ms (depends on JPEG size)
- **Total per frame set: ~1-2 seconds**

Delay between frame sets: 2 seconds (configurable in code)

## Troubleshooting

**No images received:**
- Check COM port in `receive.py`
- Verify baud rate is 921600
- Check Serial Monitor for ESP32 messages

**Incomplete frames:**
- Increase timeout in `receive.py`
- Check USB cable connection
- Reduce baud rate if unstable

**Memory issues:**
- If ESP32 crashes, reduce image quality (JPEG quality parameter)
- Or reduce input resolution

## Comparison with Original Version

| Feature | Original (q3) | All-in-One (q3_all) |
|---------|---------------|---------------------|
| Images per cycle | 1 | 3 |
| Same moment | N/A | Yes |
| Memory usage | Lower | Higher (~141KB) |
| Processing time | Faster | Slower (~1-2s) |
| Use case | Single mode testing | Comparison/demo |

