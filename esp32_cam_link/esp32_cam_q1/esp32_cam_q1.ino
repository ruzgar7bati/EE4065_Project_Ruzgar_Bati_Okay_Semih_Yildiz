#include "esp_camera.h"
#include <string.h>

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

#define FLASH_GPIO        4

#define WIDTH  96
#define HEIGHT 96
#define MAX_PIXELS 1000

void setup() {
  Serial.begin(921600);
  delay(2000);

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
  config.pixel_format = PIXFORMAT_GRAYSCALE;
  config.frame_size   = FRAMESIZE_96X96;
  config.fb_count     = 1;

  esp_camera_init(&config);
}

void loop() {
  digitalWrite(FLASH_GPIO, HIGH);   // Flash ON
  delay(20);                        // allow light to stabilize

  camera_fb_t *fb = esp_camera_fb_get();
  digitalWrite(FLASH_GPIO, LOW);    // Flash OFF

  if (!fb) return;

  // Histogram
  uint32_t hist[256] = {0};
  for (int i = 0; i < fb->len; i++) {
    hist[fb->buf[i]]++;
  }

  // Threshold selection
  uint32_t sum = 0;
  uint8_t threshold = 255;
  for (int i = 255; i >= 0; i--) {
    sum += hist[i];
    if (sum >= MAX_PIXELS) {
      threshold = i;
      break;
    }
  }

  // Binary output
  static uint8_t binary[WIDTH * HEIGHT];
  uint32_t selected = 0;

  for (int i = 0; i < fb->len; i++) {
    if (fb->buf[i] >= threshold && selected < MAX_PIXELS) {
      binary[i] = 255;
      selected++;
    } else {
      binary[i] = 0;
    }
  }

  // Send to PC
  uint8_t sync[2] = {0xAA, 0x55};
  uint32_t size = fb->len;

  Serial.write(sync, 2);
  Serial.write((uint8_t*)&size, 4);
  Serial.write(binary, size);

  esp_camera_fb_return(fb);

  delay(1000);   // 1 frame per second (stable & safe)
}
