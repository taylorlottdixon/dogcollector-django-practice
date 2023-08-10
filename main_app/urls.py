from django.urls import path
from . import views
	
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('dogs/', views.dogs_index, name='index'),
    path('dogs/<int:dog_id>/', views.dogs_detail, name='detail'),
    path('dogs/create/', views.DogCreate.as_view(), name='dogs_create'),
    path('dogs/<int:pk>/update/', views.DogUpdate.as_view(), name='dogs_update'),
    path('dogs/<int:pk>/delete/', views.DogDelete.as_view(), name='dogs_delete'),
    path('dogs/<int:dog_id>/add_feeding/', views.add_feeding, name='add_feeding'),
    path('walks/<int:walk_id>/assoc_walk/<int:dog_id>/', views.assoc_walk, name='assoc_walk'),
    path('walks/<int:walk_id>/unassoc_walk/<int:dog_id>/', views.unassoc_walk, name='unassoc_walk'),
    path('walks/', views.WalkList.as_view(), name='walks_index'),
    path('walks/<int:pk>/', views.WalkDetail.as_view(), name='walks_detail'),
    path('walks/create/', views.WalkCreate.as_view(), name='walks_create'),
    path('walks/<int:pk>/update/', views.WalkUpdate.as_view(), name='walks_update'),
    path('walks/<int:pk>/delete/', views.WalkDelete.as_view(), name='walks_delete'),
    path('dogs/<int:dog_id>/add_photo/', views.add_photo, name='add_photo'),
    path('accounts/signup/', views.signup, name='signup'),
]