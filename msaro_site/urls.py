from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from website import views

admin.site.site_header = "Msaro Guide Tanzania — Website Admin"
admin.site.site_title = "Msaro Guide Admin"
admin.site.index_title = "Edit your website"

# The old static site used addresses like /about.html; they are kept exactly
# so links already shared on Google, WhatsApp and Facebook keep working.
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.page, {"page": "home"}, name="home"),
    path("index.html", views.page, {"page": "home"}),
] + [
    path(f"{key}.html", views.page, {"page": key}, name=key)
    for key in views.PAGES if key != "home"
]

if settings.DEBUG and not settings.USE_SUPABASE_STORAGE:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
