# Ahmed Abufanas — Portfolio V2

Review package updated **1 October 2026**. Static bilingual portfolio for engineering recruiters. Approved bilingual redesign with compact contact actions and system-based light/dark themes. Release changes are reviewed through pull requests before merging into the main publishing branch.

## المعاينة على جهازك

1. فك الضغط داخل **مجلد جديد**؛ احتفظ بمجلد الموقع المنشور دون تعديل.
2. من مجلد المشروع شغّل `python -m http.server 8080 --bind 127.0.0.1` إذا كان Python مثبتًا، ثم افتح http://127.0.0.1:8080/ . أوقف الخادم بـ Ctrl+C. ملف `START_PREVIEW.cmd` بديل متاح في الأرشيف المحلي فقط إذا كان Node.js مثبتًا.
3. جرّب النسخة الألمانية والإنجليزية، صفحات المشاريع، تكبير الرسوم، تنزيل السيرة، ونسخ البريد. يمكن فتح `index.html` مباشرة أيضًا؛ عند منع المتصفح النسخ إلى الحافظة يظهر بديل نصي واضح.

German: `index.html`. English: `en/index.html`. The English download button explicitly identifies the CV as German.

## Light / dark theme

The circular sun/moon control is available in the header of every page, in both languages. On the first visit the site follows the device's light/dark preference. Clicking the control overrides the automatic choice and stores only `light` or `dark` under `aa-portfolio-theme` in localStorage; no preference is transmitted to a server. System changes continue to apply until the visitor makes an explicit choice. Clearing site storage returns to automatic behavior. The preference follows language/page navigation on the same origin and synchronizes across open tabs.

If storage is blocked, the control still works for the current page. Use the HTTP preview for dependable cross-page behavior; storage behavior on directly opened file:// pages varies by browser. Original charts, portrait and CV retain their colors. Printing uses a light palette. Without JavaScript, CSS follows the device preference and the manual toggle stays hidden.

Contact cards now use compact horizontal icon/title rows, concise descriptors and 18px desktop padding. The CV action sits beside the contact heading on desktop and moves below the introduction at smaller widths. There is no fixed clipping height; cards grow when text or clipboard feedback wraps.

## Structure and maintenance

- `index.html`, `en/index.html`: homepages with three project summaries, linked experience, skills and contact cards.
- `projects/`, `en/projects/`: three project studies per language.
- `css/style.css`: one consolidated stylesheet, desktop project rows, responsive layouts, visible focus indicators and reduced-motion support.
- `js/main.js`: progressive navigation, current-section language links, native chart dialog, clipboard feedback/fallback and theme control.
- `js/theme-init.js`: restores a saved light/dark preference before CSS loads, otherwise follows the device preference.
- `assets/images/projects/`: original PNG figures and smaller 800/1200px WebP derivatives; original figures open on enlargement. No chart data or labels were rewritten.
- `assets/docs/`: revised public German CV (two pages).
- `legal/`: operator address explicitly authorized for publication, technical hosting/function disclosures, Gmail contact handling and the approved six-month maximum for ordinary closed enquiries. Contracts, legal duties and necessary rights-related records are treated separately. These pages are not presented as legally certified.
- `sitemap.xml`, `robots.txt`: indexable portfolio URLs and crawler configuration. Legal pages are marked noindex.
- `scripts/build.py`: shared bilingual content, work history, project metrics, HTML generation and metadata.
- `scripts/build_cv.py`: CV generation from the same work history and metrics.
- `scripts/check.py`: local references, HTML structure, hreflang, privacy, numeric consistency and PDF checks.
- `scripts/check_interactions.cjs`: simulated-DOM checks of application behavior; not a browser test.
- `scripts/check_http.py`: standalone Python temporary HTTP server and asset/MIME checks; no local Node server file required.

Edit `scripts/build.py`, then run `python scripts/build.py`; generated pages should not be edited separately. Image derivatives and their manifest are supplied, so HTML generation needs only Python's standard library.

PDF maintenance requires Python, reportlab and DejaVu Sans fonts. Set `FONT_DIR` to the folder containing `DejaVuSans.ttf` and `DejaVuSans-Bold.ttf` on Windows, then run `python scripts/build_cv.py`. Never replace the public CV with the unredacted original.

Validation requires pypdf for the CV check:

```text
python scripts/check.py
node scripts/check_interactions.cjs
python scripts/check_http.py
```

These are maintenance tools. Visitors need no build system or dependencies.

## Updating projects and publishing

Uploading a repository to the GitHub profile does not automatically alter this website. Project content is maintained in `scripts/build.py`: bilingual project data, contribution summaries, card metrics and dedicated case-study content. New projects require reviewed German and English copy, verified numbers, repository/demo links and genuine figures. Update the relevant templates for the new project; the card metric logic is specific to the three current projects rather than a generic repository feed. Add responsive images and their dimensions to the image manifest. Update the public CV when relevant; the source CV stays private.

After editing, generate the HTML and run the checks listed above. Review the changes on a branch, then merge the approved pull request into `main`. The existing GitHub Pages publishing source uses the main branch root. Pages redeploys after publishing-branch changes; a push to a separate scientific repository does not trigger a portfolio content update.

For routine maintenance, clone the existing repository rather than copying a ZIP over an older working tree. Keep the legal contact address current and implement the described retention practice in the mailbox; the website has no email-deletion service.

Deployment assets: `.nojekyll`, `index.html`, `en/`, `projects/`, `css/`, `js/`, `assets/`, `legal/`, `sitemap.xml`, `robots.txt`. Scripts and review notes are maintenance source files, not browser application code.

See `REVIEW.md` for source comparisons and the precise limits of completed checks. No legal or accessibility certification is claimed.
