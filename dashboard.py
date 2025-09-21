"""dashboard.py
FastAPI dashboard exposing simple JSON endpoints and a minimal HTML view.
Run: uvicorn dashboard:app --host 0.0.0.0 --port 8080
"""
from fastapi import FastAPI, Response
import yaml, json, time
from monitor import flows, flows_lock
from anomaly_rules import check_rules

app = FastAPI()
cfg = yaml.safe_load(open('config.yaml'))

@app.get('/api/flows')
def api_flows():
    rows = []
    with flows_lock:
        for k,v in flows.items():
            src,dst,proto,sport,dport = k
            rows.append({'src':src,'dst':dst,'proto':proto,'sport':sport,'dport':dport,
                         'first':v['first'],'last':v['last'],'packets':v['packets'],'bytes':v['bytes']})
    return {'flows': rows}

@app.get('/api/alerts')
def api_alerts():
    alerts = check_rules()
    formatted = []
    for k,info in alerts:
        src,dst,proto,sport,dport = k
        formatted.append({'src':src,'dst':dst,'proto':proto,'sport':sport,'dport':dport,'info':info})
    return {'alerts': formatted}

@app.get('/')
def index():
    html = """
    <html>
    <head><title>Network Monitor</title></head>
    <body>
    <h1>Network Monitor</h1>
    <div id='flows'></div>
    <script>
    async function refresh(){
      let r = await fetch('/api/flows');
      let j = await r.json();
      document.getElementById('flows').innerText = JSON.stringify(j, null, 2);
    }
    setInterval(refresh, 2000);
    refresh();
    </script>
    </body>
    </html>
    """
    return Response(content=html, media_type='text/html')
