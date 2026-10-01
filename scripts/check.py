"""Offline checks of generated pages, links, language parity, metrics and CV.
Requires pypdf. This does not render a browser or certify accessibility.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from decimal import Decimal, ROUND_HALF_UP
from xml.etree import ElementTree as ET
from pypdf import PdfReader
from build import BASE, METRICS, WORK, PROJECTS, num
import json
ROOT = Path(__file__).resolve().parents[1]
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class Page(HTMLParser):
 def __init__(self):
  super().__init__(); self.nodes=[]; self.ids=[]; self.stack=[]; self.errors=[]; self.script=None; self.schemas=[]; self.words=[]
 def handle_starttag(self, tag, attrs):
  attrs=dict(attrs); self.nodes.append((tag,attrs))
  if 'id' in attrs:self.ids.append(attrs['id'])
  if tag not in VOID:self.stack.append(tag)
  if tag=='script' and attrs.get('type')=='application/ld+json':self.script=''
 def handle_endtag(self,tag):
  if not self.stack or self.stack[-1]!=tag:self.errors.append('invalid nesting at </'+tag+'>')
  else:self.stack.pop()
  if tag=='script' and self.script is not None:
   self.schemas.append(json.loads(self.script));self.script=None
 def handle_data(self,data):
  self.words.append(data)
  if self.script is not None:self.script+=data
 def find(self,tag,**attrs):return [a for t,a in self.nodes if t==tag and all(a.get(k)==v for k,v in attrs.items())]
 def classes(self,name):return [a for t,a in self.nodes if name in a.get('class','').split()]

pages={};errors=[];links=0;image_candidates=0
for p in ROOT.rglob('*.html'):
 if any(x in p.parts for x in ('_private','node_modules')):continue
 q=Page();q.feed(p.read_text());pages[p.resolve()]=q
for p,q in pages.items():
 name=str(p.relative_to(ROOT));raw=p.read_text();lang=q.find('html')[0].get('lang')
 if len(q.find('h1'))!=1:errors.append(name+': h1 count')
 if len(q.find('main'))!=1:errors.append(name+': main count')
 if len(q.ids)!=len(set(q.ids)):errors.append(name+': duplicate IDs')
 errors.extend(name+': '+e for e in q.errors)
 if q.stack:errors.append(name+': unclosed tags')
 if lang not in ('de','en'):errors.append(name+': missing language')
 if not q.find('meta',name='description') or not q.find('meta',name='viewport'):errors.append(name+': missing metadata')
 for forbidden in ('5,26','5.26','C1 pending','C1 in Klärung','B2.1','Gesamtnote','Oster'+'kampsweg','015'+'20','Schwer'+'behinderung','nach IEC 61400','$$'):
  if forbidden in raw:errors.append(name+': stale/private '+forbidden)
 for tag,a in q.nodes:
  refs=[]
  if tag in ('a','link','script','img'):
   u=a.get('href',a.get('src'))
   if u:refs.append(u)
  if tag=='img' and 'srcset' in a:
   for item in a['srcset'].split(','):
    refs.append(item.strip().split()[0]);image_candidates+=1
   if not all(k in a for k in ('width','height','alt','sizes')):errors.append(name+': chart image metadata')
  for u in refs:
   s=urlsplit(u)
   if s.scheme or s.netloc:continue
   dest=(p.parent/unquote(s.path)).resolve() if s.path else p
   if dest.is_dir():dest=dest/'index.html'
   links+=1
   if not dest.exists():errors.append(name+': missing '+u)
   elif s.fragment and dest in pages and s.fragment not in pages[dest].ids:errors.append(name+': missing anchor '+u)
 theme_controls=q.classes('theme-toggle')
 if len(theme_controls)!=1 or 'hidden' not in theme_controls[0] or theme_controls[0].get('aria-pressed')!='false':errors.append(name+': progressive theme control')
 theme_scripts=q.find('script',src=('../' if 'legal' in p.parts else ('../../' if 'en' in p.parts and 'projects' in p.parts else ('../' if 'en' in p.parts or 'projects' in p.parts else '')))+'js/theme-init.js')
 if len(theme_scripts)!=1 or raw.index('js/theme-init.js')>raw.index('css/style.css'):errors.append(name+': theme initialization order')
 if not q.find('meta',name='color-scheme',content='light dark'):errors.append(name+': color scheme metadata')
 if 'legal' not in p.parts:
  alts=q.find('link',rel='alternate');canon=q.find('link',rel='canonical')[0]['href']
  if len(alts)!=3:errors.append(name+': hreflang set')
  own=next((a['href'] for a in alts if a.get('hreflang')==lang),None)
  other=next((a['href'] for a in alts if a.get('hreflang')==('en' if lang=='de' else 'de')),None)
  if own!=canon:errors.append(name+': self hreflang')
  if other:
   target=(ROOT/(urlsplit(other).path.lstrip('/') or 'index.html')).resolve()
   reciprocal=pages.get(target)
   if not reciprocal or not reciprocal.find('link',rel='alternate',hreflang=lang,href=canon):errors.append(name+': reciprocal hreflang')
  for anchor in q.classes('chart-button'):
   if not anchor.get('href','').endswith('.png'):errors.append(name+': chart original fallback')
 for a in q.classes('menu-toggle'):
  if 'hidden' not in a or a.get('aria-controls')!='navigation':errors.append(name+': progressive menu')
 if p.name=='index.html':
  if len(q.classes('metric'))!=3 or len(q.classes('contribution'))!=3:errors.append(name+': project evidence')
  if len(q.classes('contact-option'))!=3 or len(q.classes('contact-resume'))!=1:errors.append(name+': contact cards')
  if len(q.find('a',download='Ahmed_Abufanas_Lebenslauf.pdf'))!=2:errors.append(name+': CV actions')
  if not q.schemas or q.schemas[0]['mainEntity']['name']!='Ahmed Abufanas':errors.append(name+': profile schema')
  for key,precision in [('efc_reduction',2)]:
   if num(METRICS[key],lang,precision) not in raw:errors.append(name+': metric '+key)
  for w in WORK:
   if w['date'] not in raw or w['title'][0 if lang=='de' else 1] not in raw:errors.append(name+': shared work content')

pdf=PdfReader(ROOT/'assets/docs/Ahmed_Abufanas_Lebenslauf.pdf')
pdftext=' '.join(' '.join(p.extract_text() for p in pdf.pages).split())
if len(pdf.pages)!=2:errors.append('CV page count')
for x in ['5,27','44.685,44','418,30','32,44','Binaurale Modellierung','477 von 758','ohne angesetzte Zyklenkosten','Deutschlandweit umzugsbereit']:
 if x not in pdftext:errors.append('CV missing '+x)
for w in WORK:
 if w['title'][0] not in pdftext or w['date'] not in pdftext:errors.append('CV work parity '+w['date'])
for x in ['Oster'+'kampsweg','015'+'20','Schwer'+'behinderung','C1','1,82','2,26','Nullkosten']:
 if x in pdftext:errors.append('CV private or unsupported '+x)
margin=100*(1-Decimal('61417.49467077563')/Decimal('64831.0573913435'))
assert margin.quantize(Decimal('.01'),rounding=ROUND_HALF_UP)==Decimal('5.27')
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
sitemap=ET.parse(ROOT/'sitemap.xml')
locations=[x.text for x in sitemap.findall('.//s:loc',ns)]
if len(locations)!=8:errors.append('sitemap count')
for u in locations:
 path=ROOT/(urlsplit(u).path.lstrip('/') or 'index.html')
 if not path.exists():errors.append('sitemap missing '+u)
for project in PROJECTS:
 for lang in ('de','en'):
  page=ROOT/(('en/' if lang=='en' else '')+'projects/'+project['slug']+'.html')
  raw=page.read_text()
  if project['slug']=='bess-dispatch':
   for metric in ('bess_net','bess_efc','efc_reduction','margin_reduction'):
    if num(METRICS[metric],lang,2) not in raw:errors.append('BESS shared metric '+metric)
report={'html_pages':len(pages),'local_links_and_assets_checked':links,'responsive_image_candidates_checked':image_candidates,'pdf_pages':len(pdf.pages),'metric_rounding':'5.27% from full-precision source values','errors':errors,'browser_visual_and_native_interaction_tests':'NOT RUN: local browser access blocked in this environment','external_links':'GitHub source documents freshly checked; Streamlit/live site endpoints not rechecked'}
print(json.dumps(report,ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)
