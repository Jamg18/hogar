from django.shortcuts import render


def dashboard(request):
    """Vista web provisional; Flutter sustituirá esta capa sin cambiar la API."""
    return render(request, "dashboard.html")


def expenses(request):
    """Gestión web provisional de salidas, persistida localmente en el navegador."""
    return render(request, "expenses.html")
