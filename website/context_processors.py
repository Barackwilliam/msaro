from .models import ContentBlock, ImageBlock, PackageCategory, SiteSettings


def site(request):
    """Data every page needs: settings, menu and all editable text blocks."""
    if request.path.startswith("/admin"):
        return {}
    return {
        "site": SiteSettings.load(),
        "menu_categories": PackageCategory.objects.filter(show_in_menu=True),
        "blocks": {b.key: b for b in ContentBlock.objects.all()},
        "image_blocks": {b.key: b for b in ImageBlock.objects.all()},
    }
