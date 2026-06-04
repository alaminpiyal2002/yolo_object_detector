from django.http import HttpResponse


def home(request):
    return HttpResponse("YOLO Object Detector homepage is working.")