"""Generate static bilingual pages and the public CV from one content source.
Run: python scripts/build.py (Python 3; reportlab required for PDF only).
"""
from pathlib import Path
from html import escape as esc
import json
import hashlib
ROOT=Path(__file__).resolve().parents[1]
CSS_VERSION=hashlib.sha256((ROOT/'css/style.css').read_bytes().replace(b'\r\n',b'\n')).hexdigest()[:12]
JS_VERSION=hashlib.sha256((ROOT/'js/main.js').read_bytes().replace(b'\r\n',b'\n')).hexdigest()[:12]
BASE='https://abufanasa-dotcom.github.io'
GITHUB='https://github.com/abufanasa-dotcom'
EMAIL='abufanasa@gmail.com'
CV='assets/docs/Ahmed_Abufanas_Lebenslauf.pdf'
# Source: bess-dispatch-analytics/reports/degradation_sensitivity_2024.csv
METRICS={'wind_samples':52560,'wind_events':5,'bess_net':44685.442039196685,'bess_efc':418.3013157894737,'bess_zero_efc':619.1157894736841,'bess_gross':61417.49467077563,'bess_zero_gross':64831.0573913435,'noise_above':477,'noise_n':758,'noise_paired_above':672,'noise_paired_n':680}
METRICS['efc_reduction']=100*(1-METRICS['bess_efc']/METRICS['bess_zero_efc'])
METRICS['margin_reduction']=100*(1-METRICS['bess_gross']/METRICS['bess_zero_gross'])
def num(x,lang,d=0):
 s=f'{x:,.{d}f}'
 return s.translate(str.maketrans(',.','.,')) if lang=='de' else s

def tr(lang,de,en):return de if lang=='de' else en
PROJECTS=[
 {'slug':'wind-turbine','repo':'wind-turbine-performance','category':['Windenergie · Messdaten','Wind energy · Measurement data'],'title':['Leistungsabweichungen einer Windenergieanlage erkennen','Making power deviations visible.'],'short':['Leistungsanalyse einer Windenergieanlage','Wind Turbine Performance Review'],'image':'wind_measured_vs_estimated.png','source':'reports/figures/02_largest_event_review.png',
 'intro':['Historische Betriebsdaten aus dem SCADA-System (Überwachung, Steuerung und Datenerfassung) einer Windenergieanlage auswerten, um anhaltende Leistungsabweichungen für die technische Prüfung einzugrenzen.','Use historical data from a wind turbine’s supervisory control and data acquisition (SCADA) system to flag sustained power deviations for engineering review.'],
 'contributions':[['Betriebsereignisse und Datenqualität prüfen; eine windgeschwindigkeitsbasierte Referenz mit Regressionsmodellen vergleichen.','Zusammenhängende Abweichungen markieren und gespeicherte Ergebnisse in einem Streamlit-Dashboard untersuchen.'],['Screen operational events and data quality; compare a wind-speed reference with regression models.','Flag sustained deviations and inspect saved results through a Streamlit dashboard.']],
 'result':['5 auffällige Ereignisse für die technische Prüfung.','5 candidate events for engineering review.'],
 'limit':['Historische Analyse; Ursachen nicht bestätigt. Keine Live-Telemetrie.','Historical analysis; causes unconfirmed. No live telemetry.'],
 'caption':['Die Grafik zeigt die gemessene und die modellierte Leistung am 17. November 2022 für das Ereignis mit der größten geschätzten Energiedifferenz.','Largest candidate event: measured and modeled power on 17 November 2022.'],
 'tags':['Python','scikit-learn','Streamlit'],
 'method':[['52.560 Zehn-Minuten-Zeitpunkte aus 2022, Kelmarsh Turbine 1. Datenquelle: Kelmarsh wind farm data, Zenodo v4 (CC BY 4.0).','Training Januar–August; Modellauswahl September–Oktober; zusätzliche Auswertung November–Dezember. Ganzjährige Voranalysen schränken die Unabhängigkeit der letzten Periode ein.','Referenz: Medianleistung in 0,5-m/s-Windklassen. Das ML-Modell nutzt Windgeschwindigkeit und Windrichtung und schätzt zeitgleiche Leistung, keine zukünftige Produktion.','Schwelle aus Entwicklungsresiduen: etwa 277,47 kW, mindestens drei aufeinanderfolgende Zehn-Minuten-Werte.'],['52,560 ten-minute timestamps from 2022, Kelmarsh turbine 1. Source: Kelmarsh wind farm data, Zenodo v4 (CC BY 4.0).','Training January–August; model selection September–October; additional evaluation November–December. Whole-year exploratory analysis limits independence of the final period.','Reference: median power in 0.5 m/s wind-speed bins. The ML model uses wind speed and direction to estimate contemporaneous power, not future production.','Development-residual threshold: approximately 277.47 kW, with at least three consecutive ten-minute values.']],
 'detail':['Beim Ereignis mit der größten geschätzten Energiedifferenz liegt die gemessene Leistung im Mittel rund 350,88 kW unter der Modellschätzung. Unter der Annahme von sechs Zehn-Minuten-Intervallen ergibt sich eine geschätzte Energiedifferenz von 350,88 kWh. Zwischen dem ersten und letzten Zeitstempel (02:10–03:00 UTC) liegen 50 Minuten. Die tatsächlichen Intervallgrenzen bleiben offen.','In the largest event, measured power is about 350.88 kW below the model estimate on average. Assuming six ten-minute intervals, the estimated energy gap is 350.88 kWh. The first and last timestamps (02:10–03:00 UTC) are 50 minutes apart. The exact interval boundaries remain uncertain.'],
 'limits':['Abweichungen sind keine bestätigten Defekte oder nachweislich rückgewinnbare Energieverluste. Die individuelle Kontextprüfung der übrigen vier Ereignisse und eine externe Jahresvalidierung stehen laut Projektdokumentation noch aus.','Deviations are not confirmed defects or proven recoverable energy losses. Individual context review of the other four events and external-year validation are outstanding in the project documentation.'],
 'demo':'https://abufanasa-dotcom-wind-turbine-performance-app-vtq3j5.streamlit.app/'},
 {'slug':'bess-dispatch','repo':'bess-dispatch-analytics','category':['Energiespeicher · Optimierung','Energy storage · Optimization'],'title':['Den Einsatz eines Batteriespeichers optimieren','Optimizing battery dispatch transparently.'],'short':['Einsatzplanung für einen Batteriespeicher','BESS Dispatch Analytics'],'image':'bess_dispatch_soc_schedule.png','source':'reports/figures/representative_day_dispatch.png',
 'intro':['Wie verändern angesetzte Zyklenkosten den Betrieb eines Batteriespeichers und die Marge aus dem Stromhandel? Die Modellstudie nutzt historische Day-Ahead-Preise der Gebotszone Deutschland/Luxemburg.','How does an assumed cycling cost affect the arbitrage margin and operation of a battery energy storage system (BESS)? The model uses historical day-ahead prices for the Germany–Luxembourg bidding zone.'],
 'contributions':[['Fahrplanoptimierung mittels gemischt-ganzzahliger linearer Programmierung (MILP) mit SciPy/HiGHS und physikalischer Konsistenzprüfung.','Zyklenkosten-Szenarien anhand von SMARD-Preisen 2024 vergleichen.'],['Dispatch optimization using mixed-integer linear programming (MILP) with SciPy/HiGHS and physical consistency checks.','Compare cycling-cost scenarios using 2024 SMARD prices.']],
 'result':['32,44 % weniger äquivalente Vollzyklen gegenüber der Optimierung ohne angesetzte Zyklenkosten.','32.44% fewer equivalent full cycles than optimization without assumed cycling costs.'],
 'limit':['Historische Simulation mit nachträglich bekannten Preisen und angesetzten Zyklenkosten von 20 € je MWh äquivalenter Zyklenenergie.','€20 per MWh of equivalent-cycle energy; historical simulation with perfect price foresight.'],
 'caption':['12. Dezember 2024: Tag mit der höchsten täglichen Nettomarge im nominalen Szenario, kein Durchschnittstag.','12 December 2024: highest daily net margin in the nominal scenario, not an average day.'],
 'tags':['Python','SciPy / HiGHS','SMARD'],
 'method':[['Batteriespeichermodell mit 1 MW / 2 MWh; Ladezustand (SOC) zwischen 10 und 90 %; Anfangs- und Endladezustand jedes Liefertags: 50 %.','8.784 Stunden im Schaltjahr 2024, DE/LU Day-Ahead-Preise. Lokale Liefertage mit 23, 24 oder 25 Stunden berücksichtigen die Zeitumstellung.','95 % Lade- und 95 % Entladewirkungsgrad, entsprechend 90,25 % Round-Trip-Wirkungsgrad. Binäre Variablen verhindern gleichzeitiges Laden und Entladen.','Optimierung je Liefertag mit bekannten historischen Preisen. Zyklenkosten werden als ökonomischer Proxy modelliert; Fahrpläne werden durch das Batteriemodell nachgerechnet.'],['1 MW / 2 MWh battery energy storage system (BESS); state of charge (SOC) between 10 and 90%; each delivery day starts and ends at 50% SOC.','8,784 hours in leap year 2024, DE/LU day-ahead prices. Local delivery days contain 23, 24 or 25 hours to account for daylight saving.','95% charging and 95% discharging efficiency, equivalent to 90.25% round-trip efficiency. Binary variables prevent simultaneous charge and discharge.','Daily optimization with known historical prices. Cycling costs act as an economic proxy; schedules are replayed through the battery model.']],
 'detail':['Verglichen werden die optimierten Szenarien mit 20 € und 0 € je MWh äquivalenter Zyklenenergie. Ein äquivalenter Vollzyklus (EFC) entspricht im Modell einem Energiedurchsatz auf Batterieseite von einer Nennkapazität beim Laden und einer beim Entladen. Die Netto-Arbitragemarge zieht die angesetzten Zyklenkosten von der Brutto-Arbitragemarge ab. Die prozentuale Änderung der Bruttomarge wird aus ungerundeten Werten berechnet. Der feste Referenzfahrplan mit 292,80 EFC dient als separate Vergleichsbasis.','The comparison uses the optimized scenarios at €20 and €0 per MWh of equivalent-cycle energy. In this model, one equivalent full cycle (EFC) represents one nominal capacity of battery-side energy charged and one discharged. Net arbitrage margin subtracts the assumed cycling cost from gross arbitrage margin. The percentage change in gross margin uses unrounded values. The fixed reference schedule of 292.80 EFC serves as a separate baseline.'],
 'limits':['Retrospektive Modellrechnung, keine real erzielten Erträge und keine validierte Handelsstrategie. Kapital-, Netz-, Steuer- und weitere Projektkosten fehlen. Weniger modellierte Zyklen belegen keine gemessene Lebensdauerverlängerung; kein elektrochemisches Alterungsmodell.','Retrospective modeling, not realized commercial earnings or a validated trading strategy. Capital, grid, tax and other project costs are excluded. Fewer modeled cycles do not establish measured lifetime extension; no electrochemical aging model.']},
 {'slug':'noise-exposure','repo':'industrial-noise-exposure','category':['Akustik · Datenqualität','Acoustics · Data quality'],'title':['Lärmexposition aus historischen Arbeitsplatzmessungen auswerten','Interpreting noise data in context.'],'short':['Lärmexposition am Arbeitsplatz','Industrial Noise Exposure'],'image':'noise_niosh_dose_distribution.png','source':'reports/figures/01_personal_niosh_dose_distribution.png',
 'intro':['Historische Arbeitsplatzmessungen aufbereiten und unterschiedliche Dosisdefinitionen vergleichen, ohne die Untersuchungsergebnisse zu verallgemeinern.','Prepare historical workplace measurements and compare dose definitions without generalizing investigation findings.'],
 'contributions':[['Daten und Qualitätskennzeichen getrennt erhalten; dokumentierte Formelabweichungen korrigieren.','NIOSH- und OSHA-Dosen in gepaarten Messungen vergleichen und geeignete Teilmengen getrennt auswerten.'],['Preserve data and quality flags; correct documented formula discrepancies.','Compare paired NIOSH and OSHA doses and analyze compatible subsets separately.']],
 'result':['477 von 758 Messungen erreichen oder überschreiten das 100-%-NIOSH-Dosiskriterium.','477 of 758 measurements meet or exceed the 100% NIOSH dose criterion.'],
 'limit':['Historische Untersuchungsstichprobe; keine repräsentative Aussage oder Konformitätsbewertung.','Historical investigation sample; no population-wide inference or compliance assessment.'],
 'caption':['Verteilung der NIOSH-Dosen: 758 gültige personenbezogene Messungen, logarithmische Dosisachse.','NIOSH dose distribution: 758 valid personal measurements, logarithmic dose axis.'],
 'tags':['Python','pandas','NumPy'],
 'method':[['Archivierte NIOSH-HHE-Untersuchungen, überwiegend 1996–2007, mit einzelnen Fällen bis 2013.','807 personenbezogene und 582 Bereichsmessungen; getrennte Tabellen und Kennzeichnung fehlender oder problematischer Werte.','758 gültige NIOSH-Dosiswerte; 680 gültige gepaarte NIOSH-/OSHA-Messungen. Diese Zahlen beschreiben Messungen, nicht zwingend unterschiedliche Personen.','Für die separate deutsche Einordnung werden nur 33 Datensätze mit geeigneten Leq- und Dauerdaten verwendet. NIOSH-Dosiswerte sind nicht mit dem Tages-Lärmexpositionspegel L<sub>EX,8h</sub> gleichzusetzen.'],['Archived NIOSH HHE investigations, mainly 1996–2007, with selected cases through 2013.','807 personal and 582 area measurements; separate tables and flags for missing or problematic values.','758 valid NIOSH dose values; 680 valid paired NIOSH/OSHA measurements. These counts describe measurements, not necessarily distinct individuals.','Only 33 records with suitable Leq and duration data support the separate German-context analysis. NIOSH dose values are not interchangeable with the daily noise exposure level L<sub>EX,8h</sub>.']],
 'detail':['In 672 von 680 gepaarten Messungen (98,82 %) liegt die NIOSH-Dosis über der OSHA-PEL-Dosis. Die NIOSH-Empfehlung (REL) verwendet einen Acht-Stunden-Bezugspegel von 85 dB(A) und eine Austauschrate von 3 dB. Für die OSHA-PEL-Dosis gelten ein Acht-Stunden-Bezugspegel von 90 dB(A) und eine Austauschrate von 5 dB. Verglichen werden zwei Dosisdefinitionen für dieselben gepaarten Messdatensätze.','In 672 of 680 paired measurements (98.82%), the NIOSH dose is higher than the OSHA PEL dose. The NIOSH recommended exposure limit (REL) uses an 85 dBA eight-hour criterion and a 3 dB exchange rate. The OSHA permissible exposure limit (PEL) uses 90 dBA over eight hours and a 5 dB exchange rate. The comparison reflects results under two dose definitions for the same paired records.'],
 'limits':['Anlassbezogene Untersuchungen sind keine repräsentative Stichprobe aller Arbeitsplätze. Die Auswertung ist keine arbeitsmedizinische Beurteilung und keine zertifizierte Prüfung deutscher Grenzwerte.','Investigation-based samples are not representative of all workplaces. The analysis is not a medical evaluation or certified assessment of German exposure limits.']}
]
PROJECTS[1]['demo']='https://bess-dispatch-analytics.streamlit.app/'
PROJECTS[2]['demo']='https://industrial-noise-exposure.streamlit.app/'
WORK=[
 {'date':'02/2026 – 09/2026','title':['Wissenschaftliche Hilfskraft – Spektralanalyse und Python-Datenverarbeitung','Research Assistant – Spectral Analysis and Python Data Processing'],'place':'Hochschule Emden/Leer','description':['Weiterentwicklung einer BACHES-Python-Pipeline, Aufbereitung von Bild- und Messdaten sowie Verbesserung der Code-Lesbarkeit und Qualitätssicherungsdokumentation.','Extended a BACHES Python pipeline, prepared image and measurement data, and improved code readability and documentation for quality assurance.']},
 {'date':'03/2026 – 09/2026','title':['Student Buddy · International Office','Student Buddy · International Office'],'place':'Carl von Ossietzky Universität Oldenburg','description':['Begleitung internationaler Studierender bei Ankunft und Orientierung; Unterstützung organisatorischer Abläufe und Kommunikation mit universitären Stellen.','Supported international students with arrival, orientation and administrative procedures, and coordinated communication with university departments.']},
 {'date':'03/2023 – 12/2023','title':['Wissenschaftliche Hilfskraft · Binaurale Modellierung & Machine Learning','Research Assistant · Binaural Modeling & Machine Learning'],'place':'Carl von Ossietzky Universität Oldenburg','description':['Komponenten zweier akustischer Modelle integriert, Modelldateien und Verarbeitungsschritte strukturiert sowie MATLAB-basierte ML-Routinen für Hörversuche und Datenanalyse implementiert und ausgewertet.','Integrated components of two acoustic models, organized model files and processing stages, and implemented and evaluated MATLAB-based ML routines for auditory experiments and data analysis.']}
]
PROJECTS[0]['result']=[f"{METRICS['wind_events']} auffällige Ereignisse für die technische Prüfung.",f"{METRICS['wind_events']} candidate events for engineering review."]
PROJECTS[1]['result']=[num(METRICS['efc_reduction'],'de',2)+' % weniger äquivalente Vollzyklen gegenüber der Optimierung ohne angesetzte Zyklenkosten.',num(METRICS['efc_reduction'],'en',2)+'% fewer equivalent full cycles than optimization without assumed cycling costs.']
PROJECTS[2]['result']=[f"{METRICS['noise_above']} von {METRICS['noise_n']} Messungen erreichen oder überschreiten das 100-%-NIOSH-Dosiskriterium.",f"{METRICS['noise_above']} of {METRICS['noise_n']} measurements meet or exceed the 100% NIOSH dose criterion."]
PROJECTS.append({'slug': 'windconnect', 'repo': 'windconnect', 'category': ['Windenergie · Kommunikationsdiagnose', 'Wind energy · Communication diagnostics'], 'title': ['WindConnect: Kommunikation und Messdaten mit Modbus TCP überwachen', 'WindConnect: Modbus TCP Monitoring and Fault Diagnostics'], 'short': ['WindConnect – Überwachung mit Modbus TCP', 'WindConnect – Modbus TCP Monitoring'], 'image': 'windconnect_stale_data.png', 'source': 'screenshots/public-stale-de.png', 'intro': ['Die Simulation einer Windenergieanlage prüft getrennt, ob die Modbus-TCP-Verbindung funktioniert und ob die Messdaten gültig und aktuell sind.', 'Simulate a wind turbine and separately monitor Modbus TCP communication, measurement validity, and data freshness.'], 'contributions': [['Einen deterministischen Simulator einer 3-MW-Windenergieanlage, eine versionierte Registerbelegung und einen separaten Modbus-TCP-Client umgesetzt.', 'Verbindungsverlust, veraltete Messdaten und ungültige Messwerte mit expliziter Diagnosepriorität, Wiederherstellungsereignissen und einem Protokoll ohne wiederholte identische Störungsmeldungen implementiert.', 'Ein deutsches lokales Dashboard und eine deutsch-englische öffentliche Demo mit getrennten Besuchersitzungen entwickelt.'], ['Built a deterministic simulator of a 3 MW wind turbine, a versioned register map, and a separate Modbus TCP client.', 'Implemented connection loss, stale measurement data, and invalid measurements with explicit diagnostic priority, recovery events, and logging that avoids repeated identical fault messages.', 'Developed a German local dashboard and a German/English public demo with isolated visitor sessions.']], 'result': ['66 automatisierte Tests bestanden; Kommunikationsfehler, Messdatenfehler, Wiederherstellung und getrennte Besuchersitzungen geprüft.', '66 automated tests passed, covering communication faults, measurement data faults, recovery, and isolated visitor sessions.'], 'limit': ['Eigenständige lokale Simulation; keine Verbindung zu realen Anlagen oder emsys-Systemen.', 'Independent local simulation; no connection to real turbines or emsys systems.'], 'caption': ['Deutschsprachige Dashboard-Aufnahme: STALE_DATA bei weiterhin erfolgreichen Modbus-Leseanfragen; sämtliche Messwerte sind synthetisch.', 'English dashboard capture: STALE_DATA while Modbus read requests continue to succeed; all measurements are synthetic.'], 'tags': ['Python', 'Modbus TCP', 'Streamlit', 'pytest'], 'method': [['Synthetische Wirkleistung in kW, Windgeschwindigkeit in m/s, Betriebszustand, UTC-Messzeitstempel und Sequenznummer; vereinfachte begrenzte Leistungskennlinie.', 'Zwölf 16-Bit-Holding-Register werden über Modbus-Funktionscode 03 (Read Holding Registers) gelesen. Mehrwortwerte verwenden in diesem Projekt das höchstwertige Wort zuerst.', 'Diagnosepriorität: CONNECTION_LOST → INVALID_MEASUREMENT → STALE_DATA → HEALTHY. Sequenznummer und Messzeitstempel müssen fortschreiten; Standard-Aktualitätsschwelle 5 s.', 'Die öffentliche Demo führt pro Abfrage einen tatsächlichen Modbus-TCP-Austausch ausschließlich serverseitig auf 127.0.0.1 aus und schließt anschließend den Listener. Der Browser zeigt Ergebnisse und steuert die eigene Simulationssitzung.'], ['Synthetic active power in kW, wind speed in m/s, operating state, UTC measurement timestamp, and sequence number, using a simplified bounded power curve.', 'Modbus function code 03 (Read Holding Registers) reads twelve 16-bit holding registers. This project places the most significant word first in multi-register values.', 'Diagnostic priority: CONNECTION_LOST → INVALID_MEASUREMENT → STALE_DATA → HEALTHY. Sequence number and measurement timestamp must advance; default freshness threshold: 5 s.', 'Each public-demo poll performs an actual Modbus TCP exchange exclusively on the server at 127.0.0.1, then closes the listener. The browser displays results and controls its own simulation session.']], 'detail': ['Die Diagnose unterscheidet die Erreichbarkeit des Modbus-Dienstes von der Gültigkeit und Aktualität seiner Messdaten. STALE_DATA kann deshalb trotz erfolgreicher Leseanfragen auftreten. Nach einer neuen, gültigen und aktuellen Probe wird RECOVERED protokolliert. Die lokale Variante bietet zusätzlich einen fortlaufenden Backend-Prozess und dateibasierte Protokolle.', 'The diagnostics distinguish Modbus service availability from the validity and freshness of its measurements. STALE_DATA can therefore occur despite successful read requests. A new, valid, fresh sample produces a RECOVERED event. The local version additionally provides a continuously running backend and file-based logs.'], 'limits': ['Eigenständige Simulation mit vereinfachter Leistungskennlinie und begrenzter Historie. Der Bezug zu einem virtuellen Kraftwerk (VPP) ist ein Anwendungskontext; keine reale VPP-Anbindung, Anlagensteuerung, emsys-Kooperation oder industrielle Zertifizierung. HEALTHY ist keine umfassende Zustandsbewertung einer echten Anlage.', 'Independent simulation with a simplified power curve and bounded history. A virtual power plant (VPP) is the application context; there is no real VPP integration, turbine control, emsys collaboration, or industrial certification. HEALTHY is not a comprehensive assessment of a real turbine.'], 'test_count': 66, 'terminology': [[('Kommunikationsstatus', 'Erfolg oder Fehlschlag der Modbus-Leseanfrage.'), ('Messwertgültigkeit', 'Registerformat, Betriebszustand und zulässige Wertebereiche.'), ('Datenaktualität', 'Fortschritt von Sequenznummer und Messzeitstempel sowie Alter der Probe.')], [('Communication status', 'Success or failure of the Modbus read request.'), ('Measurement validity', 'Register format, operating state, and permitted value ranges.'), ('Data freshness', 'Progress of the sequence number and measurement timestamp, plus sample age.')]], 'image_en': 'windconnect_stale_data_en.png', 'source_en': 'screenshots/public-stale-en.png', 'demo': 'https://windconnect-monitoring.streamlit.app/', 'demo_en': 'https://windconnect-monitoring.streamlit.app/?lang=English', 'demo_note': ['Interaktive Demo mit synthetischen Messdaten und eigener Besuchersitzung. Der tatsächliche Modbus-TCP-Austausch findet ausschließlich serverseitig auf Loopback statt.', 'Interactive demo with synthetic measurements and an isolated visitor session. The actual Modbus TCP exchange occurs exclusively on the server over loopback.']})
CONTRIBUTION_SUMMARIES=[
 ['Datenqualität geprüft, Referenz- und Regressionsmodelle verglichen und Abweichungsereignisse ausgewertet.','Screened data quality, compared reference and regression models, and reviewed deviation events.'],
 ['MILP-Fahrplanoptimierung entwickelt und Fahrpläne mit dem Batteriemodell auf physikalische Konsistenz geprüft.','Developed MILP dispatch optimization and checked schedules for physical consistency using the battery model.'],
 ['Messdaten aufbereitet, dokumentierte Formelabweichungen korrigiert und Dosisdefinitionen verglichen.','Prepared measurement data, corrected documented formula discrepancies, and compared dose definitions.']]
CONTRIBUTION_SUMMARIES.append(['Simulator, Modbus-TCP-Kommunikation, Zustandslogik und ein deutschsprachiges Dashboard entwickelt und automatisiert getestet.', 'Developed the simulator, Modbus TCP transport, diagnostic state machine, and German support dashboard with automated tests.'])
IMAGE_INFO=json.loads((ROOT/'assets/images/projects/image_manifest.json').read_text(encoding='utf-8'))

def text(v,lang):return v[0 if lang=='de' else 1]
def link(path,label,cls=''):return f'<a class="{cls}" href="{esc(path,quote=True)}">{label}</a>'
def contact_link(label,cls='',subject=''):
 from urllib.parse import quote
 href='mailto:'+EMAIL+('?subject='+quote(subject) if subject else '')
 return f'<a class="{cls}" href="{esc(href,quote=True)}" data-contact data-subject="{esc(subject,quote=True)}">{label}</a>'
def contact_dialog(lang):
 return f'''<dialog id="contact-dialog" aria-labelledby="contact-dialog-title" aria-describedby="contact-dialog-description"><div class="dialog-header"><h2 id="contact-dialog-title">{tr(lang,'Kontakt aufnehmen','Get in touch')}</h2><button class="dialog-close" autofocus>{tr(lang,'Schließen','Close')} ×</button></div><p id="contact-dialog-description">{tr(lang,'Wählen Sie, wie Sie Ihre Nachricht schreiben möchten.','Choose how you would like to write your message.')}</p><p class="contact-recipient">{EMAIL}</p><p class="contact-subject" hidden></p><div class="email-options"><a class="button primary" data-gmail href="https://mail.google.com/mail/?view=cm&amp;fs=1&amp;to={EMAIL}" target="_blank" rel="noopener noreferrer">{tr(lang,'In Gmail schreiben','Write in Gmail')} ↗</a><a class="button secondary" data-mail-app href="mailto:{EMAIL}">{tr(lang,'E-Mail-Programm öffnen','Use email app')} ↗</a><button class="button secondary copy-email" data-email="{EMAIL}">{tr(lang,'E-Mail-Adresse kopieren','Copy email address')}</button></div><p class="copy-status" role="status" aria-live="polite"></p><p class="email-note">{tr(lang,'Gmail öffnet sich in einem neuen Tab. Eine Nachricht wird erst gesendet, wenn Sie sie selbst absenden.','Gmail opens in a new tab. No message is sent until you send it yourself.')}</p></dialog>'''
def cv_link(prefix,lang):
 return f'<a class="button secondary" href="{prefix+CV}" download="Ahmed_Abufanas_Lebenslauf.pdf">{tr(lang,"Lebenslauf · PDF","CV (DE) · PDF")}</a>'

def profile_highlights(lang):
 highlights=[
  ('#work-baches',
   tr(lang,'Spektralanalyse mit Python','Spectral analysis with Python'),
   tr(lang,'Bild- und Messdaten für die BACHES-Pipeline aufbereitet.','Prepared image and measurement data for the BACHES pipeline.')),
  ('#work-binaural',
   tr(lang,'Binaurale Hörmodelle in MATLAB','Binaural hearing models in MATLAB'),
   tr(lang,'Komponenten zweier Modelle für Hörversuche integriert.','Integrated components from two models for auditory experiments.')),
  ('#education',
   tr(lang,'Studium der Ingenieurphysik','Engineering Physics studies'),
   tr(lang,'Bachelorabschluss und laufendes Masterstudium an der Universität Oldenburg.','B.Eng. and ongoing master’s studies at the University of Oldenburg.')),
 ]
 links=''.join(f'<a href="{href}"><strong>{title}</strong><span>{description}</span></a>' for href,title,description in highlights)
 return f'''<details class="profile-highlights">
 <summary>{tr(lang,'Einblicke in meine Arbeit und mein Studium','Highlights from my work and studies')}<span class="details-chevron" aria-hidden="true"></span></summary>
 <div class="highlight-links">{links}</div>
 </details>'''

def contact_section(lang):
 mail_icon='<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="3" y="5" width="18" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="m4 7 8 6 8-6" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>'
 linkedin_icon='<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M19 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2ZM8.5 17.5H6v-7h2.5v7ZM7.25 9.25a1.25 1.25 0 1 1 0-2.5 1.25 1.25 0 0 1 0 2.5ZM18 17.5h-2.5v-3.75c0-.84-.37-1.25-1-1.25-.81 0-1.25.53-1.25 1.5v3.5H10.8v-7h2.35v.95a2.56 2.56 0 0 1 2.23-1.13c1.6 0 2.62 1.04 2.62 2.95v4.23Z"/></svg>'
 github_icon='<svg viewBox="-2 -2 20 20" aria-hidden="true" focusable="false"><path fill="currentColor" d="M8 0a8 8 0 0 0-2.53 15.59c.4.07.55-.17.55-.38v-1.49c-2.23.48-2.7-.94-2.7-.94-.36-.93-.89-1.18-.89-1.18-.73-.5.06-.49.06-.49.8.06 1.22.82 1.22.82.72 1.22 1.88.87 2.34.67.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.96 0-.87.31-1.58.82-2.14-.08-.2-.36-1.01.08-2.11 0 0 .67-.21 2.2.82a7.67 7.67 0 0 1 4 0c1.53-1.03 2.2-.82 2.2-.82.44 1.1.16 1.91.08 2.11.51.56.82 1.27.82 2.14 0 3.08-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48v2.2c0 .21.15.46.55.38A8 8 0 0 0 8 0Z"/></svg>'
 button_class='button secondary contact-option'
 email_label=f"{mail_icon}<span>{tr(lang,'E-Mail','Email')}</span>"
 return f'''<section class="container contact" id="contact">
 <h2>{tr(lang,'Kontakt','Contact')}</h2>
 <p class="contact-intro">{tr(lang,'Ob Fragen, Zusammenarbeit oder berufliche Möglichkeiten – ich freue mich über Ihre Nachricht.','Feel free to get in touch with questions, ideas for collaboration, or job opportunities.')}</p>
 <div class="contact-options">
 {contact_link(email_label,button_class)}
 {link('https://www.linkedin.com/in/ahmedabufanas/',linkedin_icon+'<span>LinkedIn</span>',button_class)}
 {link(GITHUB,github_icon+'<span>GitHub</span>',button_class)}
 </div>
 </section>'''
EMSLAND_SERIES = [('B DT', 88166, 490, 329), ('C DT', 6879, 118, 76), ('D DT', 368211, 912, 537)]
EMSLAND_HOURS = 744
EMSLAND_TOTAL = EMSLAND_HOURS * len(EMSLAND_SERIES)
EMSLAND_SHARE = 100 * EMSLAND_SERIES[-1][1] / sum(row[1] for row in EMSLAND_SERIES)

PROJECTS.append({
 'slug': 'emsland-sql',
 'display_order': 5,
 'repo': 'emsland-sql',
 'code_archive': 'assets/docs/emsland-sql-code.zip',
 'category': ['Stromerzeugung · SQL-Datenanalyse', 'Power generation · SQL data analysis'],
 'short': ['Emsland: Einspeisedaten mit SQL auswerten', 'Emsland Generation Data with SQL'],
 'title': ['Einspeisezeitreihen aus Emsland mit SQL analysieren', 'Analyzing Emsland generation data with SQL'],
 'image': 'emsland_energy_de.png',
 'image_en': 'emsland_energy_en.png',
 'intro': ['Wie verteilt sich die erfasste Energie im Januar 2025 auf die drei ausgewählten Einspeisezeitreihen des Standorts Emsland?',
           'Three published Emsland generation series for January 2025: how is recorded energy distributed across them?'],
 'contributions': [
  ['Ein relationales SQLite-Schema mit Schlüsseln und einer View für die Intervallenergie aufgebaut.',
   'Neun SQL-Abfragen für Vollständigkeit, Aggregation, Rangfolgen und Zeitreihenvergleiche erstellt. Die Auswertung entstand mit KI-Unterstützung.'],
  ['Built a relational SQLite schema with keys and a view for interval energy.',
   'Developed nine SQL queries for coverage, aggregation, rankings, and time-series comparisons. The analysis was developed with AI assistance.']],
 'contribution_summary': ['SQLite-Schema aufgebaut und neun SQL-Abfragen für Vollständigkeit, Energiesummen und Zeitreihenvergleiche erstellt.',
                          'Built a SQLite schema and nine SQL queries for coverage, energy totals, and time-series comparisons.'],
 'result': [f'{num(EMSLAND_SHARE,"de",2)} % der erfassten Energie der drei ausgewählten Reihen entfallen auf D DT.',
            f'D DT accounts for {num(EMSLAND_SHARE,"en",2)}% of the recorded energy across the three selected series.'],
 'limit': ['Januar 2025 · Drei veröffentlichte Reihen. Die Zuordnung zu physischen Blöcken und ihrer Nennleistung bleibt offen.',
           'January 2025 · Three published series. Mapping to physical units and their rated capacities remains unverified.'],
 'caption': ['Erfasste Energie in GWh für B DT, C DT und D DT im Januar 2025. D DT hat den höchsten Wert.',
             'Recorded energy in GWh for B DT, C DT, and D DT in January 2025. D DT has the highest value.'],
 'tags': ['SQL', 'SQLite', 'Python', 'SMARD'],
 'method': [
  [f'{num(EMSLAND_TOTAL,"de")} Beobachtungen aus {EMSLAND_HOURS} Stunden je Reihe. Die Quelldaten verwenden die mitteleuropäische Zeit (MEZ) und werden zusätzlich in UTC gespeichert.',
   'Die mittlere Leistung in MW wird mit der Intervalldauer von einer Stunde multipliziert. Das ergibt die Intervallenergie in MWh.',
   'LAG vergleicht zwei aufeinanderfolgende Stundenmittel innerhalb derselben Reihe. Die SQL-Energiesummen wurden mit den Originalwerten unabhängig abgeglichen.'],
  [f'{num(EMSLAND_TOTAL,"en")} observations across {EMSLAND_HOURS} hours per series. The source uses Central European Time (CET), with timestamps also stored in UTC.',
   'Multiplying hourly average power in MW by the one-hour interval duration gives interval energy in MWh.',
   'LAG compares consecutive hourly averages within the same series. SQL energy totals were independently reconciled with the original values.']],
 'detail': ['Die Reihe D DT enthält in 537 von 744 Stunden einen positiven Wert. Das höchste veröffentlichte Stundenmittel für D DT beträgt 912 MW.',
            'D DT reports a positive value in 537 of 744 hours. Its highest published hourly average is 912 MW.'],
 'limits': ['Unabhängige Fallstudie mit Daten von SMARD. Die Kennzahlen gelten für die ausgewählten Quellenreihen. Ein Kapazitätsfaktor setzt eine bestätigte zeitgültige Nennleistung voraus. Die Daten liefern keine Betriebsgründe für gemeldete Nullwerte.',
            'Independent case study using SMARD data. Metrics describe the selected source series. A capacity factor would require verified, time-valid rated capacity. The data do not identify the operational causes of reported zero values.'],
})


PROJECT_NOTES = [
 ('wind-turbine', ['Windenergie: Wann lohnt sich ein genauerer Blick?', 'Wind energy: When is a closer look warranted?'],
  ['Der Vergleich von Messung und Modell zeigte fünf anhaltende Leistungsabweichungen für die technische Prüfung.',
   'Comparing measured and modeled power flagged five sustained deviations for engineering review.']),
 ('emsland-sql', ['Emsland SQL: Was ändert sich von Stunde zu Stunde?', 'Emsland SQL: What changes from one hour to the next?'],
  ['Mit LAG vergleiche ich den aktuellen Stundenmittelwert der Leistung mit dem Wert der vorherigen Stunde in derselben Reihe.',
   'I use LAG to compare each hourly average power value with the previous hour in the same series.']),
 ('bess-dispatch', ['Batteriespeicher: Was ändern Zyklenkosten?', 'Battery storage: What changes when cycling has a cost?'],
  [f"Mit angesetzten Zyklenkosten ergab die Simulation {num(METRICS['efc_reduction'],'de',2)} % weniger äquivalente Vollzyklen als die Optimierung ohne diese Kosten.",
   f"The simulation with a cycling cost produced {num(METRICS['efc_reduction'],'en',2)}% fewer equivalent full cycles than the optimization without that cost."]),
 ('noise-exposure', ['Lärmexposition: Warum zwei Dosen aus derselben Messung?', 'Noise exposure: Why can one measurement yield two doses?'],
  ['NIOSH und OSHA verwenden unterschiedliche Bezugspegel und Austauschraten. Deshalb kann dieselbe Messung zwei verschiedene Dosiswerte ergeben.',
   'NIOSH and OSHA use different criterion levels and exchange rates, so the same measurement can yield two different dose values.']),
 ('windconnect', ['WindConnect: Die Verbindung steht, die Daten sind veraltet', 'WindConnect: The connection works, but the data are stale'],
  ['In der Simulation antwortet Modbus TCP weiterhin, obwohl sich der Messzeitstempel nicht mehr ändert. Die Diagnose zeigt STALE_DATA.',
   'In the simulation, Modbus TCP keeps responding after the measurement timestamp stops advancing. The diagnostic state is STALE_DATA.']),
]

TECHNICAL_SOURCES = {
 'emsland-sql': [
  ('https://www.smard.de/home/downloadcenter/download-kraftwerksdaten', 'Bundesnetzagentur | SMARD.de: Kraftwerksdaten', 'Bundesnetzagentur | SMARD.de: power plant data'),
  ('https://www.smard.de/home/datennutzung', 'SMARD-Datennutzung (CC BY 4.0)', 'SMARD data use (CC BY 4.0)'),
 ],
 'wind-turbine': [
  ('https://zenodo.org/records/16807551', 'Kelmarsh SCADA-Datensatz (Zenodo, v4)', 'Kelmarsh SCADA dataset (Zenodo, v4)'),
  (GITHUB+'/wind-turbine-performance/blob/main/reports/underperformance_review_events.csv', 'Tabelle der identifizierten Ereignisse', 'Table of flagged events'),
 ],
 'bess-dispatch': [
  ('https://www.smard.de/home/datennutzung', 'Bundesnetzagentur | SMARD.de', 'Bundesnetzagentur | SMARD.de'),
  (GITHUB+'/bess-dispatch-analytics/blob/main/reports/degradation_aware_summary_20eur_2024.json', 'Szenarioergebnisse mit ungerundeten Werten', 'Scenario results with unrounded values'),
 ],
 'noise-exposure': [
  ('https://www.cdc.gov/niosh/noise/prevent/understand.html', 'NIOSH: Lärmexposition und Dosimetrie', 'NIOSH: noise exposure and dosimetry'),
  ('https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.95', 'OSHA: Lärmexposition am Arbeitsplatz', 'OSHA: occupational noise exposure'),
  (GITHUB+'/industrial-noise-exposure/blob/main/reports/dashboard_metric_registry.csv', 'Kennzahlen und Stichprobengrößen', 'Metrics and sample sizes'),
 ],
 'windconnect': [
  ('https://www.modbus.org/file/secure/modbusprotocolspecification.pdf', 'Modbus-Spezifikation (Abschnitt 6.3)', 'Modbus specification (section 6.3)'),
  (GITHUB+'/windconnect/blob/main/docs/test_report.md', 'Testbericht der Simulation', 'Simulation test report'),
 ],
}

def section_toggle_header(section_id,title,show,hide):
 return f'''<div class="section-head section-toggle-head">
 <h2 id="{section_id}-title">{esc(title)}</h2>
 <button class="section-toggle" type="button" aria-controls="{section_id}-content"
  aria-expanded="true" aria-describedby="{section_id}-title" data-show="{esc(show)}" data-hide="{esc(hide)}" hidden>
  <span class="section-toggle-label">{esc(hide)}</span><span class="details-chevron" aria-hidden="true"></span>
 </button>
 </div>'''

def project_notes(lang):
 cards=[]
 for slug,title,summary in PROJECT_NOTES:
  cards.append(f'''<article class="project-note">
  <h3>{link('projects/'+slug+'.html',esc(text(title,lang))+' <span aria-hidden="true">→</span>')}</h3>
  <p>{esc(text(summary,lang))}</p>
  </article>''')
 header=section_toggle_header('notes',tr(lang,'Projektnotizen','Project notes'),
  tr(lang,'Notizen anzeigen','Show notes'),tr(lang,'Notizen ausblenden','Hide notes'))
 return f'''<section class="container section project-notes section-fold" id="notes" aria-labelledby="notes-title">
 {header}
 <div class="notes-grid section-content" id="notes-content">{''.join(cards)}</div>
 </section>'''

def skill_section(lang):
 skills=[
  ('01',tr(lang,'Messdatenanalyse','Measurement data analysis'),'Python · SQL · pandas · MATLAB',
   tr(lang,'Datenqualität, Signalverarbeitung und statistische Auswertung.','Data quality, signal processing and statistical analysis.'),'#p1-card'),
  ('02',tr(lang,'Systemmodellierung','System modeling'),'SciPy / HiGHS · Simulink · SolidWorks',
   tr(lang,'Optimierung, physikalische Modelle und technische Simulation.','Optimization, physical models and engineering simulation.'),'#p2-card'),
  ('03',tr(lang,'Technische Kommunikation','Technical communication'),'Git · LaTeX · Excel · OriginPro',
   tr(lang,'Nachvollziehbare Abläufe, Visualisierung und Dokumentation.','Traceable workflows, visualization and documentation.'),'#work-baches'),
 ]
 cards=''.join(f'''<article><span class="skill-number">{number}</span><h3>{title}</h3>
 <p>{description}</p><p class="tool-list">{tools}</p>
 {link(example,tr(lang,'Beispiel ansehen','View example')+' →','skill-example')}</article>'''
  for number,title,tools,description,example in skills)
 header=section_toggle_header('skills',tr(lang,'Werkzeuge & Arbeitsweise','Tools & approach'),
  tr(lang,'Details anzeigen','Show details'),tr(lang,'Details ausblenden','Hide details'))
 return f'''<section class="container section skills section-fold" id="skills" aria-labelledby="skills-title">
 {header}
 <div class="skills-grid section-content" id="skills-content">{cards}</div>
 </section>'''

def technical_sources(p,lang):
 links=''.join('<li>'+link(url,tr(lang,de,en))+'</li>' for url,de,en in TECHNICAL_SOURCES[p['slug']])
 return f'''<section class="technical-sources"><h2>{tr(lang,'Quellen und Fachreferenzen','Sources and technical references')}</h2><ul>{links}</ul></section>'''

def certification(lang):
 label=tr(lang,'Zertifikate','Certifications')
 date_label=tr(lang,'11. November 2026','11 November 2026')
 verify=tr(lang,'Zertifikat bei HackerRank prüfen','Verify on HackerRank')
 return f'''<div class="credential">
 <h3>{label}</h3>
 <p><strong lang="en">SQL (Basic)</strong></p>
 <p>HackerRank · <time datetime="2026-11-11">{date_label}</time></p>
 <div class="credential-links">
 {link('https://www.hackerrank.com/certificates/14fcb50b9a3a',verify+' ↗','text-link')}
 {link('projects/emsland-sql.html',tr(lang,'SQL-Projekt ansehen','View the SQL project')+' →','text-link')}
 </div>
 </div>'''

def header(lang,prefix,alternate,home=False):
 homeurl=prefix+('' if lang=='de' else 'en/')+'index.html'
 section_url='' if home else homeurl
 nav=''.join(link(section_url+'#'+anchor,tr(lang,de,en)) for anchor,de,en in [('projects','Projekte','Projects'),('notes','Notizen','Notes'),('experience','Erfahrung','Experience'),('contact','Kontakt','Contact')])
 theme_label=tr(lang,'Dunkles Design','Dark theme')
 icons='<svg class="theme-moon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M20.7 13.3A9 9 0 0 1 10.7 3.3 9 9 0 1 0 20.7 13.3Z"/></svg><svg class="theme-sun" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.4 1.4m11.2 11.2L19 19M5 19l1.4-1.4M17.6 6.4 19 5"/></svg>'
 return f'''<a class="skip" href="#main">{tr(lang,'Zum Inhalt','Skip to content')}</a><header class="site-header"><div class="container header-inner">
 {link(homeurl,'<span class="monogram" aria-hidden="true">AA<span>.</span></span><span class="brand-caption">Ahmed Abufanas<br><small>Engineering Physics</small></span>','brand')}
 <div class="header-controls">
 <a class="language" href="{alternate}" hreflang="{'en' if lang=='de' else 'de'}" aria-label="{tr(lang,'EN: Switch to English','DE: Zur deutschen Version')}">{tr(lang,'EN','DE')}</a>
 <button class="theme-toggle" type="button" aria-label="{theme_label}" aria-pressed="false" hidden>{icons}</button>
 <button class="menu-toggle" type="button" aria-label="{tr(lang,'Menü','Menu')}" aria-expanded="false" aria-controls="navigation" hidden><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M4 6h16M4 12h16M4 18h16"/></svg></button>
 </div>
 <nav id="navigation" aria-label="{tr(lang,'Hauptnavigation','Main navigation')}">{nav}<span class="social-nav">{link(GITHUB,'GitHub ↗')}{link('https://www.linkedin.com/in/ahmedabufanas/','LinkedIn ↗')}{contact_link(tr(lang,'E-Mail','Email'))}</span></nav>
 </div></header>'''
def footer(lang,prefix):return f'''<footer class="container footer"><span>© 2026 Ahmed Abufanas</span><div>{link(prefix+'legal/impressum.html',tr(lang,'Impressum','Legal notice (German)'))}{link(prefix+'legal/datenschutz.html',tr(lang,'Datenschutz','Privacy (German)'))}</div></footer><dialog id="chart-dialog" aria-labelledby="chart-dialog-title" aria-describedby="chart-dialog-caption"><div class="dialog-header"><h2 id="chart-dialog-title">{tr(lang,'Projektgrafik','Project chart')}</h2><button class="dialog-close" autofocus>{tr(lang,'Schließen','Close')} ×</button></div><img alt=""><p id="chart-dialog-caption"></p></dialog>{contact_dialog(lang)}'''
def shell(title,desc,body,lang,path,prefix,alternate):
 canonical=BASE+('/' if path=='index.html' else '/'+path)
 other=BASE+'/'+('en/'+path if lang=='de' else path.removeprefix('en/'))
 if other==BASE+'/index.html':other=BASE+'/'
 schema={'@context':'https://schema.org','@type':'ProfilePage','inLanguage':lang,'url':canonical,'mainEntity':{'@type':'Person','name':'Ahmed Abufanas','url':BASE+'/','email':EMAIL,'sameAs':[GITHUB,'https://www.linkedin.com/in/ahmedabufanas/']}} if path.endswith('index.html') else None
 return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(desc,quote=True)}"><meta name="theme-color" content="#f7f7f2"><meta name="color-scheme" content="light dark"><link rel="canonical" href="{canonical}"><link rel="alternate" hreflang="{lang}" href="{canonical}"><link rel="alternate" hreflang="{'en' if lang=='de' else 'de'}" href="{other}"><link rel="alternate" hreflang="x-default" href="{BASE+'/'+path.removeprefix('en/') if path.removeprefix('en/')!='index.html' else BASE+'/'}"><meta property="og:type" content="{'profile' if schema else 'website'}"><meta property="og:title" content="{esc(title,quote=True)}"><meta property="og:description" content="{esc(desc,quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:locale" content="{'de_DE' if lang=='de' else 'en_US'}"><meta property="og:image" content="{BASE}/assets/images/ahmed-abufanas.jpg"><meta property="og:image:alt" content="Ahmed Abufanas"><meta property="og:image:width" content="1086"><meta property="og:image:height" content="1448"><meta property="og:image:type" content="image/jpeg"><link rel="icon" href="{prefix}assets/images/favicon.svg"><script src="{prefix}js/theme-init.js"></script><link rel="stylesheet" href="{prefix}css/style.css?v={CSS_VERSION}"><script defer src="{prefix}js/main.js?v={JS_VERSION}"></script>{'<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False)+'</script>' if schema else ''}</head><body>{header(lang,prefix,alternate,home=path in ('index.html','en/index.html'))}{body}{footer(lang,prefix)}</body></html>'''
def figure(p,lang,prefix,wide=False,eager=False):
 image=p.get('image_en',p['image']) if lang=='en' else p['image']
 info=IMAGE_INFO[image];stem=image.removesuffix('.png')
 src=f"{prefix}assets/images/projects/{stem}-800.webp"
 sizes="(min-width: 1232px) 1080px, calc(100vw - 100px)" if wide else "(min-width: 1232px) 510px, (min-width: 961px) 43vw, calc(100vw - 110px)"
 srcset=', '.join(f"{prefix}assets/images/projects/{stem}-{size}.webp {size}w" for size in info['sizes'])
 return f'''<figure><a class="chart-button" href="{prefix}assets/images/projects/{image}" data-chart aria-label="{tr(lang,'Grafik vergrößern','Enlarge chart')}: {esc(text(p['short'],lang))}"><img src="{src}" srcset="{srcset}" sizes="{sizes}" width="{info['width']}" height="{info['height']}" alt="{esc(text(p['caption'],lang))}" loading="{'eager' if wide or eager else 'lazy'}" decoding="async"><span class="zoom-label">{tr(lang,'Grafik vergrößern','Enlarge chart')} ↗</span></a><figcaption>{text(p['caption'],lang)}</figcaption></figure>'''
def dashboard_url(p,lang):return p.get('demo_en',p.get('demo')) if lang=='en' else p.get('demo')

def code_url(p,prefix):
 return GITHUB+'/'+p['repo'] if p['repo'] else prefix+p['code_archive']

def card(p,i,lang,prefix,position):
 slug=p['slug']
 if p['slug']=='windconnect': metric=str(p['test_count']); explanation=tr(lang,'automatisierte Tests für Simulation, Protokoll, Fehlerdiagnose und beide Dashboards bestanden.','automated tests passed for simulation, protocol, fault diagnostics, and both dashboards.')
 elif slug=='bess-dispatch': metric=num(METRICS['efc_reduction'],lang,2)+(' %' if lang=='de' else '%'); explanation=tr(lang,'weniger äquivalente Vollzyklen gegenüber der Optimierung ohne angesetzte Zyklenkosten.','fewer equivalent full cycles than optimization without assumed cycling costs.')
 elif slug=='noise-exposure': metric=tr(lang,f"{METRICS['noise_above']} von {METRICS['noise_n']}",f"{METRICS['noise_above']} of {METRICS['noise_n']}");explanation=tr(lang,'Messungen erreichen oder überschreiten das 100-%-NIOSH-Dosiskriterium.','measurements meet or exceed the 100% NIOSH dose criterion.')
 elif slug=='emsland-sql':
  metric=num(EMSLAND_SHARE,lang,2)+tr(lang,' %','%')
  explanation=tr(lang,'der erfassten Energie der drei ausgewählten Reihen entfallen auf D DT.','of recorded energy across the three selected series comes from D DT.')
 else:metric=tr(lang,f"{METRICS['wind_events']} auffällige Ereignisse",f"{METRICS['wind_events']} candidate events");explanation=tr(lang,'mit anhaltender Leistungsabweichung, ausgewählt für die technische Prüfung.','of sustained power deviation for further engineering review.')
 featured=slug in ('wind-turbine','emsland-sql')
 intro=tr(lang,'Wo weicht die gemessene Leistung vom Modell ab?','Where does measured power deviate from the model?') if slug=='wind-turbine' else text(p['intro'],lang)
 label=tr(lang,'Fallstudie ansehen','View case study') if featured else tr(lang,'Projekt ansehen','View project')
 card_class='project-card featured-project' if featured else 'project-card'
 contribution=f'<p class="contribution"><strong>{tr(lang,"Mein Beitrag","My contribution")}:</strong> {text(p['contribution_summary'] if 'contribution_summary' in p else CONTRIBUTION_SUMMARIES[i],lang)}</p>'
 result=f'<p class="result"><strong class="metric">{metric}</strong><span>{explanation}</span></p>'
 code_label=tr(lang,'Code ansehen','View code')+' ↗' if p['repo'] else tr(lang,'Code herunterladen','Download code')+' ↓'
 return f'''<article class="{card_class}" id="p{i+1}-card" tabindex="-1">
 <div class="project-copy">
 <div class="project-heading">
 <div class="eyebrow"><span>{position:02}</span> {text(p['category'],lang)}</div>
 <h3 id="p{i+1}-title">{text(p['short'],lang)}</h3>
 </div>
 <div class="project-summary">
 {result}
 <p class="scope">{text(p['limit'],lang)}</p>
 <div class="actions">{link('projects/'+p['slug']+'.html',label+' ↗','text-link')}</div>
 </div>
 </div>
 {figure(p,lang,prefix,eager=position==1)}
 <details class="project-details">
 <summary aria-labelledby="p{i+1}-toggle p{i+1}-title">
 <span id="p{i+1}-toggle"><span class="details-when-closed">{tr(lang,'Details anzeigen','Show details')}</span><span class="details-when-open">{tr(lang,'Details ausblenden','Hide details')}</span></span>
 <span class="details-chevron" aria-hidden="true"></span>
 </summary>
 <div class="project-detail-body">
 <p>{intro}</p>{contribution}
 <div class="tags">{''.join('<span>'+esc(t)+'</span>' for t in p['tags'])}</div>
 {link(code_url(p,prefix),code_label,'quiet-link')}
 </div>
 </details>
 </article>'''

def home(lang):
 prefix='' if lang=='de' else '../'
 title='Ahmed Abufanas | '+tr(lang,'Ingenieurphysik & Messdatenanalyse','Engineering Physics & Data Analysis')
 desc=tr(lang,'Ingenieurphysiker (B.Eng.) mit Erfahrung in Python, MATLAB und technischen Messdaten. Projekte, Forschungserfahrung und Lebenslauf.','Engineering Physics graduate with experience in Python, MATLAB and measurement data. Projects, research experience and résumé.')
 # Keep existing card fragment IDs while placing the two data-analysis studies first.
 ordered_projects=sorted(enumerate(PROJECTS), key=lambda entry: entry[1].get('display_order', entry[0]*10))
 cards=[card(project,i,lang,prefix,position) for position,(i,project) in enumerate(ordered_projects,1)]
 project_pairs=''.join(f'<div class="project-pair">{"".join(cards[start:start+2])}</div>' for start in range(1,len(cards),2))
 project_cards=cards[0]+project_pairs
 education=tr(lang,'<h3>Masterstudium Ingenieurphysik (laufend)</h3><p>Universität Oldenburg · seit 10/2025<br>Abschluss voraussichtlich 02/2028</p><h3>B.Eng. Ingenieurphysik</h3><p>Universität Oldenburg · 10/2015–02/2025<br>Abschlussarbeit: Binaural Detection and Auditory Modelling of Bandwidth Effects</p>','<h3>Master’s studies in Engineering Physics</h3><p>University of Oldenburg · since 10/2025<br>Expected completion 02/2028</p><h3>B.Eng. Engineering Physics</h3><p>University of Oldenburg · 10/2015–02/2025<br>Thesis: Binaural Detection and Auditory Modelling of Bandwidth Effects</p>')

 body=f'''<main id="main"><section class="container hero" id="top"><div class="hero-copy"><div class="hero-identity"><p class="hero-name">Ahmed Abufanas</p><h1>{tr(lang,'Ingenieurphysiker (B.Eng.)','Engineering Physics (B.Eng.)')}</h1></div><div class="hero-intro"><p class="hero-lead">{tr(lang,'Ich untersuche technische Fragestellungen mit Messdaten, physikalischen Modellen und Simulationen. Je nach Aufgabe arbeite ich mit Python, SQL oder MATLAB.','I use measurement data, physical models, and simulations to investigate engineering problems. Depending on the task, I work with Python, SQL, or MATLAB.')}</p><p class="hero-lead">{tr(lang,'Ich bin offen für unterschiedliche technische Aufgaben, bei denen ich mein Studium der Ingenieurphysik und meine praktische Erfahrung einbringen kann.','I’m open to a range of technical roles where I can apply my engineering physics background and practical experience.')}</p><div class="hero-actions">{link('#projects',tr(lang,'Projekte','View projects'),'button primary')}{cv_link(prefix,lang)}</div><p class="availability"><span aria-hidden="true"></span><span class="availability-text">{tr(lang,'Offen für den Berufseinstieg · Deutschlandweit umzugsbereit','Open to early-career roles · Willing to relocate within Germany')}</span></p></div></div><div class="portrait"><img src="{prefix}assets/images/ahmed-abufanas.jpg" alt="Ahmed Abufanas" width="1086" height="1448" fetchpriority="high"></div>{profile_highlights(lang)}</section><section class="container section" id="projects"><div class="section-head project-section-head"><div><h2>{tr(lang,'Projekte','Projects')}</h2><p>{tr(lang,'Fünf eigenständige Fallstudien mit Ergebnissen, Quellcode und Angaben zur Methodik.','Five independent case studies with results, source code, and methods.')}</p></div>
 <button class="project-details-toggle" type="button" hidden
 data-show="{tr(lang,'Alle Details anzeigen','Show all details')}"
 data-hide="{tr(lang,'Alle Details ausblenden','Hide all details')}">{tr(lang,'Alle Details anzeigen','Show all details')}</button></div><div class="project-grid">{project_cards}</div></section>{project_notes(lang)}<section class="experience-band" id="experience"><div class="container section"><div class="section-head"><h2>{tr(lang,'Berufserfahrung & Ausbildung','Experience & Education')}</h2></div><div class="experience-grid"><div class="work-history"><p class="eyebrow">{tr(lang,'BERUFSERFAHRUNG','EXPERIENCE')}</p>{''.join(f'<article class="work-item" id="{['work-baches','work-buddy','work-binaural'][j]}"><span class="date">{w["date"]}</span><h3>{text(w["title"],lang)}</h3><p class="institution">{w["place"]}</p><p>{text(w["description"],lang)}</p></article>' for j,w in enumerate(WORK))}</div><aside class="education" id="education"><p class="eyebrow">{tr(lang,'AUSBILDUNG','EDUCATION')}</p>{education}<div class="languages"><h3>{tr(lang,'Sprachen','Languages')}</h3><p>{tr(lang,'Deutsch & Englisch: sehr gute Kenntnisse<br>Arabisch: Muttersprache','German & English: strong proficiency<br>Arabic: native')}</p></div>{certification(lang)}</aside></div></div></section>{skill_section(lang)}{contact_section(lang)}</main>'''
 path='index.html' if lang=='de' else 'en/index.html'
 write(path,shell(title,desc,body,lang,path,prefix,'en/index.html' if lang=='de' else '../index.html'))
def detail(p,lang):
 prefix='../' if lang=='de' else '../../'
 homeurl='../index.html'
 result=text(p['result'],lang)
 demo_hint=text(p['demo_note'],lang) if p.get('demo_note') else tr(lang,'Falls die App im Ruhemodus ist, klicken Sie auf „Yes, get this app back up!“ und warten Sie, bis sie geladen ist.','If the app is asleep, click “Yes, get this app back up!” and wait for it to load.')
 rows_caption=tr(lang,'Geprüfter Funktionsumfang','Verified functionality') if p['slug']=='windconnect' else tr(lang,'Kennzahlen der dokumentierten Analyse','Metrics from the documented analysis')
 source_path=p.get('source_en',p.get('source')) if lang=='en' else p.get('source')
 source_url=GITHUB+'/'+p['repo']+'/blob/main/'+source_path if source_path else ''
 source_link=link(source_url,tr(lang,'Originalgrafik im Repository','Original figure in repository')+' ↗','source-link') if source_url else ''
 code_label=tr(lang,'Code & Dokumentation','Code & documentation')+' ↗' if p['repo'] else tr(lang,'SQL-Code herunterladen','Download SQL code')+' ↓'
 terminology=''
 if p.get('terminology'):
  terms=text(p['terminology'],lang)
  terminology='<section><h2>'+tr(lang,'Begriffe klar getrennt','Distinct technical concepts')+'</h2><table><caption>'+tr(lang,'Begriffe und Bedeutung','Terms and meanings')+'</caption><tbody>'+''.join('<tr><th scope="row">'+k+'</th><td>'+v+'</td></tr>' for k,v in terms)+'</tbody></table></section>'
 archive_link=link(prefix+p['code_archive'],tr(lang,'SQL-Code herunterladen','Download SQL code')+' ↓','button secondary') if p.get('code_archive') and p['repo'] else ''
 local_note='<p class="scope">'+text(p['local_demo'],lang)+'</p>' if p.get('local_demo') else ''
 if p['slug']=='bess-dispatch':
  rows=[(tr(lang,'Netto-Arbitragemarge (simuliert)','Net arbitrage margin (simulated)'),num(METRICS['bess_net'],lang,2)+' €'),(tr(lang,'Äquivalente Vollzyklen','Equivalent full cycles'),num(METRICS['bess_efc'],lang,2)+' EFC'),(tr(lang,'Weniger Vollzyklen gegenüber Optimierung ohne angesetzte Zyklenkosten','Fewer equivalent full cycles vs optimization without assumed cycling costs'),num(METRICS['efc_reduction'],lang,2)+' %'),(tr(lang,'Geringere Brutto-Arbitragemarge gegenüber Optimierung ohne angesetzte Zyklenkosten','Lower gross arbitrage margin vs optimization without assumed cycling costs'),num(METRICS['margin_reduction'],lang,2)+' %')]
 elif p['slug']=='emsland-sql':
  rows=[(name,f'{num(energy/1000,lang,2)} GWh') for name,energy,_,_ in EMSLAND_SERIES]
  rows.append((tr(lang,'Stundenwerte insgesamt','Total hourly readings'),num(EMSLAND_TOTAL,lang)))
 elif p['slug']=='noise-exposure':rows=[(tr(lang,'NIOSH-Dosis ≥ 100 %','NIOSH dose ≥ 100%'),'477 / 758 (62'+(',' if lang=='de' else '.')+'93 %)'),(tr(lang,'NIOSH-Dosis höher als OSHA-PEL-Dosis (gepaart)','NIOSH dose higher than OSHA PEL dose (paired)'),'672 / 680 (98'+(',' if lang=='de' else '.')+'82 %)')]
 elif p['slug']=='windconnect':rows=[(tr(lang,'Automatisierte Tests','Automated tests'),str(p['test_count'])),(tr(lang,'Diagnosezustände','Diagnostic states'),'4'),(tr(lang,'Standard-Aktualitätsschwelle','Default stale threshold'),'5 s'),(tr(lang,'Lokaler Modbus-Endpunkt','Local Modbus endpoint'),'127.0.0.1:15020')]
 else:rows=[(tr(lang,'Datengrundlage','Source timestamps'),num(52560,lang)),(tr(lang,'Auffällige Ereignisse','Candidate events'),'5')]
 body=f'''<main id="main" class="container case"><a class="back-link" href="{homeurl}#projects">← {tr(lang,'Alle Projekte','All projects')}</a><div class="case-heading"><p class="eyebrow">{text(p['category'],lang)} / {tr(lang,'EIGENSTÄNDIGES PROJEKT','INDEPENDENT PROJECT')}</p><h1>{text(p['title'],lang)}</h1><p class="case-lead">{text(p['intro'],lang)}</p><div class="actions case-actions">{link(code_url(p,prefix),code_label,'button primary')}{('<div class="dashboard-action">'+link(dashboard_url(p,lang),tr(lang,'Dashboard öffnen','Open dashboard')+' ↗','button secondary').replace('<a ', '<a aria-describedby="dashboard-note" ',1)+'<p id="dashboard-note" class="dashboard-note">'+demo_hint+'</p></div>') if p.get('demo') else ''}{archive_link}{local_note}</div></div><div class="case-visual">{figure(p,lang,prefix,wide=True)}{source_link}</div><div class="case-columns"><div><section><p class="eyebrow">01 / {tr(lang,'MEIN BEITRAG','MY CONTRIBUTION')}</p><h2>{tr(lang,'Umsetzung','Implementation')}</h2><ul>{''.join('<li>'+s+'</li>' for s in text(p['contributions'],lang))}</ul></section><section><p class="eyebrow">{tr(lang,'METHODIK','METHODOLOGY')}</p><h2>{tr(lang,'Daten und Vorgehen','Data and approach')}</h2><ol>{''.join('<li>'+s+'</li>' for s in text(p['method'],lang))}</ol></section>{terminology}<section><p class="eyebrow">{tr(lang,'ERGEBNIS','RESULT')}</p><h2>{tr(lang,"Ergebnisse im Kontext","Results in context")}</h2><p class="case-result">{result}</p><table><caption>{rows_caption}</caption><tbody>{''.join('<tr><th scope="row">'+k+'</th><td>'+v+'</td></tr>' for k,v in rows)}</tbody></table><p>{text(p['detail'],lang)}</p></section>{technical_sources(p,lang)}</div><aside class="case-aside"><p class="eyebrow">{tr(lang,'EINORDNUNG','SCOPE')}</p><h3>{tr(lang,'Aussagekraft und Grenzen.','Scope and limitations.')}</h3><p>{text(p['limits'],lang)}</p><hr><p class="eyebrow">{tr(lang,'WERKZEUGE','TOOLS')}</p><p>{' · '.join(p['tags'])}</p><hr>{link(code_url(p,prefix),tr(lang,'Vollständige Methodik ↗','Full methodology ↗') if p['repo'] else code_label,'text-link')}</aside></div><div class="case-end">{link(homeurl+'#projects','← '+tr(lang,'Zur Projektübersicht','Back to projects'),'button secondary')}{contact_link(tr(lang,'Über das Projekt sprechen','Discuss this project')+' ↗','button primary',tr(lang,'Anfrage zu: ','Question about: ')+text(p['short'],lang))}</div></main>'''
 path=('' if lang=='de' else 'en/')+'projects/'+p['slug']+'.html'
 alternate=('../../en/projects/' if lang=='de' else '../../projects/')+p['slug']+'.html'
 # German project pages are one level below root.
 if lang=='de':alternate='../en/projects/'+p['slug']+'.html'
 write(path,shell(text(p['short'],lang)+' | Ahmed Abufanas',text(p['intro'],lang),body,lang,path,prefix,alternate))
def write(path,content):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content,encoding='utf-8')
def build_legal():
 notice = '<main id="main" class="container legal"><p class="eyebrow">AHMED ABUFANAS / PORTFOLIO</p><h1>Impressum</h1><h2>Websitebetreiber und Kontakt</h2><p><strong>Ahmed Abufanas</strong><br>Osterkampsweg 70<br>26131 Oldenburg<br>Deutschland<br>E-Mail: <a href="mailto:abufanasa@gmail.com">abufanasa@gmail.com</a></p><h2>Zweck der Website</h2><p>Dieses persönliche Portfolio dient der beruflichen Vorstellung und der Dokumentation eigener technischer Projekte. Es enthält keine Kauf- oder Buchungsfunktion.</p><p><a href="../index.html">← Zurück zum Portfolio</a></p></main>'
 privacy = '<main id="main" class="container legal"><p class="eyebrow">AHMED ABUFANAS / PORTFOLIO</p><h1>Datenschutzerklärung</h1><p>Stand: 1. Oktober 2026</p><h2>1. Verantwortlicher und Kontakt</h2><p>Ahmed Abufanas<br>Osterkampsweg 70<br>26131 Oldenburg, Deutschland<br>E-Mail: <a href="mailto:abufanasa@gmail.com">abufanasa@gmail.com</a></p><p>Diese Hinweise beschreiben den Besuch dieses Portfolios und die Kontaktaufnahme über die veröffentlichte E-Mail-Adresse.</p><h2>2. Hosting über GitHub Pages</h2><p>Die Website wird über GitHub Pages bereitgestellt. Beim Abruf verarbeitet der Hostinganbieter GitHub technische Verbindungsdaten, insbesondere IP-Adresse, Geräteinformationen sowie Datum und Uhrzeit der Anfrage. Die Bereitstellung erfolgt zur zuverlässigen und sicheren Auslieferung des Portfolios auf Grundlage von Art. 6 Abs. 1 lit. f DSGVO. Es wird keine eigene Besucheranalyse betrieben.</p><p>GitHub erläutert seine Datenverarbeitung, Speicherfristen, Rechte und internationalen Datenübermittlungen in der <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub-Datenschutzerklärung</a>. Für die vom Hostinganbieter eigenständig geführten Protokolle wird hier keine eigene Löschfrist zugesagt.</p><h2>3. Darstellung, lokaler Speicher und Zwischenablage</h2><p>Der Portfolio-Code setzt keine Cookies und lädt keine Analysedienste, externen Schriftarten oder eingebetteten Social-Media-Inhalte. Bilder, Stylesheets und Skripte werden vom selben Website-Host geladen. Die Sprachwahl erfolgt über separate Seiten.</p><p>Wenn Sie das helle oder dunkle Design ausdrücklich auswählen, speichert Ihr Browser ausschließlich den Wert <code>light</code> oder <code>dark</code> unter <code>aa-portfolio-theme</code> im lokalen Browserspeicher. Diese Einstellung wird nicht an einen Server übertragen. Ohne eigene Auswahl folgt die Darstellung der Systempräferenz. Die Speicherung dient der von Ihnen angeforderten Darstellung (§ 25 Abs. 2 Nr. 2 TDDDG); das Interesse an einer benutzbaren Website bildet die Grundlage nach Art. 6 Abs. 1 lit. f DSGVO, soweit personenbezogene Daten betroffen sind.</p><p>Die Einstellung bleibt gespeichert, bis Sie die Website-Daten im Browser löschen. Danach gilt wieder die Systempräferenz. Sie können die Darstellung jederzeit über den Design-Schalter ändern. Bei gesperrtem Browserspeicher funktioniert der Wechsel für die aktuelle Seite.</p><p>Die Kopierfunktion schreibt die angezeigte E-Mail-Adresse auf Ihren Klick in die Zwischenablage. Sie liest keine vorhandenen Inhalte der Zwischenablage aus.</p><h2>4. Kontakt per E-Mail</h2><p>Über die Kontaktauswahl können Sie Gmail im Browser oder Ihr eigenes E-Mail-Programm öffnen oder die E-Mail-Adresse kopieren. Gmail wird erst nach Auswahl des entsprechenden Links aufgerufen. Bei Projektanfragen wird der Projektname als Betreff vorbelegt. Dieses Portfolio enthält kein Kontaktformular und versendet keine Nachrichten automatisch. Wenn Sie eine Nachricht senden, werden Ihre E-Mail-Adresse, Ihr Name, soweit mitgeteilt, sowie Nachricht und Anhänge zur Bearbeitung Ihrer Anfrage und für die zugehörige Kommunikation verwendet. Grundlage ist Art. 6 Abs. 1 lit. f DSGVO, insbesondere das Interesse an der Beantwortung beruflicher Anfragen. Bei erforderlichen vorvertraglichen Maßnahmen auf Ihre Anfrage gilt Art. 6 Abs. 1 lit. b DSGVO.</p><p>Für das Postfach wird Gmail (Google) verwendet. Google verarbeitet die bei der Zustellung und Bereitstellung des E-Mail-Dienstes anfallenden Daten. Angaben zu Googles Datenverarbeitung, Speicherfristen und internationalen Übermittlungen finden Sie in der <a href="https://policies.google.com/privacy?hl=de">Google-Datenschutzerklärung</a>.</p><h2>5. Aufbewahrung von Kontaktanfragen</h2><p>Offene Anfragen bleiben während der Bearbeitung gespeichert. Gewöhnliche, abgeschlossene Kontakt- und Stellenanfragen werden gelöscht, sobald sie nicht mehr benötigt werden, spätestens sechs Monate nach Abschluss der Anfrage beziehungsweise der betreffenden beruflichen Möglichkeit.</p><p>Davon getrennt werden Unterlagen aufbewahrt, die weiterhin für ein bestehendes Vertragsverhältnis, gesetzliche Pflichten oder die Geltendmachung, Ausübung oder Verteidigung von Rechtsansprüchen erforderlich sind. Ihre Speicherung beschränkt sich auf den jeweiligen Zweck und die dafür erforderliche Dauer. Die Löschung von E-Mails erfolgt im Postfach; die Website führt keine automatische E-Mail-Löschung aus.</p><h2>6. Externe Links</h2><p>Links zu LinkedIn, GitHub und dem Streamlit-Dashboard führen auf externe Websites. Erst wenn Sie diesen Links folgen, rufen Sie diese Dienste auf; dort gelten die jeweiligen Datenschutzhinweise.</p><h2>7. Ihre Rechte</h2><p>Unter den gesetzlichen Voraussetzungen haben Sie Rechte auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung und Datenübertragbarkeit. Bei einer Verarbeitung auf Grundlage von Art. 6 Abs. 1 lit. f DSGVO können Sie aus Gründen Ihrer besonderen Situation Widerspruch einlegen. Eine erteilte Einwilligung können Sie für die Zukunft widerrufen.</p><p>Anfragen zur Verarbeitung durch den Websitebetreiber richten Sie bitte an die oben genannte E-Mail-Adresse. Sie haben außerdem ein Beschwerderecht bei einer Datenschutzaufsichtsbehörde, insbesondere dem <a href="https://www.lfd.niedersachsen.de/startseite/">Landesbeauftragten für den Datenschutz Niedersachsen</a>. Es findet keine automatisierte Entscheidung oder Profilbildung durch den Portfolio-Code statt.</p><p><a href="../index.html">← Zurück zum Portfolio</a></p></main>'
 for slug,title,desc,body in [('impressum','Impressum','Betreiber und Kontakt des Portfolios von Ahmed Abufanas.',notice),('datenschutz','Datenschutzerklärung','Hinweise zu Datenschutz und Funktionen des Portfolios von Ahmed Abufanas.',privacy)]:
  path='legal/'+slug+'.html'
  head=f'<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} | Ahmed Abufanas</title><meta name="description" content="{desc}"><meta name="robots" content="noindex"><meta name="theme-color" content="#f7f7f2"><meta name="color-scheme" content="light dark"><link rel="canonical" href="{BASE}/{path}"><link rel="icon" href="../assets/images/favicon.svg"><script src="../js/theme-init.js"></script><link rel="stylesheet" href="../css/style.css?v={CSS_VERSION}"><script defer src="../js/main.js?v={JS_VERSION}"></script></head><body>'
  write(path,head+header('de','../','../en/index.html')+body+footer('de','../')+'</body></html>')

def build_all():
 build_legal()
 for lang in ('de','en'):
  home(lang)
  for p in PROJECTS:detail(p,lang)
 paths=['']+['en/index.html']+[prefix+'projects/'+p['slug']+'.html' for prefix in ('','en/') for p in PROJECTS]
 from xml.sax.saxutils import escape
 urls=''.join('<url><loc>'+escape(BASE+'/'+path)+'</loc></url>' for path in paths)
 write('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+urls+'</urlset>')
 write('robots.txt','User-agent: *\nAllow: /\nSitemap: '+BASE+'/sitemap.xml\n')
if __name__=='__main__':
 build_all()
 print(f'Generated {2+2*len(PROJECTS)} bilingual pages, sitemap and robots.txt. Gross-margin rounding:',round(METRICS['margin_reduction'],2))
