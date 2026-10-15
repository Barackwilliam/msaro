from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html, strip_tags
from django.utils.text import Truncator

from .models import (
    FAQ, Certification, ContentBlock, Destination, GalleryImage, Guide, GuidePhoto, HeroSlide, ImageBlock,
    ItineraryDay, Package, PackageCategory, PackingCategory, PageSEO, SiteSettings, Stat, Testimonial,
    TripOption, WhyReason,
)


def preview(src, height=60):
    if not src:
        return "—"
    return format_html('<img src="{}" style="height:{}px;width:auto;border-radius:6px;object-fit:cover;">', src, height)


class PreviewMixin:
    @admin.display(description="Photo")
    def photo(self, obj):
        return preview(getattr(obj, "src", ""))


class OrderedAdmin(admin.ModelAdmin):
    list_editable = ("order",)
    ordering = ("order", "id")


# --------------------------------------------------------------------------
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Business", {"fields": ("site_name", "site_url", "address", "hours", "email", "map_embed_url")}),
        ("Logo & icons", {"fields": ("brand_name", "brand_sub", "brand_mark", "logo", "favicon", "social_image")}),
        ("Phone & WhatsApp", {"fields": (
            "phone_display", "phone_link", "whatsapp_display", "whatsapp_number",
            "whatsapp2_display", "whatsapp2_number", "whatsapp_menu_title", "whatsapp_message",
            "booking_whatsapp_number", "pemba_whatsapp_number")}),
        ("Social media", {"fields": ("facebook_url", "instagram_url")}),
        ("Homepage", {"fields": ("hero_typed_strings",)}),
        ("SEO (advanced)", {"classes": ("collapse",), "fields": (
            "seo_author", "seo_theme_color", "seo_geo_region", "seo_geo_placename", "business_jsonld")}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = SiteSettings.load()
        return redirect(reverse("admin:website_sitesettings_change", args=[obj.pk]))


@admin.register(PageSEO)
class PageSEOAdmin(admin.ModelAdmin):
    list_display = ("page", "title")
    fields = ("page", "title", "description", "keywords", "breadcrumb_name", "extra_head")


@admin.register(ContentBlock)
class ContentBlockAdmin(admin.ModelAdmin):
    list_display = ("label", "short_text", "page")
    list_filter = ("page",)
    search_fields = ("text", "label", "key")
    fields = ("page", "label", "text", "is_html", "key")
    readonly_fields = ("key",)
    ordering = ("page", "order", "key")

    @admin.display(description="Text")
    def short_text(self, obj):
        return Truncator(strip_tags(obj.text)).chars(90)

    def get_readonly_fields(self, request, obj=None):
        return ("key",) if obj else ()


@admin.register(ImageBlock)
class ImageBlockAdmin(admin.ModelAdmin):
    list_display = ("label", "photo", "page")
    list_filter = ("page",)
    fields = ("page", "label", "image", "image_url", "alt", "photo", "key")
    readonly_fields = ("photo",)

    @admin.display(description="Current picture")
    def photo(self, obj):
        return preview(obj.src, 120)

    def get_readonly_fields(self, request, obj=None):
        return ("photo", "key") if obj else ("photo",)


# --------------------------------------------------------------------------
@admin.register(HeroSlide)
class HeroSlideAdmin(PreviewMixin, OrderedAdmin):
    list_display = ("__str__", "photo", "order")


@admin.register(Stat)
class StatAdmin(OrderedAdmin):
    list_display = ("number", "label", "order")


@admin.register(WhyReason)
class WhyReasonAdmin(OrderedAdmin):
    list_display = ("title", "placement", "order")
    list_filter = ("placement",)


@admin.register(Guide)
class GuideAdmin(PreviewMixin, OrderedAdmin):
    list_display = ("name", "role", "photo", "show_on_home", "order")
    fieldsets = (
        (None, {"fields": ("name", "role", "subtitle", "education", "languages", "bio")}),
        ("Photo", {"fields": ("image", "image_url", "image_alt")}),
        ("Social links", {"fields": ("whatsapp_url", "whatsapp_label", "facebook_url", "instagram_url")}),
        ("Homepage", {"fields": ("show_on_home", "home_summary")}),
        ("Display", {"classes": ("collapse",), "fields": ("order", "aos_delay")}),
    )


@admin.register(GuidePhoto)
class GuidePhotoAdmin(PreviewMixin, OrderedAdmin):
    list_display = ("__str__", "photo", "order")


@admin.register(PackingCategory)
class PackingCategoryAdmin(OrderedAdmin):
    list_display = ("title", "order")


@admin.register(Certification)
class CertificationAdmin(OrderedAdmin):
    list_display = ("title", "order")


@admin.register(Testimonial)
class TestimonialAdmin(PreviewMixin, OrderedAdmin):
    list_display = ("name", "short_quote", "placement", "photo", "order")
    list_filter = ("placement",)

    @admin.display(description="Quote")
    def short_quote(self, obj):
        return Truncator(obj.quote).chars(80)


@admin.register(FAQ)
class FAQAdmin(OrderedAdmin):
    list_display = ("question", "page", "order")
    list_filter = ("page",)
    search_fields = ("question", "answer")


@admin.register(GalleryImage)
class GalleryImageAdmin(PreviewMixin, OrderedAdmin):
    list_display = ("alt", "photo", "order")


@admin.register(Destination)
class DestinationAdmin(PreviewMixin, OrderedAdmin):
    list_display = ("name", "photo", "order")


@admin.register(TripOption)
class TripOptionAdmin(OrderedAdmin):
    list_display = ("label", "group", "order")
    list_filter = ("group",)


# --------------------------------------------------------------------------
class PackageInline(admin.TabularInline):
    model = Package
    fields = ("title", "days_badge", "order")
    extra = 0
    show_change_link = True


@admin.register(PackageCategory)
class PackageCategoryAdmin(OrderedAdmin):
    list_display = ("name", "menu_label", "show_in_menu", "show_on_home", "order")
    inlines = [PackageInline]
    fieldsets = (
        (None, {"fields": ("name", "slug", "pane_id", "intro", "order")}),
        ("Menu & footer", {"fields": ("show_in_menu", "menu_label", "landing_page")}),
        ("Included / not included lists", {"fields": (
            "included_title", "included_items", "excluded_title", "excluded_items")}),
        ("Homepage card", {"fields": (
            "show_on_home", "home_title", "home_image", "home_image_url", "home_image_alt",
            "home_badge", "home_text", "home_button", "home_aos_delay")}),
        ("Display (advanced)", {"classes": ("collapse",), "fields": ("card_columns",)}),
    )


class ItineraryDayInline(admin.StackedInline):
    model = ItineraryDay
    extra = 0
    fields = (("number", "order"), "title", "stats", "body")


@admin.register(Package)
class PackageAdmin(PreviewMixin, OrderedAdmin):
    list_display = ("title", "category", "days_badge", "photo", "order")
    list_filter = ("category",)
    search_fields = ("title", "description")
    inlines = [ItineraryDayInline]
    fieldsets = (
        (None, {"fields": ("category", "title", "days_badge", "price_text", "description", "features")}),
        ("Photo", {"fields": ("image", "image_url", "image_alt", "image_style", "placeholder_label")}),
        ("WhatsApp button", {"fields": ("ask_label", "ask_message", "ask_whatsapp")}),
        ("Itinerary window & booking form", {"fields": (
            "modal_title", "timeline_heading", "booking_heading", "booking_trip", "booking_whatsapp")}),
        ("Display (advanced)", {"classes": ("collapse",), "fields": ("slug", "layout", "order", "aos_delay")}),
    )
