from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from shortener import views
from graphene_django.views import GraphQLView
from django.contrib import admin

urlpatterns = [
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('view/', views.view),
    path('urls/', views.showUrls),
    path('delete/', views.deleteUrls),
    path('result/', views.pegarUrl),
    path('admin/', admin.site.urls),
    path('<str:url_hash>/', views.root, name='root'),
    

]