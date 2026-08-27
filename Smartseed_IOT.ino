#include <WiFi.h>
#include <HTTPClient.h>
#include <ModbusMaster.h>
#include <ArduinoJson.h>
#include <WiFiManager.h> 
#include <Preferences.h> // Save and load the IP address from flash memory

// OLED Display Libraries
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// OLED Display Configuration
#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
#define OLED_RESET    -1 // Reset pin # (or -1 if sharing ESP32 reset pin)
#define SCREEN_ADDRESS 0x3C // 0x3C for 128x64 OLED

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Initialize Preferences object for non-volatile storage
Preferences preferences;

// Default Server IP Address. This will be updated via the WiFiManager portal.
String serverIP = "192.168.8.125";

// Manual Device ID
const char* deviceId = "S_001";

// Hardware Serial and Control Pins for MAX485
#define MAX485_DE_RE 4
#define RX2_PIN 16
#define TX2_PIN 17

ModbusMaster node;

// Function prototypes for OLED
void updateOLED(float moisture, float temp, uint16_t ec, float ph, uint16_t n, uint16_t p, uint16_t k, bool isSuccess);
void showOLEDMessage(String line1, String line2);

// Callback functions for RS485 Direction Control
void preTransmission() {
  digitalWrite(MAX485_DE_RE, HIGH); // Set MAX485 to Transmit mode
  delay(2);
}

void postTransmission() {
  delay(2);
  digitalWrite(MAX485_DE_RE, LOW);  // Set MAX485 to Receive mode
}

void setup() {
  Serial.begin(115200);

  // Initialize I2C and OLED Display
  Wire.begin(21, 22); // SDA = GPIO 21, SCL = GPIO 22
  if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 OLED allocation failed!"));
    for (;;); // Don't proceed, loop forever
  }

  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  showOLEDMessage(" SmartSeed AI", "Booting Up...");

  // Configure DE/RE control pin for RS485 communication
  pinMode(MAX485_DE_RE, OUTPUT);
  digitalWrite(MAX485_DE_RE, LOW);

  // Initialize HardwareSerial 2 for Modbus RTU at 4800 Baud Rate
  Serial2.begin(4800, SERIAL_8N1, RX2_PIN, TX2_PIN);
  
  // Initialize Modbus slave ID 1
  node.begin(1, Serial2);
  node.preTransmission(preTransmission);
  node.postTransmission(postTransmission);

  // Open Preferences with the namespace "smartseed", read-write mode (false)
  preferences.begin("smartseed", false);
  
  // Retrieve the saved IP address from flash memory
  serverIP = preferences.getString("server_ip", "192.168.8.125");

  // Show WiFi Connecting message on OLED
  showOLEDMessage("Connecting WiFi", "AP: SmartSeed_Setup");

  // Initialize WiFiManager
  WiFiManager wifiManager;

  // Add a custom input field for the Flask Server IP address in the captive portal
  WiFiManagerParameter custom_server_ip("server_ip", "Flask Server IP Address", serverIP.c_str(), 40);
  wifiManager.addParameter(&custom_server_ip);

  Serial.println("Connecting to Wi-Fi...");
  
  // Creates an Access Point named "SmartSeed_Setup" if it cannot connect
  bool connected = wifiManager.autoConnect("SmartSeed_Setup");

  if (!connected) {
    Serial.println("Failed to connect and hit timeout. Restarting...");
    showOLEDMessage("WiFi Failed!", "Restarting...");
    delay(3000);
    ESP.restart();
  }

  // Retrieve the updated value from the portal input field and save it
  serverIP = custom_server_ip.getValue();
  preferences.putString("server_ip", serverIP);

  Serial.println("\nConnected to Wi-Fi network successfully.");
  
  // Show WiFi Success on OLED
  showOLEDMessage("WiFi Connected!", "IP:" + WiFi.localIP().toString());
  delay(2000);
}

void loop() {
  // Read 7 holding registers starting at address 0x0000
  uint8_t result = node.readHoldingRegisters(0x0000, 7);

  if (result == node.ku8MBSuccess) {
    // Parse all 7 sensor raw values
    float moisture     = node.getResponseBuffer(0) / 10.0;
    float temp         = node.getResponseBuffer(1) / 10.0;
    uint16_t ec        = node.getResponseBuffer(2);
    float ph           = node.getResponseBuffer(3) / 10.0;
    uint16_t nitrogen   = node.getResponseBuffer(4);
    uint16_t phosphorus = node.getResponseBuffer(5);
    uint16_t potassium  = node.getResponseBuffer(6);

    Serial.printf("Moisture: %.1f%% | Temp: %.1fC | EC: %d | pH: %.1f | N: %d | P: %d | K: %d\n",
                  moisture, temp, ec, ph, nitrogen, phosphorus, potassium);

    // Update OLED Display with new sensor data
    updateOLED(moisture, temp, ec, ph, nitrogen, phosphorus, potassium, true);

    // Transmit the parsed payload to the backend API
    sendDataToBackend(moisture, temp, ec, ph, nitrogen, phosphorus, potassium);
  } else {
    Serial.printf("Modbus communication failed! Error Code: 0x%02X\n", result);
    
    // Show Modbus error on OLED
    updateOLED(0, 0, 0, 0, 0, 0, 0, false);
  }

  // Transmit data at 30-second intervals
  delay(30000);
}

// Function to render all 7 Soil Metrics on the 128x64 OLED Screen
void updateOLED(float moisture, float temp, uint16_t ec, float ph, uint16_t n, uint16_t p, uint16_t k, bool isSuccess) {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextWrap(false); // Disable text wrapping
  
  // Header
  display.setCursor(0, 0);
  display.print("---- SMARTSEED ----");

  if (!isSuccess) {
    display.setCursor(0, 25);
    display.print("Sensor Read Error!");
    display.setCursor(0, 40);
    display.print("Check RS485 / 12V");
    display.display();
    return;
  }

  // Line 1: Moisture (Left) & Temperature (Right)
  display.setCursor(0, 14);
  display.printf("M:%.1f%%", moisture);
  display.setCursor(64, 14); // Starts at the center of the screen
  display.printf("T:%.1fC", temp);

  // Line 2: pH (Left) & EC (Right)
  display.setCursor(0, 26);
  display.printf("pH:%.1f", ph);
  display.setCursor(64, 26);
  display.printf("EC:%d", ec);

  // Line 3: N P K Values (The screen is divided into 3 equal parts)
  display.setCursor(0, 38);
  display.printf("N:%d", n);
  display.setCursor(44, 38);
  display.printf("P:%d", p);
  display.setCursor(88, 38);
  display.printf("K:%d", k);

  // Line 4: Server IP
  display.setCursor(0, 52);
  display.print("IP:");
  display.print(serverIP);

  display.display();
}

// Helper Function for Simple Status Messages
void showOLEDMessage(String line1, String line2) {
  display.clearDisplay();
  display.setTextSize(1);
  display.setCursor(0, 10);
  display.println(line1);
  display.setCursor(0, 30);
  display.println(line2);
  display.display();
}

void sendDataToBackend(float moisture, float temp, uint16_t ec, float ph, int n, int p, int k) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    
    String fullServerUrl = "http://" + serverIP + ":5000/api/sensor_update";
    
    http.begin(fullServerUrl);
    http.addHeader("Content-Type", "application/json");

    StaticJsonDocument<256> doc;
    doc["device_id"]     = deviceId;
    doc["soil_moisture"] = moisture;
    doc["temperature"]   = temp;
    doc["conductivity"]  = ec;
    doc["ph_level"]      = ph;
    doc["nitrogen"]      = n;
    doc["phosphorus"]    = p;
    doc["potassium"]     = k;

    String jsonPayload;
    serializeJson(doc, jsonPayload);

    int httpResponseCode = http.POST(jsonPayload);

    if (httpResponseCode > 0) {
      Serial.printf("Backend HTTP Response Code: %d\n", httpResponseCode);
    } else {
      Serial.printf("HTTP Request Failed: %s\n", http.errorToString(httpResponseCode).c_str());
    }
    http.end();
  } else {
    Serial.println("Transmission Error: Wi-Fi Disconnected!");
  }
}