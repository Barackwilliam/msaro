"""
Load the website's current content into the database and upload its pictures
to the configured storage (the Supabase bucket in production).

    python manage.py seed_site            # fill empty tables, keep anything already edited
    python manage.py seed_site --reset    # wipe website content and load it again
    python manage.py seed_site --no-download   # keep external pictures as links instead of copying them

Safe to run more than once: without --reset, existing rows are left alone.
"""
import json
import mimetypes
import re
import urllib.request
from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from website import models as m

SEED_FILE = Path(__file__).resolve().parents[2] / "seed" / "site_content.json"
LOCAL_IMAGES = Path(settings.BASE_DIR) / "public" / "images"

LIST_MODELS = {
    "HeroSlide": m.HeroSlide, "Stat": m.Stat, "WhyReason": m.WhyReason, "Testimonial": m.Testimonial,
    "Guide": m.Guide, "GuidePhoto": m.GuidePhoto, "PackingCategory": m.PackingCategory,
    "Certification": m.Certification, "FAQ": m.FAQ, "GalleryImage": m.GalleryImage,
    "Destination": m.Destination, "TripOption": m.TripOption,
}


class Command(BaseCommand):
    help = "Load the website's content and pictures into the database / Supabase bucket."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true",
                            help="Delete existing website content first (admin users are kept).")
        parser.add_argument("--no-download", action="store_true",
                            help="Don't copy external pictures into storage; keep their links.")

    def handle(self, *args, **opts):
        self.download = not opts["no_download"]
        self.cache = {}
        data = json.loads(SEED_FILE.read_text())
        with transaction.atomic():
            if opts["reset"]:
                self.reset()
            self.load_settings(data)
            self.load_seo(data)
            self.load_blocks(data)
            self.load_lists(data)
            self.load_packages(data)
        self.stdout.write(self.style.SUCCESS("Website content loaded."))

    # ------------------------------------------------------------------
    def reset(self):
        for model in [m.ItineraryDay, m.Package, m.PackageCategory, m.ContentBlock, m.ImageBlock, m.PageSEO,
                      *LIST_MODELS.values()]:
            model.objects.all().delete()
        m.SiteSettings.objects.all().delete()
        self.stdout.write("Old website content removed.")

    # ------------------------------------------------------------------
    def fetch(self, ref, hint):
        """Return (filename, bytes) for an image reference, or None to keep it as a URL."""
        key = json.dumps(ref, sort_keys=True)
        if key in self.cache:
            return self.cache[key]
        result = None
        if "local" in ref:
            path = LOCAL_IMAGES / ref["local"]
            if path.exists():
                result = (ref["local"], path.read_bytes())
            else:
                self.stderr.write(f"  ! missing local picture {path}")
        elif self.download:
            try:
                req = urllib.request.Request(ref["url"], headers={"User-Agent": "Mozilla/5.0 (seed_site)"})
                with urllib.request.urlopen(req, timeout=20) as resp:
                    body = resp.read()
                    ctype = resp.headers.get_content_type()
                ext = mimetypes.guess_extension(ctype) or Path(ref["url"].split("?")[0]).suffix or ".jpg"
                ext = {".jpe": ".jpg", ".jpeg": ".jpg"}.get(ext, ext)
                result = (f"{slugify(hint)[:60] or 'image'}{ext}", body)
            except Exception as exc:  # network problems: keep the link instead
                self.stderr.write(f"  ! could not download {ref['url'][:80]} ({exc}); keeping the link")
        self.cache[key] = result
        return result

    def attach(self, obj, ref, hint, file_field="image", url_field="image_url"):
        """Store a picture on obj: uploaded to storage when possible, otherwise as a URL."""
        if not ref:
            return
        got = self.fetch(ref, hint)
        if got:
            name, body = got
            getattr(obj, file_field).save(name, ContentFile(body), save=False)
            if url_field:
                setattr(obj, url_field, "")
        elif url_field and "url" in ref:
            setattr(obj, url_field, ref["url"])

    @staticmethod
    def img_ref(item):
        if "local" in item:
            return {"local": item.pop("local")}
        if "url" in item:
            return {"url": item.pop("url")}
        return item.pop("img", None)

    # ------------------------------------------------------------------
    def load_settings(self, data):
        s = m.SiteSettings.load()
        cfg = dict(data.get("settings", {}))
        fresh = not s.business_jsonld
        for field in ("logo", "favicon", "social_image"):
            ref = cfg.pop(field, None)
            if ref and not getattr(s, field):
                self.attach(s, ref, field, file_field=field, url_field=None)
        if fresh:
            for k, v in cfg.items():
                setattr(s, k, v)
        s.save()

    def load_seo(self, data):
        for row in data["seo"]:
            m.PageSEO.objects.get_or_create(page=row["page"], defaults=row)

    def load_blocks(self, data):
        existing = set(m.ContentBlock.objects.values_list("key", flat=True))
        m.ContentBlock.objects.bulk_create(
            [m.ContentBlock(**row) for row in data["blocks"] if row["key"] not in existing])
        for row in data["image_blocks"]:
            if m.ImageBlock.objects.filter(key=row["key"]).exists():
                continue
            row = dict(row)
            ref = self.img_ref(row)
            obj = m.ImageBlock(**row)
            self.attach(obj, ref, row.get("alt") or row["key"])
            obj.save()

    def load_lists(self, data):
        for name, rows in data["models"].items():
            model = LIST_MODELS[name]
            if model.objects.exists():
                continue
            for row in rows:
                row = dict(row)
                ref = self.img_ref(row)
                obj = model(**row)
                if ref:
                    self.attach(obj, ref, row.get("alt") or row.get("image_alt") or row.get("name") or name)
                obj.save()
            self.stdout.write(f"  {name}: {len(rows)}")
        # homepage guide card
        for g in data.get("home_guides", []):
            guide = m.Guide.objects.filter(name=g["name"]).first()
            if guide and not guide.show_on_home:
                guide.show_on_home = True
                guide.home_summary = g["home_summary"]
                guide.save()

    def load_packages(self, data):
        if m.PackageCategory.objects.exists():
            return
        menu = {item["href"]: item["label"] for item in data.get("menu", [])}
        home_cards = {c["href"]: c for c in data.get("home_category_cards", [])}
        for row in data["categories"]:
            row = dict(row)
            packages = row.pop("packages")
            cat = m.PackageCategory(**row)
            landing = {"kilimanjaro": "kilimanjaro", "safari": "safari"}.get(cat.slug, "")
            cat.landing_page = landing
            href = f"{landing}.html" if landing else f"packages.html#{cat.slug}"
            cat.show_in_menu = href in menu
            cat.menu_label = menu.get(href, cat.name)
            card = home_cards.get(href)
            if card:
                card = dict(card)
                card.pop("href")
                ref = card.pop("home_image")
                cat.show_on_home = True
                for k, v in card.items():
                    setattr(cat, k, v)
                self.attach(cat, ref, card["home_title"], file_field="home_image", url_field="home_image_url")
            cat.save()
            for p in packages:
                p = dict(p)
                days = p.pop("days")
                ref = p.pop("img", None)
                pkg = m.Package(category=cat, **p)
                self.attach(pkg, ref, p["title"])
                pkg.save()
                m.ItineraryDay.objects.bulk_create([m.ItineraryDay(package=pkg, **d) for d in days])
            self.stdout.write(f"  {cat.name}: {len(packages)} packages")
