'''context_processors is a list of dotted Python paths to callables that are used to 
populate the context when a template is rendered with a request. These callables 
take a request object as their argument and return a dict of items to be merged into the 
context.
It defaults to an empty list.



A context processor is a Python function that takes the request object as
an argument and returns a dictionary that gets added to the request context. 
They come in handy when you need to make something available globally to
all templates.
'''


from .models import CartItem,Cart
from .views import _cart_id
def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return()
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
                
        except Cart.DoesNotExist:
            cart_count =0 
    return dict(cart_count=cart_count)
