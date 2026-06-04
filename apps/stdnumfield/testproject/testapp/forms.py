# coding=utf-8
from django.forms import ModelForm
from django.forms.forms import Form

from stdnumfield.forms import StdnumField

from .models import SomeModel


class SampleForm(Form):
    oib = StdnumField(formats=['hr.oib'])


class SampleModelForm(ModelForm):
    class Meta:
        model = SomeModel
        fields = ('oib',)
        error_messages = {
            'oib': {
                'stdnum_format': "Foo error message",
            },
        }
