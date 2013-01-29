# coding=utf-8
from django.db import models
import datetime
from stdimage import *

#modifica1

testo_slug = 'Questo è il nome che va nella URL: lascia quello proposto di default.'


def uploadTo(istance,fname):
	"path is relative to MEDIA_ROOT"
	path='immagini_progetti/%s/%s' % (istance.progetto.slug,fname)
	return path

class Immagine_homepage(models.Model):
	attivo = models.BooleanField(default=True, help_text='immagine di copertina')
	ordine = models.IntegerField(unique=True, null=True, blank=True, help_text='Inserisci un numero per ordinare le immagini. Se lasciato vuoto si ordinano per data inserimento')
	img = StdImageField(upload_to='cover', blank=True, size=(1800, 1350, True), thumbnail_size=(100, 100))
	titolo = models.CharField(max_length=255, blank=True, unique=True)
	titolo_eng = models.CharField(max_length=255, blank=True)
	
	def admin_image(self):
		if self.img:
			return '<img src="%s"/>' % self.img.thumbnail.url()
		else:
			return 'no image'
	admin_image.allow_tags = True
	
	class Meta:
		ordering = ['ordine']
		verbose_name_plural = '01. Immagini Cover'



class Progetto(models.Model):
	attivo = models.BooleanField(default=True)
	ordine = models.IntegerField(unique=True, null=True, blank=True, help_text='Inserisci un numero per ordinare i progetti. Se lasciato vuoto si ordinano cronologicamente')
	titolo = models.CharField(max_length=255)
	titolo_eng = models.CharField(max_length=255, blank=True)
	slug = models.SlugField(max_length=255, unique=True, help_text=testo_slug)
	sottotitolo = models.CharField(max_length=255, blank=True)
	sottotitolo_eng = models.CharField(max_length=255, blank=True)
	data = models.DateField(blank=True, null=True, help_text='Data progetto')
	cliente = models.ManyToManyField('Contatto', blank=True, related_name='cliente')
	progettista = models.ManyToManyField('Contatto', blank=True, related_name='progettista')
	tag = models.ManyToManyField('Tag', blank=True)
	luogo = models.ForeignKey('Luogo', null=True, blank=True)
	descrizione = models.TextField(blank=True)
	descrizione_eng = models.TextField(blank=True)
	file = models.FileField(upload_to='progetti/files', blank=True, help_text='Puoi caricare qui un file riguardante il progetto')
	nome_file = models.CharField(max_length=50, blank=True, help_text='Inserisci qui il nome del file')
	thumb = StdImageField(upload_to='progetti/thumbnails', blank=True, size=(300, 8000, False), thumbnail_size=(100, 100))
	
	# dalla data ritorna una stringa con il decennio corrispondente es 1992 = 'anni 90'
	def decade(self):
		decade = ''
		if self.data.year > 1999:
			decade = 'recenti'
		else:
			decade = 'anni' + self.data.strftime('%Y')[2] + "0"
		return decade
	
	def decade_eng(self):
		decade_eng = ''
		if self.data.year > 1999:
			decade = 'recents'
		else:
			decade = self.data.strftime('%Y')[2] + "0's"
		return decade
	"""
	def annata(self):
		anni_40 = Progetto.objects.filter(data__range=['1940-01-01','1949-12-31']) 
		lista_anni_40 = [progetto.data.year for progetto in anni_40]
		recenti = Progetto.objects.filter(data__range=['2012-01-01','2999-12-31']) 
		lista_recenti = [progetto.data.year for progetto in recenti]
		anno = self.data.year
		annata = ''
		if anno in lista_anni_40:
			annata = 'anni_40'
			return annata
		elif anno in lista_recenti:
			annata = 'recenti'
			return annata
		else:
			return annata
	"""
	def admin_image(self):
		if self.thumb:
			return '<img src="%s"/>' % self.thumb.thumbnail.url()
		else:
			return 'no image'
	admin_image.allow_tags = True
				
	class Meta:
		ordering = ['-ordine', '-data']
		verbose_name_plural = '02. Progetti'

	def __unicode__(self):
		return self.titolo

class Documento_storico(models.Model):
	attivo = models.BooleanField(default=False)
	TIPO = (
	('documento', u'Documento'),
	('immagine', u'Immagine'),
	('articolo', u'Articolo'),
	)
	tipo = models.CharField(max_length=50, blank=True, choices=TIPO)
	data = models.DateField(blank=True, default=datetime.datetime.now, help_text='Data di oggi di default ma puoi cambiarla')
	titolo = models.CharField(max_length=255, blank=True)
	thumb = StdImageField(upload_to='archivio_storico/thumbnails', blank=True, size=(300, 8000, False), thumbnail_size=(100, 100))
	img = StdImageField(upload_to='archivio_storico/immagini', blank=True, size=(800, 8000, False))
	file = models.FileField(upload_to='archivio_storico/files', blank=True, help_text='Puoi caricare qui un file (es.pdf/articolo) storico')
	nome_file = models.CharField(max_length=50, blank=True, help_text='Inserisci qui il nome del file appena caricato')
	
	def admin_image(self):
		if self.thumb:
			return '<img src="%s"/>' % self.thumb.thumbnail.url()
		else:
			return 'no image'
	admin_image.allow_tags = True
	
	class Meta:
		ordering = ['titolo', '-data']
		verbose_name_plural = '03. Archivio storico'

	def __unicode__(self):
		return self.titolo

class Contatto(models.Model):
	categoria_contatto = models.ForeignKey('Categoria_contatto', blank=True)
	nome = models.CharField(blank=True, max_length=100)
	cognome = models.CharField(blank=True, max_length=100)
	ragione_sociale = models.CharField(blank=True, max_length=150)
	telefono = models.CharField(max_length=50, blank=True)
	mail = models.EmailField(blank=True)
	indirizzo = models.CharField(max_length=255, blank=True)
	thumb = StdImageField(upload_to='contatti/img', blank=True, size=(300, 8000, False), thumbnail_size=(100, 100))
	link = models.URLField(blank=True, help_text='Inserisci link a pagina del contatto')
	nome_link = models.CharField(max_length=50, blank=True, help_text='Inserisci qui il nome del link')
	
	def admin_image(self):
		if self.thumb:
			return '<img src="%s"/>' % self.thumb.thumbnail.url()
		else:
			return 'no image'
	admin_image.allow_tags = True
	
	class Meta:
		ordering = ['cognome', 'ragione_sociale']
		verbose_name_plural = '04. Rubrica'

	def __unicode__(self):
		return u'%s %s %s' % (self.nome, self.cognome, self.ragione_sociale)


class Prodotto(models.Model):
	attivo = models.BooleanField(default=True)
	titolo = models.CharField(max_length=255)
	titolo_eng = models.CharField(max_length=255, blank=True)
	slug = models.SlugField(max_length=255, unique=True, help_text=testo_slug)
	descrizione = models.TextField(blank=True)
	descrizione_eng = models.TextField(blank=True)
	thumb = StdImageField(upload_to='catalogo/thumb', blank=True, size=(300, 300, True), thumbnail_size=(100, 100))
	img = StdImageField(upload_to='catalogo/immagini', blank=True, size=(800, 8000, False))
	progetto = models.ManyToManyField('Progetto', null=True)
	tipologia = models.ManyToManyField('Tipologia', null=True)
	
	def admin_image(self):
		if self.thumb:
			return '<img src="%s"/>' % self.thumb.thumbnail.url()
		else:
			return 'no image'
	admin_image.allow_tags = True
	
	class Meta:
		ordering = ['titolo']
		verbose_name_plural = '05. Catalogo prodotti'

	def __unicode__(self):
		return self.titolo


class Immagine_progetto(models.Model):
	attivo = models.BooleanField(default=False)
	ordine = models.IntegerField(unique=True, null=True, blank=True, help_text='Inserisci un numero per ordinare le immagini. Se lasciato vuoto si ordinano cronologicamente')
	data = models.DateField(blank=True, default=datetime.datetime.now, help_text='Data di oggi di default ma puoi cambiarla')
	titolo = models.CharField(max_length=255, blank=True)
	titolo_eng = models.CharField(max_length=255, blank=True)
	progetto = models.ForeignKey('Progetto', null=True)
	img = StdImageField(upload_to='progetti/img', blank=True, size=(800, 8000, False), thumbnail_size=(100, 100))

	class Meta:
		ordering = ['ordine', '-data']
		verbose_name_plural = '06. Immagini Progetti'

	def __unicode__(self):
		return self.titolo


class Tag(models.Model):
	tag = models.CharField(max_length=255, blank=True)
	tag_eng = models.CharField(max_length=255, blank=True)
	slug = models.SlugField(max_length=255, unique=True, null=True, help_text=testo_slug)

	class Meta:
		ordering = ['tag']
		verbose_name_plural = '07. Tipologia progetti'

	def __unicode__(self):
		return self.tag

class Categoria_contatto(models.Model):
	categoria = models.CharField(max_length=255, blank=True)
	slug = models.SlugField(max_length=255, unique=True, null=True, help_text=testo_slug)

	class Meta:
		ordering = ['categoria']
		verbose_name_plural = '08. Tipologia contatti'

	def __unicode__(self):
		return self.categoria

class Tipologia(models.Model):
	tipologia = models.CharField(max_length=255, blank=True)
	tipologia_eng = models.CharField(max_length=255, blank=True)
	slug = models.SlugField(max_length=255, unique=True, null=True, help_text=testo_slug)

	class Meta:
		ordering = ['tipologia']
		verbose_name_plural = '09. Tipologia prodotti'

	def __unicode__(self):
		return self.tipologia

class Luogo(models.Model):
	luogo = models.CharField(max_length=255, blank=True)
	slug = models.SlugField(max_length=255, unique=True, null=True, help_text=testo_slug)

	class Meta:
		ordering = ['luogo']
		verbose_name_plural = '10. Luoghi'

	def __unicode__(self):
		return self.luogo


class News(models.Model):
	attivo = models.BooleanField(default=True)
	data = models.DateField(blank=True, default=datetime.datetime.now, help_text='Data di oggi di default ma puoi cambiarla')
	titolo = models.CharField(max_length=150)
	slug = models.SlugField(max_length=255, unique=True, null=False, help_text=testo_slug)
	sottotitolo = models.CharField(max_length=255, blank=True)
	luogo = models.CharField(max_length=255, blank=True)
	CATEGORIA = (
		('News', u'News'),
		('Evento', u'Evento'),
	)	
	categoria = models.CharField(max_length=100, choices=CATEGORIA, blank=True, help_text='Specificare il tipo di news')
	testo = models.TextField(blank=True)
	file_1 = models.FileField(upload_to='news', blank=True, help_text='Puoi caricare qui un file riguardante la news')
	nome_file_1 = models.CharField(max_length=50, blank=True, help_text='Inserisci qui il nome del file')
	file_2 = models.FileField(upload_to='news', blank=True)
	nome_file_2 = models.CharField(max_length=50, blank=True, help_text='Inserisci qui il nome del file')
	link_1 = models.URLField(blank=True)
	nome_link_1 = models.CharField(max_length=50, blank=True, help_text='Inserisci qui il nome del link')
	link_2 = models.URLField(blank=True)
	nome_link_2 = models.CharField(max_length=50, blank=True, help_text='Inserisci qui il nome del link')
	thumb = StdImageField(upload_to='archivio_storico/thumbnails', blank=True, size=(300, 8000, False))

	class Meta:
		ordering = ['-data']
		verbose_name_plural = '11. News'

	def __unicode__(self):
		return u'%s %s %s - %s' % (self.data.strftime('%d'), self.data.strftime('%b'), self.data.strftime('%Y'), self.titolo)

class Articolo(models.Model):
	attivo = models.BooleanField(default=True)
	titolo = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, unique=True, help_text=testo_slug)
	sottotitolo = models.CharField(blank=True, max_length=255)
	data = models.DateTimeField(blank=True, default=datetime.datetime.now, help_text='Data di oggi di Default ma puoi cambiarla')
	testata = models.CharField(blank=True, max_length=100)
	testo = models.TextField(blank=True)
	link = models.URLField(blank=True)
	file = models.FileField(upload_to='articoli', blank=True, help_text='Puoi caricare qui un file riguardante l\'articolo')
	thumb_testata = StdImageField(upload_to='archivio_storico/thumbnails', blank=True, size=(300, 8000, False))

	class Meta:
		ordering = ['-data']
		verbose_name_plural = '12. Press'

	def __unicode__(self):
		return u'%s - %s' % (self.titolo, self.testata)
	