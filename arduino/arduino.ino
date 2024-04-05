const int buttonPin1 = 2; // the number of the pushbutton pin
const int buttonPin2 = 3; // the number of the pushbutton pin

const int potPin = A0;                    // Potentiometer connected to A0
int lastPotValue = 0;                     // Stores the last potentiometer value
int potValue = 0;                         // Current potentiometer value
unsigned long lastChangeTime = 0;         // Last time the potentiometer value changed
const unsigned long stabilityDelay = 500; // Wait for 50ms to ensure value is stable

const int ledPin = 13;   // the number of the LED pin
const int threshold = 5; // Threshold for detecting change in potentiometer value
int lastRange = -1;      // Variable to store the last range state (-1 indicates uninitialized)

// variables will change:
bool button1State = false; // variable for reading the pushbutton status
bool button2State = false; // variable for reading the pushbutton status

void setup()
{
    Serial.begin(115200);
    // initialize the LED pin as an output:
    pinMode(ledPin, OUTPUT);
    // initialize the pushbutton pin as an input:
    pinMode(buttonPin1, INPUT);
    pinMode(buttonPin2, INPUT);

    lastPotValue = analogRead(potPin);      // Initialize lastPotValue with the initial reading
    checkAndPrintRange(lastPotValue, true); // Check and print the initial range
}

bool buttonsPressed(int button, bool &state)
{
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

void loop()
{
    handlePotentiometer();

    if (buttonsPressed(buttonPin1, button1State))
    {
        // turn LED on:
        digitalWrite(ledPin, HIGH);
        Serial.println("SCAN");
        button1State = true;
    }
    if (buttonsPressed(buttonPin2, button2State))
    {
        // turn LED off:
        digitalWrite(ledPin, LOW);
        Serial.println("GENERATE");
        button2State = true;
    }
}
void handlePotentiometer()
{
    int potValue = analogRead(potPin); // Read the current potentiometer value

    // Check if the potentiometer value has changed significantly
    if (abs(potValue - lastPotValue) > threshold)
    {
        lastChangeTime = millis(); // Update the last change time
        lastPotValue = potValue;   // Update the last potentiometer value to the current reading
    }

    // If the current time is greater than lastChangeTime + stabilityDelay, it means the value is stable
    if (millis() - lastChangeTime > stabilityDelay && lastChangeTime != 0)
    {
        checkAndPrintRange(potValue, false); // Check the current range and print if it has changed
        lastChangeTime = 0;                  // Reset lastChangeTime to avoid multiple prints
    }
}

void checkAndPrintRange(int potValue, bool forcePrint)
{
    int currentRange;
    if (potValue < 341)
    {
        currentRange = 0;
    }
    else if (potValue >= 341 && potValue < 682)
    {
        currentRange = 1;
    }
    else
    {
        currentRange = 2;
    }

    // If the range has changed or if we are forcing a print (for setup), print the message
    if (currentRange != lastRange || forcePrint)
    {
        switch (currentRange)
        {
        case 0:
            Serial.println("POT1");
            break;
        case 1:
            Serial.println("POT2");
            break;
        case 2:
            Serial.println("POT3");
            break;
        }
        lastRange = currentRange; // Update the last range to the current one
    }
}