/* 
  PERFEC System Sample Player - Plotter Data Stream Version
  Target Board: Circuit Playground Express (Secondary Testing Unit)
  Language: C++ (Arduino Core)
  Requires Library: "MIDIUSB" by Gary Grewal
*/

#include "MIDIUSB.h"

// Hardware Pin Assignment (Connect via alligator clip)
const int AUDIO_ANALOG_PIN = A1;  // Connect to target CPX's A0 Audio output or speaker line

// Configuration Settings
const unsigned long TEST_INTERVAL_MS = 1000; // 1 second intervals for clean data plotting
const byte MIDI_CHANNEL = 9;                 // "Raw" MIDI Channel 0 (Channel 1)
const byte TEST_NOTE = 36;                    // General MIDI Bass Drum Note (36)
const byte TEST_VELOCITY = 127;              // Maximum velocity for sharpest attack transient

// Audio Threshold Calibrations
const int IDLE_CENTER_VOLTAGE = 512;          // The middle of the 10-bit analog range (0-1023)
const int THRESHOLD_DEVIATION = 45;           // Sensitivity threshold window

// Rolling Average Tracking Configuration
const int FILTER_SAMPLES = 10;
float latencyHistory[FILTER_SAMPLES] = {0};
int historyIndex = 0;
float currentRollingSum = 0;
int totalSamplesCaptured = 0;

void setup() {
  // Initialize USB Serial for plotting data stream
  Serial.begin(115200);
  
  // Set up A1 as a standard analog input
  pinMode(AUDIO_ANALOG_PIN, INPUT);
  
  delay(2000); // Safe boot settling window
}

void loop() {
  // 1. Ensure the audio line has completely settled before triggering
  while (abs(analogRead(AUDIO_ANALOG_PIN) - IDLE_CENTER_VOLTAGE) > 10) {
    delay(5);
  }

  // 2. Pack the standard 4-byte USB MIDI NoteOn message
  midiEventPacket_t noteOn = {0x09, (byte)(0x90 | MIDI_CHANNEL), TEST_NOTE, TEST_VELOCITY};
  
  // 3. Transmit the USB MIDI note and capture the microsecond start timestamp
  MidiUSB.sendMIDI(noteOn);
  MidiUSB.flush(); // Force immediate transmission across the USB bus
  unsigned long startTime = micros();

  // 4. Ultra-fast hardware polling loop: Watch for the initial audio transient
  unsigned long timeoutAnchor = millis();
  bool triggered = false;
  unsigned long latencyMicros = 0;

  while ((millis() - timeoutAnchor) < 250) { // 250ms safety timeout boundary
    int audioSample = analogRead(AUDIO_ANALOG_PIN);
    
    // Check if the signal has suddenly spiked away from center idle point
    if (abs(audioSample - IDLE_CENTER_VOLTAGE) > THRESHOLD_DEVIATION) {
      unsigned long endTime = micros();
      latencyMicros = endTime - startTime;
      triggered = true;
      break;
    }
  }

  // 5. If triggered successfully, calculate data and output clean plotter stream
  if (triggered) {
    float latencyMillis = (float)latencyMicros / 1000.0;
    
    // Update the rolling history array calculations
    currentRollingSum -= latencyHistory[historyIndex];
    latencyHistory[historyIndex] = latencyMillis;
    currentRollingSum += latencyMillis;
    
    historyIndex = (historyIndex + 1) % FILTER_SAMPLES;
    if (totalSamplesCaptured < FILTER_SAMPLES) {
      totalSamplesCaptured++;
    }
    
    float rollingAverage = currentRollingSum / totalSamplesCaptured;
    
    // Format required for Arduino Serial Plotter: "Value1,Value2"
    Serial.print(latencyMillis, 3);
    Serial.print(",");
    Serial.println(rollingAverage, 3);
  } else {
    // If it timeouts, print a default high flatline or leave blank to keep plot formatting clean
    // Serial.println("0.000,0.000"); 
  }

  // 6. Send matching USB NoteOff to clear out voice tracking state
  midiEventPacket_t noteOff = {0x08, (byte)(0x80 | MIDI_CHANNEL), TEST_NOTE, 0};
  MidiUSB.sendMIDI(noteOff);
  MidiUSB.flush();

  delay(TEST_INTERVAL_MS);
}
