from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Finch

# Create your views here.
from django.http import HttpResponse


def home(request):
    return HttpResponse('<h1>Welcome</h1>')


def about(request):
    return render(request, 'about.html')


def finches_index(request):
    finches = Finch.objects.all()
    return render(request, 'finches/index.html', {'finches': finches})


def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    return render(request, 'finches/detail.html', {'finch': finch})


class FinchCreate(CreateView):
    model = Finch
    fields = ['name', 'breed', 'description', 'age']
    success_url = '/finches/'