from decimal import Context
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView

from cart.cart import Cart
# from store.products.models import Product

from .form import OrderCreateForm
from .models import Item, Order


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderCreateForm
    
    def form_valid(self, form):
        cart = Cart(self.request)
        if cart:
            order = form.save()
            for item in cart:
                Item.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            cart.clear()
            return render(self.request, 'orders/order_created.html', {'order': order})
        return HttpResponseRedirect(reverse('pages:home'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context