from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from .models import URL
from shortener.schema import CreateURL
from shortener.schema import Query
from forms.forms import urlForm

def view(request):
    form = urlForm(request.POST)
    if request.method == 'POST':
        form = urlForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['post']
            return HttpResponseRedirect('/view/')
        
        else:
            form = urlForm()
            
    return render(request, 'view.html', {'form': form})

@csrf_exempt
def pegarUrl(request):
    form = urlForm(request.GET)

    if form.is_valid():
        url = form.cleaned_data['get']
    
    data = request.POST.copy()

    full_url = data.get('url')
    
    CreateURL.mutate(0, 0, full_url)
    
    urls = Query.resolve_urls(0, 0)
    
    hashCode = Query.findUrl(full_url, 0, 0)
    
    args = {'form': form, 'url' : "http://localhost:8000/" + hashCode}
    return render(request, 'view.html', args)


def root(request, url_hash):
    url = get_object_or_404(URL, url_hash=url_hash)
    url.clicked()

    return redirect(url.full_url)