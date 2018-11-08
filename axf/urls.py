from django.conf.urls import url
from axf import views
urlpatterns=[
    url(r"^home$", views.home, name='home'),
    url(r"^market_with_params/(\d+)/(\d+)/(\d+)", views.market_with_params, name='market_with_params'),
    url(r"^market$", views.market, name='market'),
    url(r"^cart$", views.cart, name='cart'),
    url(r"^mine$", views.mine, name='mine'),
    url(r"^register$", views.register.as_view(), name="register"),
    url(r"^login$", views.login_1.as_view(), name="login"),
    url(r"^confirm/(.*)", views.confirm, name="confirm"),
    url(r"^logout$", views.logout_1.as_view(), name="logout"),
    url(r"^check_uname",views.check_uname),
    url(r"^cart_api$", views.cart_api.as_view()),
    url(r"^cart_status$", views.cart_status.as_view()),
    url(r"^cartall_status$", views.cartall_status.as_view()),
    # url(r"^cart_item$", views.cart_item.as_view()),
    # url(r"^cart_order",views.order.as_view(), name='order'),
]