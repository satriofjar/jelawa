from operator import index

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from display_text.models import NavbarFooter, IndexContent, MapsContent

from .models import City, Island
from .serialize import serialize_questions


# Homepage
def home(request):
    islands = Island.objects.all()
    index_content = IndexContent.objects.order_by("-created_at").first()
    navbar_footer = NavbarFooter.objects.order_by("-created_at").first()
    context = {
        "islands": islands,
        "index_content": index_content,
        "navbar_footer": navbar_footer,
        "home": "active",
    }
    return render(request, "base/index.html", context)


# Page mulai jelajah menampilkan maps indonesia
def maps(request):
    if request.method == "POST":
        city_name = request.POST.get("city-name")
        city = City.objects.filter(name__iexact=city_name).first()

        if city != None:
            return redirect("city-detail", city_name=city)

    islands = Island.objects.all()
    maps_content = MapsContent.objects.order_by("-created_at").first()
    navbar_footer = NavbarFooter.objects.order_by("-created_at").first()
    context = {
        "islands": islands,
        "API_BASE_URL": settings.API_BASE_URL,
        "IMG_BASE_URL": settings.IMG_BASE_URL,
        "maps_content": maps_content,
        "navbar_footer": navbar_footer,
        "jelajah": "active",
    }
    return render(request, "base/maps.html", context)


# Page city => menampilkan video dan kuis
def city_content(request, city_name):
    islands = Island.objects.all()
    city = get_object_or_404(City, name__iexact=city_name)
    navbar_footer = NavbarFooter.objects.order_by("-created_at").first()

    context = {
        "islands": islands,
        "city": city,
        "API_BASE_URL": settings.API_BASE_URL,
        "IMG_BASE_URL": settings.IMG_BASE_URL,
        "navbar_footer": navbar_footer,
    }
    return render(request, "base/learn.html", context)


def get_island(request, pk):
    island = Island.objects.get(name__iexact=pk)
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
