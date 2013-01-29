from django.conf.urls.defaults import *
from django.views.generic import TemplateView, ListView, DetailView
from allestimentiportanuovaapp.models import *
from allestimentiportanuovaapp.views import *

urlpatterns = patterns('',
	url(r'^$', ListView.as_view(template_name='cover.html', queryset=Immagine_homepage.objects.filter(attivo=True)[:5], context_object_name='immagini_cover'), name='cover'),
	url(r'^profilo/$', ListView.as_view(template_name='profilo.html', queryset=Contatto.objects.filter(categoria_contatto__categoria='Cliente'), context_object_name='Clienti'), name='profilo'),
	url(r'^storia/$', ListView.as_view(template_name='storia.html', queryset=Documento_storico.objects.filter(attivo=True), context_object_name='Documento_storico'), name='storia'),
	url(r'^progetti/$', ProgettiView.as_view(), name='progetti'),
	url(r'^progetti/decade/(?P<decade>[-\w]+)/$', ProgettiView.as_view(), name='progetti_decade'),
	url(r'^progetti/anno/(?P<anno>\d{4})/$', ProgettiView.as_view(), name='progetti_anno'),
	url(r'^progetti/tag/(?P<slug>[-\w]+)/$', ProgettiView.as_view(), name='progetti_tag'),
	url(r'^progetto/(?P<slug>[-\w]+)/$', ProgettoView.as_view(template_name='progetto_detail.html', model=Progetto), name='progetto'),
	url(r'^catalogo/$', CatalogoView.as_view(), name='catalogo'),
	url(r'^catalogo/tipologia/(?P<slug>[-\w]+)/$', CatalogoView.as_view(), name='catalogo_tipologia'),
	url(r'^carica_progetti/$', ListView.as_view(template_name='carica_progetti.html', queryset=Progetto.objects.filter(attivo=True)[10:], context_object_name='progetti'), name='carica_progetti'),

)

