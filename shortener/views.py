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
    url_hash = data.get('code')
    
    if Query.findUrl(url_hash, 0, 0) != "":
        args = {'form': form, 'url' : "Esse código já foi usado"}
        return render(request, 'view.html', args)
    
    else:
        
        CreateURL.mutate(0, 0, full_url, url_hash)
        
        args = {'form': form, 'url' : "http://localhost:8000/" + url_hash}
        return render(request, 'view.html', args)

def showUrls(request):   
    get_urls = Query.resolve_urls(0, 0)
    url = []
    
    for r in get_urls:
        url.append("Encurtado: http://localhost:8000/"+r.url_hash + " Original: " + r.full_url)
    
    return render(request, 'showUrls.html', {'urls': url})

def deleteUrls(request):
    Query.deleteAll(0, 0)
    return showUrls(request)

def root(request, url_hash):
    url = get_object_or_404(URL, url_hash=url_hash)
    url.clicked()

    return redirect(url.full_url)