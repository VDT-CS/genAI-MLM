const int buttonPin1 = 2; // the number of the pushbutton pin
const int buttonPin2 = 3; // the number of the pushbutton pin

const int potPin = A0;                    // Potentiometer connected to A0

const int potentiometers[] = {A0}; // Important! Add all potetionemeters here
const int numRanges[] = {3, 3}; // Number of ranges you want to divide the potentiometer readings into

const int numPots = sizeof(potentiometers) / sizeof(potentiometers[0]);
int lastPotValue[numPots];        // Stores the last potentiometer values
int lastRange[numPots];           // Stores the last range states for each potentiometer
unsigned long lastChangeTime[numPots]; // Last time the potentiometer value changed for each

const unsigned long stabilityDelay = 500; // Wait for 500ms to ensure value is stable
const int threshold = 5; // Threshold for detecting change in potentiometer value

const int ledPin = 13;   // the number of the LED pin

// variables will change:
bool button1State = false; // variable for reading the pushbutton status
bool button2State = false; // variable for reading the pushbutton status

void setup(){
    Serial.begin(115200);
    // initialize the LED pin as an output:
    pinMode(ledPin, OUTPUT);
    // initialize the pushbutton pin as an input:
    pinMode(buttonPin1, INPUT);
    pinMode(buttonPin2, INPUT);

    for (int i = 0; i < numPots; i++) {
        lastPotValue[i] = analogRead(potentiometers[i]);
        lastRange[i] = -1; // Initialize lastRange with -1 to indicate uninitialized
        lastChangeTime[i] = 0;
    }
}

bool buttonsPressed(int button, bool &state){
    if (digitalRead(button) == HIGH && state == false)
    {
        return true;
    }
    if (digitalRead(button) == LOW && state == true)
    {
        state = false;
    }
    return false;
}

void loop(){
    for (int i = 0; i < numPots; i++) {
        handlePotentiometer(potentiometers[i], i);
    }

    if (buttonsPressed(buttonPin1, button1State))
    {
        // turn LED on:
        digitalWrite(ledPin, HIGH);
        Serial.println("{'INPUT': 'SCAN'}");
        button1State = true;
    }
    if (buttonsPressed(buttonPin2, button2State))
    {
        // turn LED off:
        digitalWrite(ledPin, LOW);
        Serial.println("{'INPUT': 'GENERATE'}");
        button2State = true;
    }
}

void handlePotentiometer(int pot, int index) {
    int potValue = analogRead(pot); // Read the current potentiometer value

    if (abs(potValue - lastPotValue[index]) > threshold) {
        lastChangeTime[index] = millis();
        lastPotValue[index] = potValue;
    }

    if (millis() - lastChangeTime[index] > stabilityDelay && lastChangeTime[index] != 0) {
        checkAndPrintRange(potValue, index, false);
        lastChangeTime[index] = 0;
    }
}

void checkAndPrintRange(int potValue, int index, bool forcePrint) {
    float rangeWidth = 1024.0 / numRanges[index]; // Use 1024 to include the upper boundary and float for division
    int currentRange = static_cast<int>(floor(potValue / rangeWidth));

    if (currentRange != lastRange[index] || forcePrint) {
        Serial.print("{'INPUT': ");
        // Example customization based on potentiometer and range
        if (index == 0) { // For first potentiometer
        Serial.print("'STYLE', 'VALUE': ");
            switch (currentRange) {
                case 0: Serial.print("PHOTO"); break;
                case 1: Serial.print("DIGITAL_ART"); break;
                case 2: Serial.print("ANIME"); break;
            }
        } else if (index == 1) { // For second potentiometer
            switch (currentRange) {
                case 0: Serial.println("{'INPUT': 'POT2', 'VALUE': 'LOW'}"); break;
                case 1: Serial.println("{'INPUT': 'POT2', 'VALUE': 'MEDIUM'}"); break;
                case 2: Serial.println("{'INPUT': 'POT2', 'VALUE': 'HIGH'}"); break;
            }
        }
        Serial.println("'}");
        lastRange[index] = currentRange;
    }
}