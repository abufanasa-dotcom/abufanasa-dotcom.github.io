"""Run the preview server temporarily and verify local deployment bytes/MIME types.
Requires Node.js. This does not test browser layout or external services.
"""
from pathlib import Path
from urllib.request import urlopen
import os, socket, subprocess, time, json
ROOT=Path(__file__).resolve().parents[1]
MIMES={'.html':'text/html','.css':'text/css','.js':'text/javascript','.webp':'image/webp','.pdf':'application/pdf','.xml':'application/xml','.txt':'text/plain','.jpg':'image/jpeg','.png':'image/png','.svg':'image/svg+xml','.json':'application/json'}
files=[p for base in ['index.html','en','projects','legal','assets','css','js','sitemap.xml','robots.txt'] for p in ([ROOT/base] if (ROOT/base).is_file() else (ROOT/base).rglob('*')) if p.is_file()]
with socket.socket() as sock:
 sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
server=subprocess.Popen(['node',str(ROOT/'serve.js')],env={**os.environ,'PORT':str(port)},stdout=subprocess.PIPE,stderr=subprocess.PIPE)
errors=[]
try:
 for attempt in range(40):
  try:
   with urlopen(f'http://127.0.0.1:{port}/',timeout=1) as response:response.read()
   break
  except OSError:
   if server.poll() is not None:raise RuntimeError(server.stderr.read().decode())
   time.sleep(.05)
 else:raise RuntimeError('Preview server did not become ready')
 for p in files:
  relative=p.relative_to(ROOT).as_posix()
  with urlopen(f'http://127.0.0.1:{port}/'+relative,timeout=3) as response:
   data=response.read()
   if response.status!=200 or response.headers.get_content_type()!=MIMES.get(p.suffix):errors.append(relative+': HTTP/MIME')
   if data!=p.read_bytes():errors.append(relative+': stale bytes')
 print(json.dumps({'http_files_checked':len(files),'errors':errors,'not_a_browser_rendering_test':True},indent=2))
finally:
 server.terminate();server.communicate(timeout=5)
if errors:raise SystemExit(1)
