from pathlib import Path

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from PIL import Image, UnidentifiedImageError

from .utils import run_object_detection


ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def is_allowed_image_extension(filename):
    return Path(filename).suffix.lower() in ALLOWED_IMAGE_EXTENSIONS


def is_valid_image_file(uploaded_file):
    try:
        image = Image.open(uploaded_file)
        image.verify()
        uploaded_file.seek(0)
        return True
    except (UnidentifiedImageError, OSError):
        uploaded_file.seek(0)
        return False


def home(request):
    context = {}

    if request.method == "POST":
        uploaded_image = request.FILES.get("image")

        if not uploaded_image:
            context["error"] = "Please upload an image."

        elif not is_allowed_image_extension(uploaded_image.name):
            context["error"] = (
                "Unsupported file type. Please upload a JPG, JPEG, PNG, or WEBP image."
            )

        elif not is_valid_image_file(uploaded_image):
            context["error"] = "Invalid image file. Please upload a valid image."

        else:
            file_storage = FileSystemStorage(
                location=settings.MEDIA_ROOT / "uploads",
                base_url=settings.MEDIA_URL + "uploads/",
            )
            saved_filename = file_storage.save(uploaded_image.name, uploaded_image)
            uploaded_image_path = settings.MEDIA_ROOT / "uploads" / saved_filename

            try:
                detection_result = run_object_detection(uploaded_image_path)

                context["uploaded_image_name"] = saved_filename
                context["uploaded_image_url"] = file_storage.url(saved_filename)
                context["result_image_url"] = (
                    settings.MEDIA_URL
                    + "results/"
                    + detection_result["result_filename"]
                )
                context["detections"] = detection_result["detections"]

            except Exception:
                context["error"] = "Object detection failed. Please try another image."

    return render(request, "detector/index.html", context)