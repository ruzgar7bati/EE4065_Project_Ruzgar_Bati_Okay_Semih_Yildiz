#include "esp_camera.h"
#include "img_converters.h"

// ===== AI Thinker ESP32-CAM pin map =====
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

#define FLASH_GPIO 4

// Input resolution
#define IN_W 160
#define IN_H 120

// Output resolutions
#define ORIG_W IN_W
#define ORIG_H IN_H
#define DOWN_W ((IN_W * 2) / 3)   // 106
#define DOWN_H ((IN_H * 2) / 3)   // 80
#define UP_W ((IN_W * 3) / 2)     // 240
#define UP_H ((IN_H * 3) / 2)     // 180

// Image type identifiers
#define IMG_TYPE_ORIGINAL   0
#define IMG_TYPE_DOWNSAMPLED 1
#define IMG_TYPE_UPSAMPLED  2

// Buffers for resized images
static uint16_t downsampled[DOWN_W * DOWN_H];
static uint16_t upsampled[UP_W * UP_H];
static uint8_t *jpeg_buf = NULL;
static size_t jpeg_len = 0;

void setup() {
  Serial.begin(921600);
  delay(2000);

  Serial.println("ESP32 CAM: All-in-one mode (Original + Downsampled + Upsampled)");
  Serial.printf("Original: %dx%d\n", ORIG_W, ORIG_H);
  Serial.printf("Downsampled: %dx%d (2/3 scale)\n", DOWN_W, DOWN_H);
  Serial.printf("Upsampled: %dx%d (1.5x scale)\n", UP_W, UP_H);
  Serial.println("Sending all three from same frame...");

  pinMode(FLASH_GPIO, OUTPUT);
  digitalWrite(FLASH_GPIO, LOW);

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer   = LEDC_TIMER_0;

  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;

  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;

  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_RGB565;
  config.frame_size   = FRAMESIZE_QQVGA;  // 160x120
  config.fb_count     = 1;

  esp_camera_init(&config);
}

// Downsampling: 2/3 scale
void resize_downsample(uint8_t *in) {
  uint16_t *in_rgb565 = (uint16_t *)in;
  for (int y = 0; y < DOWN_H; y++) {
    for (int x = 0; x < DOWN_W; x++) {
      // Inverse mapping: scale_num=2, scale_den=3
      int src_y = (y * 3) / 2;
      int src_x = (x * 3) / 2;

      // Clamp to bounds
      if (src_y >= IN_H) src_y = IN_H - 1;
      if (src_x >= IN_W) src_x = IN_W - 1;

      downsampled[y * DOWN_W + x] = in_rgb565[src_y * IN_W + src_x];
    }
  }
}

// Upsampling: 1.5x scale (3/2)
void resize_upsample(uint8_t *in) {
  uint16_t *in_rgb565 = (uint16_t *)in;
  for (int y = 0; y < UP_H; y++) {
    for (int x = 0; x < UP_W; x++) {
      // Inverse mapping: scale_num=3, scale_den=2
      int src_y = (y * 2) / 3;
      int src_x = (x * 2) / 3;

      // Clamp to bounds
      if (src_y >= IN_H) src_y = IN_H - 1;
      if (src_x >= IN_W) src_x = IN_W - 1;

      upsampled[y * UP_W + x] = in_rgb565[src_y * IN_W + src_x];
    }
  }
}

// Send image with type identifier
void send_image(uint8_t img_type, uint8_t *img_data, size_t img_size, 
                uint16_t width, uint16_t height) {
  // Encode as JPEG
  bool ok = fmt2jpg(
      img_data,
      img_size,
      width,
      height,
      PIXFORMAT_RGB565,
      80,
      &jpeg_buf,
      &jpeg_len
  );

  if (ok) {
    // Protocol: [SYNC: 0xAA 0x55] [TYPE: 1 byte] [SIZE: 4 bytes] [JPEG DATA]
    uint8_t sync[2] = {0xAA, 0x55};
    Serial.write(sync, 2);
    Serial.write(&img_type, 1);  // Image type identifier
    Serial.write((uint8_t *)&jpeg_len, 4);
    Serial.write(jpeg_buf, jpeg_len);
    free(jpeg_buf);
  }
}

void loop() {
  digitalWrite(FLASH_GPIO, HIGH);
  delay(20);

  // Capture one frame
  camera_fb_t *fb = esp_camera_fb_get();
  digitalWrite(FLASH_GPIO, LOW);
  if (!fb) return;

  // Process all three versions from the same frame
  uint16_t *original_rgb565 = (uint16_t *)fb->buf;

  // 1. Send original image (160x120)
  send_image(IMG_TYPE_ORIGINAL, 
             (uint8_t *)original_rgb565, 
             ORIG_W * ORIG_H * 2,
             ORIG_W, ORIG_H);

  // 2. Process and send downsampled (106x80)
  resize_downsample(fb->buf);
  send_image(IMG_TYPE_DOWNSAMPLED,
             (uint8_t *)downsampled,
             DOWN_W * DOWN_H * 2,
             DOWN_W, DOWN_H);

  // 3. Process and send upsampled (240x180)
  resize_upsample(fb->buf);
  send_image(IMG_TYPE_UPSAMPLED,
             (uint8_t *)upsampled,
             UP_W * UP_H * 2,
             UP_W, UP_H);

  esp_camera_fb_return(fb);
  
  Serial.println("Sent all three images from same frame");
  delay(2000);  // 2 second delay between frame sets
}

