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


from .models import Category

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)
