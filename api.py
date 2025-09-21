from fastapi import FastAPI, WebSocket
import sqlite3, time
import yaml, psutil

app = FastAPI()
cfg = yaml.safe_load(open('config.yaml'))

@app.get('/stats')
def stats():
    counters = psutil.net_io_counters(pernic=True)
    nic = cfg['interface']
    if nic not in counters:
        return {'error':'Interface not found'}
    st = counters[nic]
    return {'bytes_sent': st.bytes_sent, 'bytes_recv': st.bytes_recv}

@app.websocket('/ws')
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    while True:
        counters = psutil.net_io_counters(pernic=True)
        nic = cfg['interface']
        st = counters.get(nic)
        if st:
            await ws.send_json({'time': time.time(), 'sent': st.bytes_sent, 'recv': st.bytes_recv})
        await ws.receive_text()  # simple keep-alive
