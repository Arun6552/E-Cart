from django.shortcuts import render,redirect,get_object_or_404
from store.models import  Product
from .models import CartItem,Cart
from django.core.exceptions import  ObjectDoesNotExist
from django.http import HttpResponse
from  store.models import Variation
# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart 



def add_cart(request,product_id):
    product = Product.objects.get(id=product_id) #get the product
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass
    try: 
        cart = Cart.objects.get(cart_id=_cart_id(request)) #get the cart using cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
        cart.save() 
    is_cart_item_exists = CartItem.objects.filter(product=product,cart=cart).exists()
    if is_cart_item_exists :
        cart_item  = CartItem.objects.filter(product=product,cart=cart)
        #existing variation--->>database
        #current variation--->>product_variation
        #item id --->>id 
        ex_var_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variation.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)
        if product_variation in ex_var_list:
                #increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product = product, id = item_id)
                item.quantity+=1
                item.save() 
        else:
                #create new cart_items
                item = CartItem.objects.create(product = product,quantity=1,cart=cart)
                if len(product_variation) > 0:
                    item.variation.clear()
                    item.variation.add(*product_variation) #* add all the production variation
                item.save()
        # cart_item.quantity +=1 
                # cart_item.save()
    else:
        cart_item = CartItem.objects.create(
            product = product, 
            quantity = 1,
            cart = cart,
        )
        if len(product_variation)>0:
            cart_item.variation.clear()
            cart_item.variation.add(*product_variation)
            cart_item.save()
    # return HttpResponse(cart_item.product)
    # exit()
    return redirect('cart')

def remove_cart(request,product_id,cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product,id=product_id)   
    try:
        cart_item = CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
        if cart_item.quantity >1:
            cart_item.quantity-=1
            cart_item.save() 
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')
def remove_cart_item(request,product_id,cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product,id=product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
    cart_item.delete()
    return redirect("cart")
    

def cart(request,total=0,quantity=0,cart_items=None):
    try:
        tax = 0 
        grandtotal=0
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        
        for cart_item in cart_items:
            total+=(cart_item.product.price * cart_item.quantity)
            quantity+=cart_item.quantity
            
        tax = (2 * total)/100
        grandtotal = tax + total 
    except ObjectDoesNotExist:
        pass #jst ignore 
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax':tax,
        'grandtotal':grandtotal,
    }
    
    return render(request, 'store/cart.html',context=context)
    