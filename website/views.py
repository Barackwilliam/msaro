import json
from itertools import groupby

from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import render

from .models import (
    FAQ, Certification, Destination, GalleryImage, Guide, GuidePhoto, HeroSlide, ItineraryDay, Package,
    PackageCategory, PackingCategory, PageSEO, SiteSettings, Stat, Testimonial, TripOption, WhyReason,
)

# page key -> (template, value of <body data-page="…">)
PAGES = {
    "home": ("website/pages/home.html", "home"),
    "about": ("website/pages/about.html", "about"),
    "guides": ("website/pages/guides.html", "guides"),
    "certifications": ("website/pages/certifications.html", "certifications"),
    "packages": ("website/pages/packages.html", "packages"),
    "kilimanjaro": ("website/pages/kilimanjaro.html", "packages"),
    "safari": ("website/pages/safari.html", "packages"),
    "destinations": ("website/pages/destinations.html", "destinations"),
    "gallery": ("website/pages/gallery.html", "gallery"),
    "why-us": ("website/pages/why_us.html", "why-us"),
    "testimonials": ("website/pages/testimonials.html", "testimonials"),
    "faq": ("website/pages/faq.html", "faq"),
    "contact": ("website/pages/contact.html", "contact"),
}


def _packages_queryset():
    return Package.objects.prefetch_related(Prefetch("days", queryset=ItineraryDay.objects.all()))


def _faq_jsonld(faqs):
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": f.question,
             "acceptedAnswer": {"@type": "Answer", "text": f.answer}}
            for f in faqs
        ],
    }
    return json.dumps(data, indent=2, ensure_ascii=False).replace("</", "<\\/")


def page(request, page="home"):
    if page not in PAGES:
        raise Http404
    template, body_page = PAGES[page]
    site = SiteSettings.load()
    seo = PageSEO.objects.filter(page=page).first() or PageSEO(page=page, title=site.site_name, description="")

    base_url = site.site_url.rstrip("/")
    social = site.social_image.url if site.social_image else ""
    if social.startswith("/"):
        social = base_url + social

    ctx = {
        "page": page,
        "seo": seo,
        "body_page": body_page,
        "canonical_url": f"{base_url}/" if page == "home" else f"{base_url}/{page}.html",
        "social_image_url": social,
        "site_config": {
            "siteName": site.site_name,
            "typedStrings": site.typed_strings,
            "bookingWhatsApp": site.booking_whatsapp_number,
            "pembaWhatsApp": site.pemba_whatsapp_number,
            "whatsApp": site.whatsapp_number,
            "pembaTrips": list(TripOption.objects.filter(group__icontains="pemba").values_list("label", flat=True)),
        },
    }

    if page == "home":
        ctx.update(
            hero_slides=HeroSlide.objects.all(),
            stats=Stat.objects.all(),
            home_guides=Guide.objects.filter(show_on_home=True),
            home_reasons=WhyReason.objects.filter(placement=WhyReason.HOME),
            home_categories=PackageCategory.objects.filter(show_on_home=True),
            testimonials=Testimonial.objects.filter(placement=Testimonial.HOME),
        )
    elif page == "about":
        ctx["stats"] = Stat.objects.all()
    elif page == "guides":
        ctx.update(guides=Guide.objects.all(), guide_photos=GuidePhoto.objects.all(),
                   packing=PackingCategory.objects.all())
    elif page == "certifications":
        ctx["certifications"] = Certification.objects.all()
    elif page == "packages":
        cats = list(PackageCategory.objects.prefetch_related(Prefetch("packages", queryset=_packages_queryset())))
        ctx.update(categories=cats, modal_packages=[p for c in cats for p in c.packages.all()])
    elif page in ("kilimanjaro", "safari"):
        cat = (PackageCategory.objects.filter(landing_page=page)
               .prefetch_related(Prefetch("packages", queryset=_packages_queryset())).first())
        faqs = list(FAQ.objects.filter(page=page))
        ctx.update(category=cat, faqs=faqs, faq_jsonld=_faq_jsonld(faqs) if faqs else "",
                   modal_packages=list(cat.packages.all()) if cat else [])
    elif page == "destinations":
        ctx["destinations"] = Destination.objects.all()
    elif page == "gallery":
        ctx["gallery"] = GalleryImage.objects.all()
    elif page == "why-us":
        ctx["reasons"] = WhyReason.objects.filter(placement=WhyReason.PAGE)
    elif page == "testimonials":
        ctx["testimonials"] = Testimonial.objects.filter(placement=Testimonial.PAGE)
    elif page == "faq":
        faqs = list(FAQ.objects.filter(page="faq"))
        ctx.update(faqs=faqs, faq_jsonld=_faq_jsonld(faqs) if faqs else "")
    elif page == "contact":
        options = list(TripOption.objects.all())
        ctx["trip_groups"] = [(g, list(items)) for g, items in groupby(options, key=lambda o: o.group)]

    return render(request, template, ctx)
