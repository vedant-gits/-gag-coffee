from django.urls import path
from . import views

urlpatterns = [
    # Orders
    path("orders/",                        views.orders,              name="orders"),
    path("orders/<str:order_id>/",         views.order_detail,        name="order-detail"),
    path("orders/<str:order_id>/status/",  views.update_order_status, name="order-status"),

    # Contact
    path("contact/",                       views.contact,             name="contact"),

    # Auth
    path("auth/login/",                    views.login_view,          name="login"),
    path("auth/refresh/",                  views.refresh_view,        name="refresh"),

    # Admin Stats
    path("admin/stats/",                   views.admin_stats,         name="admin-stats"),

    # Menu
    path("menu/",                          views.menu,                name="menu"),
    path("menu/<str:item_id>/",            views.menu_item,           name="menu-item"),

    # Order tracking (public)
    path("orders/track/<str:order_id>/",   views.track_order,         name="track-order"),

    # Orders by phone (public)
    path("orders/by-phone/",               views.orders_by_phone,     name="orders-by-phone"),
]
