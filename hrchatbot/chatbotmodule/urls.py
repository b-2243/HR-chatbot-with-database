from django.contrib import admin
from django.urls import path
from chatbotmodule.views import ChatbotView

urlpatterns = [
    path("chatbot/",ChatbotView.as_view(),name="chatbot"),
   
]
