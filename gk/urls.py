from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mainApp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    
    path('shop/<str:mc>/<str:sc>/<str:br>/',views.shop),
    path('singleProduct/<int:id>/',views.singleProduct),
    path('login/', views.login, name='login'),  # ✅ Add this,
    path('signup/', views.signup, name='signup'),
    path('profile/',views.profilePage),
    path('logout/',views.logout),
    path('updateprofile/',views.updateSellerProfile),
    path('add-product/',views.addProduct),
    path('update-Product/<int:id>/',views.updateProduct),
    path('delete-Product/<int:id>/', views.deleteProduct, name='delete-Product'),
    path('delete-order/<int:id>/', views.delete_order, name='delete_order'),
    path('add-to-Wishlist/<int:id>/',views.addToWishlist),
    path('delete-wishlist/<int:id>/',views.deleteWishlist),
    path('add-to-cart/<int:id>/',views.addToCart),
    path('remove-from-cart/<int:id>/',views.removeFromCart),
    path('update-cart/<int:id>/<int:num>/',views.updateCart),
    path('cart/',views.cartPage),
    path('about/',views.aboutPage),
    path('newslatter/',views.newsletter_signup),    
    path("forget/", views.forget_password, name="forget_password"),
    path('forget/verify_otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),    
    path('confirmation/', views.confirmation, name='confirmation'),
    path('place_order/', views.place_order, name='place_order'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('checkout/', views.checkoutPage, name='checkout'),
    path('contact/', views.contactpage, name='contact')
    
    



]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
