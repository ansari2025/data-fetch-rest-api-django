from .views import StudentView  
from django.urls import path  
  
urlpattern = [  
    path('insertdata/', StudentView.as_view())  
]  