from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

from .models import URL
from shortener.schema import CreateURL
from shortener.schema import Query

from forms.forms import urlForm

#Função da tela inicial da view
def view(request):
    
    base_url = request.META.get('HTTP_HOST')
    
    form = urlForm(request.POST)
    if request.method == 'POST':
        
        form = urlForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['post']
            return HttpResponseRedirect('/view/')
        else:
            form = urlForm()
            
    return render(request, 'view.html', {'form': form, 'base_url': base_url})

#Função que carrega a view, guarda a URL no banco de dados e atribui o codigo a ela, encurtando a URL
@csrf_exempt
def pegarUrl(request):
    form = urlForm(request.POST)
    base_url = request.META.get('HTTP_HOST')
    
    if form.is_valid():
        url = form.cleaned_data['get']
    
    data = request.POST.copy()

    full_url = data.get('url')
    url_hash = data.get('code')
     
    if Query.findUrl(url_hash, 0, 0) != "" or None:
        args = {'form': form, 'url' : "Esse código já foi usado", 'base_url': base_url}
        return render(request, 'view.html', args)
    
    else:
        try:
            CreateURL.mutate(0, 0, full_url, url_hash)
        except:
            args = {'form': form, 'url' : "Esse código já foi usado"}
            return render(request, 'view.html', args)
    
        args = {'form': form, 'url' : "http://"+ base_url + "/" + url_hash, 'base_url': base_url}
        return render(request, 'view.html', args)

#Função que mostra as URLS encurtadas salvas no banco e os equivalentes originais
def showUrls(request):   
    get_urls = Query.resolve_urls(0, 0)
    url = []
    base_url = request.META.get('HTTP_HOST')
    
    for r in get_urls:
        url.append("Encurtado: http://"+ base_url + "/" +r.url_hash + " Original: " + r.full_url)
    
    context = {'urls' : get_urls, 'base_url': base_url}
    
    return render(request, 'showUrls.html', context)

#Função que deleta todas as URLS salvas no banco (Util no ambiente de teste)
def deleteUrls(request):
    Query.deleteAll(0, 0)
    return showUrls(request)

#Função que redireciona a URL encurtada para a URL original e adiciona um Click a ela
def root(request, url_hash):
    url = get_object_or_404(URL, url_hash=url_hash)
    url.clicked()

    return redirect(url.full_url)