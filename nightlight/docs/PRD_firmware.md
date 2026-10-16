# Nightlight Bedside Unit: Product Requirements Document (for FirmGen)

**Target:** ESP32 dev board, ESP-IDF v5.5
**Purpose:** A bedside lamp-like unit that responds kindly and escalates gently when the vision system reports a suspected fall.

## 1. Hardware

| Item | Connection (adjust to your kit) |
|---|---|
| Status LED, RGB (or three LEDs: amber, blue, red) | GPIO 25 (R), 26 (G), 27 (B) via PWM |
| Piezo buzzer | GPIO 18 (PWM/LEDC) |
| Push button "I'm OK" (active low, internal pull-up) | GPIO 4 |
| UART link to the bridge PC | UART0 over USB, 115200 8N1 |
| Optional OLED/display | I2C SDA 21, SCL 22 |

## 2. Serial protocol (ASCII, newline-terminated)

Host to board:
- `HB` : heartbeat, sent every 1 s while the vision pipeline is healthy
- `FALL` : fall suspected
- `CLEAR` : person is upright or recovered

Board to host:
- `ACK,<stage>,<ms>` : user pressed the button during `<stage>`, `<ms>` after the fall began
- `STAGE,<n>` : stage changed (0 idle, 1 glow, 2 check-in, 3 alert, 9 vision-offline)

## 3. Functional requirements

**FR-1 Idle.** In stage 0 the LED shows a dim, steady green "all is well" glow (about 5% brightness).

**FR-2 Stage 1, soft glow.** On `FALL` in stage 0, the unit enters stage 1 within 200 ms: a slow amber breathing glow (about 4 s period). No sound.

**FR-3 Stage 2, check-in.** If 10 s (configurable, default 10 000 ms) pass in stage 1 without button press or `CLEAR`, enter stage 2: blue pulse on the LED plus a gentle two-note chime every 5 s at low volume.

**FR-4 Stage 3, alert.** If 15 s (configurable, default 15 000 ms) pass in stage 2 with no button press or `CLEAR`, enter stage 3: solid red LED, loud alarm tone pattern, and begin BLE advertising of an alert payload.

**FR-5 Human cancel.** A button press in stages 1, 2 or 3 immediately returns the unit to stage 0, plays a short friendly rising chime, flashes green twice, and sends `ACK,<stage>,<ms>`. The press must be debounced (20 ms).

**FR-6 Auto-clear.** `CLEAR` in stages 1 or 2 returns to stage 0 silently. In stage 3, `CLEAR` stops the alarm sound but keeps the red LED until the button is pressed (a person must acknowledge a real alert).

**FR-7 Cancel latch.** After a button cancel, ignore `FALL` for 30 s (configurable) so the person is not re-alarmed while getting up.

**FR-8 Heartbeat watchdog (honesty rule).** If no `HB` (or any valid host line) is received for 5 s, enter stage 9: slow white double-blink every 2 s, no sound. When messages resume, return to stage 0. A `FALL` received after resuming is handled normally.

**FR-9 BLE alert.** In stage 3 the unit advertises device name `NIGHTLIGHT` with manufacturer data flag `0x01` (alert). Advertising stops on return to stage 0.

**FR-10 Boot self-test.** On boot, run an LED sweep (R, G, B) and one short chime, then print `READY` on UART.

## 4. Non-functional requirements

**NFR-1** Stage transitions are driven by a single state-machine task; LED, buzzer and UART tasks must not block it.
**NFR-2** All timing constants are `#define`s or Kconfig options so the demo can use shortened timers.
**NFR-3** Every stage change logs one line on UART: `STAGE,<n>`.
**NFR-4** Invalid or unknown serial lines are ignored and counted, never crash the firmware.
**NFR-5** Idle current draw should stay low: LED dimmed, no radio advertising outside stage 3.

## 5. Acceptance criteria (verify on the board, capture UART output and video)

| ID | Test | Expected |
|---|---|---|
| AC-1 | Power on | LED sweep, chime, `READY` on UART, then dim green |
| AC-2 | Send `HB` each second, then `FALL` | `STAGE,1` within 200 ms, amber breathing, silent |
| AC-3 | Wait 10 s after `FALL` | `STAGE,2`, blue pulse, soft chime |
| AC-4 | Wait 15 s more | `STAGE,3`, red, loud alarm, BLE `NIGHTLIGHT` visible in a phone BLE scanner |
| AC-5 | Press button in stage 2 | `ACK,2,<ms>` on UART, `STAGE,0`, green double flash |
| AC-6 | Send `FALL` 10 s after a cancel | Ignored (latch active) |
| AC-7 | Send `FALL` then `CLEAR` during stage 1 | Returns to stage 0 silently |
| AC-8 | Stop sending `HB` for 6 s | `STAGE,9`, white double-blink; resume `HB` returns `STAGE,0` |
| AC-9 | Send garbage lines | No crash, no stage change |

## 6. Live Intelligence (telemetry to enable in FirmGen)

Expose live: current stage, time-in-stage, heartbeat age (ms), count of invalid lines, free heap, and button-press count. Show this panel on the demo screen next to the pipeline view.
