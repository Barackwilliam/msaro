"""
Everything shown on the website lives in these tables and can be edited from
the Django admin. Images are uploaded to the Supabase Storage bucket (see
settings.py); an optional "image URL" lets you point at an external picture
instead of uploading one.
"""
from urllib.parse import quote

from django.core.exceptions import ValidationError
from django.db import models

PAGES = [
    ("global", "All pages (header, menu & footer)"),
    ("home", "Home"),
    ("about", "About Us"),
    ("guides", "Meet Our Guides"),
    ("certifications", "Certifications"),
    ("packages", "Tour Packages"),
    ("kilimanjaro", "Kilimanjaro packages"),
    ("safari", "Safari packages"),
    ("destinations", "Destinations"),
    ("gallery", "Gallery"),
    ("why-us", "Why Us"),
    ("testimonials", "Testimonials"),
    ("faq", "FAQ"),
    ("contact", "Contact"),
]

AOS_HELP = "Animation delay in milliseconds when the item scrolls into view (blank = none)."
ICON_HELP = 'Icon class, e.g. "bi bi-award-fill" (Bootstrap Icons) or "fa-brands fa-whatsapp".'


def wa_link(number, message=""):
    """https://wa.me/<number>?text=<message>, encoded like the original site."""
    url = f"https://wa.me/{number}"
    if message:
        url += "?text=" + quote(message, safe="()")
    return url


class Ordered(models.Model):
    order = models.PositiveIntegerField("Order", default=0, db_index=True,
                                        help_text="Lower numbers are shown first.")

    class Meta:
        abstract = True
        ordering = ["order", "id"]


class WithImage(models.Model):
    image = models.ImageField("Image (upload)", upload_to="site/", blank=True)
    image_url = models.URLField("…or image URL", max_length=600, blank=True,
                                help_text="Used only when no image is uploaded.")

    class Meta:
        abstract = True

    @property
    def src(self):
        if self.image:
            return self.image.url
        return self.image_url

    def clean(self):
        super().clean()
        if not self.image and not self.image_url:
            raise ValidationError("Upload an image or enter an image URL.")


# --------------------------------------------------------------------------
# Site-wide settings (one row)
# --------------------------------------------------------------------------
class SiteSettings(models.Model):
    site_name = models.CharField(max_length=120, default="Msaro Guide Tanzania")
    site_url = models.URLField("Live site address", default="https://www.msaroguidetanzania.com",
                               help_text="Used for canonical links and social-media previews.")
    brand_name = models.CharField("Logo text (bold)", max_length=60, default="Msaro Guide")
    brand_sub = models.CharField("Logo text (small)", max_length=60, default="Tanzania")
    brand_mark = models.CharField("Logo initials", max_length=4, default="MG",
                                  help_text="Shown while the logo image loads, or if there is none.")
    logo = models.ImageField(upload_to="site/", blank=True)
    favicon = models.ImageField("Browser tab icon", upload_to="site/", blank=True)
    social_image = models.ImageField("Social share image (1200×630)", upload_to="site/", blank=True,
                                     help_text="Shown when a link is shared on WhatsApp, Facebook, X…")

    address = models.CharField(max_length=200, default="Arusha, Mianzini, Tanzania")
    hours = models.CharField("Opening hours", max_length=100, default="Open 24 Hours")
    email = models.EmailField(default="info@msaroguidetanzania.com")
    phone_display = models.CharField("Phone (as shown)", max_length=40, default="+255 749 235 394")
    phone_link = models.CharField("Phone (for tap-to-call)", max_length=40, default="+255749235394",
                                  help_text="International format without spaces, e.g. +255749235394")
    whatsapp_display = models.CharField("WhatsApp (as shown)", max_length=40, default="+255 749 235 394")
    whatsapp_number = models.CharField("WhatsApp number", max_length=20, default="255749235394",
                                       help_text="Digits only with country code, no + (used in wa.me links).")
    whatsapp2_display = models.CharField("Second WhatsApp (as shown)", max_length=40, blank=True, default="0795 852 413")
    whatsapp2_number = models.CharField("Second WhatsApp number", max_length=20, blank=True, default="255795852413")
    whatsapp_message = models.CharField("Floating WhatsApp button message", max_length=300,
                                        default="Hello Msaro Guide Tanzania, I'd like to know more about your tours.")
    whatsapp_menu_title = models.CharField("Floating WhatsApp menu title", max_length=120,
                                           default="Chat on WhatsApp — choose a number")
    booking_whatsapp_number = models.CharField(
        "Contact-form WhatsApp number", max_length=20, default="255749235394",
        help_text="Booking requests from the contact page open WhatsApp to this number.")
    pemba_whatsapp_number = models.CharField(
        "Pemba trips WhatsApp number", max_length=20, default="255749235394",
        help_text="Contact-form requests for Pemba trips go to this number.")
    map_embed_url = models.URLField("Google Maps embed link", max_length=1000, blank=True,
                                    help_text="Google Maps → Share → Embed a map → copy the src=\"…\" address.")
    facebook_url = models.URLField(blank=True, default="https://www.facebook.com/share/1CoySG7f4M/")
    instagram_url = models.URLField(blank=True, default="https://www.instagram.com/msaroguidetanzania")

    hero_typed_strings = models.TextField(
        "Homepage rotating lines", blank=True,
        help_text="One line per sentence shown under the homepage headline.")

    seo_author = models.CharField(max_length=120, default="Msaro Guide Tanzania")
    seo_theme_color = models.CharField(max_length=20, default="#14213d")
    seo_geo_region = models.CharField(max_length=20, default="TZ-01")
    seo_geo_placename = models.CharField(max_length=100, default="Arusha, Tanzania")
    business_jsonld = models.TextField(
        "Business structured data (JSON-LD)", blank=True,
        help_text="Advanced SEO: the TravelAgency JSON shown to Google on every page.")

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return "Site settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def logo_src(self):
        return self.logo.url if self.logo else ""

    @property
    def favicon_src(self):
        return self.favicon.url if self.favicon else ""

    @property
    def typed_strings(self):
        return [line.strip() for line in self.hero_typed_strings.splitlines() if line.strip()]

    @property
    def whatsapp_link(self):
        return wa_link(self.whatsapp_number)

    @property
    def whatsapp_link_with_message(self):
        return wa_link(self.whatsapp_number, self.whatsapp_message)

    @property
    def whatsapp2_link_with_message(self):
        return wa_link(self.whatsapp2_number, self.whatsapp_message)


# --------------------------------------------------------------------------
# Per-page SEO and free text
# --------------------------------------------------------------------------
class PageSEO(models.Model):
    page = models.CharField(max_length=30, choices=PAGES[1:], unique=True)
    title = models.CharField("Browser / Google title", max_length=200)
    description = models.TextField("Google description", max_length=400)
    keywords = models.TextField(blank=True)
    breadcrumb_name = models.CharField(max_length=120, blank=True,
                                       help_text="Name of this page in Google's breadcrumb trail.")
    extra_head = models.TextField(
        "Extra structured data", blank=True,
        help_text="Advanced: extra JSON-LD <script> blocks for this page (FAQ and trip lists are added automatically).")

    class Meta:
        verbose_name = "Page SEO"
        verbose_name_plural = "Page SEO"
        ordering = ["page"]

    def __str__(self):
        return self.get_page_display()


class ContentBlock(models.Model):
    """A piece of text on a page (heading, paragraph, button label…)."""
    page = models.CharField(max_length=30, choices=PAGES, db_index=True)
    key = models.CharField(max_length=80, unique=True)
    label = models.CharField("Where it appears", max_length=200, blank=True)
    text = models.TextField(blank=True)
    is_html = models.BooleanField("Contains formatting (HTML)", default=False,
                                  help_text="Ticked when the text uses tags such as <strong> or links.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Page text"
        verbose_name_plural = "Page texts"
        ordering = ["page", "order", "key"]

    def __str__(self):
        return self.label or self.key


class ImageBlock(models.Model):
    """A single picture on a page that isn't part of a list."""
    page = models.CharField(max_length=30, choices=PAGES, db_index=True)
    key = models.CharField(max_length=80, unique=True)
    label = models.CharField("Where it appears", max_length=200, blank=True)
    image = models.ImageField("Image (upload)", upload_to="site/", blank=True)
    image_url = models.URLField("…or image URL", max_length=600, blank=True)
    alt = models.CharField("Description (for Google & screen readers)", max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Page picture"
        verbose_name_plural = "Page pictures"
        ordering = ["page", "order", "key"]

    def __str__(self):
        return self.label or self.key

    @property
    def src(self):
        return self.image.url if self.image else self.image_url


# --------------------------------------------------------------------------
# Home page
# --------------------------------------------------------------------------
class HeroSlide(WithImage, Ordered):
    class Meta(Ordered.Meta):
        verbose_name = "Homepage background photo"
        verbose_name_plural = "Homepage background photos"

    def __str__(self):
        return f"Slide {self.order}"


class Stat(Ordered):
    number = models.CharField(max_length=40)
    label = models.CharField(max_length=120)

    class Meta(Ordered.Meta):
        verbose_name = "Key fact (Home & About)"
        verbose_name_plural = "Key facts (Home & About)"

    def __str__(self):
        return f"{self.number} — {self.label}"


class WhyReason(Ordered):
    HOME, PAGE = "home", "why-us"
    placement = models.CharField(max_length=10, choices=[(HOME, "Home page"), (PAGE, "Why Us page")], default=PAGE)
    icon = models.CharField(max_length=60, help_text=ICON_HELP)
    title = models.CharField(max_length=120)
    text = models.TextField()
    aos_delay = models.PositiveIntegerField(null=True, blank=True, help_text=AOS_HELP)

    class Meta(Ordered.Meta):
        verbose_name = "Reason to choose us"
        verbose_name_plural = "Reasons to choose us"

    def __str__(self):
        return self.title


# --------------------------------------------------------------------------
# Guides
# --------------------------------------------------------------------------
class Guide(WithImage, Ordered):
    name = models.CharField(max_length=120)
    image_alt = models.CharField(max_length=200, blank=True)
    role = models.CharField("Badge on photo", max_length=120)
    subtitle = models.CharField("Line under the name", max_length=200, blank=True)
    education = models.CharField(max_length=200, blank=True)
    languages = models.CharField(max_length=200, blank=True, help_text="Comma separated, e.g. English, Spanish, Swahili")
    bio = models.TextField(blank=True)
    whatsapp_url = models.URLField(blank=True)
    whatsapp_label = models.CharField(max_length=80, blank=True, default="WhatsApp")
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    show_on_home = models.BooleanField("Show on the homepage", default=False)
    home_summary = models.CharField("Short text on the homepage", max_length=300, blank=True)
    aos_delay = models.PositiveIntegerField(null=True, blank=True, help_text=AOS_HELP)

    class Meta(Ordered.Meta):
        verbose_name = "Guide"
        verbose_name_plural = "Guides"

    def __str__(self):
        return self.name

    @property
    def language_list(self):
        return [x.strip() for x in self.languages.split(",") if x.strip()]

    @property
    def has_socials(self):
        return bool(self.whatsapp_url or self.facebook_url or self.instagram_url)


class GuidePhoto(WithImage, Ordered):
    alt = models.CharField("Description", max_length=200, blank=True)
    aos_delay = models.PositiveIntegerField(null=True, blank=True, help_text=AOS_HELP)

    class Meta(Ordered.Meta):
        verbose_name = "Guide page photo"
        verbose_name_plural = "Guide page photos"

    def __str__(self):
        return self.alt or f"Photo {self.pk}"


class PackingCategory(Ordered):
    icon = models.CharField(max_length=60, help_text=ICON_HELP)
    title = models.CharField(max_length=120)
    items = models.TextField(help_text="One item per line.")
    aos_delay = models.PositiveIntegerField(null=True, blank=True, help_text=AOS_HELP)

    class Meta(Ordered.Meta):
        verbose_name = "Packing list"
        verbose_name_plural = "Packing lists"

    def __str__(self):
        return self.title

    @property
    def item_list(self):
        return [x.strip() for x in self.items.splitlines() if x.strip()]


class Certification(Ordered):
    icon = models.CharField(max_length=60, help_text=ICON_HELP)
    title = models.CharField(max_length=120)
    text = models.TextField()
    aos_delay = models.PositiveIntegerField(null=True, blank=True, help_text=AOS_HELP)

    class Meta(Ordered.Meta):
        verbose_name = "Certification"
        verbose_name_plural = "Certifications"

    def __str__(self):
        return self.title


# --------------------------------------------------------------------------
# Testimonials, FAQ, gallery, destinations
# --------------------------------------------------------------------------
class Testimonial(WithImage, Ordered):
    HOME, PAGE = "home", "testimonials"
    placement = models.CharField(max_length=15, choices=[(HOME, "Home page"), (PAGE, "Testimonials page")], default=PAGE)
    quote = models.TextField()
    name = models.CharField(max_length=120)
    trip = models.CharField(max_length=120, blank=True)
    image_alt = models.CharField(max_length=200, blank=True, default="Traveler review")
    stars = models.PositiveSmallIntegerField(default=5)

    class Meta(Ordered.Meta):
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.name}: {self.quote[:50]}"

    def clean(self):
        pass  # the photo is optional

    @property
    def star_range(self):
        return range(min(max(self.stars, 0), 5))


class FAQ(Ordered):
    PAGE_CHOICES = [("faq", "FAQ page"), ("kilimanjaro", "Kilimanjaro page"), ("safari", "Safari page")]
    page = models.CharField(max_length=15, choices=PAGE_CHOICES, default="faq")
    question = models.CharField(max_length=300)
    answer = models.TextField()

    class Meta(Ordered.Meta):
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class GalleryImage(WithImage, Ordered):
    alt = models.CharField("Description", max_length=200)
    aos_delay = models.PositiveIntegerField(null=True, blank=True, help_text=AOS_HELP)

    class Meta(Ordered.Meta):
        verbose_name = "Gallery photo"
        verbose_name_plural = "Gallery photos"

    def __str__(self):
        return self.alt


class Destination(WithImage, Ordered):
    name = models.CharField(max_length=120)
    image_alt = models.CharField(max_length=200, blank=True)

    class Meta(Ordered.Meta):
        verbose_name = "Destination"
        verbose_name_plural = "Destinations"

    def __str__(self):
        return self.name


class TripOption(Ordered):
    group = models.CharField(max_length=120, blank=True,
                             help_text="Heading in the contact-form dropdown. Leave blank for a stand-alone option.")
    label = models.CharField(max_length=200)

    class Meta(Ordered.Meta):
        verbose_name = "Contact form trip option"
        verbose_name_plural = "Contact form trip options"

    def __str__(self):
        return f"{self.group} › {self.label}" if self.group else self.label


# --------------------------------------------------------------------------
# Tour packages
# --------------------------------------------------------------------------
class PackageCategory(Ordered):
    name = models.CharField("Tab name", max_length=120)
    slug = models.SlugField("Link anchor", max_length=40, unique=True,
                            help_text='Used in links like packages.html#meru')
    pane_id = models.SlugField("Tab id", max_length=40, unique=True, help_text="e.g. pkg-meru")
    card_columns = models.CharField("Card width classes", max_length=60, default="col-md-6 col-lg-4")
    intro = models.TextField("Intro text above the cards", blank=True)

    show_in_menu = models.BooleanField("Show in the Packages menu & footer", default=True)
    menu_label = models.CharField(max_length=120, blank=True)
    landing_page = models.CharField(
        "Has its own page", max_length=20, blank=True,
        choices=[("", "No"), ("kilimanjaro", "kilimanjaro.html"), ("safari", "safari.html")])

    included_title = models.CharField(max_length=120, blank=True, default="What's Included")
    included_items = models.TextField("Included (one per line)", blank=True)
    excluded_title = models.CharField(max_length=120, blank=True, default="What's Not Included")
    excluded_items = models.TextField("Not included (one per line)", blank=True)

    show_on_home = models.BooleanField("Show a card on the homepage", default=False)
    home_title = models.CharField(max_length=120, blank=True)
    home_image = models.ImageField(upload_to="site/", blank=True)
    home_image_url = models.URLField(max_length=600, blank=True)
    home_image_alt = models.CharField(max_length=200, blank=True)
    home_badge = models.CharField(max_length=60, blank=True)
    home_text = models.CharField(max_length=200, blank=True)
    home_button = models.CharField(max_length=60, blank=True, default="View Details")
    home_aos_delay = models.PositiveIntegerField(null=True, blank=True, help_text=AOS_HELP)

    class Meta(Ordered.Meta):
        verbose_name = "Package category"
        verbose_name_plural = "Package categories"

    def __str__(self):
        return self.name

    @property
    def url(self):
        if self.landing_page:
            return f"{self.landing_page}.html"
        return f"packages.html#{self.slug}"

    @property
    def home_src(self):
        return self.home_image.url if self.home_image else self.home_image_url

    @property
    def included_list(self):
        return [x.strip() for x in self.included_items.splitlines() if x.strip()]

    @property
    def excluded_list(self):
        return [x.strip() for x in self.excluded_items.splitlines() if x.strip()]


class Package(WithImage, Ordered):
    IMG_NORMAL, IMG_BOXED = "normal", "boxed"
    LAYOUT_COMPACT, LAYOUT_DETAILED = "compact", "detailed"

    category = models.ForeignKey(PackageCategory, related_name="packages", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField("Itinerary id", max_length=60, unique=True,
                            help_text='Short id used by the "View Full Itinerary" button, e.g. machame')
    days_badge = models.CharField(max_length=80, blank=True)
    image_alt = models.CharField(max_length=200, blank=True)
    placeholder_label = models.CharField(
        "Placeholder caption", max_length=200, blank=True,
        help_text="Small caption shown only if the photo can't load.")
    image_style = models.CharField(max_length=10, default=IMG_NORMAL, choices=[
        (IMG_NORMAL, "Normal photo"), (IMG_BOXED, "Photo inside a placeholder box")])
    layout = models.CharField(max_length=10, default=LAYOUT_COMPACT, choices=[
        (LAYOUT_COMPACT, "Compact card"), (LAYOUT_DETAILED, "Detailed card (equal height, feature list)")])
    price_text = models.CharField(max_length=120, blank=True)
    description = models.TextField()
    features = models.TextField("Features (one per line)", blank=True)
    ask_label = models.CharField('"Ask" button text', max_length=80, blank=True,
                                 help_text="Leave blank to hide the WhatsApp button.")
    ask_message = models.CharField("WhatsApp message", max_length=300, blank=True)
    ask_whatsapp = models.CharField("WhatsApp number (optional)", max_length=20, blank=True,
                                    help_text="Leave blank to use the main WhatsApp number.")
    aos_delay = models.PositiveIntegerField(null=True, blank=True, help_text=AOS_HELP)

    modal_title = models.CharField("Itinerary window title", max_length=200)
    timeline_heading = models.CharField(max_length=120, default="Full Day-by-Day Itinerary")
    booking_heading = models.CharField(max_length=200,
                                       default="Book This Trip — We'll Send Your Details via WhatsApp")
    booking_trip = models.CharField("Trip name in booking requests", max_length=200)
    booking_whatsapp = models.CharField("Booking WhatsApp number (optional)", max_length=20, blank=True)

    class Meta(Ordered.Meta):
        verbose_name = "Tour package"
        verbose_name_plural = "Tour packages"

    def __str__(self):
        return self.title

    def clean(self):
        pass  # image optional

    @property
    def feature_list(self):
        return [x.strip() for x in self.features.splitlines() if x.strip()]

    def ask_url(self, site):
        return wa_link(self.ask_whatsapp or site.whatsapp_number, self.ask_message)

    def booking_number(self, site):
        return self.booking_whatsapp or site.whatsapp_number


class ItineraryDay(Ordered):
    package = models.ForeignKey(Package, related_name="days", on_delete=models.CASCADE)
    number = models.CharField("Day", max_length=10)
    title = models.CharField(max_length=300)
    stats = models.TextField(
        "Quick facts", blank=True,
        help_text='One per line as "icon | text", e.g. "bi-signpost-split | 8km". '
                  'Icons: bi-signpost-split, bi-clock, bi-arrow-up-right, bi-tree, bi-cloud…')
    body = models.TextField()

    class Meta(Ordered.Meta):
        verbose_name = "Itinerary day"
        verbose_name_plural = "Itinerary days"

    def __str__(self):
        return f"Day {self.number}: {self.title}"

    @property
    def stat_list(self):
        out = []
        for line in self.stats.splitlines():
            if not line.strip():
                continue
            icon, _, text = line.partition("|")
            icon = icon.strip()
            if icon and not icon.startswith("bi ") and icon.startswith("bi-"):
                icon = "bi " + icon
            out.append((icon, text.strip()))
        return out
