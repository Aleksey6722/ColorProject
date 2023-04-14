from . import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from core.views import index, sign_in, sign_up, find_cars, Fav, sign_out, about

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("signin", sign_in, name="signin"),
    path("signup", sign_up, name="signup"),
    path("api/", include('core.urls')),
    path("find-cars", find_cars, name='find-cars'),
    path("fav", Fav.as_view(), name="fav"),
    path("signout", sign_out, name="signout"),
    path("about", about, name="about"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)