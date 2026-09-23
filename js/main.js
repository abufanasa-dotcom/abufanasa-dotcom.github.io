/**
 * Ahmed Abufanas - Portfolio Scripts
 * Handles: Bilingual toggling (DE/EN), accessible mobile nav, and accessible legal modal dialogs
 */

(function () {
  'use strict';

  // Translation dictionary for elements using data-i18n keys
  const translations = {
    de: {
      siteTitle: "Ahmed Abufanas | Ingenieurphysik & Datenanalyse",
      navProjects: "Projekte",
      navExperience: "Werdegang",
      navSkills: "Fähigkeiten",
      navAbout: "Über mich",
      navContact: "Kontakt",
      navResume: "Lebenslauf (PDF)",
      heroStatus: "Absolvent der Ingenieurphysik (B.Eng.)",
      heroHeadline: "Technische Datenanalyse, wissenschaftliche Programmierung & Messsysteme",
      heroLead: "Fokus auf standardisierte Auswertung, physikalische Modellierung und Datenpipelines in den Bereichen Energiesysteme und Akustik. Präzise Methoden, dokumentierte Grenzen und reproduzierbare Ergebnisse.",
      ctaProjects: "Ausgewählte Projekte",
      ctaResume: "Lebenslauf herunterladen",
      ctaContact: "Kontakt aufnehmen",
      
      secProjectsTitle: "Ausgewählte technische Projekte",
      secProjectsDesc: "Konkrete Arbeiten mit dokumentierten Datensätzen, methodischer Validierung und klaren technischen Abgrenzungen.",
      
      // Project 1
      p1Tag: "Windenergie & SCADA-Analytik",
      p1Title: "Wind Turbine Performance Review",
      p1ProblemLabel: "Problemstellung",
      p1Problem: "Erkennung chronischer Leistungsdefizite und unplausibler Betriebszustände in hochdimensionalen 10-Minuten-SCADA-Messreihen industrieller Windenergieanlagen ohne Verzerrung durch fehlerhafte Sensorereignisse.",
      p1ContributionLabel: "Beitrag & Methoden",
      p1Contribution: "Analyse der Betriebsdaten von Turbine 1 des Kelmarsh-Windparks (52.560 Zeitschritte, 2022). Bereinigung und physikalische Plausibilitätsfilterung, Entwicklung eines Referenz-Leistungskurvenmodells nach Windgeschwindigkeitsklassen, Vergleich mit Regressionsmodellen (scikit-learn) sowie Aggregation persistenter Minderleistungsphasen. Bereitstellung eines interaktiven Streamlit-Dashboards zur strukturierten Ereignisinspektion.",
      p1ResultLabel: "Ergebnis & Kennzahlen",
      p1Result: "Erfolgreiche Segmentierung von Ausfallzeiten und Identifikation konsistenter Minderleistungsintervalle zur Priorisierung technischer Vor-Ort-Überprüfungen.",
      p1Metric1Val: "52.560",
      p1Metric1Lbl: "10-Minuten-Zeitstempel (2022)",
      p1Metric2Val: "2.050 kW",
      p1Metric2Lbl: "Nennleistung (Senvion MM92)",
      p1Metric3Val: "Streamlit",
      p1Metric3Lbl: "Interaktive Ereignisinspektion",
      p1LimitTitle: "Dokumentierte Limitation:",
      p1LimitText: "Die Reduktion des Modellfehlers stellt keine reale Erhöhung des Turbinenwirkungsgrads oder nachgewiesene finanzielle Einsparung dar. Das Dashboard visualisiert statisch vorberechnete Analyseergebnisse historischer Daten und führt keine Live-Telemetrie durch.",
      
      // Project 2
      p2Tag: "Batteriespeicher & Energiemarkt",
      p2Title: "German BESS Dispatch & Degradation Analytics",
      p2ProblemLabel: "Problemstellung",
      p2Problem: "Reine Arbitrage-Optimierungen im Day-Ahead-Strommarkt neigen dazu, Batteriespeicher selbst bei minimalen Preisspreads intensiv zu zyklisieren. Dies führt zu unverhältnismäßiger Zellalterung ohne substantiellen wirtschaftlichen Mehrwert.",
      p2ContributionLabel: "Beitrag & Methoden",
      p2Contribution: "Ex-post techno-ökonomische Analyse eines netzgekoppelten 1 MW / 2 MWh Großspeichers anhand stündlicher SMARD-Strommarktdaten (Zone DE/LU, 8.784 Stunden im Kalenderjahr 2024). Formulierung eines Mixed-Integer Linear Program (MILP via SciPy/HiGHS) unter Berücksichtigung von Sommer-/Winterzeitwechseln, Lade-/Entladeeffizienzen (95 %) und SOC-Grenzbedingungen. Unabhängige physikalische Replay-Validierung (< 10⁻¹⁰ EUR Diskrepanz) und Sensitivitätsanalyse über variierende Zyklenkostenansätze.",
      p2ResultLabel: "Ergebnis & Kennzahlen",
      p2Result: "Simulierte Margen unter den definierten Kostenannahmen: Bei einem nominalen Zyklenkostenansatz von 20 €/MWh äquivalenter Zyklenenergie erzielte das Modell eine simulierte Nettomarge von 44.685,44 € bei 418,30 Vollzyklen (EFC). Gegenüber dem ungedämpften Modell sinkt die jährliche Zyklenbelastung um 32,44 % bei nur 5,26 % Erlösverzicht, während der erzielte Arbitragewert pro Vollzyklus von 104,72 €/EFC auf 146,83 €/EFC ansteigt. Vollständige Methodik im Repository.",
      p2Metric1Val: "8.784 Std.",
      p2Metric1Lbl: "SMARD-Marktdaten 2024 (DE/LU)",
      p2Metric2Val: "-32,44 % EFC",
      p2Metric2Lbl: "Zyklenreduktion durch Zyklenkosten",
      p2Metric3Val: "+467 %",
      p2Metric3Lbl: "Simulierte Nettomarge vs. starrer Fahrplan",
      p2LimitTitle: "Dokumentierte Limitation:",
      p2LimitText: "Die Ergebnisse sind retrospektive mathematische Simulationen unter definierten Markt- und Effizienzannahmen, keine real erzielten Umsatzerlöse. Der Zyklenkostenansatz dient als ökonomischer Steuerungsfaktor zur Dämpfung flacher Spreads und ist kein elektrochemisches Alterungsmodell.",
      
      // Project 3
      p3Tag: "Akustik & Messdatenanalyse",
      p3Title: "Industrial Noise Exposure Analysis",
      p3ProblemLabel: "Problemstellung",
      p3Problem: "Widersprüchliche regulatorische Dosimetrie-Definitionen (3-dB-Energieäquivalenzprinzip nach NIOSH/ISO vs. 5-dB-Regelverdopplung nach OSHA), ausgeprägte physikalische Schiefe industrieller Schallenergie und Verzerrungen durch Mehrfachmessungen in Einzelbetrieben.",
      p3ContributionLabel: "Beitrag & Methoden",
      p3Contribution: "Systematische Aufbereitung und quantitative Auswertung der historischen NIOSH Health Hazard Evaluation Datenbank (807 personenbezogene Dosimetriemessungen, 582 stationäre Schallpegelmessungen an 77 Betriebsstätten). Bereinigung von Formelfehlern historischer Erfasser ohne Datenverlust, statistische Analyse von 680 zeitgleichen Zweikanal-Messungen am selben Arbeitsplatz und internationaler Abgleich mit den Auslösewerten der deutschen LärmVibrationsArbSchV bzw. DIN EN ISO 9612.",
      p3ResultLabel: "Ergebnis & Kennzahlen",
      p3Result: "477 von 758 gültigen personenbezogenen Messungen erreichten oder überschritten das 100-%-NIOSH-Dosiskriterium (Median-Dosis: 174,20 %, entsprechend 87,41 dBA Dauerschallpegel über 8 h). In 98,82 % der Schichten (672 von 680 zeitgleichen Zweikanal-Messungen) lag die physikalisch basierte NIOSH-Dosis systematisch über dem OSHA-Wert (Median-Differenz: +151,60 Prozentpunkte). Vollständige Methodik im Repository.",
      p3Metric1Val: "758",
      p3Metric1Lbl: "Gültige persönliche Messungen",
      p3Metric2Val: "62,93 %",
      p3Metric2Lbl: "Erreichten/überschritten NIOSH REL",
      p3Metric3Val: "98,82 %",
      p3Metric3Lbl: "Systematische NIOSH > OSHA Diskrepanz",
      p3LimitTitle: "Dokumentierte Limitation:",
      p3LimitText: "Historische Portfolio-Auswertung von Untersuchungsberichten (1996–2007), keine Schätzung der aktuellen betrieblichen Gesamtexposition in Deutschland oder den USA und keine arbeitsmedizinische oder zertifizierte Rechtskonformitätsprüfung.",
      
      linkCode: "Repository ansehen",
      linkLive: "Live-Dashboard",
      allProjectsGitHub: "Weitere Projekte auf GitHub ansehen",
      
      // Experience
      secExpTitle: "Ausbildung & Werdegang",
      secExpDesc: "Akademischer Hintergrund in der Ingenieurphysik und praktische Tätigkeiten in Forschung, Messtechnik und Datenverarbeitung.",
      colEduTitle: "Ausbildung",
      colWorkTitle: "Berufliche Erfahrung & Forschung",
      
      edu1Date: "10/2025 – 02/2028 (vorauss.)",
      edu1Title: "Masterstudium Ingenieurphysik",
      edu1Place: "Carl von Ossietzky Universität Oldenburg",
      edu1Desc: "Schwerpunkte: Energiesysteme, Energiespeicher, Photovoltaik, Messtechnik, Modellierung und numerische Simulation.",
      
      edu2Date: "10/2015 – 02/2025",
      edu2Title: "Bachelor of Engineering (B.Eng.) – Ingenieurphysik",
      edu2Place: "Carl von Ossietzky Universität Oldenburg",
      edu2Desc: "Schwerpunkte: Technische Physik, Elektrodynamik, Optik, Elektronik, Regelungstechnik, Signalverarbeitung und Materialwissenschaften.<br><strong>Abschlussarbeit:</strong> <em>Binaural Detection and Auditory Modelling of Bandwidth Effects</em> – MATLAB-basierte Signalverarbeitung, Filterung und statistische Auswertung psychoakustischer Messdaten.",
      
      work1Date: "02/2026 – 06/2026",
      work1Title: "Wissenschaftliche Hilfskraft – Spektralanalyse & Python-Datenverarbeitung",
      work1Place: "Hochschule Emden/Leer",
      work1Desc: "Weiterentwicklung einer wissenschaftlichen Python-Pipeline zur automatisierten Verarbeitung und Kalibrierung hochauflösender Spektraldaten eines BACHES-Echelle-Spektrographen. Refactoring gewachsener Codebasen, Standardisierung von Parametern und strukturierte Dokumentation zur Sicherung der Reproduzierbarkeit.",
      
      work2Date: "03/2026 – 09/2026",
      work2Title: "Student Buddy – International Office",
      work2Place: "Carl von Ossietzky Universität Oldenburg",
      work2Desc: "Fachliche und organisatorische Begleitung internationaler Studierender in der Orientierungsphase sowie Schnittstellenkommunikation mit universitären Stellen.",
      
      work3Date: "03/2023 – 12/2023",
      work3Title: "Wissenschaftliche Hilfskraft – Datenanalyse & Dokumentation",
      work3Place: "Carl von Ossietzky Universität Oldenburg",
      work3Desc: "Strukturierte Aufbereitung, Konsistenzprüfung und statistische Qualitätskontrolle experimenteller Messreihen mit MATLAB und Excel. Entwicklung wiederverwendbarer Routinen zur standardisierten Auswertung.",
      
      // Skills
      secSkillsTitle: "Fachliche Kenntnisse & Werkzeuge",
      secSkillsDesc: "Schwerpunkte in wissenschaftlicher Programmierung, Prüfstands- und Messtechnik sowie physikalischer Systemanalyse.",
      cat1Title: "Programmierung & Datenanalyse",
      cat1Item1: "<strong>Python:</strong> pandas, NumPy, scikit-learn, SciPy, Matplotlib, Plotly, Streamlit, pytest",
      cat1Item2: "<strong>MATLAB & Simulink:</strong> Signalverarbeitung, Filterentwurf, statistische Auswertung",
      cat1Item3: "<strong>C++ & Embedded:</strong> Grundlegende Algorithmen, Arduino Microcontroller-Sensorik",
      cat1Item4: "<strong>Versionsverwaltung & Umgebungen:</strong> Git, GitHub, virtuelle Umgebungen, Linux/PowerShell",
      
      cat2Title: "Messtechnik & Prüfstände",
      cat2Item1: "<strong>Sensordatenerfassung:</strong> Zeit- und frequenzaufgelöste Messdaten, Filterung & Glättung",
      cat2Item2: "<strong>Optische Messsysteme:</strong> Echelle-Spektroskopie (BACHES), Kalibrierungsabläufe, LIDAR-Daten",
      cat2Item3: "<strong>Akustik & Schwingungen:</strong> Binaurale Detektion, psychoakustische Schwellen, Lärmdosimetrie",
      cat2Item4: "<strong>Experimentelle Prüfungen:</strong> Temperatur- und Belastungstests, Kennlinienermittlung",
      
      cat3Title: "Modellierung & Simulation",
      cat3Item1: "<strong>Energiesysteme:</strong> BESS-Batteriespeichermodelle, Dispatch-Optimierung (HiGHS MILP)",
      cat3Item2: "<strong>Regelungstechnik:</strong> Modellierung technischer Regelkreise, Sensor-Aktor-Kopplung",
      cat3Item3: "<strong>3D-CAD & Mechanik:</strong> SolidWorks (parametrische Modellierung, strukturmechanische Simulation)",
      cat3Item4: "<strong>Wissenschaftliche Dokumentation:</strong> LaTeX, OriginPro, technische Berichte",
      
      cat4Title: "Sprachen & Arbeitsweise",
      cat4Item1: "<strong>Deutsch:</strong> Verhandlungssicher / Sehr gut (C1)",
      cat4Item2: "<strong>Englisch:</strong> Verhandlungssicher / Sehr gut (C1)",
      cat4Item3: "<strong>Arabisch:</strong> Muttersprache",
      cat4Item4: "<strong>Methodik:</strong> Selbstständige Einarbeitung, saubere Code-Struktur, analytische Fehleridentifikation",
      
      // About & Contact
      secAboutTitle: "Über mich & Kontakt",
      secAboutDesc: "Direkte Kontaktaufnahme für technische Einstiegspositionen und Projekte.",
      aboutP1: "Als Absolvent der Ingenieurphysik (B.Eng.) verbinde ich ein fundiertes Verständnis physikalischer Wirkprinzipien mit zielgerichteter Programmierung und Datenverarbeitung. Ob bei der Kalibrierung astronomischer Spektrographen, der Modellierung von Batterieeinsätzen oder der Identifikation von Leistungseinbußen bei Windkraftanlagen: Im Mittelpunkt steht für mich stets die verlässliche, transparente und reproduzierbare Analyse technischer Messdaten.",
      aboutP2: "Ich arbeite mich eigenständig in komplexe mathematische und technische Problemstellungen ein, teste Modellannahmen gewissenhaft gegen reale Daten und dokumentiere Ergebnisse nachvollziehbar. Mein Ziel ist der Einstieg in Prüfstandstechnik, Messdatenauswertung, Energiespeicher oder technische Systementwicklung.",
      contactCardTitle: "Kontaktdaten & Profile",
      lblLocation: "Standort",
      valLocation: "Oldenburg, Niedersachsen, Deutschland",
      lblEmail: "E-Mail",
      lblLinkedIn: "LinkedIn",
      lblGitHub: "GitHub",
      cvBoxTitle: "Offizieller Lebenslauf",
      cvBoxDesc: "Vollständiges Dokument mit Studienmodulen, detailliertem Projektverzeichnis und Zeugnisreferenzen.",
      btnDownloadCV: "Lebenslauf herunterladen (PDF)",
      
      footerCopyright: "© 2026 Ahmed Abufanas. Alle Rechte vorbehalten.",
      footerLegal: "Impressum",
      footerPrivacy: "Datenschutz",
      modalClose: "Schließen",
      
      impressumTitle: "Impressum",
      impressumText: "Angaben gemäß § 5 DDG (Digitale-Dienste-Gesetz):<br><br><strong>Ahmed Abufanas</strong><br>Osterkampsweg 70<br>26131 Oldenburg<br>Deutschland<br><br><strong>Kontakt:</strong><br>E-Mail: abufanasa@gmail.com<br><br><strong>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV:</strong><br>Ahmed Abufanas, Anschrift wie oben.<br><br><em>Hinweis:</em> Diese Website dient ausschließlich der beruflichen Vorstellung und Dokumentation technischer Projekte. Es werden keine kostenpflichtigen Waren oder Dienstleistungen angeboten.",
      
      privacyTitle: "Datenschutzerklärung",
      privacyText: "<strong>1. Datenschutz auf einen Blick</strong><br>Der Schutz Ihrer persönlichen Daten ist mir ein wichtiges Anliegen. Diese Portfolio-Website wird als statische Website über GitHub Pages (GitHub Inc., 88 Colin P Kelly Jr St, San Francisco, CA 94107, USA) bereitgestellt.<br><br><strong>2. Datenerfassung & Hosting</strong><br>Beim Aufruf dieser Website verzeichnet der Webserver von GitHub technisch bedingt Protokolldaten (z. B. IP-Adresse, Datum und Uhrzeit des Abrufs, Browsertyp, Betriebssystem). Dies ist zur sicheren und stabilen Bereitstellung der Website technisch erforderlich (Rechtsgrundlage: Art. 6 Abs. 1 lit. f DSGVO). Es werden auf dieser Website keine Cookies, keine Analysedienste (wie Google Analytics) und keine externen Webfonts oder Werbetracker eingesetzt.<br><br><strong>3. Kontaktaufnahme</strong><br>Wenn Sie mich per E-Mail kontaktieren, werden Ihre Angaben (Name, E-Mail-Adresse und Inhalt Ihrer Nachricht) zur Bearbeitung der Anfrage und für mögliche Anschlussfragen bei mir gespeichert. Diese Daten gebe ich ohne Ihre Einwilligung nicht weiter.<br><br><strong>4. Ihre Rechte</strong><br>Sie haben jederzeit das Recht auf unentgeltliche Auskunft über Ihre gespeicherten personenbezogenen Daten, deren Herkunft und Empfänger sowie den Zweck der Datenverarbeitung und ein Recht auf Berichtigung, Sperrung oder Löschung dieser Daten. Wenden Sie sich hierzu bitte an die angegebene E-Mail-Adresse."
    },
    
    en: {
      siteTitle: "Ahmed Abufanas | Engineering Physics & Data Analysis",
      navProjects: "Projects",
      navExperience: "Experience",
      navSkills: "Skills",
      navAbout: "About",
      navContact: "Contact",
      navResume: "Résumé (PDF)",
      heroStatus: "Engineering Physics Graduate (B.Eng.)",
      heroHeadline: "Engineering Data Analysis, Scientific Computing & Measurement Systems",
      heroLead: "Focused on standardized data analysis, physical modeling, and processing pipelines in energy systems and acoustics. Rigorous methods, documented constraints, and reproducible results.",
      ctaProjects: "View Selected Projects",
      ctaResume: "Download Résumé",
      ctaContact: "Get in Touch",
      
      secProjectsTitle: "Selected Technical Projects",
      secProjectsDesc: "Practical engineering studies featuring documented datasets, methodical validation, and transparent technical boundaries.",
      
      // Project 1
      p1Tag: "Wind Energy & SCADA Analytics",
      p1Title: "Wind Turbine Performance Review",
      p1ProblemLabel: "Problem Definition",
      p1Problem: "Detecting persistent underperformance and operational anomalies across high-dimensional 10-minute SCADA measurements from utility-scale wind assets without distortion from sensor error events.",
      p1ContributionLabel: "Contribution & Methodology",
      p1Contribution: "Analyzed operational measurements from Kelmarsh wind farm Turbine 1 (52,560 timestamps, 2022). Performed screening and physical plausibility filtering, developed a reference power-curve binning model, conducted comparative evaluations against regression models (scikit-learn), and aggregated persistent underperformance intervals. Built an interactive Streamlit dashboard for structured event inspection.",
      p1ResultLabel: "Key Findings & Metrics",
      p1Result: "Successfully segmented curtailment/fault intervals and isolated consistent underperformance events to prioritize targeted engineering field reviews.",
      p1Metric1Val: "52,560",
      p1Metric1Lbl: "10-minute SCADA timestamps (2022)",
      p1Metric2Val: "2,050 kW",
      p1Metric2Lbl: "Rated power (Senvion MM92)",
      p1Metric3Val: "Streamlit",
      p1Metric3Lbl: "Interactive event inspection",
      p1LimitTitle: "Documented Limitation:",
      p1LimitText: "Model error reduction represents algorithmic fitting accuracy, not increased physical turbine efficiency or confirmed financial gain. The dashboard serves static evaluation results from historical data and does not ingest live telemetry.",
      
      // Project 2
      p2Tag: "Battery Energy Storage & Power Markets",
      p2Title: "German BESS Dispatch & Degradation Analytics",
      p2ProblemLabel: "Problem Definition",
      p2Problem: "Pure price-arbitrage optimization in day-ahead wholesale electricity markets tends to cycle grid batteries aggressively on negligible price spreads, accelerating cell wear without delivering proportional economic value.",
      p2ContributionLabel: "Contribution & Methodology",
      p2Contribution: "Ex-post techno-economic evaluation of a grid-connected 1 MW / 2 MWh BESS using official SMARD day-ahead electricity spot prices (DE/LU bidding zone, 8,784 hourly intervals in calendar year 2024). Formulated a Mixed-Integer Linear Program (MILP via SciPy/HiGHS) resolving daylight-saving transitions, asymmetric conversion efficiencies (95%), and SOC boundary constraints. Replayed all schedules through an independent physical battery engine (< 10⁻¹⁰ EUR discrepancy) and conducted degradation-cost sensitivity sweeps.",
      p2ResultLabel: "Key Findings & Metrics",
      p2Result: "Simulated margins under stated cost assumptions: Under a nominal cycling-cost assumption of €20/MWh-equivalent-cycle-energy, the model produced a simulated net margin of €44,685.44 across 418.30 equivalent full cycles (EFC). Annual cycling was dampened by 32.44% while sacrificing only 5.26% gross revenue, raising realized gross arbitrage per cycle from €104.72/EFC to €146.83/EFC. Full methodology documented in the repository.",
      p2Metric1Val: "8,784 hrs",
      p2Metric1Lbl: "SMARD market data 2024 (DE/LU)",
      p2Metric2Val: "-32.44% EFC",
      p2Metric2Lbl: "Cycle reduction via degradation cost",
      p2Metric3Val: "+467%",
      p2Metric3Lbl: "Simulated net margin vs. rigid schedule",
      p2LimitTitle: "Documented Limitation:",
      p2LimitText: "Findings are retrospective mathematical simulations under stated market and efficiency assumptions, not commercial revenue earned. The cycling-cost assumption serves as an economic dispatch proxy and is not an electrochemical degradation model.",
      
      // Project 3
      p3Tag: "Acoustics & Measurement Data Analysis",
      p3Title: "Industrial Noise Exposure Analysis",
      p3ProblemLabel: "Problem Definition",
      p3Problem: "Resolving regulatory divergence (3-dB equal-energy exchange rate under NIOSH/ISO vs. 5-dB regulatory rate under OSHA), managing severe upper-tail acoustic skewness, and auditing pseudo-replication from multi-worker sampling in single facilities.",
      p3ContributionLabel: "Contribution & Methodology",
      p3Contribution: "Conducted zero-loss data engineering and quantitative analysis across the historical NIOSH Health Hazard Evaluation archive (807 worker dosimetry records, 582 stationary sound surveys across 77 enterprises). Rectified documented historical compiler formula errors, evaluated 680 simultaneous dual-channel worker shifts, and benchmarked measurements against German occupational noise standards (DIN EN ISO 9612 / LärmVibrationsArbSchV).",
      p3ResultLabel: "Key Findings & Metrics",
      p3Result: "477 of 758 valid personal measurements met or exceeded the 100% NIOSH dose criterion (median dose 174.20%, equivalent to an 8-hour continuous level of 87.41 dBA). In 98.82% of paired shifts (672 of 680 simultaneous dual-channel measurements), NIOSH physical dose exceeded the OSHA PEL value (median difference: +151.60 percentage points). Full methodology documented in the repository.",
      p3Metric1Val: "758",
      p3Metric1Lbl: "Valid personal measurements",
      p3Metric2Val: "62.93%",
      p3Metric2Lbl: "Met/exceeded NIOSH REL criterion",
      p3Metric3Val: "98.82%",
      p3Metric3Lbl: "Systematic NIOSH > OSHA disparity",
      p3LimitTitle: "Documented Limitation:",
      p3LimitText: "Historical portfolio analysis of archived investigation reports (1996–2007). Does not represent current national workplace prevalence and does not constitute a certified occupational hygiene compliance assessment or medical evaluation.",
      
      linkCode: "View Repository",
      linkLive: "Live Dashboard",
      allProjectsGitHub: "View further projects on GitHub",
      
      // Experience
      secExpTitle: "Education & Experience",
      secExpDesc: "Academic foundation in Engineering Physics and research experience in data pipelines, optical spectroscopy, and acoustic measurement.",
      colEduTitle: "Education",
      colWorkTitle: "Research & Professional Experience",
      
      edu1Date: "10/2025 – 02/2028 (exp.)",
      edu1Title: "Master of Science in Engineering Physics",
      edu1Place: "Carl von Ossietzky University of Oldenburg, Germany",
      edu1Desc: "Focus areas: Energy systems, energy storage, photovoltaics, measurement technology, modeling, and numerical simulation.",
      
      edu2Date: "10/2015 – 02/2025",
      edu2Title: "Bachelor of Engineering (B.Eng.) – Engineering Physics",
      edu2Place: "Carl von Ossietzky University of Oldenburg, Germany",
      edu2Desc: "Focus areas: Applied physics, electrodynamics, optics, measurement systems, control engineering, and materials science.<br><strong>Thesis:</strong> <em>Binaural Detection and Auditory Modelling of Bandwidth Effects</em> – MATLAB-based signal processing, adaptive filtering, and statistical evaluation of psychoacoustic measurement data.",
      
      work1Date: "02/2026 – 06/2026",
      work1Title: "Research Assistant – Spectral Analysis & Python Data Processing",
      work1Place: "Emden/Leer University of Applied Sciences",
      work1Desc: "Extended a scientific Python pipeline for automated processing and calibration of high-resolution spectral data from a BACHES Echelle spectrograph. Refactored legacy codebases, standardized analysis parameters, and documented testing workflows to ensure analytical reproducibility.",
      
      work2Date: "03/2026 – 09/2026",
      work2Title: "Student Buddy – International Office",
      work2Place: "Carl von Ossietzky University of Oldenburg",
      work2Desc: "Guided and assisted incoming international students during arrival and orientation phases; supported administrative procedures and university correspondence.",
      
      work3Date: "03/2023 – 12/2023",
      work3Title: "Research Assistant – Data Analysis & Documentation",
      work3Place: "Carl von Ossietzky University of Oldenburg",
      work3Desc: "Performed structured processing, consistency checks, and statistical quality control of experimental datasets using MATLAB and Excel. Developed standardized routines to ensure repeatable analytical outputs.",
      
      // Skills
      secSkillsTitle: "Technical Skills & Capabilities",
      secSkillsDesc: "Proficiencies in scientific computing, test bench engineering, signal processing, and physical system modeling.",
      cat1Title: "Programming & Data Analysis",
      cat1Item1: "<strong>Python:</strong> pandas, NumPy, scikit-learn, SciPy, Matplotlib, Plotly, Streamlit, pytest",
      cat1Item2: "<strong>MATLAB & Simulink:</strong> Signal processing, filter design, statistical analysis",
      cat1Item3: "<strong>C++ & Embedded:</strong> Core algorithms, Arduino microcontroller sensor prototyping",
      cat1Item4: "<strong>Version Control & Environment:</strong> Git, GitHub, virtual environments, Linux/PowerShell",
      
      cat2Title: "Measurement & Test Systems",
      cat2Item1: "<strong>Sensor Data Acquisition:</strong> Time- and frequency-resolved data, filtering & smoothing",
      cat2Item2: "<strong>Optical Measurement Systems:</strong> Echelle spectroscopy (BACHES), calibration flows, LIDAR signals",
      cat2Item3: "<strong>Acoustics & Vibration:</strong> Binaural detection, auditory thresholds, noise dosimetry",
      cat2Item4: "<strong>Experimental Testing:</strong> Thermal and load characterization, electrical parameter curves",
      
      cat3Title: "Modeling & Simulation",
      cat3Item1: "<strong>Energy Systems:</strong> BESS battery models, dispatch optimization (HiGHS MILP)",
      cat3Item2: "<strong>Control Systems:</strong> Feedback loop modeling, sensor-actuator integration",
      cat3Item3: "<strong>3D CAD & Mechanics:</strong> SolidWorks (parametric modeling, structural FEA simulation)",
      cat3Item4: "<strong>Scientific Documentation:</strong> LaTeX, OriginPro, technical reports",
      
      cat4Title: "Languages & Work Approach",
      cat4Item1: "<strong>German:</strong> Professional working proficiency (C1)",
      cat4Item2: "<strong>English:</strong> Professional working proficiency (C1)",
      cat4Item3: "<strong>Arabic:</strong> Native proficiency",
      cat4Item4: "<strong>Work Approach:</strong> Autonomous learning, clean code architecture, systematic error isolation",
      
      // About & Contact
      secAboutTitle: "About & Contact",
      secAboutDesc: "Direct contact details for engineering and technical data positions.",
      aboutP1: "As an Engineering Physics graduate (B.Eng.), I combine a rigorous understanding of physical systems with scientific programming and structured data analysis. Whether calibrating astronomical spectrographs, modeling battery dispatch strategies, or detecting wind turbine underperformance: my focus is always on delivering transparent, reproducible, and verifiable analysis from complex measurement datasets.",
      aboutP2: "I work independently, test mathematical assumptions directly against empirical data, and document methods clearly so team members and stakeholders can build on the results. I am looking forward to contributing to test bench engineering, measurement data analysis, energy systems, or technical development teams.",
      contactCardTitle: "Contact & Profiles",
      lblLocation: "Location",
      valLocation: "Oldenburg, Lower Saxony, Germany",
      lblEmail: "Email",
      lblLinkedIn: "LinkedIn",
      lblGitHub: "GitHub",
      cvBoxTitle: "Official Résumé",
      cvBoxDesc: "Comprehensive CV detailing academic modules, course projects, and credentials.",
      btnDownloadCV: "Download Résumé (PDF)",
      
      footerCopyright: "© 2026 Ahmed Abufanas. All rights reserved.",
      footerLegal: "Legal Notice",
      footerPrivacy: "Privacy Policy",
      modalClose: "Close",
      
      impressumTitle: "Legal Notice (Impressum)",
      impressumText: "Information according to § 5 DDG (German Digital Services Act):<br><br><strong>Ahmed Abufanas</strong><br>Osterkampsweg 70<br>26131 Oldenburg<br>Germany<br><br><strong>Contact:</strong><br>Email: abufanasa@gmail.com<br><br><strong>Responsible for editorial content (§ 18 Abs. 2 MStV):</strong><br>Ahmed Abufanas (address above).<br><br><em>Note:</em> This website serves solely for professional representation and documentation of engineering projects. No commercial services or products are sold.",
      
      privacyTitle: "Privacy Policy",
      privacyText: "<strong>1. Overview</strong><br>Protecting your personal data is a priority. This portfolio website is hosted as a static site via GitHub Pages (GitHub Inc., 88 Colin P Kelly Jr St, San Francisco, CA 94107, USA).<br><br><strong>2. Data Collection & Hosting</strong><br>When accessing this website, the GitHub web server automatically records log files (e.g., IP address, access timestamp, browser type, operating system) necessary for technical delivery and security (Art. 6(1)(f) GDPR). This site uses no cookies, no tracking services (such as Google Analytics), and no external web fonts.<br><br><strong>3. Contact Requests</strong><br>If you contact me by email, the information you provide (name, email, and message content) is stored solely for processing your inquiry. It will not be shared without your consent.<br><br><strong>4. Your Rights</strong><br>You have the right to request information about your stored personal data, its origin, recipient, and processing purpose, as well as the right to rectification, blocking, or erasure under GDPR. Please reach out via the provided email address."
    }
  };

  // State
  let currentLang = 'de';

  function setLanguage(lang) {
    if (!translations[lang]) return;
    currentLang = lang;
    document.documentElement.lang = lang;
    localStorage.setItem('portfolio_lang', lang);

    // Update switcher buttons
    document.querySelectorAll('.lang-btn').forEach(btn => {
      const isActive = btn.getAttribute('data-lang') === lang;
      btn.classList.toggle('active', isActive);
      btn.setAttribute('aria-pressed', isActive ? 'true' : 'false');
    });

    // Update all i18n text nodes
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (translations[lang][key] !== undefined) {
        // If string contains HTML (e.g. <strong>, <br>), use innerHTML, else textContent
        if (translations[lang][key].includes('<')) {
          el.innerHTML = translations[lang][key];
        } else {
          el.textContent = translations[lang][key];
        }
      }
    });

    // Update document title
    if (translations[lang].siteTitle) {
      document.title = translations[lang].siteTitle;
    }
  }

  // Initialize
  function init() {
    // 1. Language Setup
    const storedLang = localStorage.getItem('portfolio_lang');
    const initialLang = (storedLang === 'en' || storedLang === 'de') ? storedLang : 'de';
    
    document.querySelectorAll('.lang-btn').forEach(btn => {
      btn.addEventListener('click', function () {
        const selected = this.getAttribute('data-lang');
        setLanguage(selected);
      });
    });
    
    setLanguage(initialLang);

    // 2. Mobile Menu Toggle
    const mobileBtn = document.querySelector('.mobile-nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (mobileBtn && navLinks) {
      mobileBtn.addEventListener('click', () => {
        const isOpen = navLinks.classList.toggle('open');
        mobileBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      });

      // Close menu when clicking any nav item
      navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
          if (navLinks.classList.contains('open')) {
            navLinks.classList.remove('open');
            mobileBtn.setAttribute('aria-expanded', 'false');
          }
        });
      });
    }

    // 3. Accessible Legal Modal
    const modal = document.getElementById('legalModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');
    const modalClose = document.getElementById('modalCloseBtn');
    let lastActiveElement = null;

    function openModal(type) {
      if (!modal) return;
      lastActiveElement = document.activeElement;
      
      if (type === 'impressum') {
        modalTitle.textContent = translations[currentLang].impressumTitle;
        modalBody.innerHTML = translations[currentLang].impressumText;
      } else if (type === 'privacy') {
        modalTitle.textContent = translations[currentLang].privacyTitle;
        modalBody.innerHTML = translations[currentLang].privacyText;
      }
      
      modal.classList.add('active');
      modal.setAttribute('aria-hidden', 'false');
      modalClose.focus();
      document.body.style.overflow = 'hidden';
    }

    function closeModal() {
      if (!modal) return;
      modal.classList.remove('active');
      modal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      if (lastActiveElement) {
        lastActiveElement.focus();
      }
    }

    document.querySelectorAll('[data-modal-open]').forEach(trigger => {
      trigger.addEventListener('click', (e) => {
        e.preventDefault();
        const type = trigger.getAttribute('data-modal-open');
        openModal(type);
      });
    });

    if (modalClose) {
      modalClose.addEventListener('click', closeModal);
    }

    if (modal) {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) {
          closeModal();
        }
      });
      
      // Close on Escape key
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
          closeModal();
        }
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
