#!/usr/bin/env python3
"""
Asha Garment Factory — service page builder

Builds each service landing page (e.g. /t-shirt-manufacturer-india/) plus
404.html and sitemap.xml.

Each page's own content lives in _tools/pages/<slug>.html: a JSON block inside
an HTML comment (title, meta description, hero, FAQs…) followed by the page's
body sections. The shared parts — head, nav, hero, process, testimonial, FAQ,
quote form, footer — are filled in here so every page stays consistent.

Folders starting with "_" are not published by GitHub Pages, so this script
and its sources stay out of the live site.

Run after editing any page source:   python3 _tools/build_pages.py
The homepage (index.html) is edited by hand; keep its footer in sync with
footer() below.
"""

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / '_tools' / 'pages'
SITE = 'https://www.ashagarmentfactory.co.in'
CSS_VERSION = '2026-11-03'
LASTMOD = '2026-11-03'

WHATSAPP = 'https://wa.me/919985931288?text=Hi%2C+I%27d+like+to+enquire+about+garment+manufacturing+at+Asha+Garment+Factory.'

# Order here is the order used in footers, related links and the sitemap.
SERVICES = [
    ('private-label-clothing-manufacturer-india', 'Private Label Clothing'),
    ('t-shirt-manufacturer-india',                'T-Shirt Manufacturing'),
    ('womens-wear-manufacturer-india',            "Women's Wear Manufacturing"),
    ('kids-wear-manufacturer-india',              'Kids Wear Manufacturing'),
    ('low-moq-clothing-manufacturer-india',       'Low MOQ Production'),
    ('ethical-clothing-manufacturer-india',       'Ethical Manufacturing'),
    ('garment-embroidery-printing-india',         'Embroidery & Printing'),
]

TESTIMONIALS = {
    'barbara': ('🇨🇭', 'Mrs. Barbara', 'Swiss Bedsheet Brand · Switzerland',
                'Ever since we began working with Asha Garment Factory, we have been very happy to count on their '
                'skills — from stitching to dispatching our product. Their attention to detail and reliability '
                'has been exceptional from day one.'),
    'arathoon': ('🇺🇸', 'Mr. Arathoon', 'Ethical Fashion Brand · USA',
                 'We have been consistently amazed by the exceptional quality of the products that Asha Garment '
                 'Factory produces — and even more moved by the life-transformation work they do through their '
                 'foundation. A truly remarkable manufacturing partner.'),
    'kadambini': ('🤝', 'Kadambini', 'Brand Partner · 2+ Years',
                  'We have been working with Asha Garment Factory for more than two years and have been very satisfied '
                  'with the experience. From sampling our designs to packaging and shipping, we receive end-to-end '
                  'servicing from them. Their standard is pretty high and we have faced no significant issues in '
                  'production. Beulah is easy to work with and always open to feedback and improving processes where '
                  'need be. Would easily recommend them to anyone looking to outsource their garment production needs.'),
    'lev': ('👕', 'Verified Client', 'Oversized Shirts Order to Lev Apparel, USA',
            "I received the box of oversized shirts yesterday. I've only had a chance to pull out two of them, "
            'but from the two I pulled out, they are beautiful! I cannot believe the quality of this fabric and '
            'the sewing. Thank you so much.'),
}

PRODUCT_OPTIONS = ["Women's Wear", "Men's Wear", 'T-Shirts & Polos', 'Kids Wear',
                   'Lifestyle / Activewear', 'Multiple Categories', 'Not sure yet']


def esc(text):
    return html.escape(text, quote=True)


def plain(text):
    """FAQ answers may contain <strong>/<a>; schema.org text must be plain."""
    return html.unescape(re.sub(r'<[^>]+>', '', text))


def url_for(slug):
    return f'{SITE}/{slug}/'


# ─────────────────────────────────────────────
# Shared blocks
# ─────────────────────────────────────────────

def head(meta, canonical, schema, noindex=False):
    robots = 'noindex, follow' if noindex else 'index, follow'
    canonical_tag = '' if noindex else f'\n  <link rel="canonical" href="{canonical}" />'
    hero_preload = (f'\n  <link rel="preload" as="image" href="/Images/{meta["hero_image"]}" fetchpriority="high" />'
                    if meta.get('hero_image') else '')
    schema_tag = ''
    if schema:
        schema_tag = ('\n\n  <script type="application/ld+json">\n'
                      + json.dumps(schema, ensure_ascii=False, indent=2)
                      + '\n  </script>')
    return f'''<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(meta["title"])}</title>
  <meta name="description" content="{esc(meta["description"])}" />{canonical_tag}
  <meta name="robots" content="{robots}" />
  <meta name="theme-color" content="#0f1c2e" />

  <link rel="icon" href="/favicon.ico" sizes="48x48" />
  <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
  <link rel="icon" href="/favicon-96.png" type="image/png" sizes="96x96" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />

  <meta name="geo.region" content="IN-TG" />
  <meta name="geo.placename" content="Hyderabad, Telangana, India" />

  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:title" content="{esc(meta["title"])}" />
  <meta property="og:description" content="{esc(meta["description"])}" />
  <meta property="og:site_name" content="Asha Garment Factory" />
  <meta property="og:image" content="{SITE}/Images/og-image.jpg" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:locale" content="en_IN" />
  <meta name="twitter:card" content="summary_large_image" />{schema_tag}

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="preload"
    href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap" as="style"
    onload="this.onload=null;this.rel='stylesheet'" />
  <noscript>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap"
      rel="stylesheet" />
  </noscript>{hero_preload}

  <link rel="stylesheet" href="/css/styles.css?v={CSS_VERSION}" />
</head>

<body>
'''


def nav():
    return f'''
  <nav class="navbar" id="navbar">
    <div class="container nav-inner">

      <a href="/" class="nav-logo">
        <img src="/Images/logo.svg" alt="Asha Garment Factory" class="nav-logo-img" />
      </a>

      <ul class="nav-links" id="nav-links">
        <li><a href="/#about">About</a></li>
        <li><a href="/#why-us">Why Us</a></li>
        <li><a href="/#products">Products</a></li>
        <li><a href="/#testimonials">Clients</a></li>
        <li><a href="#quote">Contact</a></li>
        <li class="nav-cta-mobile"><a href="#quote" class="btn btn-primary">Get a Quote</a></li>
      </ul>

      <a href="#quote" class="btn btn-primary nav-cta">Get a Quote</a>

      <button class="nav-toggle" id="nav-toggle" aria-label="Toggle menu" aria-controls="nav-links"
        aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </nav>
'''


def page_hero(meta):
    return f'''
  <section class="page-hero">
    <div class="hero-overlay"></div>
    <img class="hero-img" src="/Images/{meta["hero_image"]}" alt="{esc(meta["hero_alt"])}"
      width="{meta["hero_w"]}" height="{meta["hero_h"]}" loading="eager" fetchpriority="high" />

    <div class="container hero-content">
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <ol>
          <li><a href="/">Home</a></li>
          <li aria-current="page">{esc(meta["short_name"])}</li>
        </ol>
      </nav>
      <p class="hero-badge">{esc(meta["badge"])}</p>
      <h1>{meta["h1"]}</h1>
      <p class="hero-sub">{meta["sub"]}</p>
      <div class="hero-btns">
        <a href="#quote" class="btn btn-primary">Request a Quote</a>
        <a href="{WHATSAPP}" target="_blank" rel="noopener noreferrer" class="btn btn-whatsapp">💬 WhatsApp Us</a>
      </div>
    </div>
  </section>
'''


def stats_strip():
    return '''
  <section class="stats-strip" aria-label="Asha Garment Factory at a glance">
    <dl class="container stats-grid">
      <div>
        <dt class="stat-item-label">Minimum order per style</dt>
        <dd class="stat-item-num">100 pcs</dd>
      </div>
      <div>
        <dt class="stat-item-label">Sample development</dt>
        <dd class="stat-item-num">~3 wks</dd>
      </div>
      <div>
        <dt class="stat-item-label">Bulk production</dt>
        <dd class="stat-item-num">6–10 wks</dd>
      </div>
      <div>
        <dt class="stat-item-label">Manufacturing since</dt>
        <dd class="stat-item-num">2011</dd>
      </div>
    </dl>
  </section>
'''


PROCESS = [
    ('Sampling', 'Send a tech pack, sketch or reference garment. We develop your first sample in about three weeks and revise until you approve it.'),
    ('Fabric & Trims', 'We source the fabric, trims and labels your design needs from selected mills and suppliers, and confirm them with you.'),
    ('Cutting & Stitching', 'Patterns are cut and sewn on industrial lockstitch and overlock machines by skilled craftspeople in our Hyderabad factory.'),
    ('Embellishment', 'Embroidery, screen printing, heat transfer, labels and hangtags are planned into production and quality-checked with the garment.'),
    ('Quality Control', 'Three-stage inspection — in-process, post-production and pre-shipment — covering stitching, colour fastness, measurements and finish.'),
    ('Packing & Export', 'Export packing, documentation and shipping to the USA, UK, Europe, the Middle East or wherever your brand is based.'),
]


def process():
    steps = '\n'.join(f'''        <div class="process-step">
          <div class="step-number">{i:02d}</div>
          <h3>{title}</h3>
          <p>{text}</p>
        </div>''' for i, (title, text) in enumerate(PROCESS, 1))
    return f'''
  <section class="section section-dark" id="process">
    <div class="container">
      <div class="section-header text-center">
        <span class="section-label">How It Works</span>
        <h2>From Sample to Shipment</h2>
        <p style="max-width:560px;margin:0.75rem auto 0;">
          Samples take about 3 weeks. Once you approve the sample, bulk production takes 6–10 weeks depending on
          quantity, fabric and embellishment.
        </p>
      </div>
      <div class="process-steps reveal">
{steps}
      </div>
    </div>
  </section>
'''


def testimonial(key):
    flag, name, role, text = TESTIMONIALS[key]
    return f'''
  <section class="section section-alt" id="testimonials">
    <div class="container">
      <div class="section-header text-center">
        <span class="section-label">Client Feedback</span>
        <h2>What Brands Say About Working With Us</h2>
      </div>
      <div class="testimonial-card testimonial-single reveal">
        <div class="testimonial-stars">★★★★★</div>
        <p class="testimonial-text">"{text}"</p>
        <div class="testimonial-author">
          <div class="author-avatar">{flag}</div>
          <div>
            <div class="author-name">{name}</div>
            <div class="author-role">{role}</div>
          </div>
        </div>
      </div>
    </div>
  </section>
'''


def faq(meta):
    items = '\n'.join(f'''
          <div class="faq-item">
            <button class="faq-q" aria-expanded="false">
              {esc(q)}
              <span class="faq-icon" aria-hidden="true">+</span>
            </button>
            <div class="faq-a">
              <div class="faq-a-inner">
                {a}
              </div>
            </div>
          </div>''' for q, a in meta['faqs'])
    return f'''
  <section class="section" id="faq">
    <div class="container">
      <div class="section-header text-center">
        <span class="section-label">Buyer Questions</span>
        <h2>{esc(meta["faq_heading"])}</h2>
      </div>
      <div class="faq-list">{items}

      </div>
    </div>
  </section>
'''


def related(current):
    links = '\n'.join(f'        <a class="related-link" href="/{slug}/">{esc(name)}</a>'
                      for slug, name in SERVICES if slug != current)
    return f'''
  <section class="section section-alt" id="services">
    <div class="container">
      <div class="section-header text-center" style="margin-bottom:2rem;">
        <span class="section-label">More From AGF</span>
        <h2>Explore Our Manufacturing Services</h2>
      </div>
      <div class="related-grid">
{links}
      </div>
    </div>
  </section>
'''


def quote_form(selected=''):
    options = '\n'.join(
        f'                  <option{" selected" if opt == selected else ""}>{esc(opt)}</option>'
        for opt in PRODUCT_OPTIONS)
    return f'''
  <section class="section section-dark" id="quote">
    <img class="section-bg-img" src="/Images/quote-embroidery.jpg" alt="" width="932" height="1400" loading="lazy" />
    <div class="container">
      <div class="two-col" style="gap:3.5rem;">

        <div>
          <span class="section-label">Get in Touch</span>
          <h2 style="color:#fff;">Get a Quote<br />in 24 Hours</h2>
          <p style="margin:1rem 0 2rem;color:rgba(255,255,255,0.72);">
            Tell us what you need and we'll reply within 24 hours with a tailored proposal. No obligation —
            just a conversation about how we can serve your brand.
          </p>
          <ul class="feature-list" style="margin-bottom:2rem;">
            <li style="color:rgba(255,255,255,0.8);border-color:rgba(255,255,255,0.1);">Minimum order from 100 pieces per style</li>
            <li style="color:rgba(255,255,255,0.8);border-color:rgba(255,255,255,0.1);">Sample in about 3 weeks; bulk in 6–10 weeks</li>
            <li style="color:rgba(255,255,255,0.8);border-color:rgba(255,255,255,0.1);">Export documentation and shipping handled</li>
          </ul>
          <p style="color:rgba(255,255,255,0.72);">
            📧 <a href="mailto:ashagarmentfactory@gmail.com" style="color:var(--gold);font-weight:700;">ashagarmentfactory@gmail.com</a><br />
            📍 Hyderabad, Telangana, India
          </p>
        </div>

        <div class="booking-form-wrap">
          <h3>Request a Quote</h3>
          <p class="sub">Fill in your details below — we'll respond within 24 hours.</p>

          <form id="quote-form">
            <div class="form-grid">

              <div class="form-group">
                <label for="name">Your Name *</label>
                <input type="text" id="name" name="name" placeholder="Full name" autocomplete="name" required />
              </div>

              <div class="form-group">
                <label for="company">Company / Brand *</label>
                <input type="text" id="company" name="company" placeholder="Your brand name" autocomplete="organization"
                  required />
              </div>

              <div class="form-group">
                <label for="email">Email Address *</label>
                <input type="email" id="email" name="email" placeholder="your@email.com" autocomplete="email"
                  inputmode="email" required />
              </div>

              <div class="form-group">
                <label for="phone">WhatsApp / Phone</label>
                <input type="tel" id="phone" name="phone" placeholder="+1 XXX XXX XXXX" autocomplete="tel"
                  inputmode="tel" />
              </div>

              <div class="form-group">
                <label for="country">Country *</label>
                <select id="country" name="country" autocomplete="country-name" required>
                  <option value="">Select your country…</option>
                  <option>United States</option>
                  <option>United Kingdom</option>
                  <option>Germany</option>
                  <option>France</option>
                  <option>Switzerland</option>
                  <option>Netherlands</option>
                  <option>UAE</option>
                  <option>Qatar</option>
                  <option>Saudi Arabia</option>
                  <option>Kuwait</option>
                  <option>Australia</option>
                  <option>Canada</option>
                  <option>India</option>
                  <option>Other</option>
                </select>
              </div>

              <div class="form-group">
                <label for="product">Product Category *</label>
                <select id="product" name="product" required>
                  <option value="">Select category…</option>
{options}
                </select>
              </div>

              <div class="form-group">
                <label for="quantity">Estimated Order Quantity</label>
                <select id="quantity" name="quantity">
                  <option value="">Select range…</option>
                  <option>100 – 500 pieces</option>
                  <option>500 – 2,000 pieces</option>
                  <option>2,000 – 5,000 pieces</option>
                  <option>5,000 – 10,000 pieces</option>
                  <option>10,000+ pieces</option>
                </select>
              </div>

              <div class="form-group">
                <label for="stage">Where Are You In Your Sourcing?</label>
                <select id="stage" name="stage">
                  <option value="">Select…</option>
                  <option>Just exploring options</option>
                  <option>Comparing manufacturers</option>
                  <option>Ready to request samples</option>
                  <option>Ready to place a bulk order</option>
                </select>
              </div>

              <div class="form-group full">
                <label for="message">Tell Us About Your Requirements</label>
                <textarea id="message" name="message"
                  placeholder="Describe the garments you need — fabrics, styles, embellishments, certifications required, lead times, or anything else we should know…"></textarea>
              </div>

            </div>

            <div class="form-submit">
              <button type="submit" class="btn btn-primary">Send My Request</button>
              <a href="https://wa.me/919985931288?text=Hi%2C+I%27d+like+to+get+a+quote+from+Asha+Garment+Factory."
                target="_blank" rel="noopener noreferrer" class="btn btn-whatsapp">💬 WhatsApp Instead</a>
            </div>
            <p class="form-note">We'll respond within 24 hours. No spam, no obligation.</p>
            <div class="success-msg" id="form-success"></div>
          </form>
        </div>

      </div>
    </div>
  </section>
'''


def footer():
    service_links = '\n'.join(f'            <li><a href="/{slug}/">{esc(name)}</a></li>'
                              for slug, name in SERVICES)
    return f'''
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">

        <div class="footer-brand">
          <img src="/Images/logo.svg" alt="Asha Garment Factory" class="footer-logo-img" />
          <p>An ethical clothing manufacturer for global brands. Women's, men's and kids wear from Hyderabad, India —
            since 2011.</p>
          <div class="footer-social">
            <a href="https://www.instagram.com/ashagarmentfactory" target="_blank" rel="noopener noreferrer"
              title="Instagram" aria-label="Asha Garment Factory on Instagram">📸</a>
            <a href="https://www.facebook.com/shopforasha" target="_blank" rel="noopener noreferrer"
              title="Facebook" aria-label="Asha Garment Factory on Facebook">📘</a>
          </div>
        </div>

        <div class="footer-col">
          <h5>Navigate</h5>
          <ul class="footer-links">
            <li><a href="/#about">About AGF</a></li>
            <li><a href="/#why-us">Why Manufacture With Us</a></li>
            <li><a href="/#products">Products &amp; Catalogues</a></li>
            <li><a href="/#impact">Our Mission</a></li>
            <li><a href="/#testimonials">Client Testimonials</a></li>
            <li><a href="/#faq">Buyer FAQ</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h5>Manufacturing</h5>
          <ul class="footer-links">
{service_links}
          </ul>
        </div>

        <div class="footer-col">
          <h5>Get in Touch</h5>
          <div class="footer-contact-item">
            <span class="footer-contact-icon">📧</span>
            <div class="footer-contact-text">
              <a href="mailto:ashagarmentfactory@gmail.com">ashagarmentfactory@gmail.com</a>
            </div>
          </div>
          <div class="footer-contact-item">
            <span class="footer-contact-icon">📸</span>
            <div class="footer-contact-text">
              <a href="https://www.instagram.com/ashagarmentfactory" target="_blank"
                rel="noopener noreferrer">@ashagarmentfactory</a>
            </div>
          </div>
          <div class="footer-contact-item">
            <span class="footer-contact-icon">📍</span>
            <address class="footer-contact-text" style="font-style:normal;">Hyderabad, Telangana, India</address>
          </div>
          <a href="/#quote" class="btn btn-primary" style="margin-top:1.25rem;width:100%;justify-content:center;">
            Get a Quote
          </a>
        </div>

      </div>

      <div class="footer-bottom">
        <p>&copy; 2026 Asha Garment Factory. All rights reserved.</p>
        <p style="color:rgba(255,255,255,0.25);">Manufacturing with purpose. Built with care.</p>
      </div>
    </div>
  </footer>

  <!-- Sticky WhatsApp button — mobile only via CSS -->
  <a href="{WHATSAPP}"
    class="whatsapp-float" target="_blank" rel="noopener noreferrer" aria-label="Chat with us on WhatsApp">💬</a>

  <script src="/js/main.js?v={CSS_VERSION}"></script>

</body>

</html>
'''


# ─────────────────────────────────────────────
# Structured data
# ─────────────────────────────────────────────

def schema_for(slug, meta):
    url = url_for(slug)
    org = {'@type': 'Organization', '@id': f'{SITE}/#organization',
           'name': 'Asha Garment Factory', 'url': f'{SITE}/'}
    return {
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'WebPage', '@id': f'{url}#webpage', 'url': url,
                'name': meta['title'], 'description': meta['description'],
                'isPartOf': {'@id': f'{SITE}/#website'},
                'about': {'@id': f'{url}#service'},
                'breadcrumb': {'@id': f'{url}#breadcrumb'},
                'dateModified': LASTMOD, 'inLanguage': 'en',
            },
            {
                '@type': 'BreadcrumbList', '@id': f'{url}#breadcrumb',
                'itemListElement': [
                    {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': f'{SITE}/'},
                    {'@type': 'ListItem', 'position': 2, 'name': meta['short_name'], 'item': url},
                ],
            },
            {
                '@type': 'Service', '@id': f'{url}#service',
                'name': meta['service_name'], 'serviceType': meta['service_type'],
                'description': meta['description'], 'provider': org,
                'areaServed': ['US', 'GB', 'EU', 'CH', 'QA', 'AE', 'IN'],
                'offers': {
                    '@type': 'Offer',
                    'eligibleQuantity': {'@type': 'QuantitativeValue', 'minValue': 100,
                                         'unitText': 'pieces per style'},
                },
            },
            {
                '@type': 'FAQPage', '@id': f'{url}#faq',
                'mainEntity': [
                    {'@type': 'Question', 'name': q,
                     'acceptedAnswer': {'@type': 'Answer', 'text': plain(a)}}
                    for q, a in meta['faqs']
                ],
            },
        ],
    }


# ─────────────────────────────────────────────
# Builders
# ─────────────────────────────────────────────

def read_source(slug):
    text = (SRC / f'{slug}.html').read_text(encoding='utf-8')
    match = re.match(r'\s*<!--(.*?)-->(.*)', text, re.S)
    if not match:
        raise SystemExit(f'{slug}.html must start with a <!-- {{json}} --> block')
    return json.loads(match.group(1)), match.group(2).strip('\n')


def build_service(slug):
    meta, body = read_source(slug)
    page = (head(meta, url_for(slug), schema_for(slug, meta))
            + nav()
            + '\n  <main id="main">\n'
            + page_hero(meta)
            + stats_strip()
            + '\n' + body + '\n'
            + process()
            + testimonial(meta['testimonial'])
            + faq(meta)
            + related(slug)
            + quote_form(meta.get('product', ''))
            + '\n  </main>\n'
            + footer())
    out = ROOT / slug / 'index.html'
    out.parent.mkdir(exist_ok=True)
    out.write_text(page, encoding='utf-8')
    print(f'  built /{slug}/')


def build_404():
    meta = {'title': 'Page Not Found | Asha Garment Factory',
            'description': 'The page you were looking for has moved. Explore garment manufacturing services from Asha Garment Factory, Hyderabad, India.'}
    links = '\n'.join(f'        <a class="related-link" href="/{slug}/">{esc(name)}</a>'
                      for slug, name in SERVICES)
    body = f'''
  <section class="section" style="padding-top:9rem;">
    <div class="container text-center">
      <span class="section-label">Page Not Found</span>
      <h1 style="margin-bottom:1rem;">This page has moved</h1>
      <p style="max-width:560px;margin:0 auto 2rem;">
        Our website has a new home. The page you were looking for may have moved — try one of the pages below,
        or head back to the homepage.
      </p>
      <a href="/" class="btn btn-primary">Go to Homepage</a>
      <h2 class="related-intro" style="font-size:1.4rem;">Manufacturing services</h2>
      <div class="related-grid" style="text-align:left;">
{links}
      </div>
    </div>
  </section>
'''
    page = head(meta, '', None, noindex=True) + nav() + '\n  <main id="main">\n' + body + '\n  </main>\n' + footer()
    # Quote links on this page should go to the homepage form
    page = page.replace('href="#quote"', 'href="/#quote"')
    (ROOT / '404.html').write_text(page, encoding='utf-8')
    print('  built /404.html')


def build_sitemap():
    service_urls = '\n'.join(f'''  <url>
    <loc>{url_for(slug)}</loc>
    <lastmod>{LASTMOD}</lastmod>
  </url>''' for slug, _ in SERVICES)
    sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">
  <url>
    <loc>{SITE}/</loc>
    <lastmod>{LASTMOD}</lastmod>
    <image:image><image:loc>{SITE}/Images/hero.jpg</image:loc></image:image>
    <image:image><image:loc>{SITE}/Images/gallery-embroidery.jpg</image:loc></image:image>
    <image:image><image:loc>{SITE}/Images/gallery-sewing-line.jpg</image:loc></image:image>
    <image:image><image:loc>{SITE}/Images/gallery-cutting.jpg</image:loc></image:image>
    <image:image><image:loc>{SITE}/Images/catalogue-womens.webp</image:loc></image:image>
    <image:image><image:loc>{SITE}/Images/catalogue-mens.webp</image:loc></image:image>
    <image:image><image:loc>{SITE}/Images/catalogue-kids.webp</image:loc></image:image>
    <video:video>
      <video:thumbnail_loc>{SITE}/Images/agf-intro-poster.jpg</video:thumbnail_loc>
      <video:title>Inside Asha Garment Factory — from design sketch to export packing</video:title>
      <video:description>A 40-second look inside Asha Garment Factory in Hyderabad, India: sampling, cutting, stitching, embroidery, quality control and export packing.</video:description>
      <video:content_loc>{SITE}/Videos/agf-intro.mp4</video:content_loc>
      <video:duration>40</video:duration>
    </video:video>
  </url>
{service_urls}
</urlset>
'''
    (ROOT / 'sitemap.xml').write_text(sitemap, encoding='utf-8')
    print('  built /sitemap.xml')


if __name__ == '__main__':
    print('Building AGF service pages…')
    for slug, _ in SERVICES:
        build_service(slug)
    build_404()
    build_sitemap()
    print('Done.')
