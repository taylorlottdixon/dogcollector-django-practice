from django.shortcuts import render, redirect

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Dog, Walk
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

def dogs_index(request):
    dogs = Dog.objects.all()
    return render(request, 'dogs/index.html', {
        'dogs': dogs
    })

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

class DogCreate(CreateView):
  model = Dog
  fields = ['name', 'nickname', 'breed', 'age']

class DogUpdate(UpdateView):
  model = Dog
  # Let's disallow the renaming of a Dog by excluding the name field!
  fields = ['nickname', 'breed', 'age']

class DogDelete(DeleteView):
  model = Dog
  success_url = '/dogs'

def add_feeding(request, dog_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.dog_id = dog_id
        new_feeding.save()
    return redirect('detail', dog_id=dog_id)

class WalkList(ListView):
  model = Walk

class WalkDetail(DetailView):
  model = Walk

class WalkCreate(CreateView):
  model = Walk
  fields = '__all__'

class WalkUpdate(UpdateView):
  model = Walk
  fields = ['date', 'time_start', 'time_end', 'length']

class WalkDelete(DeleteView):
  model = Walk
  success_url = '/walks'

def assoc_walk(request, dog_id, walk_id):
  # Note that you can pass a walk's id instead of the whole walk object
  Walk.objects.get(id=walk_id).walks.add(dog_id)
  return redirect('detail', walk_id=walk_id)

def unassoc_walk(request, dog_id, walk_id):
  # Note that you can pass a walk's id instead of the whole walk object
  Walk.objects.get(id=walk_id).walks.remove(dog_id)
  return redirect('detail', walk_id=walk_id)

def walks_detail(request, walk_id):
  walk = Walk.objects.get(id=walk_id)
  id_list = walk.dogs.all().values_list('id')
  dog_not_on_walk = Dog.objects.exclude(id__in=id_list)
  # instantiate FeedingForm to be rendered in detail.html
  return render(request, 'main_app/walk_detail.html', {
    'walk': walk, 
    'dogs': dog_not_on_walk,
  })