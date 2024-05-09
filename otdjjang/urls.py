from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from otdjjangapi.models import *
from otdjjangapi.views import *
from django.conf.urls.static import static

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"brands", Brands, "brand")
router.register(r"types", Types, "type")
router.register(r"sizes", Sizes, "size")
router.register(r"articles", Articles, "article")
router.register(r"userarticles", UserArticles, "userarticle")
router.register(r"outfits", Outfits, "outfit")
router.register(r"outfitarticles", OutfitArticles, "outfitarticle")
router.register(r"outfitphotos", OutfitPhotos, "outfitphoto")


urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path("api-token-auth", obtain_auth_token),
    path("api-auth", include("rest_framework.urls", namespace="rest_framework")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
