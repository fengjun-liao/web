import random

from django.shortcuts import render


def index(request):
    """Render the personal website home page."""
    soil_moisture = random.randint(28, 73)
    context = {
        "title": "土壤濕度敢測自動澆水系統",
        "heading": "土壤濕度敢測自動澆水系統",
        "message": "即時顯示土壤濕度，幫助您自動澆水，保持植物健康。",
        "soil_moisture": soil_moisture,
        "name": "廖烽均",
    }
    return render(request, "mainapp/index.html", context)


def about(request):
    """Render a simple about page."""
    context = {
        "title": "About This Site",
        "heading": "About the Test Website",
        "message": "This sample site shows a basic Django view, URL routing, and template.",
    }
    return render(request, "mainapp/about.html", context)
