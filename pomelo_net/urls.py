"""pomelo_net URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from pomelo.views import *
from . import settings
from django.contrib.staticfiles.urls import static
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from cart.views import *

urlpatterns = [
    # Strona Administracyjna
    url(r'^admin/', admin.site.urls),
    # Homepage
    url(r'^$', HomePageView.as_view(), name='home'),
    # Widok koszyka
    url(r'^cart/$', CartPageView.as_view(), name='cart'),
    # Formularz Kontaktowy
    url(r'^contact$', ContactView.as_view(), name='contact'),
    # Detale Produktu
    url(r'^product/(?P<pk>[0-9]+)/$', ProductDetailView.as_view(), name='product_page'),
    # Modal logowania
    url(r'^login/$', CustomLoginView.as_view(), name='login'),
    # Logowanie alternatywne
    url(r'^login_alt/$', CustomLoginView.as_view(template_name='login_alt.html'), name='login_alt'),
    # Wylogowywanie
    url(r'^logout/$', CustomLogoutView.as_view(), name='logout'),
    # Rejestracja
    url('^register/', RegisterView.as_view(), name='register'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),
    # Kategorie
    url(r'^categories/$', CategoriesView.as_view(), name='category'),
    # Produkty po kategoriach
    url(r'^category/(?P<pk>[0-9]+)/(?P<name>[-\w])+', CategoryProductsView.as_view(), name='category_products'),
    # Produkty po przecenach
    url(r'^products/$', ProductOffers.as_view(), name='offers'),
    # Dodawanie do koszyka
    url(r'^add/(?P<product_id>\d+)/$', cart_add, name='cart_add'),
    # Usuwanie z koszyka
    url(r'^remove/(?P<product_id>\d+)/$', cart_remove, name='cart_remove'),
    # Aktualizowanie koszyka
    url(r'^update/$', cart_update, name='cart_update'),
    # Czyszczenie koszyka
    url(r'^clear/$', cart_clear, name='cart_clear'),
    # Edycja profilu
    url(r'^update_profile/$', UpdateProfileView.as_view(), name='update_profile'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)

