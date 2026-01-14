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

// ===== SCALE FACTOR CONFIGURATION =====
// Set to 0 for ORIGINAL (1/1), 1 for UPSAMPLING (1.5x = 3/2), or 2 for DOWNSAMPLING (2/3)
#define IMAGE_MODE 2  // 0=Original, 1=Upsample, 2=Downsample

#if IMAGE_MODE == 0
  // Original: 1/1 → scale_num=1, scale_den=1
  #define SCALE_NUM 1
  #define SCALE_DEN 1
#elif IMAGE_MODE == 1
  // Upsampling: 1.5x → scale_num=3, scale_den=2
  #define SCALE_NUM 3
  #define SCALE_DEN 2
#else
  // Downsampling: 2/3 → scale_num=2, scale_den=3
  #define SCALE_NUM 2
  #define SCALE_DEN 3
#endif

#define OUT_W ((IN_W * SCALE_NUM) / SCALE_DEN)
#define OUT_H ((IN_H * SCALE_NUM) / SCALE_DEN)

static uint16_t resized[OUT_W * OUT_H];
static uint8_t *jpeg_buf = NULL;
static size_t jpeg_len = 0;

void setup() {
  Serial.begin(921600);
  delay(2000);

  #if IMAGE_MODE == 0
    Serial.println("ESP32 CAM: ORIGINAL mode (1/1 - no resizing)");
    Serial.printf("Output: %dx%d\n", OUT_W, OUT_H);
  #elif IMAGE_MODE == 1
    Serial.println("ESP32 CAM: UPSAMPLING mode (1.5x = 3/2)");
    Serial.printf("Input: %dx%d -> Output: %dx%d\n", IN_W, IN_H, OUT_W, OUT_H);
  #else
    Serial.println("ESP32 CAM: DOWNSAMPLING mode (2/3)");
    Serial.printf("Input: %dx%d -> Output: %dx%d\n", IN_W, IN_H, OUT_W, OUT_H);
  #endif

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

// Nearest neighbor resize (RGB565 color)
// Works for both upsampling and downsampling using integer arithmetic
// Uses inverse mapping: for each output pixel, find nearest input pixel
void resize_nearest(uint8_t *in) {
  uint16_t *in_rgb565 = (uint16_t *)in;
  for (int y = 0; y < OUT_H; y++) {
    for (int x = 0; x < OUT_W; x++) {
      // Inverse mapping: calculate source pixel position
      int src_y = (y * SCALE_DEN) / SCALE_NUM;
      int src_x = (x * SCALE_DEN) / SCALE_NUM;

      // Clamp to bounds
      if (src_y >= IN_H) src_y = IN_H - 1;
      if (src_x >= IN_W) src_x = IN_W - 1;

      // Copy pixel from source to destination
      resized[y * OUT_W + x] =
        in_rgb565[src_y * IN_W + src_x];
    }
  }
}

void loop() {
  digitalWrite(FLASH_GPIO, HIGH);
  delay(20);

  camera_fb_t *fb = esp_camera_fb_get();
  digitalWrite(FLASH_GPIO, LOW);
  if (!fb) return;

  #if IMAGE_MODE == 0
    // Original mode: copy directly without resizing
    uint16_t *in_rgb565 = (uint16_t *)fb->buf;
    for (int i = 0; i < OUT_W * OUT_H; i++) {
      resized[i] = in_rgb565[i];
    }
  #else
    // Upsampling or downsampling: use resize function
    resize_nearest(fb->buf);
  #endif

  // Encode resized image as JPEG
  // Debug: print actual dimensions being encoded
  Serial.printf("Encoding image: %dx%d pixels\n", OUT_W, OUT_H);
  
  bool ok = fmt2jpg(
      (uint8_t *)resized,
      OUT_W * OUT_H * 2,
      OUT_W,
      OUT_H,
      PIXFORMAT_RGB565,
      80,
      &jpeg_buf,
      &jpeg_len
  );

  if (ok) {
    Serial.printf("JPEG encoded: %d bytes\n", jpeg_len);
    uint8_t sync[2] = {0xAA, 0x55};
    Serial.write(sync, 2);
    Serial.write((uint8_t *)&jpeg_len, 4);
    Serial.write(jpeg_buf, jpeg_len);
    free(jpeg_buf);
  } else {
    Serial.println("JPEG encoding failed!");
  }

  esp_camera_fb_return(fb);
  delay(1000);
}
