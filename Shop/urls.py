from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm
urlpatterns = [
    # path('',views.index, name='index'),
    path('',views.ProductView.as_view(),name='index'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('address/',views.address,name='address'),
    path('add_to_cart/',views.add_to_cart,name='add_to_cart'),
    path('cart/',views.show_cart,name='showcart'),
    path('pluscart/',views.plus_cart,name='pluscart'),
    path('minuscart/',views.minus_cart,name='minuscart'),
    path('removecart/',views.remove_cart,name='remove-cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('paymentdone/',views.paymentdone,name='paymentdone'),
    path('orders/',views.orders,name='orders'),
    path('productDetails/<int:id>',views.productDetails,name='productDetails'),
    path('registration/',views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='registration/login.html',
                                                        authentication_form=LoginForm),name='login'),

    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name="logout")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)