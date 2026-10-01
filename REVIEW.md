# Implementation and review record — 1 October 2026

This package follows the user's German/English full-page screenshot review and approval to implement. The published main branch is unchanged. The accepted files are prepared for a separate release review branch; no deployment has been made. A separate checkpoint of the preceding version was kept outside this package.

## Changes completed

- Direct degree-based hero title, separate technical specialism, concise professional introduction and clear target roles in both languages. Exactly two hero actions: projects and downloadable CV.
- Original square portrait retained without cropping, alteration or marketing caption. Restrained border and shadow.
- Consistent horizontal desktop project rows, 16px project body copy, separated contribution, prominent metric and contextual explanation, concise scope, code/detail links and original scientific figures.
- Consolidated stylesheet replaces layered overrides. Unified spacing, hierarchy, readable captions and buttons. Desktop emphasis retained; tablet/mobile rules supplied without claiming rendered validation.
- 800/1200px WebP derivatives with responsive image attributes and reserved aspect ratios. Largest derivative set totals 218,086 bytes vs 720,660 bytes for the three originals (69.7% smaller). This is a file-size comparison, not a measured page-speed improvement. All three original figures and the portrait are byte-for-byte unchanged.
- Native chart dialog opens the original PNG, has labeled title/caption and a visible close control; direct-image fallback works without dialog support. Modified clicks retain native link behavior.
- Full BACHES research title, direct experience/education heading, shared work history and dates. Professional German/English terminology reviewed, without unverified proficiency certificates or grades.
- Skills link to relevant project or work examples. Three prominent contact cards, readable email/copy controls and a second CV download action.
- Progressive mobile navigation; without JavaScript the links remain visible. Menu resets on outside click, Escape and desktop resize. Same-page mobile links move focus to their destination. Language switching retains the visible section, including the contact section at the page bottom. Active navigation is implemented.
- Availability: full-time/part-time from 1 November 2026 and relocation within Germany follow user authorization, rather than being attributed to the source CV.
- Updated two-page public German résumé; shared work and metric values. PDF downloaded from both languages is explicitly identified as German in the English UI.
- Canonical URLs, reciprocal German/English/x-default hreflang, Open Graph metadata, factual ProfilePage/Person structured data on homepages, sitemap and robots.txt.
- Private residential address removed from the old legal notice. Both legal pages are conspicuous local-review drafts, with incomplete details identified and no legal-compliance claim. They have noindex and are excluded from the sitemap. The user must resolve appropriate operator/address and email-processing details before publication. Do not use the city-only draft as a legally certified notice.

## Authoritative content and calculation record

Latest personal source: uploaded `Abufanas-Lebenslauf_EngPhy.docx.pdf`, pages 1–2, reviewed in this conversation. Supports Emden/Leer February–June 2026; Student Buddy March–September 2026; binaural modeling and machine learning March–December 2023; degree history and academic projects. Original personal source was not overwritten or included here.

Project documents were read earlier in this conversation. This build checks consistency against the recorded source values; it does not rerun the underlying scientific analyses. Earlier retrieval attempts were blocked; the release preflight below records a successful fresh GitHub source check.

- Wind: `wind-turbine-performance/README.md`: 52,560 timestamps and five candidate events. Wind-speed/direction model estimates contemporaneous power, not a future production forecast. Causes unconfirmed; no live telemetry. Largest event: approximately 350.88 kW/kWh. Timestamp span 50 minutes vs six ten-minute intervals (60 minutes); exact boundaries unresolved. Chronological evaluation periods and outstanding context/external-year checks remain visible.
- BESS: `bess-dispatch-analytics/reports/degradation_sensitivity_2024.csv`, recorded blob `f9cc1bfad7c452d8d46122075c5b937758944378`, cost-0 and cost-20 rows. Nominal net margin 44,685.442039196685 EUR; EFC 418.3013157894737 vs 619.1157894736841; gross margin 61,417.49467077563 vs 64,831.0573913435 EUR. Recomputed ratios: 32.44% fewer EFC and 5.27% lower gross margin. The repository README's earlier 5.26% is a recorded rounding discrepancy, not a new physical result. Baseline is optimization without assumed cycling costs, not the fixed schedule. 95% charging × 95% discharging = 90.25% round-trip efficiency; historical MILP, known prices, no measured aging or earned commercial revenue.
- Noise: `industrial-noise-exposure/reports/dashboard_metric_registry.csv`, recorded blob `24e27ebfa0d86e232596ca851877a752e99414aa`, M02/M05/M08/M15. 477/758 valid personal measurements meet or exceed 100% NIOSH dose; 672/680 paired readings exceed OSHA PEL dose. Counts are measurements, not necessarily distinct workers. Historical investigation sample, mainly 1996–2007 with selected cases through 2013. German-context subset of 33 suitable records is separate from NIOSH dose analysis; no population-wide inference or certified compliance assessment.

Repositories:
- https://github.com/abufanasa-dotcom/wind-turbine-performance
- https://github.com/abufanasa-dotcom/bess-dispatch-analytics
- https://github.com/abufanasa-dotcom/industrial-noise-exposure

Legal/hosting references consulted for the draft scope (no legal certification):
- https://www.gesetze-im-internet.de/ddg/__5.html
- https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement

## Verification completed

- Ten HTML pages parsed: eight bilingual portfolio pages and two legal drafts.
- 199 local page/anchor/asset references, including 24 srcset candidates, resolved successfully.
- Exactly one H1/main per page, valid checked tag nesting and unique IDs; descriptive metadata, reciprocal hreflang and homepage structured data parsed.
- Shared work dates/titles checked in both languages and the CV. BESS source ratios/values checked across both detail pages and PDF; stale 5.26/C1 notices and specified private data absent from all public HTML and CV.
- 64 simulated-DOM assertions passed: menu state/Escape/outside/resize, destination focus call, original-chart selection, close/focus restoration calls, modified-click/direct-link fallback, bilingual copy success/failure and section-preserving language links, including page bottom. These tests exercise JavaScript logic; they do not test native browser behavior.
- JavaScript and preview server syntax checked with Node.
- 29 local HTTP deployment files returned 200, correct MIME types and exact current on-disk bytes. Temporary server stopped after test.
- Public PDF: exactly two pages, selectable text, no specified private details. Both pages rendered with Poppler and visually inspected; no observed clipping/overlap.
- Original portrait/three featured PNGs compared to the checkpoint by SHA-256; unchanged. WebP widths checked; BESS derivative visually inspected.
- Text contrast examples against the light background exceed 4.5:1 for ink, muted copy and blue controls; former low-contrast skill numbering now uses the muted text color. This is a limited color check, not WCAG certification.

## Checks still required before publication

Real-browser layout and interaction testing could not run because the available browser surface blocks local URLs/file browsing. No substitute browser screenshots were generated. Earlier supplied screenshots describe the version before this final implementation.

Review locally:
1. German and English desktop at 1440×900 and 1366×768: hero wrapping, portrait alignment, project-row proportions, figure readability, experience and contact balance.
2. Tablet 768px and phone 375–390px: menu, no horizontal overflow, figure aspect ratios, email wrapping and touch controls.
3. Keyboard: skip link, visible focus, menu destinations, native chart focus trapping, Escape, close-button/backdrop behavior and return focus.
4. Language switch after scrolling to each section and from every project detail page; corresponding page/section should remain reachable.
5. Clipboard success/restriction fallback, both PDF download buttons and all external links/dashboard.
6. Complete legal drafts before publishing. Do not interpret the missing residential address as confirmed legal sufficiency.

Lighthouse/Core Web Vitals, full accessibility conformance, native browser tests, fresh external link reachability and formal legal review are not claimed. No merge, push or publication occurred.


## Approved compact contact and theme update — 1 October 2026

- Implemented the user's approval after review of the two 14:43 contact screenshots. Contact icons now sit beside titles; repeated all-caps labels removed; LinkedIn/GitHub descriptions reduced to one line. Desktop padding 18px and minimum card height 146px target approximately half the preceding card height, without claiming a measured rendered reduction. Text and feedback are allowed to grow; no fixed-height clipping. Email remains 20px and contact actions retain 44px minimum height.
- Contact CV moved into the heading row on desktop. Contact heading and introduction shortened naturally in both languages; no career or project facts changed.
- Added light/dark support to all ten pages. Default follows reported device/browser color preference; explicit choice persists in localStorage, overrides later system changes and synchronizes across same-origin pages/tabs. Clearing site storage restores automatic preference. Access/write errors are caught and leave the current-page toggle usable.
- Small pre-stylesheet initializer restores preference before CSS; stylesheet also supplies a system-preference fallback without JavaScript. Labeled, keyboard-operable theme toggle uses aria-pressed and translated action tooltips. Header control remains available outside the collapsed mobile navigation.
- Separate dark semantic palette for page, cards, typography, buttons, menus and dialog. Original scientific plot colors are not inverted, and plot links remain dark blue on the original white figure surface. Print palette is light regardless of theme.
- Privacy draft updated to accurately disclose the local display preference and no server transmission. This supersedes the earlier statement about using no local browser storage; legal documents remain drafts.
- Passed: 10 pages; 209 local references; 24 responsive image candidates; theme-script loading order/metadata/control markup; 116 simulated-DOM assertions; 30 HTTP/MIME/byte checks; JS syntax. Theme cases cover system changes, manual overrides, saved/invalid values, reload, cross-tab updates/clearing and denied storage. These are not native browser tests.
- Compared with the preceding checkpoint: all 14 asset/manifest files unchanged, including PDF, portrait and original/optimized charts. Shared metric and work-history source blocks are byte-for-byte unchanged.
- Calculated contrast samples: dark main text/page 15.84:1; dark secondary text/card 8.38:1; dark accent/wash 7.44:1; primary white text 5.75:1, hover 4.60:1; light secondary text/wash 5.45:1; original-figure link on white 7.00:1. This limited color check does not certify WCAG conformance.
- Still requires local browser review: actual compact-card heights in DE/EN, responsive wrapping, light/dark rendering, native controls/focus and cross-page persistence in the target browser. No remote writes or publication.

Theme implementation references:
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme
- https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage


## Release preflight — approved desktop screenshots, 1 October 2026

- Reviewed the supplied full-page German and English dark-mode screenshots taken at 15:01. Contact cards are compact and aligned; photo, project rows, experience and education are coherent. No obvious image cropping or horizontal overflow is visible in these captures. Screenshot dimensions 675×2048 and 712×2048 reflect reduced captures; they do not establish actual viewport/font sizes or mobile behavior. User approved both versions.
- Re-fetched project documentation through the connected GitHub app. BESS CSV and noise registry SHAs match the recorded sources exactly. Wind README SHA: 3d0eb9fea4659c907c12093ff84897c67ef0ecff. Headline counts, stated scopes, BESS numeric inputs and ratios agree. No scientific analysis was rerun.
- BESS README still states 5.26%; the full-precision CSV calculation gives 5.27%, as already implemented on the website and CV. Other repositories were not edited.
- Added .nojekyll for direct static GitHub Pages deployment. Confirmed existing site repository main commit 592583e75c672b68f0d6e392acd7796df8171364; main tree 90c36b7c39b79baef58419d9b687dc01f9fda7e4.
- Preparation targets a separate release branch and draft PR. Do not merge or publish the legal drafts before the owner supplies suitable public operator/address details and confirms email processing/retention wording. This is a missing-information step, not a request to reapprove the already accepted design.
