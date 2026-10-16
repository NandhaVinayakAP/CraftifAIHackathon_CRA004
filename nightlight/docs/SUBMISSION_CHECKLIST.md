# Submission Checklist (deadline 4:00 pm)

## Setup (do first)
- [ ] CraftifAI account created, PipeGen v0.5.1 (`pipegen --version` prints 0.5.1) and FirmGen v0.4.1 installed
- [ ] ESP32 on ESP-IDF v5.5; USB camera plugged in; videos stored under /home
- [ ] MQTT broker running (`mosquitto`), `pip install -r bridge/requirements.txt`

## Track A evidence (PipeGen)
- [ ] All five stages completed (Requirement, Pipeline IR, Model, Compiler, Run)
- [ ] Screenshot of Pipeline IR node graph
- [ ] TensorRT speed report (FP16 and INT8)
- [ ] Live run on USB camera, MQTT/JSON output shown
- [ ] PipeGen export folder copied to `pipegen_export/`

## Track B evidence (FirmGen)
- [ ] PRD uploaded, requirements reviewed and **frozen**
- [ ] Firmware flashed to real ESP32
- [ ] Acceptance criteria AC-1 to AC-9 shown with UART/Monitor output and video of physical behavior
- [ ] Traceability report exported to `evidence/`
- [ ] Project pushed through FirmGen's Git view

## Bonuses
- [ ] Closed Loop: live camera event triggers lamp stage change (record it)
- [ ] Live Intelligence: telemetry enabled, panel visible during demo
- [ ] Edge Optimization: INT8 engine run, speed/power/accuracy table filled in

## Submit
- [ ] Repo link, project description (paste README sections), evidence screenshots
- [ ] Submit both forms if claiming both tracks: FirmGen https://forms.gle/bnocK9CNLndiZLwf8 and PipeGen https://forms.gle/eJyeCKCG2UH757QZ8
- [ ] Optional: 60-90 s pitch video

## Disqualification guardrails
- Do not skip the PRD freeze or the five PipeGen stages
- No simulation-only firmware
- Keep both tools load-bearing (write the bridge protocol into the PRD, as done here)
