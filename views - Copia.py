 # coding=utf-8
from models import Progetto, Prodotto, Tipologia, Tag
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic import TemplateView, ListView, DetailView



class ProgettiView(ListView):
	template_name='progetti.html'
	context_object_name='progetti'
	
	def get_queryset(self):
		if 'slug' in self.kwargs:
			progetti = Progetto.objects.filter(tag__slug=self.kwargs['slug'])
		elif 'anno' in self.kwargs:
			progetti = Progetto.objects.filter(data__year=self.kwargs['anno'])
		elif 'decade' in self.kwargs:
			if self.kwargs['decade'] == 'anni40':
				progetti = Progetto.objects.filter(data__range=['1940-01-01','1949-12-31'])
			elif self.kwargs['decade'] == 'anni50':
				progetti = Progetto.objects.filter(data__range=['1950-01-01','1959-12-31'])
			elif self.kwargs['decade'] == 'anni60':
				progetti = Progetto.objects.filter(data__range=['1960-01-01','1969-12-31'])
			elif self.kwargs['decade'] == 'anni70':
				progetti = Progetto.objects.filter(data__range=['1970-01-01','1979-12-31'])
			elif self.kwargs['decade'] == 'anni80':
				progetti = Progetto.objects.filter(data__range=['1980-01-01','1989-12-31'])
			elif self.kwargs['decade'] == 'anni90':
				progetti = Progetto.objects.filter(data__range=['1990-01-01','1999-12-31'])
			elif self.kwargs['decade'] == 'recenti':
				progetti = Progetto.objects.filter(data__range=['2000-01-01','3000-12-31'])
		else:
			progetti = Progetto.objects.filter(attivo=True)

		return progetti
	
	
	def get_context_data(self, **kwargs):
		context = super(ProgettiView, self).get_context_data(**kwargs)
		context['decadi'] = Progetto.objects.all().order_by('-data')
		context['tags'] = Tag.objects.all()
		context['anni'] = Progetto.objects.all()
		breadcrumbs = ''
		breadcrumbs_eng = ''
		if 'anno' in self.kwargs:
			anno = self.kwargs['anno']
			breadcrumbs = '{}'.format(anno)
		elif 'decade' in self.kwargs:
			if self.kwargs['decade'] == 'anni40':
				breadcrumbs = 'anni 40'
				breadcrumbs_eng = "40's"
			elif self.kwargs['decade'] == 'anni50':
				breadcrumbs = 'anni 50'
				breadcrumbs_eng = "50's"
			elif self.kwargs['decade'] == 'anni60':
				breadcrumbs = 'anni 60'
				breadcrumbs_eng = "60's"
			elif self.kwargs['decade'] == 'anni70':
				breadcrumbs = 'anni 70'
				breadcrumbs_eng = "70's"
			elif self.kwargs['decade'] == 'anni80':
				breadcrumbs = 'anni 80'
				breadcrumbs_eng = "80's"
			elif self.kwargs['decade'] == 'anni90':
				breadcrumbs = 'anni 90'
				breadcrumbs_eng = "90's"
			elif self.kwargs['decade'] == 'recenti':
				breadcrumbs = 'recenti'
				breadcrumbs_eng = "recents"
		elif 'slug' in self.kwargs:
			tag = Tag.objects.get(slug=self.kwargs['slug'])
			breadcrumbs = '{}'.format(tag.tag)
			breadcrumbs_eng = '{}'.format(tag.tag_eng)
		if breadcrumbs_eng:
			context['breadcrumbs_eng'] = breadcrumbs_eng
		if breadcrumbs:
			context['breadcrumbs'] = breadcrumbs
		return context

	
class CatalogoView(ListView):
	template_name='catalogo.html'
	context_object_name='catalogo'
	
	def get_queryset(self):
		if 'slug' in self.kwargs:
			catalogo = Prodotto.objects.filter(tipologia__slug=self.kwargs['slug'])
		else:
			catalogo = Prodotto.objects.filter(attivo=True)
		return catalogo
	
	def get_context_data(self, **kwargs):
		context = super(CatalogoView, self).get_context_data(**kwargs)
		context['tipologie'] = Tipologia.objects.all()
		breadcrumbs = ''
		breadcrumbs_eng = ''
		if 'slug' in self.kwargs:
			tipologia = Tipologia.objects.get(slug=self.kwargs['slug'])
			breadcrumbs = '{}'.format(tipologia.tipologia)
			breadcrumbs_eng = '{}'.format(tipologia.tipologia_eng)
		if breadcrumbs_eng:
			context['breadcrumbs_eng'] = breadcrumbs_eng
		if breadcrumbs:
			context['breadcrumbs'] = breadcrumbs
		return context

class ProgettoView(DetailView):
    def get_context_data(self, **kwargs):
        context = super(ProgettoView, self).get_context_data(**kwargs)
        context['immagini_progetto'] = self.object.immagine_progetto_set.all()
        return context