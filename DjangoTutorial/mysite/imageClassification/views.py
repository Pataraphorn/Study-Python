from django.shortcuts import render

# Create your views here.
def classification(response):
    return render(response,"imageClassification/home.html",{})