const int buttonPin1 = 2;  // the number of the pushbutton pin
const int buttonPin2 = 3;  // the number of the pushbutton pin

const int ledPin = 13;    // the number of the LED pin

// variables will change:
bool button1State = false;  // variable for reading the pushbutton status
bool button2State = false;  // variable for reading the pushbutton status

void setup() {
    Serial.begin(115200);
    // initialize the LED pin as an output:
    pinMode(ledPin, OUTPUT);
    // initialize the pushbutton pin as an input:
    pinMode(buttonPin1, INPUT);
    pinMode(buttonPin2, INPUT);
}

bool buttonsPressed(int button, bool &state) {
    if (digitalRead(button) == HIGH && state == false) {
        return true;
    } if (digitalRead(button) == LOW && state == true) {
        state = false;
    }
    return false;
}

void loop() {
    if (buttonsPressed(buttonPin1, button1State)) {
        // turn LED on:
        digitalWrite(ledPin, HIGH);
        Serial.println("SCAN");
        button1State = true;
    }
    if (buttonsPressed(buttonPin2, button2State)) {
        // turn LED off:
        digitalWrite(ledPin, LOW);
        Serial.println("GENERATE");
        button2State = true;
    }
}