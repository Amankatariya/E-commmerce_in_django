from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include
from app.views import *
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from django.views.generic.base import RedirectView




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('base/', base, name='base'),
    path('aboutus/', about, name='about_us'),
    path('shop/', shop, name='shop'),
    path('contactus/', contact, name='contact_us'),
    path('products/<slug:slug>/',product_detail, name='product_detail'),
    path('error/404/' ,error ,name='error'),
    path('orders/' ,myorder ,name='myorder'),
    path('ordersji/' ,myorderji ,name='myorderji'),
    path('cancel-order/<id>',cancel_order, name='cancel_order'),


    
#===============================================================#
#CART URLS :-

    path('cart/add/<int:id>/',cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/',item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',item_decrement, name='item_decrement'),
    path('cart/cart_clear/',cart_clear, name='cart_clear'),
    path('cart/cart-detail/',cart_detail,name='cart_detail'),

#===================================================================#
    
    path('cart/cart-detail/checkout',checkout,name='checkout'),
    path('cart/cart-detail/checkout/placeorder',placeorder,name='placeorder'),
    path('cart/cart-detail/checkout/placeorder/thankyou',thankyoupage,name='thankyou'),
    path('cart/cart-detail/checkout/placeorder/success/', success, name='success'),
    path('cart/cart-detail/checkout/placeorder/success', RedirectView.as_view(url='/cart/cart-detail/checkout/placeorder/success/')),

  






    
#==================ACCOUT VIEWS FUN()===================#
    path('accounts/login', account, name='account'),
    path('accounts/rigster', rigester, name='account_rigester'),
    path('accounts/login_user', login_user, name='handlelogin'),
    path('accounts/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='set_password.html'), name='password_reset_confirm'),
    # path('accounts/profile', home, name='home'),
    path('accounts/password_reset/', PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('accounts/password_reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
     path('accounts/reset/done/', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile', profile,name='profile'),
    path('accounts/profile/update', profile_update ,name='profile_update'),

] +static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

