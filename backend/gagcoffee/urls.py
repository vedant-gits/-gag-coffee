from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
]

# Customise the admin site header
admin.site.site_header  = "GAG Coffee Co. Admin"
admin.site.site_title   = "GAG Coffee"
admin.site.index_title  = "Dashboard"
