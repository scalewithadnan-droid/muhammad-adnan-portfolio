# Adnan Afzal — Mobile Growth & Publishing

Static portfolio for **growthbyadnan.site**. Plain HTML/CSS/JS + GSAP and ScrollTrigger, which are bundled in the repo, so nothing loads from a CDN. It runs on GitHub Pages with no build step.

## Structure

```
index.html                 Homepage (hero, expertise, growth OS, case studies, platforms, experience, insights, contact)
case-studies/              Index + 4 case study pages
insights/                  3 article pages (blog.html lists them)
resume.html                Printable resume ("Print / Save PDF")
404.html                   Custom 404 (works on github.io sub-path and custom domain)
assets/css/main.css        Design system + all components
assets/js/main.js          Interactions & motion (respects prefers-reduced-motion)
assets/js/vendor/          gsap.min.js, ScrollTrigger.min.js (GSAP 3, free license)
assets/fonts/              Inter + Manrope variable fonts (self-hosted, OFL)
assets/img/                Original SVG artwork (case covers, portrait placeholder), OG image
tools/build.py             Generator — all page content lives here
legacy/                    Backup of the previous email-marketing page (noindex)
```

## Editing content

All copy, case studies, experience and articles are in `tools/build.py`. Edit them there, then run:

```bash
python3 tools/build.py
```

This regenerates the HTML, `sitemap.xml` and `robots.txt`. Commit the output.

## Deploying

GitHub Pages → *Deploy from branch* → `main` / root. No Actions workflow is needed.

To serve this repo on **growthbyadnan.site**, add a `CNAME` file containing `growthbyadnan.site` and set the custom domain in this repo's Pages settings. The domain is currently served by a different repository, so remove it there first. Leave DNS settings as they are.

## Assets to replace

- `assets/img/portrait-placeholder.svg` → a professional portrait (WebP, ~800×1000)
- Optional: real (client-approved) screenshots for each case study in `assets/img/cases/`
- Optional: a PDF resume file, if you want a direct download in addition to Print / Save PDF
