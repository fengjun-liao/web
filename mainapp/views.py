from django.shortcuts import render


def index(request):
    """Render the test website home page."""
    context = {
        "title": "Test Website",
        "heading": "Welcome to the Test Website",
        "message": "This is a simple Django test website created for demonstration.",
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
