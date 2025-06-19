#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;
int16_t ax, ay, az;
const int pin = 7;
bool disabled = false;
unsigned long disableTime = 0;

void setup() {
    Serial.begin(9600);
    Wire.begin();
    mpu.initialize();
    
    pinMode(pin, INPUT_PULLUP); // Enable internal pull-up resistor

    if (!mpu.testConnection()) {
        Serial.println("MPU6050 connection failed");
        while (1);
    }
}

void loop() {
    mpu.getAcceleration(&ax, &ay, &az);
    
    // Normalize acceleration values
    float xAcc = ax / 16384.0; // Assuming +/-2g sensitivity
    float yAcc = ay / 16384.0;

    // Read pin state (active LOW due to pull-up)
    int pinState = digitalRead(pin);

    // If button is pressed and not already disabled
    if (pinState == LOW && !disabled) {
        disabled = true;
        disableTime = millis();
    }

    // Reactivate after 5ms
    if (disabled && millis() - disableTime >= 100) {
        disabled = false;
    }

    // Send acceleration values and pin state
    Serial.print(xAcc);
    Serial.print(",");
    Serial.print(yAcc);
    Serial.print(",");
    Serial.println(disabled ? "0" : "1");  // Send 0 when disabled, otherwise 1
    delay(100);
}

