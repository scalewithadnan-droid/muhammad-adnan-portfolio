#!/usr/bin/env python3
"""
Static site generator for growthbyadnan.site.

All content lives in this file. Edit the DATA section, then run:
    python3 tools/build.py
It rewrites the .html files, sitemap.xml and robots.txt in the repo root.
Output is plain static HTML/CSS/JS — GitHub Pages serves it as-is. Nothing
here runs in the browser.
"""
import json, os, html as H
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://growthbyadnan.site"
TODAY = date.today().isoformat()

# ============================================================================
# DATA — sourced from the live site (growthbyadnan.site) and its resume page.
# ============================================================================
PERSON = {
    "name": "Adnan Afzal",
    "title": "Mobile Growth & Publishing Expert",
    "email": "adinrajpoot@gmail.com",
    "linkedin": "https://www.linkedin.com/in/adnan-afzal-growth",
    "linkedin_label": "linkedin.com/in/adnan-afzal-growth",
    # Calendly link from the previous version of this repository.
    "booking": "https://calendly.com/scalewithadnan/new-meeting",
    "location": "Pakistan · Working globally",
}

STATS = [  # value, prefix, suffix, label
    (200, "", "M+", "installs delivered"),
    (6, "", "+", "years in mobile growth"),
    (40, "+", "%", "organic installs (ASO)"),
    (10, "", "+", "markets optimised"),
]

EXPERIENCE = [
    {
        "role": "Marketing Team Lead", "company": "Void Games",
        "from": "Apr 2022", "to": "Present", "current": True,
        "summary": "Global UA, ASO, monetization, and live-ops strategy.",
        "points": [
            "Lead mobile growth initiatives across UA, ASO, monetization, analytics, and live operations.",
            "Scale user acquisition campaigns across global markets while optimizing ROAS and acquisition efficiency.",
            "Drive monetization improvements through ad mediation, pricing, and revenue optimization strategies.",
            "Collaborate with product, creative, and analytics teams to accelerate growth and profitability.",
        ],
    },
    {
        "role": "Product Growth Manager", "company": "JanBark Technologies",
        "from": "Aug 2021", "to": "Mar 2022",
        "summary": "Full-funnel acquisition, retention, and revenue growth.",
        "points": [
            "Managed acquisition, retention, and monetization strategies for multiple mobile applications.",
            "Improved marketing efficiency through attribution analysis, audience segmentation, and creative experimentation.",
            "Supported growth planning using cohort analysis and performance forecasting.",
        ],
    },
    {
        "role": "ASO Growth Specialist", "company": "Khastech Solutions",
        "from": "Sep 2020", "to": "Jul 2021",
        "summary": "Keyword strategy, creative experimentation, and market expansion.",
        "points": [
            "Developed ASO strategies including keyword optimization, localization, metadata management, and store conversion improvements.",
            "Conducted competitor research and market intelligence to identify growth opportunities.",
        ],
    },
    {
        "role": "ASO Specialist", "company": "Mobi Pixels",
        "from": "Mar 2020", "to": "Aug 2020",
        "summary": "Competitor research, store creative, and KPI tracking.",
        "points": [
            "Managed keyword research, store optimization, performance reporting, and competitive analysis for mobile applications.",
        ],
    },
]

PLATFORMS = [  # (group, [(name, monogram)])
    ("App Stores", [("Google Play Console", "GP"), ("App Store Connect", "AS")]),
    ("User Acquisition", [("Google Ads", "GA"), ("Meta Ads", "MA"), ("TikTok Ads", "TT"), ("Apple Search Ads", "SA"), ("Unity Ads", "UA")]),
    ("Monetization", [("Google AdMob", "AM"), ("AppLovin MAX", "MX"), ("Unity LevelPlay", "LP"), ("Mintegral", "MT"), ("Pangle", "PG")]),
    ("Attribution", [("Tenjin", "TJ"), ("Adjust", "AD"), ("AppsFlyer", "AF")]),
    ("Analytics", [("Firebase", "FB"), ("GA4", "G4"), ("GameAnalytics", "GN"), ("BigQuery", "BQ")]),
    ("ASO Intelligence", [("AppTweak", "AT"), ("Sensor Tower", "ST"), ("Mobile Action", "MA")]),
    ("Engagement & QA", [("OneSignal", "OS"), ("Firebase Cloud Messaging", "FC"), ("Remote Config", "RC"), ("Crashlytics", "CR")]),
]

CASES = [
    {
        "slug": "void-games-aso-ua",
        "company": "Void Games", "discipline": "ASO + UA",
        "cats": "games aso ua",
        "title": "Turned store conversion into a growth multiplier.",
        "summary": "Redesigned the ASO creative strategy and linked paid campaign signals with store performance to stop budget leakage.",
        "metrics": [("+35%", "Organic conversion"), ("−20%", "Cost per install")],
        "role": "Marketing Team Lead", "period": "2022 — Present", "platform": "Mobile games",
        "overview": "Void Games acquires players through both paid campaigns and organic store discovery. The engagement focused on the point where those two journeys meet — the store page — and on making paid and organic decisions from the same set of signals.",
        "challenge": "Paid campaigns were sending traffic to store pages whose creative had not been designed around what the ads promised. Every click that failed to convert on the store page was paid-for traffic lost, and that leakage showed up as a higher cost per install. Store creative and campaign creative were being managed as separate problems.",
        "strategy": [
            "Treat the store listing as the final step of every paid campaign, not a separate organic asset.",
            "Rebuild the ASO creative strategy so icon, screenshots and messaging match the strongest campaign angles.",
            "Use campaign signals — which creative themes win clicks — as input for store creative tests, and store conversion data as input for campaign decisions.",
        ],
        "execution": [
            "Audited the existing store creative against the ad creative driving the most spend.",
            "Redesigned the ASO creative set and tested variants through structured store experiments.",
            "Linked paid campaign reporting with store performance so conversion could be read by traffic source.",
            "Shifted budget away from traffic that was not converting on the store page.",
        ],
        "tools": ["Google Play Console", "App Store Connect", "Google Ads", "Meta Ads", "Firebase"],
        "contribution": "Led the ASO creative redesign and the integration of paid-campaign signals with store performance, as Marketing Team Lead responsible for UA and ASO.",
    },
    {
        "slug": "void-games-monetization",
        "company": "Void Games", "discipline": "Monetization",
        "cats": "games monetization",
        "title": "Unlocked revenue beyond install volume.",
        "summary": "Built a full-funnel monetization and live-ops testing framework across ad placements and in-app purchase tiers.",
        "metrics": [("+28%", "ARPDAU"), ("+15%", "Retention")],
        "role": "Marketing Team Lead", "period": "2022 — Present", "platform": "Mobile games",
        "overview": "Growth that depends only on install volume is fragile. This work focused on increasing the revenue each active player generates while protecting — and improving — retention.",
        "challenge": "Revenue decisions — ad placements, frequency and in-app purchase tiers — were not being tested in a structured way, and changes were hard to read against their effect on player retention. Without a framework, monetization changes risked trading long-term retention for short-term revenue.",
        "strategy": [
            "Design monetization as a full funnel, from first session through to repeat purchases and ad engagement.",
            "Test ad placements and IAP tiers together with live-ops changes, reading every test against retention as well as revenue.",
            "Optimise ad revenue through mediation rather than single-network decisions.",
        ],
        "execution": [
            "Built a testing framework covering ad placements and in-app purchase tiers.",
            "Aligned live-ops events with monetization tests so their effects could be measured.",
            "Optimised ad mediation and pricing as part of ongoing revenue work.",
            "Reviewed results on ARPDAU and retention together before rolling changes out.",
        ],
        "tools": ["Google AdMob", "AppLovin MAX", "Unity LevelPlay", "Firebase", "Remote Config"],
        "contribution": "Owned the monetization and live-ops testing framework as Marketing Team Lead, working with product, creative and analytics teams.",
    },
    {
        "slug": "janbark-uac",
        "company": "JanBark Technologies", "discipline": "UAC",
        "cats": "apps ua",
        "title": "Recovered ROAS while scaling three apps.",
        "summary": "Audited campaign structure, introduced phased scaling, and aligned budgets with stronger store performance signals.",
        "metrics": [("+12%", "ROAS recovery"), ("Stable", "CPI control")],
        "role": "Product Growth Manager", "period": "Aug 2021 — Mar 2022", "platform": "Mobile apps",
        "overview": "JanBark Technologies was running app campaigns across three apps. The goal was to scale spend without the return on ad spend falling apart as budgets grew.",
        "challenge": "As budgets increased, return on ad spend was slipping. Campaign structure made it hard to see which campaigns deserved more budget, and scaling too quickly risked pushing algorithms into lower-quality traffic.",
        "strategy": [
            "Audit campaign structure before adding budget.",
            "Scale in phases, so each step could be judged before the next one.",
            "Allocate budget towards apps and campaigns with stronger store performance signals.",
        ],
        "execution": [
            "Audited the structure of app campaigns across all three apps.",
            "Introduced a phased scaling plan in place of large one-off budget increases.",
            "Aligned budgets with store performance so spend followed conversion strength.",
            "Monitored CPI throughout to keep acquisition costs stable while scaling.",
        ],
        "tools": ["Google Ads (App campaigns)", "Firebase", "Google Play Console"],
        "contribution": "Ran the campaign audit and phased scaling plan as Product Growth Manager responsible for acquisition, retention and revenue.",
    },
    {
        "slug": "khastech-aso",
        "company": "Khastech Solutions", "discipline": "ASO",
        "cats": "aso",
        "title": "Rebuilt organic discovery across 10+ markets.",
        "summary": "Overhauled keyword architecture, metadata, icons, screenshots, and copy through structured experimentation.",
        "metrics": [("+40%", "Organic installs"), ("10+", "Markets improved")],
        "role": "ASO Growth Specialist", "period": "Sep 2020 — Jul 2021", "platform": "Google Play & App Store",
        "overview": "Organic discovery is the cheapest installs a mobile product can get — when the store presence is built for it. This project rebuilt that presence across more than ten markets.",
        "challenge": "Keyword coverage, metadata and store creative had not been built as a system, and localisation for international markets was limited. That capped how often the apps appeared in search and how well store visits converted.",
        "strategy": [
            "Rebuild keyword architecture from research rather than incremental edits.",
            "Localise metadata and creative per market instead of translating one listing.",
            "Change one thing at a time through structured experiments, so every improvement could be attributed.",
        ],
        "execution": [
            "Overhauled keyword architecture and metadata.",
            "Redesigned icons, screenshots and store copy.",
            "Ran structured store experiments to validate creative changes.",
            "Rolled improvements out market by market across 10+ markets.",
        ],
        "tools": ["Google Play Console", "App Store Connect", "AppTweak", "Sensor Tower", "Mobile Action"],
        "contribution": "Developed and executed the ASO strategy — keywords, localisation, metadata and store conversion — as ASO Growth Specialist.",
    },
]

CAT_LABELS = [("all", "All work"), ("games", "Mobile Games"), ("apps", "Mobile Apps"), ("ua", "User Acquisition"), ("aso", "ASO"), ("monetization", "Monetization")]

ARTICLES = [
    {
        "slug": "aso-ua-feedback-loop", "anchor": "aso-ua", "cat": "ASO & Store Growth", "catkey": "aso", "mins": 7,
        "title": "Why ASO and paid acquisition should share one feedback loop",
        "dek": "The most expensive growth leak often happens between the ad click and the store page.",
        "body": """
<p>Most mobile teams split growth into two lanes. One team buys traffic. Another team, or the same person on a different day, looks after the store listing. Both lanes report their own numbers, and both can look healthy while the business quietly overpays for every install.</p>
<p>The reason is simple: <strong>every paid install passes through the store page.</strong> A user sees an ad, taps it, lands on your listing, and then decides. If the listing doesn't continue the story the ad started, a share of the clicks you paid for never become installs. That cost doesn't show up as an ASO problem or a UA problem. It shows up as a cost per install that never seems to come down.</p>
<h3>Where the leak hides</h3>
<p>Ad platforms optimise towards the events you give them. If the store page converts poorly for a particular audience or creative angle, the platform sees fewer installs from that segment and adjusts — usually by finding cheaper, lower-intent traffic elsewhere. The campaign keeps spending, the dashboard keeps showing installs, and quality drifts down without a single obvious failure.</p>
<blockquote>The store page is the last step of every paid campaign. Treat it like one.</blockquote>
<h3>What a shared loop looks like</h3>
<ol>
<li><strong>Campaign creative informs store creative.</strong> The angles that win clicks in ads are evidence of what your audience responds to. Your first screenshots and icon should be tested against those same angles.</li>
<li><strong>Store conversion informs campaign decisions.</strong> Read store conversion by traffic source. A campaign that wins cheap clicks but converts poorly on the store page is not a cheap campaign.</li>
<li><strong>One owner for the hand-off.</strong> Someone needs to be accountable for the path from impression to install — not just for each half.</li>
</ol>
<h3>Practical starting points</h3>
<ul>
<li>Put your top three ad creatives next to your store listing. Does the listing deliver what the ads promise in the first two screenshots?</li>
<li>Use your store's native experiment tools to test creative that mirrors winning ad themes.</li>
<li>Add store conversion by source to the weekly UA review, so budget decisions see it.</li>
</ul>
<div class="callout"><strong>The takeaway</strong>ASO and UA are not two channels. They are two halves of the same conversion path, and they get cheaper when they share signals.</div>
""",
    },
    {
        "slug": "scale-without-losing-signal", "anchor": "scale", "cat": "User Acquisition", "catkey": "ua", "mins": 5,
        "title": "Scale spend without losing signal quality",
        "dek": "A practical framework for controlled campaign expansion.",
        "body": """
<p>Almost every app campaign looks good at a small budget. The real test is what happens when you try to spend more. Push too hard and return on ad spend falls, CPI jumps, and it becomes difficult to tell whether the campaign got worse or the market did.</p>
<p>Scaling well is less about finding a magic budget number and more about protecting the quality of the signal the platform is learning from.</p>
<h3>Why aggressive scaling breaks campaigns</h3>
<p>Automated bidding learns from conversion events. A large, sudden budget increase forces the system to find many more users quickly, and it will widen its targeting to do so. Without enough strong conversion signal, it reaches for cheaper, lower-intent users. Performance drops, and the team often reacts by changing several things at once — which resets learning again.</p>
<h3>A phased approach</h3>
<ol>
<li><strong>Audit structure first.</strong> Before adding budget, make sure campaigns are organised so you can see what's working: clear separation by goal, geography and creative set, and no campaigns competing for the same users.</li>
<li><strong>Scale in steps.</strong> Increase budgets in measured increments and give each step enough time and conversion volume to stabilise before judging it.</li>
<li><strong>Follow conversion strength.</strong> Move budget towards campaigns, apps and markets where the store page converts well. Spend amplifies whatever is already happening — make sure it's amplifying something good.</li>
<li><strong>Watch quality, not just volume.</strong> Track retention and revenue by cohort alongside CPI. An install that never comes back isn't growth.</li>
</ol>
<blockquote>Spend amplifies whatever is already happening. Make sure it's amplifying something good.</blockquote>
<h3>Signals to watch while scaling</h3>
<ul>
<li>Cohort ROAS against your payback target, not blended ROAS alone.</li>
<li>CPI trend relative to the step increase you made.</li>
<li>Early retention by campaign — the first warning sign of drifting quality.</li>
<li>Store conversion by source, to catch traffic that clicks but doesn't install.</li>
</ul>
<div class="callout"><strong>The takeaway</strong>Controlled steps, clean structure and quality metrics let you grow spend while keeping the platform learning from the right users.</div>
""",
    },
    {
        "slug": "metrics-for-growth-decisions", "anchor": "metrics", "cat": "Analytics & Attribution", "catkey": "analytics", "mins": 6,
        "title": "The metrics that make growth decisions clearer",
        "dek": "Move beyond dashboards toward decision-ready measurement.",
        "body": """
<p>Most mobile teams don't lack data. They have attribution dashboards, analytics events, ad revenue reports and store consoles. What they often lack is a short list of numbers that actually change decisions.</p>
<p>A useful metric answers a question someone is about to act on: where should the next dollar of budget go, which creative should we scale, which change should we roll back?</p>
<h3>Connect spend to value, not just installs</h3>
<p>Installs and CPI tell you what you paid. They don't tell you what you got. The core of decision-ready measurement is linking acquisition cost to what each cohort does afterwards.</p>
<ul>
<li><strong>Cohort ROAS</strong> by source, campaign and country — read at the days that matter for your payback window.</li>
<li><strong>Retention by cohort</strong> (D1, D7, D30) — the multiplier on every other number.</li>
<li><strong>ARPDAU and LTV curves</strong> — combining ad revenue and in-app purchases.</li>
<li><strong>Payback period</strong> — how long until a cohort returns what it cost.</li>
</ul>
<h3>Read every number in context</h3>
<p>A single blended number hides the decisions. Blended ROAS can look stable while one channel carries another that is losing money. Break metrics down to the level at which you actually make decisions — usually campaign, creative set and market.</p>
<blockquote>If a metric doesn't change a decision, it's decoration.</blockquote>
<h3>Build the view once</h3>
<ol>
<li>Agree on definitions — what counts as an install, a payer, a retained user — across attribution, analytics and revenue tools.</li>
<li>Join acquisition, behaviour and revenue data into one view instead of reconciling three dashboards every week.</li>
<li>Review the same small set of metrics on a fixed rhythm, and write down the decision each review produces.</li>
</ol>
<div class="callout"><strong>The takeaway</strong>Good measurement isn't more dashboards. It's a connected view of spend, behaviour, retention and revenue that makes the next decision obvious.</div>
""",
    },
]

# ============================================================================
# ICONS (original, 48×48 stroke)
# ============================================================================
ICONS = {
    "ua": '<path d="M6 40 L18 26 L26 32 L42 12"/><path d="M32 12 H42 V22"/><circle cx="18" cy="26" r="2.5"/><circle cx="26" cy="32" r="2.5"/>',
    "aso": '<rect x="14" y="4" width="20" height="40" rx="5"/><path d="M20 10 H28"/><rect x="19" y="16" width="10" height="10" rx="3"/><path d="M19 32 H29 M19 37 H25"/><circle cx="38" cy="16" r="5"/><path d="M41.5 19.5 L45 23"/>',
    "monetization": '<circle cx="24" cy="24" r="18"/><path d="M24 12 V36"/><path d="M30 17 H21.5 a4.5 4.5 0 0 0 0 9 h5 a4.5 4.5 0 0 1 0 9 H17"/>',
    "publishing": '<path d="M24 4 C32 10 34 20 30 30 H18 C14 20 16 10 24 4 Z"/><circle cx="24" cy="17" r="3.5"/><path d="M18 30 L12 36 L18 36 M30 30 L36 36 L30 36"/><path d="M21 36 V42 M27 36 V44 M24 36 V40"/>',
    "analytics": '<path d="M6 42 H42"/><rect x="9" y="26" width="6" height="12" rx="1.5"/><rect x="21" y="18" width="6" height="20" rx="1.5"/><rect x="33" y="8" width="6" height="30" rx="1.5"/><path d="M8 18 L22 10 L34 4" stroke-dasharray="2 3"/>',
    "strategy": '<circle cx="24" cy="24" r="18"/><circle cx="24" cy="24" r="10"/><circle cx="24" cy="24" r="2.5"/><path d="M24 2 V10 M24 38 V46 M2 24 H10 M38 24 H46"/>',
}

EXPERTISE = [
    ("ua", "User Acquisition", "Structured campaigns built around sustainable ROAS, not vanity installs.", ["Google App Campaigns", "Meta Ads", "TikTok Ads", "Apple Search Ads", "Unity Ads", "Creative testing"]),
    ("aso", "App Store Optimization", "Keyword intelligence, high-converting creative, metadata, and global market positioning.", ["Keyword research", "Store creative", "Localisation", "Store experiments", "Competitor intel"]),
    ("monetization", "Ad Monetization", "Revenue frameworks grounded in cohort behaviour, placement testing, and live ops.", ["AdMob", "AppLovin MAX", "Mediation & bidding", "IAP tiers", "Placement tests"]),
    ("publishing", "Mobile Publishing", "Bringing acquisition, store, monetization and live-ops together into one global growth plan.", ["Go-to-market", "Live-ops", "Market expansion", "Cross-team delivery"]),
    ("analytics", "Growth Analytics", "Full-funnel measurement that connects spend, behaviour, retention, and revenue.", ["AppsFlyer", "Adjust", "Tenjin", "Firebase", "GA4", "Cohort analysis"]),
    ("strategy", "Growth Strategy", "A connected growth system — not isolated tactics — with clear priorities and decision-ready numbers.", ["Full-funnel planning", "Budget allocation", "Forecasting", "ROAS targets"]),
]

GOS_STAGES = [("acquisition", "Acquisition"), ("conversion", "Store Conversion"), ("activation", "Activation"), ("retention", "Retention"), ("monetization", "Monetization"), ("optimization", "Optimization")]

# ============================================================================
# TEMPLATE HELPERS
# ============================================================================
e = H.escape
ARROW = '<svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M1 13 L13 1 M4 1 H13 V10" stroke="currentColor" stroke-width="1.6"/></svg>'
ARROW_R = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M1 8 H15 M9 2 L15 8 L9 14" stroke="currentColor" stroke-width="1.6"/></svg>'

HEAD_JS = "document.documentElement.classList.add('js');if(!window.matchMedia('(prefers-reduced-motion: reduce)').matches)document.documentElement.classList.add('motion');setTimeout(function(){document.documentElement.classList.add('ready-fallback')},4000);"


def icon(k, cls="xicon"):
    return f'<svg class="{cls}" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[k]}</svg>'


def person_ld():
    return {
        "@context": "https://schema.org", "@type": "Person",
        "name": PERSON["name"], "jobTitle": PERSON["title"],
        "url": SITE + "/", "email": "mailto:" + PERSON["email"],
        "image": SITE + "/assets/img/og-image.png",
        "sameAs": [PERSON["linkedin"]],
        "address": {"@type": "PostalAddress", "addressCountry": "PK"},
        "worksFor": {"@type": "Organization", "name": "Void Games"},
        "knowsAbout": ["Mobile Growth", "User Acquisition", "App Store Optimization", "Ad Monetization", "Mobile Game Publishing", "Mobile Analytics", "ROAS Optimization"],
    }


def head(title, desc, path, rel, ld=None, og_type="website"):
    url = SITE + "/" + path.replace("index.html", "")
    lds = [ld] if isinstance(ld, dict) else (ld or [])
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in lds)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="author" content="{PERSON['name']}">
<meta name="theme-color" content="#090B0F">
<meta name="color-scheme" content="dark">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{PERSON['name']} — Mobile Growth">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{SITE}/assets/img/og-image.png">
<link rel="icon" href="{rel}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{rel}apple-touch-icon.png">
<link rel="preload" href="{rel}assets/fonts/manrope-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{rel}assets/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{rel}assets/css/main.css">
<script>{HEAD_JS}</script>
{ld_html}</head>
'''


def nav(rel, current=""):
    home = rel or "./"
    items = [("Home", home, "home"), ("About", f"{home}#about", "about"), ("Expertise", f"{home}#expertise", "expertise"),
             ("Case Studies", f"{rel}case-studies/", "work"), ("Experience", f"{rel}resume.html", "experience"),
             ("Insights", f"{rel}blog.html", "insights"), ("Contact", f"{home}#contact", "contact")]
    if not rel:  # homepage: in-page anchors for section highlighting
        items = [("Home", "#top", "home"), ("About", "#about", "about"), ("Expertise", "#expertise", "expertise"),
                 ("Case Studies", "#work", "work"), ("Experience", "#experience", "experience"),
                 ("Insights", "#insights", "insights"), ("Contact", "#contact", "contact")]
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if k == current else ""}>{t}</a>' for t, h, k in items)
    mlinks = "".join(f'<li><a href="{h}">{t}</a></li>' for t, h, k in items)
    contact = "#contact" if not rel else f"{home}#contact"
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="ptrans" aria-hidden="true"></div>
<header class="nav" id="top">
  <div class="wrap nav__in">
    <a class="logo" href="{home if rel else '#top'}" ><span class="logo__mark" aria-hidden="true">AA</span><span>Adnan Afzal</span></a>
    <nav class="nav__links" aria-label="Primary">{links}</nav>
    <div class="nav__cta">
      <a class="btn btn--primary btn--sm" href="{contact}">Let’s talk growth <span class="arrow">{ARROW}</span></a>
      <button class="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mmenu"><span></span><span></span></button>
    </div>
  </div>
  <div class="nav__progress" aria-hidden="true"></div>
</header>
<div class="mmenu" id="mmenu" aria-hidden="true">
  <nav aria-label="Mobile"><ol>{mlinks}</ol></nav>
  <div class="mmenu__foot">
    <a class="btn btn--primary" href="{contact}">Let’s talk growth <span class="arrow">{ARROW}</span></a>
    <a href="mailto:{PERSON['email']}">{PERSON['email']}</a>
  </div>
</div>
'''


def footer(rel):
    home = rel or "./"
    return f'''<footer class="footer">
  <div class="wrap">
    <div class="footer__top">
      <div>
        <a class="logo" href="{home}"><span class="logo__mark" aria-hidden="true">AA</span><span>Adnan Afzal</span></a>
        <p class="footer__tag">Mobile growth systems for apps and games — acquisition, store conversion, monetization and analytics working as one.</p>
      </div>
      <div><h4>Explore</h4><ul>
        <li><a href="{home}#about">About</a></li><li><a href="{home}#expertise">Expertise</a></li>
        <li><a href="{rel}case-studies/">Case studies</a></li><li><a href="{rel}blog.html">Insights</a></li></ul></div>
      <div><h4>Profile</h4><ul>
        <li><a href="{rel}resume.html">Resume</a></li><li><a href="{home}#experience">Experience</a></li>
        <li><a href="{home}#platforms">Platforms</a></li></ul></div>
      <div><h4>Contact</h4><ul>
        <li><a href="mailto:{PERSON['email']}">Email</a></li>
        <li><a href="{PERSON['linkedin']}" target="_blank" rel="noopener">LinkedIn ↗</a></li>
        <li><a href="{PERSON['booking']}" target="_blank" rel="noopener">Book a call ↗</a></li></ul></div>
    </div>
    <div class="footer__word" aria-hidden="true" data-word="GROWTH SYSTEMS"></div>
    <div class="footer__bottom"><span>© <span data-year>2026</span> {PERSON['name']}. All rights reserved.</span><span>{PERSON['location']}</span></div>
  </div>
</footer>
<script src="{rel}assets/js/vendor/gsap.min.js" defer></script>
<script src="{rel}assets/js/vendor/ScrollTrigger.min.js" defer></script>
<script src="{rel}assets/js/main.js" defer></script>
</body>
</html>
'''


def lines(parts):
    return "".join(f'<span class="line"><span>{p}</span></span>' for p in parts)


def case_card(c, i, rel):
    m = "".join(f'<div class="metric"><div class="metric__v">{v}</div><div class="metric__l">{l}</div></div>' for v, l in c["metrics"])
    return f'''<article class="case" data-cats="{c['cats']}" data-cursor="View">
  <div class="case__media"><span class="case__idx">{i:02d}</span><img src="{rel}assets/img/cases/{c['slug']}.svg" alt="Illustration for the {e(c['company'])} {e(c['discipline'])} case study" width="1600" height="1000" loading="lazy" decoding="async"></div>
  <div class="case__body">
    <div class="case__client">{e(c['company'])} · {e(c['discipline'])}</div>
    <h3><a class="case__stretch" href="{rel}case-studies/{c['slug']}.html">{e(c['title'])}</a></h3>
    <p class="case__summary">{e(c['summary'])}</p>
    <div class="case__metrics">{m}</div>
    <div class="case__link" aria-hidden="true"><span>Read case study</span><span class="circ">{ARROW}</span></div>
  </div>
</article>'''


def filters():
    out = '<div class="filters" role="group" aria-label="Filter case studies">'
    for k, lab in CAT_LABELS:
        out += f'<button type="button" class="filter" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{lab}<span class="filter__count"></span></button>'
    return out + '</div><p class="sr-only" aria-live="polite" data-filter-live></p>'


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(content)


# ============================================================================
# HOMEPAGE
# ============================================================================
HERO_SVG = '''<svg viewBox="0 0 560 620" role="img" aria-labelledby="hv-t" data-hero="visual">
<title id="hv-t">Illustrative mobile growth dashboard connecting acquisition, store, and monetization views</title>
<defs>
  <linearGradient id="hvA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D9FF43" stop-opacity=".28"/><stop offset="1" stop-color="#D9FF43" stop-opacity="0"/></linearGradient>
  <linearGradient id="hvP" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1B212B"/><stop offset="1" stop-color="#11151B"/></linearGradient>
</defs>
<!-- main dashboard -->
<rect x="10" y="40" width="440" height="330" rx="22" fill="#151A22" stroke="#252B35"/>
<circle cx="36" cy="66" r="4.5" fill="#252B35"/><circle cx="52" cy="66" r="4.5" fill="#252B35"/><circle cx="68" cy="66" r="4.5" fill="#252B35"/>
<text x="36" y="108" font-family="Manrope, Inter, sans-serif" font-weight="800" font-size="20" fill="#F4F5F6" letter-spacing="-.5">Growth overview</text>
<text x="36" y="130" font-family="Inter, sans-serif" font-size="11.5" fill="#929BA8">Acquisition · Store · Revenue</text>
<rect x="292" y="92" width="44" height="24" rx="12" fill="#D9FF43"/><text x="314" y="108" text-anchor="middle" font-family="Inter, sans-serif" font-weight="700" font-size="10.5" fill="#0D1200">UA</text>
<rect x="342" y="92" width="44" height="24" rx="12" fill="none" stroke="#252B35"/><text x="364" y="108" text-anchor="middle" font-family="Inter, sans-serif" font-weight="600" font-size="10.5" fill="#929BA8">ASO</text>
<rect x="392" y="92" width="40" height="24" rx="12" fill="none" stroke="#252B35"/><text x="412" y="108" text-anchor="middle" font-family="Inter, sans-serif" font-weight="600" font-size="10.5" fill="#929BA8">LTV</text>
<g stroke="#252B35" stroke-dasharray="2 6"><path d="M36 190 H430"/><path d="M36 240 H430"/><path d="M36 290 H430"/></g>
<path d="M36 320 C 90 312, 120 300, 160 284 S 230 262, 270 240 S 350 196, 430 160 V 336 H 36 Z" fill="url(#hvA)"/>
<path class="hv-line" d="M36 320 C 90 312, 120 300, 160 284 S 230 262, 270 240 S 350 196, 430 160" fill="none" stroke="#D9FF43" stroke-width="3" stroke-linecap="round"/>
<path class="hv-line" d="M36 326 C 110 322, 180 312, 250 300 S 360 280, 430 262" fill="none" stroke="#929BA8" stroke-width="1.6" stroke-dasharray="3 6" opacity=".6"/>
<circle cx="430" cy="160" r="6" fill="#D9FF43"/><circle class="pulse" cx="430" cy="160" r="13" fill="none" stroke="#D9FF43"/>
<g font-family="Inter, sans-serif" font-size="10" fill="#929BA8"><text x="36" y="356">D0</text><text x="150" y="356">D7</text><text x="270" y="356">D14</text><text x="410" y="356">D30</text></g>
<!-- monetization mix card -->
<rect x="10" y="390" width="230" height="200" rx="22" fill="#151A22" stroke="#252B35"/>
<text x="32" y="426" font-family="Inter, sans-serif" font-weight="600" font-size="10.5" fill="#929BA8" letter-spacing="1.6">MONETIZATION MIX</text>
<g transform="translate(86 512) rotate(-90)">
  <circle r="46" fill="none" stroke="#252B35" stroke-width="14"/>
  <circle class="hv-line" r="46" fill="none" stroke="#D9FF43" stroke-width="14" stroke-dasharray="120 300"/>
  <circle r="46" fill="none" stroke="#F4F5F6" stroke-opacity=".8" stroke-width="14" stroke-dasharray="70 300" stroke-dashoffset="-124"/>
  <circle r="46" fill="none" stroke="#929BA8" stroke-width="14" stroke-dasharray="50 300" stroke-dashoffset="-198"/>
</g>
<g font-family="Inter, sans-serif" font-size="11" fill="#F4F5F6">
  <rect x="152" y="470" width="9" height="9" rx="2" fill="#D9FF43"/><text x="168" y="479">Rewarded</text>
  <rect x="152" y="496" width="9" height="9" rx="2" fill="#F4F5F6" fill-opacity=".8"/><text x="168" y="505">IAP</text>
  <rect x="152" y="522" width="9" height="9" rx="2" fill="#929BA8"/><text x="168" y="531">Interstitial</text>
</g>
<!-- bars card -->
<rect x="256" y="390" width="120" height="200" rx="22" fill="#151A22" stroke="#252B35"/>
<text x="274" y="426" font-family="Inter, sans-serif" font-weight="600" font-size="10.5" fill="#929BA8" letter-spacing="1.6">COHORTS</text>
<g>
  <rect class="hv-bar" x="274" y="500" width="12" height="70" rx="3" fill="#252B35"/>
  <rect class="hv-bar" x="292" y="486" width="12" height="84" rx="3" fill="#252B35"/>
  <rect class="hv-bar" x="310" y="470" width="12" height="100" rx="3" fill="#3A414D"/>
  <rect class="hv-bar" x="328" y="456" width="12" height="114" rx="3" fill="#D9FF43" fill-opacity=".7"/>
  <rect class="hv-bar" x="346" y="440" width="12" height="130" rx="3" fill="#D9FF43"/>
</g>
<!-- phone -->
<g transform="translate(372 196)">
  <rect width="178" height="356" rx="30" fill="url(#hvP)" stroke="#2E3541" stroke-width="1.5"/>
  <rect x="8" y="8" width="162" height="340" rx="23" fill="#0E1116"/>
  <rect x="64" y="16" width="50" height="13" rx="6.5" fill="#090B0F"/>
  <rect x="22" y="44" width="46" height="46" rx="12" fill="#D9FF43"/>
  <path d="M33 78 L45 54 L57 78 Z" fill="none" stroke="#090B0F" stroke-width="4" stroke-linejoin="round"/>
  <rect x="78" y="50" width="70" height="9" rx="4.5" fill="#F4F5F6" opacity=".9"/>
  <rect x="78" y="66" width="48" height="7" rx="3.5" fill="#929BA8" opacity=".6"/>
  <rect x="78" y="78" width="40" height="13" rx="6.5" fill="#D9FF43"/>
  <rect x="22" y="104" width="40" height="84" rx="8" fill="#151A22" stroke="#252B35"/>
  <rect x="68" y="104" width="40" height="84" rx="8" fill="#151A22" stroke="#252B35"/>
  <rect x="114" y="104" width="40" height="84" rx="8" fill="#151A22" stroke="#252B35"/>
  <circle cx="42" cy="146" r="11" fill="none" stroke="#D9FF43" stroke-width="2"/>
  <path d="M80 160 L88 140 L96 152" fill="none" stroke="#D9FF43" stroke-width="2"/>
  <rect x="124" y="134" width="20" height="24" rx="3" fill="none" stroke="#D9FF43" stroke-width="2"/>
  <rect x="22" y="204" width="132" height="6" rx="3" fill="#929BA8" opacity=".35"/>
  <rect x="22" y="218" width="112" height="6" rx="3" fill="#929BA8" opacity=".35"/>
  <rect x="22" y="232" width="122" height="6" rx="3" fill="#929BA8" opacity=".35"/>
  <rect x="22" y="258" width="132" height="64" rx="12" fill="#151A22" stroke="#252B35"/>
  <text x="34" y="280" font-family="Inter, sans-serif" font-size="8.5" font-weight="600" fill="#929BA8" letter-spacing="1">STORE TEST</text>
  <rect x="34" y="290" width="108" height="7" rx="3.5" fill="#252B35"/><rect x="34" y="290" width="62" height="7" rx="3.5" fill="#929BA8"/>
  <rect x="34" y="304" width="108" height="7" rx="3.5" fill="#252B35"/><rect x="34" y="304" width="88" height="7" rx="3.5" fill="#D9FF43"/>
</g>
<!-- data connections -->
<path class="flow-dash" d="M240 490 C 250 470, 250 420, 256 420" fill="none" stroke="#D9FF43" stroke-opacity=".6" stroke-width="1.5"/>
<path class="flow-dash" d="M430 160 C 470 160, 470 190, 470 196" fill="none" stroke="#D9FF43" stroke-opacity=".6" stroke-width="1.5"/>
<circle class="pulse" cx="470" cy="196" r="4" fill="#D9FF43"/>
<circle class="pulse" cx="256" cy="420" r="4" fill="#D9FF43"/>
</svg>'''


def gos_svg():
    cx, cy, rx, ry = 360, 280, 262, 200
    import math
    pts = []
    for i in range(6):
        a = math.radians(-90 + i * 60)
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    nodes = ""
    for i, ((key, lab), (x, y)) in enumerate(zip(GOS_STAGES, pts)):
        w = 214
        active = " is-active" if i == 0 else ""
        nodes += f'''<g class="gos__node{active}" data-stage="{key}" tabindex="0" role="button" aria-pressed="{"true" if i == 0 else "false"}" aria-label="Stage {i+1}: {lab}">
  <rect class="n-bg" x="{x-w/2:.1f}" y="{y-30:.1f}" width="{w}" height="60" rx="30" fill="#151A22" stroke="#252B35"/>
  <text x="{x-w/2+26:.1f}" y="{y+5:.1f}" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#929BA8">0{i+1}</text>
  <text x="{x-w/2+54:.1f}" y="{y+6:.1f}" font-family="Manrope, Inter, sans-serif" font-size="17" font-weight="800" fill="#F4F5F6" letter-spacing="-.3">{lab}</text>
</g>'''
    return f'''<svg class="gos__svg" viewBox="0 0 720 560" role="group" aria-label="Growth operating system: six connected stages">
<defs><marker id="arr" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#D9FF43"/></marker></defs>
<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#252B35" stroke-width="1"/>
<path class="gos__path" d="M {cx} {cy-ry} A {rx} {ry} 0 1 1 {cx-1} {cy-ry}" fill="none" stroke="#D9FF43" stroke-width="2"/>
<ellipse class="flow-dash" cx="{cx}" cy="{cy}" rx="{rx-60}" ry="{ry-56}" fill="none" stroke="#3A414D"/>
<text x="{cx}" y="{cy-10}" text-anchor="middle" font-family="Manrope, Inter, sans-serif" font-size="30" font-weight="800" fill="#F4F5F6" letter-spacing="-1">Growth OS</text>
<text x="{cx}" y="{cy+20}" text-anchor="middle" font-family="Inter, sans-serif" font-size="12" fill="#929BA8" letter-spacing="2">EVERY STAGE FEEDS THE NEXT</text>
{nodes}
</svg>'''


def gos_list():
    out = '<div class="gos__list" role="group" aria-label="Growth stages">'
    for i, (k, lab) in enumerate(GOS_STAGES):
        out += f'<button type="button" class="gos__node{" is-active" if i == 0 else ""}" data-stage="{k}" aria-pressed="{"true" if i == 0 else "false"}"><span>0{i+1}</span>{lab}</button>'
    return out + "</div>"


def build_home():
    rel = ""
    stats = "".join(
        f'<div class="stat"><div class="stat__num" data-count="{v}">{p}<span class="n">{v}</span><span class="accent">{s}</span></div><div class="stat__label">{l}</div></div>'
        for v, p, s, l in STATS)
    xcards = "".join(
        f'''<article class="xcard" data-reveal><div class="xcard__top"><span class="xcard__n">0{i+1}</span>{icon(k)}</div>
<h3>{t}</h3><p>{d}</p><ul>{"".join(f"<li>{x}</li>" for x in caps)}</ul></article>'''
        for i, (k, t, d, caps) in enumerate(EXPERTISE))
    cases = "".join(case_card(c, i + 1, rel) for i, c in enumerate(CASES))
    pgroups = "".join(
        f'<div class="pgroup" data-reveal><div class="pgroup__name"><span>0{i+1}</span>{g}</div><div class="pgroup__items">'
        + "".join(f'<div class="ptile"><span class="ptile__mono" aria-hidden="true">{m}</span>{n}</div>' for n, m in items)
        + "</div></div>"
        for i, (g, items) in enumerate(PLATFORMS))
    jobs = "".join(
        f'''<article class="job" data-reveal>
  <div class="job__when">{j["from"]} — {j["to"]}{'<br><span class="now">Current</span>' if j.get("current") else ""}</div>
  <div><h3>{j["role"]}</h3><div class="job__co">{j["company"]}</div></div>
  <ul>{"".join(f"<li>{p}</li>" for p in j["points"])}</ul>
</article>''' for j in EXPERIENCE)
    insights = "".join(
        f'''<a class="icard" href="insights/{a["slug"]}.html" data-reveal>
  <div class="icard__meta"><span class="cat">{a["cat"]}</span><span>{a["mins"]} min read</span></div>
  <h3>{e(a["title"])}</h3><p>{e(a["dek"])}</p>
  <span class="icard__more">Read article <span>{ARROW_R}</span></span>
</a>''' for a in ARTICLES)
    marquee_words = ["User Acquisition", "App Store Optimization", "Ad Monetization", "Mobile Publishing", "Growth Analytics", "ROAS Optimization", "Live-ops"]
    mq = "".join(f'<span class="marquee__item">{w}</span>' for w in marquee_words)

    ld = [person_ld(), {"@context": "https://schema.org", "@type": "WebSite", "name": "Adnan Afzal — Mobile Growth", "url": SITE + "/"}]
    page = head("Adnan Afzal — Mobile Growth & Publishing Expert for Apps & Games",
                "Adnan Afzal builds growth systems for mobile apps and games — user acquisition, ASO, ad monetization, analytics and publishing. 200M+ installs delivered.",
                "index.html", rel, ld)
    page += '<body>\n' + nav(rel, "home")
    page += f'''<main id="main">
<section class="hero" aria-labelledby="hero-title">
  <div class="hero__grid-bg" aria-hidden="true"></div><div class="hero__glow" aria-hidden="true"></div>
  <div class="wrap">
    <div class="hero__layout">
      <div>
        <span class="eyebrow" data-hero="eyebrow">Mobile Growth &amp; Publishing Expert</span>
        <h1 id="hero-title" data-hero="h1">{lines(["I build growth", "systems for", '<span class="accent">mobile apps</span>', '<span class="accent">&amp; games.</span>'])}</h1>
        <p class="hero__lead" data-hero="fade">Connecting user acquisition, app store optimization, monetization, analytics, and publishing to build scalable mobile businesses.</p>
        <div class="hero__ctas" data-hero="fade">
          <a class="btn btn--primary" href="#contact">Discuss your project <span class="arrow">{ARROW}</span></a>
          <a class="btn btn--ghost" href="#work">Explore my work <span class="arrow">{ARROW}</span></a>
        </div>
      </div>
      <div class="hero__visual">
        {HERO_SVG}
        <div class="hv-float" data-depth="1.4" style="left:-4%;top:2%"><div class="chip"><span class="chip__dot">{icon("ua", "")}</span><div><strong>200M+</strong><small>installs delivered</small></div></div></div>
        <div class="hv-float" data-depth="-1" style="right:-2%;top:22%"><div class="chip"><div><strong class="accent">+35%</strong><small>organic conversion · Void Games</small></div></div></div>
        <div class="hv-float" data-depth="0.8" style="left:30%;bottom:-2%"><div class="chip"><span class="chip__dot">{icon("strategy", "")}</span><div><strong>ROAS-led</strong><small>growth strategy</small></div></div></div>
      </div>
    </div>
    <div class="hero__meta" data-hero="fade">{stats}</div>
  </div>
  <div class="scroll-cue" aria-hidden="true"><span class="scroll-cue__bar"></span>Scroll to explore</div>
</section>

<div class="marquee" aria-hidden="true"><div class="marquee__track">{mq}</div><div class="marquee__track">{mq}</div></div>

<section class="section" id="about" aria-labelledby="about-title">
  <div class="wrap about">
    <div>
      <div class="portrait" data-clip>
        <img src="assets/img/portrait-placeholder.svg" alt="Portrait placeholder for Adnan Afzal" width="800" height="1000" loading="lazy" decoding="async">
      </div>
    </div>
    <div>
      <span class="eyebrow">01 — About</span>
      <h2 id="about-title" class="about__statement" data-scrub-words>I fix the systems behind the numbers. Growth should be understandable, measurable, and built to last.</h2>
      <div class="about__body" data-reveal>
        <p>I’m Adnan Afzal, a mobile growth specialist based in Pakistan and working with teams globally. Over the past six years I’ve helped mobile products move from early traction to more than <strong class="accent">200 million installs</strong> across global markets.</p>
        <p>My work connects acquisition, store conversion, retention and revenue into one decision-ready picture — so paid growth, organic discovery and monetization stop competing and start compounding.</p>
      </div>
      <div class="principles">
        <div class="principle" data-reveal><div class="principle__n">01</div><h3>Straight insight</h3><p>No inflated reports or artificial complexity. You hear what the data actually says.</p></div>
        <div class="principle" data-reveal><div class="principle__n">02</div><h3>Systems thinking</h3><p>Paid growth, organic discovery and monetization work better when they share signals.</p></div>
        <div class="principle" data-reveal><div class="principle__n">03</div><h3>Commercial focus</h3><p>Sustainable ROAS and payback over vanity installs.</p></div>
        <div class="principle" data-reveal><div class="principle__n">04</div><h3>Experiment-led</h3><p>Structured tests, one variable at a time, so every win can be explained.</p></div>
      </div>
      <div class="tags" data-reveal>{"".join(f'<span class="tag">{t}</span>' for t in ["Mobile Games", "Mobile Apps", "User Acquisition", "ASO", "Monetization", "Analytics", "Performance Marketing"])}</div>
      <div class="about__actions" data-reveal>
        <a class="btn btn--primary" href="resume.html">View resume <span class="arrow">{ARROW}</span></a>
        <a class="btn btn--ghost" href="{PERSON['linkedin']}" target="_blank" rel="noopener">LinkedIn <span class="arrow">{ARROW}</span></a>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt" id="expertise" aria-labelledby="exp-title">
  <div class="wrap">
    <div class="sec-head">
      <div><span class="eyebrow">02 — Expertise</span><h2 id="exp-title" data-split>Built for scalable app growth.</h2></div>
      <p data-reveal>Strategy and execution across the complete mobile growth loop — from the first impression to the last dollar of lifetime value.</p>
    </div>
    <div class="xgrid">{xcards}</div>
  </div>
</section>

<section class="section" id="system" aria-labelledby="gos-title">
  <div class="wrap">
    <div class="sec-head">
      <div><span class="eyebrow">03 — My Growth Operating System</span><h2 id="gos-title" data-split>One loop. Six stages. Compounding results.</h2></div>
      <p data-reveal>Isolated tactics plateau. A connected system lets every stage feed the next — select a stage to see how it contributes.</p>
    </div>
    <div class="gos">
      <div>{gos_svg()}{gos_list()}</div>
      <div class="gos__panel" aria-live="polite">
        <div class="gos__step">STAGE 01 / 06</div>
        <h3>Acquisition</h3>
        <p>Buy and earn the right users, not just the cheapest installs. Campaign structure, bidding and creative are judged on downstream value — retention and revenue — so spend scales without diluting quality.</p>
        <dl><div><dt>Levers</dt><dd data-lever>Campaign structure, bid strategy, creative testing, channel mix</dd></div>
        <div><dt>Signals I watch</dt><dd data-signal>CPI, install-to-D1 quality, cohort ROAS</dd></div></dl>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt" id="work" aria-labelledby="work-title" data-filter-scope>
  <div class="wrap">
    <div class="sec-head">
      <div><span class="eyebrow">04 — Case Studies</span><h2 id="work-title" data-split>Outcomes, not activity.</h2></div>
      <p data-reveal>Selected results from app and game growth engagements. Every number shown comes from the work itself.</p>
    </div>
    {filters()}
  </div>
  <div class="hscroll" data-pin>
    <div class="wrap"><div class="hscroll__track">{cases}</div><div class="hs-progress" aria-hidden="true"><span></span></div></div>
  </div>
  <div class="wrap" style="margin-top:40px"><a class="link-u" href="case-studies/">All case studies {ARROW_R}</a></div>
</section>

<section class="section" id="platforms" aria-labelledby="plat-title">
  <div class="wrap">
    <div class="sec-head">
      <div><span class="eyebrow">05 — Platforms &amp; Technology</span><h2 id="plat-title" data-split>The stack behind the system.</h2></div>
      <p data-reveal>Hands-on experience across stores, ad networks, mediation, attribution and analytics.</p>
    </div>
    <div class="pgroups">{pgroups}</div>
    <p class="pnote">Tools used in professional work. Names and trademarks belong to their owners; no partnership or certification is implied.</p>
  </div>
</section>

<section class="section section--alt" id="experience" aria-labelledby="xp-title">
  <div class="wrap">
    <div class="sec-head">
      <div><span class="eyebrow">06 — Experience</span><h2 id="xp-title" data-split>From store visibility to global growth.</h2></div>
      <p data-reveal>Six years moving from ASO specialist to leading UA, ASO, monetization and live-ops for a games studio. <a class="link-u accent" href="resume.html">Full resume {ARROW_R}</a></p>
    </div>
    <div class="timeline"><div class="timeline__rail" aria-hidden="true"><div class="timeline__fill"></div></div>{jobs}</div>
  </div>
</section>

<section class="section" id="insights" aria-labelledby="ins-title">
  <div class="wrap">
    <div class="sec-head">
      <div><span class="eyebrow">07 — Growth Intelligence</span><h2 id="ins-title" data-split>Notes from the growth loop.</h2></div>
      <p data-reveal>Practical field notes on acquisition, store performance, monetization and the systems connecting them. <a class="link-u accent" href="blog.html">All articles {ARROW_R}</a></p>
    </div>
    <div class="igrid">{insights}</div>
  </div>
</section>

{contact_block(rel)}
</main>
'''
    page += footer(rel)
    write("index.html", page)


def contact_block(rel):
    return f'''<section class="section contact section--alt" id="contact" aria-labelledby="contact-title">
  <div class="wrap">
    <span class="eyebrow">08 — Contact</span>
    <h2 id="contact-title" class="contact__big" style="margin-top:24px" data-split>Have a mobile product ready to scale?</h2>
    <p class="contact__lead" data-reveal>Let’s discuss your product, growth opportunities, and the strategy behind sustainable mobile success.</p>
    <div class="contact__grid">
      <div class="cmethods" data-reveal>
        <a class="cmethod" href="mailto:{PERSON['email']}"><div><div class="cmethod__k">Email</div><div class="cmethod__v">{PERSON['email']}</div></div><span class="circ">{ARROW}</span></a>
        <a class="cmethod" href="{PERSON['booking']}" target="_blank" rel="noopener"><div><div class="cmethod__k">Consultation</div><div class="cmethod__v">Book a call</div></div><span class="circ">{ARROW}</span></a>
        <a class="cmethod" href="{PERSON['linkedin']}" target="_blank" rel="noopener"><div><div class="cmethod__k">LinkedIn</div><div class="cmethod__v">{PERSON['linkedin_label']}</div></div><span class="circ">{ARROW}</span></a>
        <a class="cmethod" href="{rel}resume.html"><div><div class="cmethod__k">Resume</div><div class="cmethod__v">View / save as PDF</div></div><span class="circ">{ARROW}</span></a>
      </div>
      <form class="form" id="brief" data-to="{PERSON['email']}" novalidate data-reveal>
        <h3>Send a consultation brief</h3>
        <p>Your message opens in your own email app, pre-filled. No account, tracking, or third-party form service.</p>
        <div class="frow">
          <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" autocomplete="name" required></div>
          <div class="field"><label for="f-email">Your email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
        </div>
        <div class="frow">
          <div class="field"><label for="f-type">Consultation type</label>
            <select id="f-type" name="type" required><option value="">Choose a consultation</option><option>ASO Consultation</option><option>UAC &amp; Paid Growth</option><option>Monetization Review</option><option>Overall Growth Audit</option></select></div>
          <div class="field"><label for="f-link">App or game link</label><input id="f-link" name="link" type="url" inputmode="url" placeholder="https://play.google.com/…"></div>
        </div>
        <div class="field"><label for="f-msg">What would you like to solve?</label><textarea id="f-msg" name="message" required></textarea></div>
        <div class="form__foot">
          <p class="form__note">This opens a pre-filled email to Adnan. Nothing is sent until you press send.</p>
          <button class="btn btn--primary" type="submit">Prepare email <span class="arrow">{ARROW}</span></button>
        </div>
        <p class="form__status" role="status"></p>
      </form>
    </div>
  </div>
</section>'''


# ============================================================================
# CASE STUDY PAGES
# ============================================================================
def build_cases():
    rel = "../"
    # index
    cards = "".join(case_card(c, i + 1, rel) for i, c in enumerate(CASES))
    page = head("Case Studies — Adnan Afzal | Mobile Growth", "Mobile growth case studies: ASO, user acquisition, app campaigns and monetization for mobile games and apps.", "case-studies/", rel,
                {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Case studies", "url": SITE + "/case-studies/"})
    page += "<body>\n" + nav(rel, "work")
    page += f'''<main id="main">
<section class="phero"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb" data-hero="eyebrow"><a href="../">Home</a><span aria-hidden="true">/</span><span>Case studies</span></nav>
  <h1 data-hero="h1">{lines(["Outcomes,", '<span class="accent">not activity.</span>'])}</h1>
  <p class="phero__lead" data-hero="fade">Selected engagements across mobile games and apps — acquisition, store conversion and monetization.</p>
</div></section>
<section class="section--tight" data-filter-scope style="padding-top:0"><div class="wrap">
  {filters()}
  <div class="hscroll"><div class="hscroll__track">{cards}</div></div>
</div></section>
<section class="section--tight"><div class="wrap"><div class="cta-band" data-reveal><h2>Want results like these?</h2><a class="btn btn--primary" href="../#contact">Discuss your project <span class="arrow">{ARROW}</span></a></div></div></section>
</main>
'''
    page += footer(rel)
    write("case-studies/index.html", page)

    for i, c in enumerate(CASES):
        nxt = CASES[(i + 1) % len(CASES)]
        results = "".join(f'<div class="result" data-reveal><div class="result__v">{v}</div><div class="result__l">{l}</div></div>' for v, l in c["metrics"])
        ld = {"@context": "https://schema.org", "@type": "Article", "headline": c["title"], "description": c["summary"],
              "author": {"@type": "Person", "name": PERSON["name"], "url": SITE + "/"},
              "image": f"{SITE}/assets/img/og-image.png", "url": f"{SITE}/case-studies/{c['slug']}.html",
              "about": f"{c['company']} — {c['discipline']}"}
        page = head(f"{c['company']} · {c['discipline']} — Case Study | Adnan Afzal", f"{c['title']} {c['summary']}", f"case-studies/{c['slug']}.html", rel, ld, "article")
        page += "<body>\n" + nav(rel, "work")
        page += f'''<main id="main">
<article>
<section class="phero"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb" data-hero="eyebrow"><a href="../">Home</a><span aria-hidden="true">/</span><a href="./">Case studies</a><span aria-hidden="true">/</span><span>{e(c['company'])}</span></nav>
  <p class="eyebrow" style="margin-top:28px" data-hero="fade">{e(c['company'])} · {e(c['discipline'])}</p>
  <h1 data-hero="h1" style="max-width:20ch">{lines([e(c['title'])])}</h1>
  <p class="phero__lead" data-hero="fade">{e(c['summary'])}</p>
  <dl class="facts" data-hero="fade">
    <div class="fact"><dt>Company</dt><dd>{e(c['company'])}</dd></div>
    <div class="fact"><dt>My role</dt><dd>{e(c['role'])}</dd></div>
    <div class="fact"><dt>Period</dt><dd>{e(c['period'])}</dd></div>
    <div class="fact"><dt>Focus</dt><dd>{e(c['discipline'])} · {e(c['platform'])}</dd></div>
  </dl>
</div></section>
<section><div class="wrap"><div class="cover" data-clip><img src="../assets/img/cases/{c['slug']}.svg" alt="Illustration for the {e(c['company'])} {e(c['discipline'])} case study" width="1600" height="1000" decoding="async"></div></div></section>
<section class="section"><div class="wrap">
  <div class="prose-grid"><h2><span>01</span>Overview</h2><div class="prose" data-reveal><p>{e(c['overview'])}</p></div></div>
  <div class="prose-grid"><h2><span>02</span>Business challenge</h2><div class="prose" data-reveal><p>{e(c['challenge'])}</p></div></div>
  <div class="prose-grid"><h2><span>03</span>Strategy</h2><div class="prose" data-reveal><ul>{"".join(f"<li>{e(x)}</li>" for x in c['strategy'])}</ul></div></div>
  <div class="prose-grid"><h2><span>04</span>Execution</h2><div class="prose" data-reveal><ol>{"".join(f"<li>{e(x)}</li>" for x in c['execution'])}</ol></div></div>
  <div class="prose-grid"><h2><span>05</span>Platforms used</h2><div data-reveal><ul class="pill-list">{"".join(f"<li>{e(x)}</li>" for x in c['tools'])}</ul></div></div>
  <div class="prose-grid"><h2><span>06</span>Results</h2><div><div class="results">{results}</div></div></div>
  <div class="prose-grid"><h2><span>07</span>My contribution</h2><div class="prose" data-reveal><p>{e(c['contribution'])}</p></div></div>
</div></section>
</article>
<section><div class="wrap">
  <a class="next-case" href="{nxt['slug']}.html"><div><span class="eyebrow eyebrow--plain">Next case study</span><div class="next-case__t" style="margin-top:14px">{e(nxt['company'])} · {e(nxt['discipline'])}</div></div><span class="circ">{ARROW}</span></a>
</div></section>
<section class="section--tight" style="padding-top:0"><div class="wrap"><div class="cta-band" data-reveal><h2>Facing a similar problem?</h2><a class="btn btn--primary" href="../#contact">Discuss your project <span class="arrow">{ARROW}</span></a></div></div></section>
</main>
'''
        page += footer(rel)
        write(f"case-studies/{c['slug']}.html", page)


# ============================================================================
# RESUME
# ============================================================================
def build_resume():
    rel = ""
    jobs = "".join(f'''<article class="rjob" data-reveal>
  <div class="rjob__h"><h3>{j["role"]}</h3><span class="rjob__d">{j["from"]} – {j["to"]}</span></div>
  <div class="rjob__co">{j["company"]}</div>
  <div class="prose"><ul>{"".join(f"<li>{p}</li>" for p in j["points"])}</ul></div>
</article>''' for j in EXPERIENCE)
    tools = " • ".join(n for g, items in PLATFORMS for n, m in items)
    page = head("Resume — Adnan Afzal | Mobile Growth Manager", "Resume of Adnan Afzal, Mobile Growth Manager: user acquisition, ASO and monetization for mobile apps and games.", "resume.html", rel, person_ld())
    page += "<body>\n" + nav(rel, "experience")
    page += f'''<main id="main">
<section class="phero"><div class="wrap">
  <span class="eyebrow" data-hero="eyebrow">Resume</span>
  <h1 data-hero="h1">{lines(["Adnan Afzal", '<span class="accent">Mobile Growth Manager</span>'])}</h1>
  <p class="phero__lead" data-hero="fade">User Acquisition, ASO &amp; Monetization. Mobile Growth Specialist with 6+ years of experience scaling mobile apps and games through User Acquisition, App Store Optimization (ASO), Monetization, and Performance Marketing.</p>
  <div class="hero__ctas no-print" data-hero="fade">
    <button class="btn btn--primary" type="button" onclick="window.print()">Print / Save PDF <span class="arrow">{ARROW}</span></button>
    <a class="btn btn--ghost" href="./#contact">Get in touch <span class="arrow">{ARROW}</span></a>
  </div>
</div></section>
<section class="section--tight" style="padding-top:0"><div class="wrap resume">
  <aside>
    <div><h2>Contact</h2><ul>
      <li><a href="mailto:{PERSON['email']}">{PERSON['email']}</a></li>
      <li><a href="{PERSON['linkedin']}" target="_blank" rel="noopener">{PERSON['linkedin_label']}</a></li>
      <li>Pakistan · Open to global opportunities</li></ul></div>
    <div><h2>Core expertise</h2><ul>{"".join(f"<li>{x}</li>" for x in ["Mobile Growth Strategy", "User Acquisition (UA)", "App Store Optimization (ASO)", "Performance Marketing", "Monetization &amp; Ad Revenue Optimization", "Creative Testing &amp; Store Conversion", "Attribution &amp; Analytics", "Retention &amp; Revenue Growth"])}</ul></div>
    <div><h2>Specializations</h2><ul>{"".join(f"<li>{x}</li>" for x in ["Mobile Apps", "Mobile Games", "App Growth", "Monetization", "Analytics"])}</ul></div>
  </aside>
  <div>
    <h2 class="eyebrow" style="margin-bottom:36px">Professional experience</h2>
    {jobs}
    <h2 class="eyebrow" style="margin:12px 0 20px">Platforms &amp; tools</h2>
    <p class="muted">{tools}</p>
  </div>
</div></section>
</main>
'''
    page += footer(rel)
    write("resume.html", page)


# ============================================================================
# BLOG + ARTICLES
# ============================================================================
def build_blog():
    rel = ""
    cats = [("all", "All")] + [(a["catkey"], a["cat"]) for a in ARTICLES]
    fl = '<div class="filters bfilters" role="group" aria-label="Filter articles">' + "".join(
        f'<button type="button" class="filter" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{l}<span class="filter__count"></span></button>' for k, l in cats) + '</div><p class="sr-only" aria-live="polite" data-filter-live></p>'
    items = "".join(f'''<a class="bitem" id="{a["anchor"]}" data-cats="{a["catkey"]}" href="insights/{a["slug"]}.html">
  <span class="bitem__cat">{a["cat"]}</span>
  <div><h2>{e(a["title"])}</h2><p>{e(a["dek"])}</p></div>
  <span class="bitem__time">{a["mins"]} min read</span>
  <span class="circ" aria-hidden="true">{ARROW}</span>
</a>''' for a in ARTICLES)
    page = head("Growth Notes — Adnan Afzal | Mobile Growth Insights", "Practical field notes on mobile user acquisition, ASO, monetization, analytics and attribution.", "blog.html", rel,
                {"@context": "https://schema.org", "@type": "Blog", "name": "Growth Notes", "url": SITE + "/blog.html", "author": {"@type": "Person", "name": PERSON["name"]}})
    page += "<body>\n" + nav(rel, "insights")
    page += f'''<main id="main">
<section class="phero"><div class="wrap">
  <span class="eyebrow" data-hero="eyebrow">Growth Intelligence</span>
  <h1 data-hero="h1">{lines(["Clear thinking for", '<span class="accent">complicated growth</span>', "problems."])}</h1>
  <p class="phero__lead" data-hero="fade">Practical field notes on mobile acquisition, store performance, monetization, and the systems connecting them.</p>
</div></section>
<section class="section--tight" style="padding-top:0" data-filter-scope><div class="wrap">{fl}<div class="blist">{items}</div></div></section>
</main>
'''
    page += footer(rel)
    write("blog.html", page)

    for i, a in enumerate(ARTICLES):
        rel = "../"
        nxt = ARTICLES[(i + 1) % len(ARTICLES)]
        ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a["title"], "description": a["dek"],
              "author": {"@type": "Person", "name": PERSON["name"], "url": SITE + "/"}, "articleSection": a["cat"],
              "image": f"{SITE}/assets/img/og-image.png", "url": f"{SITE}/insights/{a['slug']}.html", "inLanguage": "en"}
        page = head(f"{a['title']} — Adnan Afzal", a["dek"], f"insights/{a['slug']}.html", rel, ld, "article")
        page += "<body>\n" + nav(rel, "insights")
        page += f'''<main id="main">
<article>
<section class="phero"><div class="wrap article-head">
  <nav class="crumbs" aria-label="Breadcrumb" data-hero="eyebrow"><a href="../">Home</a><span aria-hidden="true">/</span><a href="../blog.html">Insights</a><span aria-hidden="true">/</span><span>{a["cat"]}</span></nav>
  <h1 data-hero="h1" style="font-size:clamp(2.2rem,5.4vw,5rem);max-width:22ch">{lines([e(a["title"])])}</h1>
  <p class="phero__lead" data-hero="fade">{e(a["dek"])}</p>
  <div class="article-meta" data-hero="fade"><span>By <b>{PERSON["name"]}</b></span><span>{a["cat"]}</span><span>{a["mins"]} min read</span></div>
</div></section>
<section class="section--tight" style="padding-top:0"><div class="wrap"><div class="article-body"><div class="prose" data-reveal>{a["body"]}</div></div></div></section>
</article>
<section><div class="wrap">
  <a class="next-case" href="{nxt['slug']}.html"><div><span class="eyebrow eyebrow--plain">Next article</span><div class="next-case__t" style="margin-top:14px;font-size:clamp(1.5rem,3.6vw,3rem)">{e(nxt['title'])}</div></div><span class="circ">{ARROW}</span></a>
</div></section>
<section class="section--tight" style="padding-top:0"><div class="wrap"><div class="cta-band" data-reveal><h2>Want this applied to your product?</h2><a class="btn btn--primary" href="../#contact">Discuss your project <span class="arrow">{ARROW}</span></a></div></div></section>
</main>
'''
        page += footer(rel)
        write(f"insights/{a['slug']}.html", page)


# ============================================================================
# 404, sitemap, robots
# ============================================================================
def build_404():
    # Works from any depth: base href is computed for project-page or custom-domain hosting.
    base_js = "(function(){var p=location.pathname.split('/')[1];var b=((location.hostname.indexOf('github.io')>-1||location.hostname==='localhost')&&p&&p!=='404.html')?'/'+p+'/':'/';document.write('<base href=\"'+b+'\">');})();"
    page = head("Page not found — Adnan Afzal", "The page you were looking for doesn't exist.", "404.html", "").replace('<meta charset="utf-8">', f'<meta charset="utf-8">\n<script>{base_js}</script>\n<meta name="robots" content="noindex">')
    page += "<body>\n" + nav("./", "")
    page += f'''<main id="main" class="nf">
  <div>
    <div class="nf__code" aria-hidden="true">4<span>0</span>4</div>
    <h1>This page didn’t convert.</h1>
    <p>The link may be outdated, or the page has moved during the redesign.</p>
    <div class="hero__ctas"><a class="btn btn--primary" href="./">Back to home <span class="arrow">{ARROW}</span></a><a class="btn btn--ghost" href="case-studies/">See case studies <span class="arrow">{ARROW}</span></a></div>
  </div>
</main>
'''
    page += footer("./")
    write("404.html", page)


def build_meta():
    urls = ["", "case-studies/", "resume.html", "blog.html"] + [f"case-studies/{c['slug']}.html" for c in CASES] + [f"insights/{a['slug']}.html" for a in ARTICLES]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        pr = "1.0" if u == "" else "0.8" if "case" in u or u in ("resume.html",) else "0.6"
        sm += f"  <url><loc>{SITE}/{u}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n"
    write("sitemap.xml", sm + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /legacy/\nDisallow: /tools/\n\nSitemap: {SITE}/sitemap.xml\n")


if __name__ == "__main__":
    build_home(); build_cases(); build_resume(); build_blog(); build_404(); build_meta()
    print("Built", ROOT)
