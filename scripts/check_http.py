"""Serve files temporarily and verify local deployment bytes/MIME types.
Uses Python's standard library. This does not test browser layout or external services.
"""
from pathlib import Path
from urllib.request import urlopen
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
import json
ROOT=Path(__file__).resolve().parents[1]
MIMES={'.html':'text/html','.css':'text/css','.js':'text/javascript','.webp':'image/webp','.pdf':'application/pdf','.xml':'application/xml','.txt':'text/plain','.jpg':'image/jpeg','.png':'image/png','.svg':'image/svg+xml','.json':'application/json'}
files=[p for base in ['index.html','en','projects','legal','assets','css','js','sitemap.xml','robots.txt'] for p in ([ROOT/base] if (ROOT/base).is_file() else (ROOT/base).rglob('*')) if p.is_file()]
class PreviewHandler(SimpleHTTPRequestHandler):
 extensions_map={**SimpleHTTPRequestHandler.extensions_map,**MIMES}
 def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT),**kwargs)
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),PreviewHandler)
port=server.server_address[1]
thread=Thread(target=server.serve_forever,daemon=True)
thread.start()
errors=[]
try:
 for p in files:
  relative=p.relative_to(ROOT).as_posix()
  with urlopen(f'http://127.0.0.1:{port}/'+relative,timeout=3) as response:
   data=response.read()
   if response.status!=200 or response.headers.get_content_type()!=MIMES.get(p.suffix):errors.append(relative+': HTTP/MIME')
   if data!=p.read_bytes():errors.append(relative+': stale bytes')
 print(json.dumps({'http_files_checked':len(files),'errors':errors,'not_a_browser_rendering_test':True},indent=2))
finally:
 server.shutdown();server.server_close();thread.join(timeout=5)
if errors:raise SystemExit(1)
