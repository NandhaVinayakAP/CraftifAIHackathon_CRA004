#!/usr/bin/env python3
"""Nightlight bridge: MQTT posture events (PipeGen) -> serial commands (FirmGen ESP32).

- Debounces posture so a brief bend or sit-down never triggers a fall.
- Sends a 1 Hz heartbeat only while the pipeline is actually publishing,
  so the lamp can honestly say "I can't see" when vision is down.
- Logs incidents as JSON lines with no images.
"""
import argparse
import json
import threading
import time

import paho.mqtt.client as mqtt
import serial

LYING = {"lying", "fallen"}


def make_client():
    try:
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    except AttributeError:  # paho-mqtt 1.x
        return mqtt.Client()


class Bridge:
    def __init__(self, args):
        self.args = args
        self.ser = serial.Serial(args.port, args.baud, timeout=0.2)
        self.lock = threading.Lock()
        self.lying_since = None
        self.suspected = False
        self.last_event = 0.0  # last time pipeline published anything

    def send(self, line):
        with self.lock:
            self.ser.write((line + "\n").encode())

    def log_incident(self, kind, **extra):
        rec = {"ts": time.time(), "event": kind, **extra}
        with open(self.args.log, "a") as f:
            f.write(json.dumps(rec) + "\n")
        print("[incident]", rec)

    # --- MQTT ---
    def on_message(self, *cb_args):
        msg = cb_args[2]  # works for both paho v1 and v2 callback signatures
        try:
            d = json.loads(msg.payload)
            posture = d["posture"]
            conf = float(d.get("conf", 0))
        except (ValueError, KeyError, TypeError):
            return
        now = time.time()
        self.last_event = now
        if conf < self.args.min_conf:
            return

        if posture in LYING:
            if self.lying_since is None:
                self.lying_since = now
            held = now - self.lying_since
            if held >= self.args.hold and not self.suspected:
                self.suspected = True
                self.send("FALL")
                self.log_incident("fall_suspected", held_s=round(held, 1),
                                  track_id=d.get("track_id"))
        else:
            self.lying_since = None
            if self.suspected:
                self.suspected = False
                self.send("CLEAR")
                self.log_incident("recovered", posture=posture)

    # --- background threads ---
    def heartbeat_loop(self):
        while True:
            if time.time() - self.last_event < self.args.stale:
                self.send("HB")
            time.sleep(1.0)

    def serial_reader(self):
        while True:
            raw = self.ser.readline()
            if not raw:
                continue
            line = raw.decode(errors="ignore").strip()
            if line.startswith("ACK"):
                self.log_incident("human_ack", detail=line)
                self.suspected = False
                self.lying_since = None
            elif line:
                print("[board]", line)

    def run(self):
        threading.Thread(target=self.heartbeat_loop, daemon=True).start()
        threading.Thread(target=self.serial_reader, daemon=True).start()
        c = make_client()
        c.on_message = self.on_message
        c.connect(self.args.broker, self.args.mqtt_port)
        c.subscribe(self.args.topic)
        print(f"Bridge up: {self.args.topic} -> {self.args.port}")
        c.loop_forever()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--port", default="/dev/ttyUSB0")
    p.add_argument("--baud", type=int, default=115200)
    p.add_argument("--broker", default="localhost")
    p.add_argument("--mqtt-port", type=int, default=1883)
    p.add_argument("--topic", default="nightlight/posture")
    p.add_argument("--hold", type=float, default=3.0,
                   help="seconds a lying posture must persist before FALL")
    p.add_argument("--min-conf", type=float, default=0.5)
    p.add_argument("--stale", type=float, default=3.0,
                   help="seconds without events before heartbeats stop")
    p.add_argument("--log", default="incidents.jsonl")
    Bridge(p.parse_args()).run()


if __name__ == "__main__":
    main()
