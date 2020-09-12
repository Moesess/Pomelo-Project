# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import FormView
from .models import *
from .forms import ContactForm
from django.contrib.auth import login as auth_login, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from bootstrap_modal_forms.mixins import LoginAjaxMixin
from .forms import CustomAuthenticationForm, RegisterForm
from django.core.mail import send_mail
from pomelo_net import settings
from cart.cart import Cart
from cart.forms import CartAddProductForm
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib import messages
from forms import *
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.http import HttpResponse


class HomePageView(ListView):
    """
    Widok wyświetlający stronę główną.
    """
    template_name = "homepage.html"
    model = Product

    def get_context_data(self, *args, **kwargs):
        """
        Funkcja odpowiada za przekazywanie contextu, czyli danych z obiektów i ogólnie z tej funkcji (title np.).
        Innymi słowy, by móc wyświetlić obiekt na stronie. W tym przypadku Produkty na stronie głównej.
        """
        title = "Pomelo.Net | Najlepszy sklep pod słońcem"

        context = {'title': title,
                   'product': Product.objects.all(),
                   'discount': ProductDiscount.objects.all(),
                   'category': Category.objects.all()
                   }

        return context


class ProductDetailView(DetailView, CreateView):
    """
    Widok odpowiadający za detale produktu, czyli wyświetla strone tego produktu po kliknieciu na niego.
    """
    template_name = "product.html"
    model = Product
    form_class = ReviewForm

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        title = "Pomelo.Net | " + self.object.name
        total_quantity = 0

        cart_product_form = CartAddProductForm(
            initial={
                'quantity': 1
            })
        if self.request.user.is_authenticated():
            user_form = User.objects.get(id=self.request.user.id)
        else:
            user_form = None

        product_review_form = ReviewForm(
            initial={
                'user': user_form,
                'product': self.object.id
            })

        # obliczam ilość produktu we wszystkich magazynach
        for stock in self.object.ProductStatus.all():
            total_quantity += stock.quantity

        # zapisuje produkty powiązane po kategorii
        related = Product.objects.all().filter(category=self.object.category)

        # Jeśli nie bedzie obniżki w bazie danych przydzielam jej 0
        try:
            discount = ProductDiscount.objects.get(product=self.object)
        except ProductDiscount.DoesNotExist:
            discount = 0

        context.update({
            'title': title,
            'product': Product.objects.all(),
            'images': self.object.images,
            'quantity': total_quantity,
            'related': related,
            'discount': discount,
            'category': Category.objects.all(),
            'form_cart': cart_product_form,
            'form': product_review_form
        })

        return context

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, "Pomyślnie dodano opinię")
        return HttpResponseRedirect(self.request.path_info)

    def form_invalid(self, form):
        print form.errors
        messages.add_message(
            self.request, messages.WARNING, 'Wystąpił problem z formularzem. Popraw błedy i spróbuj ponownie'
        )
        return HttpResponseRedirect(self.request.path_info)


class CategoriesView(ListView):
    """
    Widok Kategorii, pokazuje wszystkie dostepne kategorie
    """
    template_name = 'categories.html'
    model = Category

    def get_queryset(self):
        if self.request.GET.get('sort'):
            order = self.request.GET.get('sort')
            return super(CategoriesView, self).get_queryset().order_by(order)
        else:
            return super(CategoriesView, self).get_queryset().order_by('name')

    def get_context_data(self, *args, **kwargs):
        context = super(CategoriesView, self).get_context_data(**kwargs)
        title = "Pomelo.Net | Kategorie Produktów"

        context.update({
            'title': title,
            'category': Category.objects.all()
        })

        return context


class CartPageView(TemplateView):
    """
    Widok koszyka
    """
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super(CartPageView, self).get_context_data(**kwargs)
        title = "Pomelo.Net | Koszyk"

        cart = Cart(self.request)

        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(
                initial={
                    'quantity': item['quantity'],
                    'update': True
                })

        context.update({
            'cart': cart,
            'title': title,
            'category': Category.objects.all()
        })
        return context


class ContactView(FormView):
    """
    Widok odpowiadajacy za formularz kontaktowy.
    """
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/'

    def form_valid(self, form):
        """
        Jeśli formularz będzie prawidłowy
        :param form:
        :return: Widok Formularza Kontaktowego i przesłanie wiadomości email na naszą skrzynkę pocztową.
        """
        message = "{name} / {email} said: ".format(
            name=form.cleaned_data.get("name"),
            email=form.cleaned_data.get("email")
        )
        message += "\n\n{0}".format(form.cleaned_data.get("message"))
        send_mail(
            subject=form.cleaned_data.get("subject").strip(),
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER]
        )
        messages.add_message(self.request, messages.SUCCESS, "Pomyślnie wysłano wiadomość. Odpowiemy jak najprędzej!")
        return super(ContactView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        title = "Pomelo.Net | Kontakt"

        context.update({
            'title': title,
            'category': Category.objects.all()
        })
        return context


class CustomLoginView(LoginAjaxMixin, LoginView, FormView):
    """
    Widok odpowiadający za wyświetlenie modala z logowaniem
    """
    authentication_form = CustomAuthenticationForm
    template_name = 'components/login.html'
    success_url = "/"

    def form_valid(self, form):
        """
        Jeśli formularz przejdzie prawidłowo
        :param form:
        :return: Logowanie użytkownika wraz z weryfikacją.
        """
        auth_login(self.request, form.get_user())
        messages.add_message(self.request, messages.SUCCESS, "Zalogowano")
        url = "http://" + self.request.META['HTTP_HOST'] + '/login/'

        if self.request.META['HTTP_REFERER'] == url:
            return redirect('home')
        else:
            return redirect(self.request.META['HTTP_REFERER'])

    def form_invalid(self, form):
        """
        Jeśli zostały wprowadzone błędne dane.
        :param form:
        :return: Formularz Logowania z errorami.
        """
        title = "Pomelo.Net | Logowanie"

        return render(self.request, 'login_alt.html', {'form': form, 'title': title})


class CustomLogoutView(LogoutView):
    """
    Wylogowywanie użytkownika, widok po prostu usuwa sesję.
    """
    template_name = "homepage.html"

    def get_next_page(self):
        messages.add_message(self.request, messages.SUCCESS, "Wylogowano")
        url = "http://"+self.request.META['HTTP_HOST']+'/update_profile/'
        if self.request.META['HTTP_REFERER'] == url:
            next_page = '/'
        else:
            next_page = self.request.META['HTTP_REFERER']
        return next_page


class RegisterView(CreateView):
    template_name = 'components/register.html'
    form_class = RegisterForm
    success_url = '/'

    def get_context_data(self, *args, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        title = "Pomelo.Net | Rejestracja"

        context.update({
            'view_name': 'Rejestracja',
            'title': title
        })

        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        mail_subject = 'Aktywuj swoje konto w sklepie Pomelo.Net!'
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, 'Pomelo.Net <office@pomelo.nazwa.pl>', [to_email])
        email.send()
        messages.add_message(
            self.request,
            messages.INFO, "Pomyślnie zarejestrowano. Proszę aktywować konto w wiadomości wysłanej na podany email"
        )
        return redirect("home")

    def form_invalid(self, form):
        messages.add_message(
            self.request, messages.WARNING, 'Wystąpił problem z formularzem. Popraw błedy i spróbuj ponownie'
        )
        return super(RegisterView, self).form_invalid(form)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')


class CategoryProductsView(DetailView):
    """
    Formularz odpowiadający za wyświetlanie produktów po kategorii.
    """
    template_name = "category_products.html"
    model = Category

    def get_queryset(self):
        if self.request.GET.get('sort'):
            order = self.request.GET.get('sort')
            return super(CategoryProductsView, self).get_queryset()
        else:
            return super(CategoryProductsView, self).get_queryset().order_by('name')

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryProductsView, self).get_context_data(**kwargs)
        title = "Pomelo.Net | " + self.object.name

        if self.request.GET.get('sort'):
            order = self.request.GET.get('sort')
            products = Product.objects.all().filter(category=self.object).order_by(order)
        else:
            products = Product.objects.all().filter(category=self.object).order_by('name')

        context.update({
            'products': products,
            'title': title,
            'category': Category.objects.all()
        })

        return context


class ProductOffers(ListView):
    template_name = "offers.html"
    model = Product

    def get_queryset(self):
        if self.request.GET.get('sort'):
            order = self.request.GET.get('sort')
            return super(ProductOffers, self).get_queryset().order_by(order)
        else:
            return super(ProductOffers, self).get_queryset().order_by('name')

    def get_context_data(self, *args, **kwargs):
        title = "Pomelo.Net | Najlepsze Oferty"
        view_name = "Najlepsze Oferty"

        if self.request.GET.get('sort'):
            order = self.request.GET.get('sort')
            offers = self.object_list.filter(product_discount__discount__gte=0).order_by(order)
        else:
            offers = self.object_list.filter(product_discount__discount__gte=0).order_by('-product_discount__discount')

        context = {
            'offers': offers,
            'title': title,
            'view_name': view_name,
            'category': Category.objects.all(),
        }

        return context


class UpdateProfileView(UpdateView):
    template_name = 'profile_edit.html'
    model = User
    form_class = UpdateUser

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS, 'Zmieniono dane użytkownika'
        )
        form.save()
        return redirect(self.request.path_info)

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(UpdateProfileView, self).get_context_data(**kwargs)
        title = "Pomelo.Net | Edycja Profilu"
        view_name = "Edycja Profilu"
        user_edit_form = UpdateUser()

        context.update({
            'title': title,
            'category': Category.objects.all(),
            'user_form': user_edit_form,
            'view_name': view_name
        })

        return context

