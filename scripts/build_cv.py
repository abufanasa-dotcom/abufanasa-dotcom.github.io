"""Build the public two-page German résumé. Uses the same work and metric source as HTML."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT
from build import ROOT, WORK, METRICS, num, PROJECTS
fontdir=Path('/usr/share/fonts/truetype/dejavu')
# Set FONT_DIR to a folder containing DejaVuSans.ttf and DejaVuSans-Bold.ttf on another computer.
import os
fontdir=Path(os.environ.get('FONT_DIR',str(fontdir)))
pdfmetrics.registerFont(TTFont('DV',str(fontdir/'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DVB',str(fontdir/'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
W,H=595.28,841.89
c=canvas.Canvas(str(ROOT/'assets/docs/Ahmed_Abufanas_Lebenslauf.pdf'),pagesize=(W,H))
c.setTitle('Ahmed Abufanas | Lebenslauf');c.setAuthor('Ahmed Abufanas')
INK=HexColor('#172c3d');BLUE=HexColor('#125f85');MUTED=HexColor('#536473')
styles={
 'body':ParagraphStyle('body',fontName='DV',fontSize=9,leading=13,textColor=INK,spaceAfter=6),
 'small':ParagraphStyle('small',fontName='DV',fontSize=8,leading=11,textColor=MUTED),
 'title':ParagraphStyle('title',fontName='DVB',fontSize=11,leading=15,textColor=INK),
 'section':ParagraphStyle('section',fontName='DVB',fontSize=12,leading=16,textColor=BLUE),
}
y=0
def para(s,kind='body',gap=5):
 global y
 p=Paragraph(s,styles[kind]);_,height=p.wrap(W-88,1000)
 if y-height<45:raise ValueError('CV overflow')
 p.drawOn(c,44,y-height);y-=height+gap

def section(s):
 global y
 y-=8;para(s,'section',7)

def start(page):
 global y
 c.setFillColor(BLUE);c.rect(0,H-9,W,9,fill=1,stroke=0)
 c.setFillColor(INK);c.setFont('DVB',25);c.drawString(44,H-53,'Ahmed Abufanas')
 c.setFillColor(MUTED);c.setFont('DV',10);c.drawString(44,H-73,'Ingenieurphysik (B.Eng.) | Messdatenanalyse & Energiesysteme')
 c.setStrokeColor(HexColor('#dce4e8'));c.line(44,39,W-44,39)
 c.setFont('DV',8);c.drawString(44,25,'Ahmed Abufanas · Öffentlicher Lebenslauf · 01.10.2026');c.drawRightString(W-44,25,f'{page} / 2')
 y=H-92
start(1)
para('Oldenburg, Deutschland · <link href="mailto:abufanasa@gmail.com">abufanasa@gmail.com</link>','small')
para('<link href="https://www.linkedin.com/in/ahmedabufanas/">linkedin.com/in/ahmedabufanas</link> · <link href="https://github.com/abufanasa-dotcom">github.com/abufanasa-dotcom</link>','small')
para('<link href="https://abufanasa-dotcom.github.io/">abufanasa-dotcom.github.io</link> · Vollzeit / Teilzeit ab 01.11.2026 · Deutschlandweit umzugsbereit','small')
section('Profil')
para('Ingenieurphysiker (B.Eng.) mit Erfahrung in Python-basierter Messdatenanalyse, experimenteller Prüfung und technischer Dokumentation. Kenntnisse in MATLAB, SolidWorks, Modellierung und sensorbasierter Prototypenentwicklung. Beruflicher Schwerpunkt: Teststandstechnik, Energiespeicherung und technische Systementwicklung.')
section('Berufserfahrung')
for w in WORK:
 para(w['title'][0],'title',3)
 para(w['place']+' · '+w['date'],'small',5)
 para(w['description'][0],gap=10)
section('Ausbildung')
para('Masterstudium Ingenieurphysik (laufend)','title',3)
para('Carl von Ossietzky Universität Oldenburg · 10/2025 – voraussichtlich 02/2028','small')
para('Schwerpunkte: Energiesysteme, Energiespeicher, Photovoltaik, Messtechnik, Modellierung und Simulation.')
para('Bachelor of Engineering (B.Eng.) – Ingenieurphysik','title',3)
para('Carl von Ossietzky Universität Oldenburg · 10/2015 – 02/2025','small')
para('Abschlussarbeit: Binaural Detection and Auditory Modelling of Bandwidth Effects. MATLAB-basierte Signalverarbeitung und statistische Auswertung psychoakustischer Messdaten.')
c.showPage();start(2)
section('Ausgewählte Portfolio-Projekte')
para('Wind Turbine Performance Review','title',3)
para('Analyse von 52.560 Zehn-Minuten-Zeitpunkten aus SCADA-Daten (Kelmarsh Turbine 1, 2022). Referenzmodell, Regressionsvergleich und Streamlit-Dashboard; 5 Kandidaten-Ereignisse für weitere technische Prüfung. Historische Analyse, keine bestätigten Fehlerursachen.')
para('BESS Dispatch Analytics','title',3)
para('Historische MILP-Optimierung (SciPy/HiGHS) eines 1 MW / 2 MWh Speichers mit SMARD-Preisen 2024. 95 % Lade- und 95 % Entladewirkungsgrad (90,25 % Round-Trip). Bei 20 € je MWh äquivalenter Zyklenenergie: '+num(METRICS['bess_net'],'de',2)+' € simulierte Nettomarge und '+num(METRICS['bess_efc'],'de',2)+' EFC. Gegenüber der Optimierung ohne angesetzte Zyklenkosten: '+num(METRICS['efc_reduction'],'de',2)+' % weniger EFC bei '+num(METRICS['margin_reduction'],'de',2)+' % geringerer Brutto-Arbitragemarge. Bekannte historische Preise; keine real erzielten Erträge oder gemessene Zellalterung.')
para('Industrial Noise Exposure','title',3)
para('Datenaufbereitung und Dosisvergleich historischer NIOSH-HHE-Messungen. 477 von 758 gültigen personenbezogenen Messungen erreichten oder überschritten das 100-%-NIOSH-Dosiskriterium. Historische Untersuchungsstichprobe, keine repräsentative Aussage oder Konformitätsbewertung.')
section('Weitere akademische und technische Projekte')
for title,date,desc in [
('Electricity System Analysis & Energy Mix Optimization','03/2026 – 06/2026','Python-Modelle für europäische Energiesysteme; Kosten, Versorgungssicherheit, Emissionen und Wasserstoffszenarien.'),
('LIDAR-Based Insect Detection & Optical Signal Processing','02/2026 – 04/2026','Analyse zeit- und distanzaufgelöster LIDAR-Daten sowie Polarisations-, Reflexions- und Flügelschlagsignale.'),
('Binaurale Signaldetektion','02/2023 – 05/2023','Psychoakustische 3IFC-Experimente, N0Sπ-Stimuli und MATLAB-Auswertung.'),
('Solarzellen: Effizienz- und Belastungsanalyse','04/2022 – 08/2022','Temperatur- und Bestrahlungstests mit AM1.5-referenzierter Beleuchtung; MATLAB-Messdatenauswertung.'),
('Autonomer Fahrzeugprototyp','10/2019 – 03/2020','Arduino-Sensorik, Hinderniserkennung, Navigation und Python-Bedienoberfläche.'),
('3D-CAD und strukturmechanische Analyse','04/2019 – 08/2019','Parametrisches Hebesystem in SolidWorks; Untersuchung von Spannung, Verformung und Belastbarkeit.')]:
 para('<b>'+title+'</b> · '+date+'<br/>'+desc,'small',6)
section('Kenntnisse & Sprachen')
para('<b>Programmierung & Analyse:</b> Python, MATLAB, C++, Arduino, pandas, NumPy, SciPy, scikit-learn.<br/><b>Werkzeuge:</b> Simulink, SolidWorks, Git, Excel, Office 365, OriginPro, LaTeX, SharePoint.<br/><b>Deutsch und Englisch:</b> sehr gute Kenntnisse. <b>Arabisch:</b> Muttersprache.','small')
c.save()
print('Built two-page public CV')
