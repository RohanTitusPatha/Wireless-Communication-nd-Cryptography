#include <RH_ASK.h>
#include <tinyECC.h>

tinyECC ecc;

RH_ASK radio(2000, 11, 12);
const int maxLength = 128; // Maximum length of the input
char inputBuffer[maxLength]; // Buffer to store the input

void setup() {
    Serial.begin(9600);
    ecc.genSig();

    if (!radio.init()) {
        Serial.println("Radio module failed to initialize");
    }
}

void loop() {
    if (Serial.available() > 0) {
        // Read characters from the Serial Monitor and store them in the buffer
        int bytesRead = Serial.readBytesUntil('\n', inputBuffer, maxLength - 1);

        // Null-terminate the string (add a null character at the end)
        inputBuffer[bytesRead] = '\0';

        // Encrypt the input data using tinyECC
        ecc.plaintext = inputBuffer;
        ecc.encrypt();

        // Send the encrypted message
        radio.send((uint8_t*)ecc.ciphertext.c_str(), ecc.ciphertext.length());
        radio.waitPacketSent();

        // Print information to the Serial Monitor
        Serial.println("Sent");
        Serial.println("Plain Text: " + ecc.plaintext);
        Serial.println("Cipher Text: " + ecc.ciphertext);
    }

    delay(1000);
}