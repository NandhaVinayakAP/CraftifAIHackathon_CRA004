# Nightlight Perception Pipeline: PipeGen Spec

## Requirement text (paste into PipeGen's Requirement stage)

> Detect people from a USB camera and estimate their body pose with a YOLO-pose model. Track each person across frames. For each tracked person, classify posture as standing, sitting, or lying using keypoint geometry (torso angle and head-to-hip height relative to the bounding box). Publish one small JSON message per second per person over MQTT on topic `nightlight/posture`. Never save raw frames. If a display is shown, blur the person's face and body region. Run in real time on an NVIDIA GPU or Jetson with TensorRT, and compare FP16 and INT8.

## Five-stage walkthrough (screenshots needed for evidence)

| Stage | What to do | Evidence to capture |
|---|---|---|
| 1. Requirement | Use the text above; confirm tasks: detection, pose, tracking, analytics | Screenshot of the requirement |
| 2. Pipeline IR | Camera source, YOLO-pose primary model, tracker, analytics/posture node, MQTT + JSON sinks, blurred display | **Screenshot of the node graph** |
| 3. Model | Pick a pose model from the catalog (Deep Search GitHub if needed) | Model card/selection |
| 4. Compiler | Build TensorRT engines: FP16 and INT8 (with calibration images of people in varied poses) | **Speed report**, plus power and accuracy where available |
| 5. Run | `run.sh` on the live USB camera | Live demo, MQTT feed in a terminal |

## Posture logic (in the analytics node or a small custom probe)

Using COCO keypoints (shoulders 5/6, hips 11/12, ankles 15/16, nose 0):

- `torso_angle` = angle of the shoulder-midpoint to hip-midpoint vector from vertical
- `aspect` = bounding box width / height
- **lying**: torso_angle > 60 degrees AND aspect > 1.0
- **sitting**: hip-midpoint y within 0.25 of knee/ankle level and torso upright
- **standing**: otherwise
- `confidence` = mean keypoint confidence of the used points

## MQTT message schema (anonymous by design)

Topic: `nightlight/posture`

```json
{
  "ts": 1760633280.512,
  "track_id": 3,
  "posture": "lying",
  "conf": 0.87,
  "torso_angle": 78.4,
  "frame_id": 12045
}
```

No pixels, no faces, no embeddings. The `track_id` is a short-lived integer that resets when the pipeline restarts.

## Edge Optimization report template

| Precision | FPS | Latency (ms) | Power (W) | Accuracy note |
|---|---|---|---|---|
| FP16 | fill from PipeGen | | | baseline |
| INT8 | fill from PipeGen | | | posture-label agreement vs FP16 on your test clips |

Suggested accuracy check: record 5 short clips (stand, sit, bend, lie down, fall onto a mat) and compare posture labels between FP16 and INT8.
