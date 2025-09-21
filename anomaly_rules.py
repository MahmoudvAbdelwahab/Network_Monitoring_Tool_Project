"""anomaly_rules.py
Simple rule-based checks over flows to flag suspicious flows.
"""
import yaml
from monitor import flows, flows_lock
import time

cfg = yaml.safe_load(open('config.yaml'))
PKT_RATE_THRESH = cfg.get('alert_pkt_rate_per_sec', 1000)
BYTES_THRESH = cfg.get('alert_bytes_threshold', 10_000_000)

def check_rules():
    alerts = []
    now = time.time()
    with flows_lock:
        for k,v in flows.items():
            duration = max(1.0, v['last'] - v['first'])
            pkt_rate = v['packets'] / duration
            if pkt_rate > PKT_RATE_THRESH or v['bytes'] > BYTES_THRESH:
                alerts.append((k, {'pkt_rate':pkt_rate, 'bytes':v['bytes']}))
    return alerts

if __name__ == '__main__':
    a = check_rules()
    print('alerts:', a)
