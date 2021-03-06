from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from .models import Finch, Toy, Photo
from .forms import FeedingForm
# the template the CreateView and the UpdateView use is the same
# templates/<app_name>/<model>_form.html
# templates/main_app/finch_form.html

# Create your views here.
from django.http import HttpResponse


S3_BASE_URL = 'https://s3.us-west-1.amazonaws.com/'
BUCKET = 'finchcollec'

def signup(request):
    # on a GET lets render a template with a form 
    error_message = ''
    if request.method == 'POST':
        # On a POST lets signup the user and log them in
        # This is how to create a 'user' form object that inlcudes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid(): 
            # This will add the user to the database 
            user = form.save()
            login(request, user) # user is logged in and available on every request and in every template 
            return redirect('index')
        else: 
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

class FinchCreate(LoginRequiredMixin, CreateView):
    model = Finch
    fields = ['name', 'breed', 'description', 'age']

    # This inheritedmethod is called when a valid finch form is being submitted
    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user # form.instance is the cat
        return super().form_valid(form)

class FinchUpdate(LoginRequiredMixin, UpdateView): 
    model = Finch 
    # we dont want to let anyone change finches name, so lets not include the name in the fields
    fields = ['breed', 'description', 'age']
    # where's the redirect defined at for a put request?

class FinchDelete(LoginRequiredMixin, DeleteView):
    model = Finch
    # because our model is redirecting to specific finch but we just deleted it
    success_url = '/finches/'

def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

@login_required
def finches_index(request):
    finches = Finch.objects.filter(user=request.user)
    return render(request, 'finches/index.html', {'finches': finches})

@login_required
# path('finches/<int:finch_id>/' <- this is where finch_id comes from
def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    # Get the toys the finch doesn't have 
    toys_finch_doesnt_have = Toy.objects.exclude(id__in = finch.toys.all().values_list('id'))
    # create an instance of FeedingForm
    feeding_form = FeedingForm()
    return render(request, 'finches/detail.html', {'finch': finch, 'feeding_form': feeding_form, 'toys': toys_finch_doesnt_have
    })

@login_required
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

@login_required
def add_photo(request, finch_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            Photo.objects.create(url=url, finch_id=finch_id)
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', finch_id=finch_id)

@login_required
def assoc_toy(request, finch_id, toy_id):
    Finch.objects.get(id=finch_id).toys.add(toy_id)
    return redirect('detail', finch_id=finch_id)

class ToyList(LoginRequiredMixin, ListView):
    model = Toy

class ToyCreate(LoginRequiredMixin, CreateView): 
    model = Toy
    fields = '__all__'

class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView): 
    model = Toy
    success_url = '/toys/'