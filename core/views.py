from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def login_page(request):
    return render(request, "auth/login.html")


def register_page(request):
    return render(request, "auth/register.html")


def candidate_dashboard(request):
    return render(request, "candidate/dashboard.html")


def recruiter_dashboard(request):
    return render(request, "recruiter/dashboard.html")


def job_list(request):
    return render(request, "jobs/list.html")


def job_detail(request, pk):
    return render(request, "jobs/detail.html", {"job_id": pk})


def notifications_page(request):
    return render(request, "notifications/list.html")