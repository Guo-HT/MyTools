from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect


# Create your views here.
def index(request):
    return render(request, "online/index.html")
