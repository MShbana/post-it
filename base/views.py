from django.shortcuts import render

def error_404(request, exception, template_name='error_404.html'):
    return render(request, 'error_404.html', status=404)