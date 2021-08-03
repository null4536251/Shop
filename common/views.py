from django.shortcuts import render
from common.models import Types


# Create your views here.
def loadinfo(request):
    context = {}
    context['types'] = Types.objects.all()
    return context
