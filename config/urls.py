from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("mall/", include("mall.urls")),
    path("mall_sample/", include("mall_sample.urls")),
    path("", TemplateView.as_view(template_name="root.html"), name="root"),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    static(settings.MEDIA_URL, document_url=settings.MEDIA_ROOT)
