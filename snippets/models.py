from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLES_CHOICES = sorted([(item, item) for item in get_all_styles()])

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    lineos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLES_CHOICES, default='friendly', max_length=100)
    
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField()
    
    class Meta:
        ordering = ['created']
        
    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        lineos = 'table' if self.lineos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, lineos=lineos,
                                full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super().save(*args, **kwargs)
        


class TransportCompany(models.Model):
    TransportTypes = [
        ("BU", "BUS"),
        ("PL", "PLANE"),
        ("TR", "TRAIN"),
        ("BO", "BOAT"),
    ]

    name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(max_length=254, unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=255, null=False, blank=False)
    description = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(choices=TransportTypes, default=TransportTypes[0][0], max_length=2)
