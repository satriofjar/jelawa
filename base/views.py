from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import City, Island
from .serialize import serialize_questions


# Homepage
def home(request):
    context = {}
    return render(request, "base/index.html", context)


# Page mulai jelajah menampilkan maps indonesia
def maps(request):
    if request.method == "POST":
        city_name = request.POST.get("city-name")
        city = City.objects.filter(name=city_name).first()

        if city != None:
            return redirect("city-detail", city_name=city)

    context = {
        "API_BASE_URL": settings.API_BASE_URL,
        "IMG_BASE_URL": settings.IMG_BASE_URL,
    }
    return render(request, "base/maps.html", context)


# Page pulau => menampilkan video dan kuis
def island(request, city_name):
    city = get_object_or_404(City, name=city_name)

    context = {
        "city": city,
        "API_BASE_URL": settings.API_BASE_URL,
        "IMG_BASE_URL": settings.IMG_BASE_URL,
    }
    return render(request, "base/learn.html", context)


def get_island(request, pk):
    island = Island.objects.get(name=pk)
    cities = island.city_set.all()
    data = {
        "name": island.name,
        "desc": island.description,
        "cities": [{"name": city.name} for city in cities],
    }
    return JsonResponse(data, safe=False)


def get_questions(request, city_name):
    questions = serialize_questions(city_name)
    return JsonResponse(questions, safe=False)
