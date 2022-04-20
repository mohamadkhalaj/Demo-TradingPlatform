from django.shortcuts import render


def page_not_found_view(request, exception):
    return render(request, "404.html", status=404)


def handler500(request):
    return render(request, "500.html", status=500)


def handler403(request, exception):
    return render(request, "403.html", status=403)
