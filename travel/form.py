from django import forms
from dal import autocomplete
from travel.models import Attraction


class AttractionForm(forms.ModelForm):

    class Meta:
        model = Attraction
        fields = '__all__'
        widgets = {
            'province': autocomplete.ModelSelect2(
                url='/area/province-autocomplete',
                attrs={'class': 'select2-object'}
            ),
            'city': autocomplete.ModelSelect2(
                url='/area/city-autocomplete',
                forward=['province'],  # 关键！联动字段
                attrs={'class': 'select2-object'}
            ),
        }