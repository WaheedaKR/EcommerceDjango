from django.shortcuts import render
from shop.models import item

def home(request):
    # return HttpResponse('you are at Home page')
    items = item.objects.all().filter(availability=True)

    seeHere = {
        'items': items,
    }
    return render(request, 'home.html', seeHere)
