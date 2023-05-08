from .models import Categories

def Some_linkage(request):
    links = Categories.objects.all()
    return dict(links=links)