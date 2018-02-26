# RDFSerializer


Examples:
=========
```
class PubOrigin(models.Model):
    url = models.URLField(unique=True, db_index=True)
    
class PubAuthor(models.Model):
    name = models.CharField(max_length=256)

class PubPublisher(models.Model):
    name = models.CharField(max_length=1024, unique=True, db_index=True)
    href = models.URLField(blank=True, null=True)

    def __str__(self):
        return str(self.name)

class Publication(models.Model):
    title = models.CharField(max_length=1024, blank=True, null=True)
    authors = models.ManyToManyField(PubAuthor)
    journal = models.ForeignKey(PubJournal, blank=True, null=True, on_delete=models.DO_NOTHING)
    publisher = models.ForeignKey(PubPublisher, blank=True, null=True, on_delete=models.DO_NOTHING)
    published = models.DateField(blank=True, null=True)
    summary = models.TextField(default="", blank=True, null=True)
    origins = models.ManyToManyField(PubOrigin)
```

```
class PublicationRDFSerializer(RDFModelSerialiser):
    _type = SCHEMA.Article
    model = Publication
    uri = reverse('publications:details')
    entries = [
        RDFSimpleField(SCHEMA.name, 'title'),
        RDFManyField(SCHEMA.authors, 'authors', lambda _obj: _obj.name),
        RDFSimpleField(SCHEMA.datePublished, 'published'),
        RDFSimpleField(SCHEMA.publisher, 'publisher'),
        RDFSimpleField(SCHEMA.description, 'summary'),
        RDFManyField(SCHEMA.sameAs, 'origins', lambda _obj: _obj.url),
        RDFLeftBinder(SCHEMA.isPartOf, 'journal', OriginRDFSerializer)
    ]  
```
