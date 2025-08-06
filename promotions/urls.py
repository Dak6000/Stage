from django.conf import settings
from django.conf.urls.static import static

from accounts.urls import app_name

app_name = "promotions"
urlpatterns = [

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)