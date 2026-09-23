# Ahmed Abufanas - Professional Engineering Portfolio

Professional, accessible, and high-performance engineering portfolio website built for real-world online use and deployed via **GitHub Pages** (`abufanasa-dotcom.github.io`).

## Overview & Architecture

- **Technology**: Semantic HTML5, Modern Vanilla CSS (custom design system, responsive clamp, CSS Grid/Flexbox), and lightweight Vanilla JavaScript. Zero external runtime libraries or build dependencies.
- **Languages**: Bilingual support with German (default, `de`) and English (`en`), switchable instantly via header toggle without page reloads.
- **Accessibility & Contrast**: Built to WCAG AA/AAA guidelines with visible keyboard focus rings (`:focus-visible`), skip-to-content links, semantic landmark roles, and ARIA modal dialogs.
- **Privacy & Compliance**: German legal notice (§ 5 DDG *Impressum*) and GDPR (*Datenschutzerklärung*) compliant with zero external trackers, analytics, or cookies.

---

## File Structure

```
.
├── index.html                   # Main bilingual portfolio page
├── css/
│   └── style.css                # Polished light design system & responsive layout
├── js/
│   └── main.js                  # Language toggling, mobile nav, and accessible modal handling
├── assets/
│   ├── images/
│   │   ├── ahmed-abufanas.jpg   # High-resolution web-optimized portrait (~60 KB)
│   │   ├── ahmed-abufanas-orig.png # Full original resolution image
│   │   └── favicon.svg          # Minimalist engineering SVG icon
│   └── docs/
│       └── Ahmed_Abufanas_Lebenslauf.pdf # Downloadable verified PDF résumé
├── legal/
│   ├── impressum.html           # Standalone German Impressum
│   └── datenschutz.html         # Standalone GDPR Privacy Policy
├── README.md                    # Project documentation & deployment guide
└── .gitignore                   # Git hygiene
```

---

## Featured Engineering Projects

1. **[Wind Turbine Performance Review](https://github.com/abufanasa-dotcom/wind-turbine-performance)**
   - Historical SCADA analysis (Kelmarsh turbine 1, 52,560 timestamps in 2022).
   - Baseline binned power curve modeling, ML regression benchmarking, and sustained-deviation review.
   - Interactive Streamlit app: [abufanasa-dotcom-wind-turbine-performance-app-vtq3j5.streamlit.app](https://abufanasa-dotcom-wind-turbine-performance-app-vtq3j5.streamlit.app/)
2. **[German BESS Dispatch & Degradation Analytics](https://github.com/abufanasa-dotcom/bess-dispatch-analytics)**
   - Ex-post techno-economic evaluation of a 1 MW / 2 MWh battery in the German/Luxembourg day-ahead electricity market (8,784 hourly intervals in 2024).
   - SciPy/HiGHS MILP optimizer, daylight-saving transitions, independent physical replay validation, and degradation-cost sensitivity sweeps.
3. **[Industrial Noise Exposure Analysis](https://github.com/abufanasa-dotcom/industrial-noise-exposure)**
   - Quantitative evaluation of the historical NIOSH Health Hazard Evaluation noise database (807 personal dosimetry records, 582 area surveys across 77 facilities).
   - Compiler formula corrections, empirical NIOSH (3 dB) vs. OSHA (5 dB) divergence, and benchmarking against German noise safety standards (DIN EN ISO 9612 / LärmVibrationsArbSchV).

---

## Local Preview & Verification

To run and preview the site locally using Node.js:

```powershell
# Using Python (if available):
python -m http.server 8000

# Or using Node.js npx:
npx http-server . -p 8000
```
Open `http://localhost:8000` in your browser.

---

## Deployment to GitHub Pages (`abufanasa-dotcom.github.io`)

Because this repository is named after your GitHub username, it serves as your primary user website.

### Step 1: Initialize Git Repository
In your PowerShell terminal inside this folder (`c:\Users\PC\Desktop\Ahmed_Protfolie`):

```powershell
git init
git add .
git commit -m "Initial commit: professional engineering portfolio website"
```

### Step 2: Create Remote Repository on GitHub
1. Log in to [GitHub](https://github.com/).
2. Create a new repository named exactly:
   ```
   abufanasa-dotcom.github.io
   ```
3. Set the visibility to **Public** (do not initialize with a README, .gitignore, or license as they are already created here).

### Step 3: Link and Push
```powershell
git branch -M main
git remote add origin https://github.com/abufanasa-dotcom/abufanasa-dotcom.github.io.git
git push -u origin main
```

### Step 4: Verify GitHub Pages Activation
1. In your GitHub repository, navigate to **Settings** > **Pages**.
2. Under **Build and deployment** > **Source**, ensure `Deploy from a branch` is selected with branch `main` and folder `/ (root)`.
3. Within 1-2 minutes, your website will be live at:
   ```
   https://abufanasa-dotcom.github.io/
   ```

---

## How to Update Content

- **Updating the Résumé:** Replace `assets/docs/Ahmed_Abufanas_Lebenslauf.pdf` with your new PDF export. Commit and push.
- **Adding or Editing Projects:** Edit the project articles in `index.html` and their corresponding text keys in `js/main.js`.
- **Styling Changes:** Adjust CSS custom variables (`:root`) in `css/style.css`.
