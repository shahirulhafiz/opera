# Mesiniaga — Website Inspection Report

**Target:** `mesiniaga-page` — https://mesiniaga.com.my/
**Goal:** Explore core user flows
**Method:** Bounded browser crawl (real browser drive + same-origin verification), persisted to `docs/browse/webapp.db` (run_id 1).
**Date:** 2026-07-02

> Companion documents: [`mesiniaga-report.md`](./mesiniaga-report.md) is the full per-page behavior/transition map. This file is the curated executive summary.

---

## 1. At a glance

| Metric | Value |
|--------|-------|
| Pages discovered | 41 |
| Pages inspected | 41 |
| Actions logged | 43 |
| Errors (HTTP 4xx) | 4 |
| Error rate | 9.3% |
| Avg load time | 1,014 ms |
| p95 load time | 1,846 ms |
| Max load time | 2,469 ms (Chatgu) |

**Platform:** WordPress + Elementor. Every page shares the same header navigation, footer, and newsletter block; product/service pages add a reCAPTCHA-protected lead form.

**Verdict:** COMPLETE — full reachable in-scope frontier was crawled within bounds.

---

## 2. Key findings

### 🔴 Broken links (4 × HTTP 404) — highest priority
| Broken URL | Linked from | Notes |
|------------|-------------|-------|
| `/xyberguard/` | Home — "Security · Extensive Protection" hero card | A working `/security/` page exists; the card points to the wrong slug. |
| `/prompt-engineering-workshop/` | Home — promo "Learn More" | Dead promo target. |
| `/mb-evergreen/` | `/cloud-infrastructure/` | Sub-offering link 404s. |
| `/mb-hybrid/` | `/cloud-infrastructure/` | Sub-offering link 404s. |

### 🟠 Duplicate / inconsistent URLs
- Both `/network-solutions/` (Services menu) and `/network-solution/` (home card) exist and render the "Network Solutions" page. Two URLs for the same content dilutes SEO and is a maintenance risk — consolidate + 301 redirect.

### 🟢 Working as expected
- **Newsletter form** validates email format client-side (HTML5).
- **Lead forms** enforce required fields and are protected by Google reCAPTCHA.
- **FAQ accordions** expand/collapse correctly.
- **Hero carousel** auto-rotates and has working prev/next + pagination.
- Contact info is complete (3 office locations with phone lines).

---

## 3. Interactive components & verified behavior

| Component | Where | Verified behavior |
|-----------|-------|-------------------|
| Hero carousel (Swiper) | Home | Auto-rotates through 5 slides (observed 1→2→3 unprompted); prev/next + 5 pagination dots. |
| Newsletter form (Elementor) | Every page (footer) | `email` required; invalid input blocked with *"Please include an '@' in the email address…"*. Real subscribe not submitted (safety). |
| Lead-capture form | All product/service pages | Fields: Name, Work Email, Mobile — all required. Empty submit → *"Please fill out this field."* on each. Google reCAPTCHA present. Real submit not performed. |
| FAQ accordion | LegalEye, Minits, Chatgu, Network Solutions | Click toggles collapsed↔expanded, reveals answer region. |
| Product video | Minits | "Play Video" embed (not exercised to avoid autoplay media). |
| Dropdown menus | Global nav | PRODUCTS / SERVICES / ABOUT US reveal submenus on hover. |
| Social links | Footer | Facebook, Instagram, LinkedIn, X — external origins, not followed (out of scope). |

---

## 4. Site structure (information architecture)

- **Products (7):** LegalEye, Minits, Chatgu, Ailmu, eHandbook Assistant, Translate Helper, NetSysCare
- **Services (6):** The Art of Conversing with AI, MIMS, MECS-Link, Network Solutions, IT Maintenance, Project Management
- **Solutions / offerings:** AI First Culture (→ Scope of Work Extraction), Cloud Infrastructure (→ mb-evergreen/mb-hybrid ⚠️404), End-User, Project Delivery, Industry Solutions, Security
- **About Us (8):** About Mesiniaga, AGM, Anti-Bribery & Corruption, Achievements & Certifications, Investor Relations, Partners, News & Events, Careers
- **Corporate/culture:** Life at Mesiniaga, Company Leadership
- **Legal:** Privacy Policy, Terms of Use
- **Contact:** Contact Us (HQ Subang Jaya + Penang + Johor branches)
- **News articles (depth 2):** "AI Engineering Workshop with TAR UMT Students" (2025-04-17), "Advancing GenAI education" (2025-03-19)

---

## 5. Performance (page load / response time)

Slowest pages:

| Page | Load (ms) | Status |
|------|-----------|--------|
| Chatgu | 2,469 | 200 |
| Industry Solutions | 1,912 | 200 |
| IT Maintenance | 1,846 | 200 |
| Scope of Work Extraction | 1,827 | 200 |
| Network Solutions | 1,769 | 200 |
| The Art of Conversing with AI | 1,762 | 200 |
| Ailmu | 1,736 | 200 |

Fastest pages were largely cached corporate pages (Careers, Investor Relations, About, Security ≈ 110–210 ms). Load times vary widely (110 ms – 2.47 s), consistent with cold-vs-warm cache rather than a systemic slowdown.

---

## 6. Recommendations

1. **Fix the 4 broken links** — repoint the home "Security" card to `/security/`, and either build or remove `/prompt-engineering-workshop/`, `/mb-evergreen/`, `/mb-hybrid/`.
2. **Consolidate `/network-solution/` → `/network-solutions/`** with a 301 redirect.
3. **Review slow product pages** (Chatgu ~2.5 s) for image/asset optimization.
4. Consider adding a dedicated **contact/enquiry form** on Contact Us (currently only the newsletter + static address/phone info).

---

## 7. How to explore the data

The SQLite store (`docs/browse/webapp.db`) is the source of truth. Examples:

```bash
python scripts/store.py --db docs/browse/webapp.db stats  --slug mesiniaga-page
python scripts/store.py --db docs/browse/webapp.db logs   --run 1
python scripts/store.py --db docs/browse/webapp.db find    --text "lead form"
python scripts/store.py --db docs/browse/webapp.db feedback
```
