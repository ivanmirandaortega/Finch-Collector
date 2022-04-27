from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Finch, Toy
from .forms import FeedingForm
# the template the CreateView and the UpdateView use is the same
# templates/<app_name>/<model>_form.html
# templates/main_app/finch_form.html

# Create your views here.
from django.http import HttpResponse

class FinchCreate(CreateView):
    model = Finch
    fields = '__all__'

class FinchUpdate(UpdateView): 
    model = Finch 
    # we dont want to let anyone change finches name, so lets not include the name in the fields
    fields = ['breed', 'description', 'age']
    # where's the redirect defined at for a put request?

class FinchDelete(DeleteView):
    model = Finch
    # because our model is redirecting to specific finch but we just deleted it
    success_url = '/finches/'

def home(request):
    return HttpResponse('<h1>Welcome</h1>')


def about(request):
    return render(request, 'about.html')

def finches_index(request):
    finches = Finch.objects.all() # using our model to get all the rows in our finch table in psql
    return render(request, 'finches/index.html', {'finches': finches})


# path('finches/<int:finch_id>/' <- this is where finch_id comes from
def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    # create an instance of FeedingForm
    feeding_form = FeedingForm()
    return render(request, 'finches/detail.html', {'finch': finch, 'feeding_form': feeding_form
    })

def add_feeding(request, finch_id):
    # create a ModelForm Instance using the data in the request
    form = FeedingForm(request.POST)
    # validate
    if form.is_valid():
        # do somestuff
		# creates an instance of out feeding to be put in the database
		# lets not save it yet, commit=False because we didnt add the foreign key
        new_feeding = form.save(commit=False)
        #look at the note for finch field in the Feeding Model
        new_feeding.finch_id = finch_id
        new_feeding.save()# adds the feeding to the database, and the feeding be associated with the finch
		# with same id as the argument to the function finch_id
    return redirect('detail', finch_id=finch_id)

class ToyList(ListView):
    model = Toy

class ToyCreate(CreateView): 
    model = Toy
    fields = '__all__'

class ToyDetail(DetailView):
    model = Toy

class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(DeleteView): 
    model = Toy
    success_url = '/toys/'