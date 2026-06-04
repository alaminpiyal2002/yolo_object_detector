from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render


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

            context["uploaded_image_name"] = saved_filename
            context["uploaded_image_url"] = file_storage.url(saved_filename)
        else:
            context["error"] = "Please upload an image."

    return render(request, "detector/index.html", context)