from django import forms

from core.erp.choices import TYPE_PRODUCT
from core.erp.models import Employee, Provider, Product, Sale
from core.user.models import User


class ReportForm(forms.Form):
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }), label='Buscar por rango de fechas')

    year_month = forms.CharField(widget=forms.TextInput(
        attrs={
            'autocomplete': 'off',
            'placeholder': 'MM / AA',
            'class': 'form-control datetimepicker-input',
            'id': 'year_month',
            'data-toggle': 'datetimepicker',
            'data-target': '#year_month',
        }
    ), label='Año/Mes')

    type_sale = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;'
    }), label='Tipo de Venta')

    employee = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;'
    }), queryset=Employee.objects.all(), label='Empleado')

    user = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;'
    }), queryset=User.objects.all(), label='Usuario')

    provider = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;'
    }), queryset=Provider.objects.all(), label='Proveedor')

    product = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;'
    }), queryset=Product.objects.filter(type=TYPE_PRODUCT[0][0]), label='Producto')

    sale = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;'
    }), queryset=Sale.objects.all(), label='Número de guía')
