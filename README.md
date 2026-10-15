# Msaro Guide Tanzania — website

A Django site. Everything you see on the pages (texts, phone numbers, photos,
packages, itineraries, guides, FAQs, reviews, SEO titles) lives in the database
and can be changed from **/admin/**.

* Database: **Supabase Postgres**
* Uploaded pictures: **Supabase Storage** bucket (public)
* Design: the original CSS/JS in `static/` — unchanged

`legacy_static_site/` is the old plain-HTML version, kept only for reference.

## What can be edited in the admin

| Admin section | What it controls |
|---|---|
| Site settings | Business name, logo, phones, WhatsApp numbers, email, address, hours, map, Facebook/Instagram, homepage typing words, SEO business info |
| Page SEO | Title, description and keywords for each page |
| Content blocks | Every heading, paragraph and button text on every page (filter by page) |
| Image blocks | Single photos such as the About page picture |
| Hero slides, Stats, Why-us reasons, Testimonials, Guides, Guide photos, Packing list, Certifications, FAQs, Gallery, Destinations | The repeating sections — add, remove, reorder |
| Package categories → Packages → Itinerary days | Tabs on the packages pages, every package card, its "View Full Itinerary & Book" window and day-by-day plan |
| Trip options | The trips listed in the contact / booking form |

Change the `order` number to move an item up or down.

## Supabase setup (once)

1. **Database** — Project Settings → Database → Connection string → **Session pooler**.
   Copy it and put your database password in it. This is `DATABASE_URL`.
2. **Bucket** — Storage → New bucket → name it `media` → tick **Public bucket**.
3. **Storage keys** — Storage → Settings → **S3 Connection**: copy the *Endpoint* and
   *Region*, then *New access key* to get the access key ID and secret.

## Deploy on Render

1. New → **Blueprint** (uses `render.yaml`) or New → Web Service with
   * Build command: `./build.sh`
   * Start command: `gunicorn msaro_site.wsgi --workers 2 --threads 4 --timeout 60`
2. Fill in the environment variables from `.env.example`.
3. Deploy. The build collects CSS/JS, creates the tables and loads all the
   current website content and pictures into Supabase (first time only).
4. Create your admin login — Render → Shell:
   ```
   python manage.py createsuperuser
   ```
5. Point `msaroguidetanzania.com` / `www.msaroguidetanzania.com` to the Render service
   (Render → Settings → Custom Domains).

## Run on your computer

```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # fill in, or leave DATABASE_URL empty to use SQLite
python manage.py migrate
python manage.py seed_site
python manage.py createsuperuser
python manage.py runserver
```

`seed_site` only fills empty tables, so it never overwrites what you edited.
`python manage.py seed_site --reset` wipes the website content and loads the
original again (admin users are kept).
