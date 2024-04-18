from .models import CropType


def menu_links(request):
    links = CropType.objects.all()
    return dict(links=links)