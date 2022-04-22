import imp
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def home(request):
    return HttpResponse('<h1>Welcome</h1>')


def about(request):
    return render(request, 'about.html')


def finches_index(request):
    return render(request, 'finches/index.html', {'finches': finches})


class Finch:
    def __init__(self, name, breed, description, age):
        self.name = name
        self.breed = breed
        self.description = description
        self.age = age


finches = [
    Finch('Robin', 'The Spice Finch', 'Cute bird', 2)
]
