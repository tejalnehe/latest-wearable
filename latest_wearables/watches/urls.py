from watches import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('navbar/',views.navbar),
    path('home/',views.home, name='home'),
    path('collection/',views.collections, name='collections'),
    path('aboutus/',views.aboutus, name='about_us'),
    path('cart/',views.cart, name='cart'),
    path('signup/',views.signup, name="signup"),
    path('login/',views.log_in, name="login"),
    path('',views.home, name="home"),
    path('logout/',views.log_out, name="logout"),
    path('watch_details/<int:id>/',views.watchDetailView.as_view(),name='watchdetails'),
    path('view_cart/',views.view_cart, name="viewcart"),
    path('add_to_cart/<int:id>/',views.add_to_cart, name="addtocart"),
    path('add_quantity/<int:id>/', views.add_quantity, name='add_quantity'),
    path('delete_quantity/<int:id>/', views.delete_quantity, name='delete_quantity'),
    path('delete/<int:id>/',views.delete,name='delete'),
    path('address/',views.address,name='address'),
    path('delete_address/<int:id>',views.delete_address,name='deleteaddress'),
    path('checkout/',views.checkout,name='checkout'),
    path('profile/',views.profile,name='profile'),
    path('changepassword/',views.changepassword, name="changepassword"),

    path('payment/',views.payment,name='payment'),
    
    path('payment_success/<int:selected_address_id>/',views.payment_success,name='paymentsuccess'),

    path('payment_failed/',views.payment_failed,name='paymentfailed'),

    path('order/',views.order,name='order'),

    path('buynow/<int:id>',views.buynow,name='buynow'),

    path('buynow_payment/<int:id>',views.buynow_payment,name='buynowpayment'),

    path('buynow_payment_success/<int:selected_address_id>/<int:id>',views.buynow_payment_success,name='buynowpaymentsuccess'),


    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
