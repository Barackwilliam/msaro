MSARO GUIDE TANZANIA — Static Multi-Page Website
==================================================

Pure static HTML/CSS/JS. No Django, no build step, no server required.
Open index.html in a browser, or upload the whole folder to any static
host (Netlify, GitHub Pages, cPanel, etc).

PAGES
  index.html            Home (hero + previews of every section)
  about.html             About Us
  guides.html             Meet Our Guides (Mussa & Amani)
  certifications.html     Certifications
  packages.html            Tour Packages (Kilimanjaro / Meru / Udzungwa / Safari tabs)
  destinations.html         Destinations
  gallery.html               Gallery
  why-us.html                  Why Choose Us
  testimonials.html              Testimonials
  faq.html                         FAQ
  contact.html                       Contact (booking form + map)

Every page shares the same header (top bar + navbar) and footer, so
navigation is consistent site-wide — edit css/style.css or js/script.js
once and it applies everywhere.

MOBILE MENU
  On screens under 992px, the horizontal nav is replaced by a slide-in
  SIDEBAR (tap the icon top-right). It has its own expandable "About"
  and "Packages" groups, contact details and social icons — a true
  off-canvas sidebar, similar to emadventuretanzania.com.

DESIGN
  Colors and typography follow the original template's design system:
  teal, coral, golden-sand and navy, with Lora for headings and Open
  Sans for body text. The navbar and top bar are dark navy, matching
  the reference site's look.

IMAGES
  images/ is empty — drop your real photos in using the exact filenames
  already referenced across the pages, e.g.:
    hero-kilimanjaro.jpg   mussa-guide.jpg        amani-guide.jpg
    about-guides.jpg       kilimanjaro-marangu.jpg kilimanjaro-machame.jpg
    kilimanjaro-lemosho.jpg kilimanjaro-rongai.jpg kilimanjaro-umbwe.jpg
    meru-3days.jpg         meru-4days.jpg          udzungwa.jpg
    safari-4day.jpg        safari-7day.jpg         kilimanjaro.jpg
    meru.jpg               tarangire.jpg           lake-manyara.jpg
    serengeti.jpg          ngorongoro.jpg          lake-natron.jpg
    gallery1.jpg ... gallery8.jpg
    review1.jpg review2.jpg review3.jpg
    favicon.png            og-cover.jpg

  Until real photos are added, each image slot shows a clean teal/gold
  placeholder tile instead of a broken-image icon.

LIBRARIES (CDN, no install needed)
  Bootstrap 5.3, Bootstrap Icons, Font Awesome (WhatsApp icon), AOS
  (scroll animation), Swiper.js (carousels), GLightbox (gallery),
  CountUp.js (stat counters), Typed.js (homepage hero typing text)

CONTACT INFO USED THROUGHOUT
  Phone:    +255 749 235 394
  WhatsApp: +255 749 235 394 (secondary WhatsApp option on the floating chat button: 0628 839 187)
  Email:    info@msaroguidetanzania.com
  Location: Arusha, Mianzini, Tanzania
  Hours:    Open 24 Hours

The contact page's "Send via WhatsApp" form doesn't submit to a server —
it opens WhatsApp with the visitor's details pre-filled, so it works on
any static host with zero backend.
