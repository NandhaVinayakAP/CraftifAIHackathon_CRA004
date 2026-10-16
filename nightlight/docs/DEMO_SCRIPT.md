# Nightlight: 3-Minute Demo Script

**Setup on the table:** laptop/Jetson with USB camera, ESP32 lamp with button, a yoga mat on the floor, a phone with a BLE scanner, three screens or windows: (1) pipeline view with blur, (2) MQTT terminal, (3) FirmGen Live Intelligence panel.

Tip: set the firmware timers short for the demo (stage 2 at 6 s, stage 3 at 8 s) and say so out loud.

## 0:00 The story (20 s)
"Falls are dangerous, but cameras feel like surveillance and alarms cry wolf. Nightlight fixes both: nothing leaves the box except a few bytes of posture, and the room asks 'are you okay?' before it ever calls anyone."

## 0:20 Privacy proof (20 s)
Show the MQTT terminal. "This is everything that leaves the camera. No images. Look at the payload." Show the blurred display.

## 0:40 False alarms that must NOT alarm (40 s)
1. Sit down in a chair. Lamp stays green.
2. Bend to pick something up. Stays green.
3. Say "see, no siren."

## 1:20 The kind escalation (60 s)
1. Lie down on the mat. After 3 s: amber breathing glow.
2. Keep still: blue pulse and soft chime. Point at Live Intelligence: stage and timers counting.
3. **Press the button.** Green flash, `ACK` appears in the incident log. "A human answered, so no alert."
4. Lie down again, do not respond: red, alarm, phone shows `NIGHTLIGHT` BLE alert.

## 2:20 Honesty (20 s)
Cover the camera or kill the pipeline. After 5 s the lamp double-blinks white. "When it can't see, it tells you. It never fails silently."

## 2:40 Tool depth and numbers (20 s)
Show the Pipeline IR graph, the TensorRT speed report (FP16 vs INT8), and the FirmGen traceability report. Close: "PipeGen sees, FirmGen acts, and the person stays in charge."

## Backup plan
- Pre-record the full demo on video.
- If the camera fails, replay a recorded video file through the pipeline (allowed live-run input).
- If MQTT fails, send `FALL`/`CLEAR`/`HB` manually over the serial monitor to prove the firmware.
