import uuid
import boto3
from django.shortcuts import render, redirect
import os

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Dog, Walk, Photo
from .forms import FeedingForm


### Add siblings many to many relationship
### Or family one to many relationship that shows siblings on detail page

# dogs = [
#     {'name': 'Juniper Jane', 'nickname': 'June Bug', 'breed': 'Belgian Mallanois Mix', 'age': 12, 
#      'favorites': ['My Mom', 'Jasper', 'Rolling in the grass', 'Keeping the peace (aka finding an excuse to "attack")', 'Being outside'],
#      'hates': ['Strangers', 'Being ignored', 'All other animals', 'When people rough-house without me'], 'pic': '/images/june-1.jpg'},
#     {'name': 'Jasper', 'nickname': 'Mr. Sweet Face', 'breed': 'German Shepard Mix', 'age': 10, 
#      'favorites': ['My Mom', 'June', 'Eating breakfast with my mom', 'Laying under my mom''s feet', 'Just basically my mom'],
#      'hates': []},
# ]

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def dogs_index(request):
    dogs = Dog.objects.filter(user=request.user)
    return render(request, 'dogs/index.html', {
        'dogs': dogs
    })

@login_required
def dogs_detail(request, dog_id):
    dog = Dog.objects.get(id=dog_id)
    id_list = dog.walks.all().values_list('id')
    walks_taken = Walk.objects.exclude(id__in=id_list)
    feeding_form = FeedingForm()
    return render(request, 'dogs/detail.html', {
        'dog': dog,
        'feeding_form': feeding_form,
        'walks': walks_taken,
    })

class DogCreate(LoginRequiredMixin, CreateView):
  model = Dog
  fields = ['name', 'nickname', 'breed', 'age']

  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the cat
    # Let the CreateView do its job as usual
    return super().form_valid(form)

class DogUpdate(LoginRequiredMixin, UpdateView):
  model = Dog
  # Let's disallow the renaming of a Dog by excluding the name field!
  fields = ['nickname', 'breed', 'age']

class DogDelete(LoginRequiredMixin, DeleteView):
  model = Dog
  success_url = '/dogs'

@login_required
def add_feeding(request, dog_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.dog_id = dog_id
        new_feeding.save()
    return redirect('detail', dog_id=dog_id)

class WalkList(LoginRequiredMixin, ListView):
  model = Walk

class WalkDetail(LoginRequiredMixin, DetailView):
  model = Walk

class WalkCreate(LoginRequiredMixin, CreateView):
  model = Walk
  fields = '__all__'

class WalkUpdate(LoginRequiredMixin, UpdateView):
  model = Walk
  fields = ['date', 'time_start', 'time_end', 'length']

class WalkDelete(LoginRequiredMixin, DeleteView):
  model = Walk
  success_url = '/walks'

@login_required
def assoc_walk(request, dog_id, walk_id):
  # Note that you can pass a walk's id instead of the whole walk object
  Walk.objects.get(id=walk_id).walks.add(dog_id)
  return redirect('detail', walk_id=walk_id)

@login_required
def unassoc_walk(request, dog_id, walk_id):
  # Note that you can pass a walk's id instead of the whole walk object
  Walk.objects.get(id=walk_id).walks.remove(dog_id)
  return redirect('detail', walk_id=walk_id)

def walks_detail(request, walk_id):
  walk = Walk.objects.get(id=walk_id)
  id_list = walk.dogs.all().values_list('id')
  dog_not_on_walk = Dog.objects.exclude(id__in=id_list)
  dogs_left = Dog.objects.exclude(dog_not_on_walk)
  # instantiate FeedingForm to be rendered in detail.html
  return render(request, 'main_app/walk_detail.html', {
    'walk': walk, 
    'dogs_walking': dog_not_on_walk,
    'dogs_left': dogs_left,
  })

@login_required
def add_photo(request, dog_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to dog_id or dog (if you have a dog object)
            Photo.objects.create(url=url, dog_id=dog_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', dog_id=dog_id)


def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)