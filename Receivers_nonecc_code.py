#include <RH_ASK.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

RH_ASK radio(2000, 11, 12);
const int maxLength = 128; // Maximum length of the input
char receivedBuffer[maxLength]; // Buffer to store the received message

void setup() {
    Serial.begin(9600);

    if (!radio.init()) {
        Serial.println("Radio module failed to initialize");
    }

    lcd.begin(16, 2);
    lcd.backlight();
}

void loop() {
    uint8_t buf[RH_ASK_MAX_MESSAGE_LEN];
    uint8_t buflen = sizeof(buf);

    if (radio.recv(buf, &buflen)) {
        Serial.println("Received Sender's Public key");

        // Message received successfully
        Serial.print("Received: ");
        for (int i = 0; i < buflen; i++) {
            Serial.print((char)buf[i]);
        }
        Serial.println();

        // Display the received message on the LCD
        lcd.clear();
        lcd.setCursor(0, 0); // Set the cursor to the first line
        lcd.print("Received Message:");
        lcd.setCursor(0, 1); // Set the cursor to the second line
        lcd.print((char*)buf);
    }

    delay(1000); // Adjust the delay as needed to control how often you check for incoming messages
}
