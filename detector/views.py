from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

from .utils import run_object_detection


def home(request):
    context = {}

    if request.method == "POST":
        uploaded_image = request.FILES.get("image")

        if uploaded_image:
            file_storage = FileSystemStorage(
                location=settings.MEDIA_ROOT / "uploads",
                base_url=settings.MEDIA_URL + "uploads/",
            )
            saved_filename = file_storage.save(uploaded_image.name, uploaded_image)

            uploaded_image_path = settings.MEDIA_ROOT / "uploads" / saved_filename
            detection_result = run_object_detection(uploaded_image_path)

            context["uploaded_image_name"] = saved_filename
            context["uploaded_image_url"] = file_storage.url(saved_filename)
            context["result_image_url"] = settings.MEDIA_URL + "results/" + detection_result["result_filename"]
            context["detections"] = detection_result["detections"]
        else:
            context["error"] = "Please upload an image."

    return render(request, "detector/index.html", context)