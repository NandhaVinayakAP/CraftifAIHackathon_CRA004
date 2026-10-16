# Nightlight

**A fall-detection system that treats the person as a person, not a threat to be monitored.**

*Embedded SF: CraftifAI Physical AI Hackathon. Track: Closed Loop (PipeGen + FirmGen), with Live Intelligence and Edge Optimization bonuses.*

---

## The human problem

Every year millions of older adults fall at home, and many lie on the floor for an hour or more because nobody knows. Families want to know, but the common answers fail people in two ways:

1. **Cameras feel like surveillance.** Many older adults refuse them, and they are right to. Nobody wants their bathroom or bedroom streamed to a cloud.
2. **Alarms cry wolf.** A dropped book or a nap on the floor with a grandchild triggers a siren. After two false alarms, people switch the device off.

Nightlight is designed around both objections:

- **Privacy by architecture.** Video never leaves the box. The pipeline emits only anonymous posture events (a few bytes of JSON). No frame is ever saved, and no face is ever stored.
- **A kind escalation ladder instead of a siren.** The room responds like a caring neighbour would: first a soft glow, then a gentle voice-free chime, then a big friendly "I'm OK" button. Only if there is no human answer does it call family.
- **It admits when it is blind.** If the camera pipeline stops, the lamp says so, instead of silently pretending everything is fine.

## How it works

```
 USB camera --> [PipeGen: DeepStream + TensorRT pose pipeline, on GPU/Jetson]
                        |  anonymous posture events (MQTT, JSON, no pixels)
                        v
                 [bridge.py: debounce + heartbeat]  --serial/UART-->  [FirmGen: ESP32 bedside lamp]
                                                                          |  soft amber -> chime + blue pulse -> red + alarm
                                                                          |  "I'm OK" button cancels at any stage
                                                                          |  BLE alert advert for family phone
                                                                          v
                                                             [Live Intelligence: telemetry on judges' screen]
```

| Part | Tool | What it does |
|---|---|---|
| Perception | **PipeGen** | Pose estimation (YOLO-pose family) compiled to TensorRT, run on DeepStream, outputs posture labels + MQTT/JSON with a privacy blur on any display output |
| Action | **FirmGen** | ESP32 firmware generated from a reviewed PRD: escalation state machine, LED/buzzer/button, BLE alert, heartbeat watchdog |
| Glue | `bridge/bridge.py` | Subscribes to MQTT, debounces posture, sends serial commands, logs incidents without images |

Both tools are load-bearing. Delete either and the product stops working: no pipeline means no events, and no firmware means no gentle response.

## Why it stands out

- It is a **designed experience**, not a detector with a buzzer. The escalation ladder, the "I'm OK" cancel and the fail-safe "I can't see" signal are product decisions grounded in how people actually react.
- **Privacy is measurable.** Judges can inspect the MQTT feed live and see there are no images.
- **Honest evidence.** The demo shows false-alarm handling (sitting down, bending to pick something up, deliberately lying down and pressing the button) as well as the true positive.
- **Live Intelligence** shows the firmware's escalation timers and heartbeat age live while the pipeline drives it.
- **Edge Optimization** compares FP16 vs INT8 TensorRT engines (speed, power, accuracy) from PipeGen's reports.

## Bonuses claimed

- Closed Loop (perception event triggers physical action in real time)
- Live Intelligence (telemetry enabled in FirmGen)
- Edge Optimization (INT8 engine, ideally on a Jetson)

## Repository layout

```
nightlight/
  README.md
  docs/PRD_firmware.md          # paste into FirmGen
  docs/PIPEGEN_REQUIREMENT.md   # paste into PipeGen
  docs/DEMO_SCRIPT.md
  docs/SUBMISSION_CHECKLIST.md
  bridge/bridge.py
  bridge/requirements.txt
  pipegen_export/               # export folder from PipeGen (add after your run)
  firmgen_project/              # pushed via FirmGen Git view (add after your run)
  evidence/                     # screenshots, speed report, traceability report, UART log
```

## Safety note

Nightlight is a hackathon prototype and an assistive aid. It is not a certified medical alert device.
