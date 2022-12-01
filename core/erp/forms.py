from django.forms import ModelForm
from django import forms

from .models import *


class CompanyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True
        for key in self.fields:
            input = self.fields[key]
            if type(input) is forms.CharField:
                input.widget.attrs.update({'placeholder': 'Ingrese una {}'.format(input.label.lower()), 'class': 'form-control', 'autocomplete': 'off'})

    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'ruc': forms.TextInput(attrs={'placeholder': 'Ingrese un ruc'}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Ingrese un teléfono celular'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Ingrese un teléfono convencional'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese un email'}),
            'address': forms.TextInput(attrs={'placeholder': 'Ingrese una dirección'}),
            'website': forms.TextInput(attrs={'placeholder': 'Ingrese una dirección web'}),
            'description': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
            'mission': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
            'vision': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
            'about_us': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
            'iva': forms.TextInput(),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class SizeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Size
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class CityForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = City
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TariffForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].widget.attrs['autofocus'] = True

    class Meta:
        model = Tariff
        fields = '__all__'
        widgets = {
            'city': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'minimum_weight': forms.TextInput(),
            'maximum_weight': forms.TextInput(),
            'price': forms.TextInput(),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ConditionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Condition
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class EventTypeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = EventType
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'names': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'dni': forms.TextInput(attrs={'placeholder': 'Ingrese un número de cedula'}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Ingrese un teléfono celular'}),
            'address': forms.TextInput(attrs={'placeholder': 'Ingrese una dirección'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese un email'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                instace = super().save()
                data = instace.toJSON()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class EmployeeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True
        self.fields['headings'].queryset = Headings.objects.filter(state=True)

    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'names': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'dni': forms.TextInput(attrs={'placeholder': 'Ingrese un número de cédula'}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Ingrese un teléfono celular'}),
            'address': forms.TextInput(attrs={'placeholder': 'Ingrese una dirección'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese un email'}),
            'rmu': forms.TextInput(),
            'headings': forms.SelectMultiple(attrs={'class': 'select2', 'multiple': 'multiple', 'style': 'width:100%'})
        }
        exclude = ['date_joined']

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                instace = super().save()
                data = instace.toJSON()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class HeadingsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Headings
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'percent': forms.TextInput(),
            'type': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'calculation_method': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
        }
        exclude = ['valor']

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class SalaryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Salary
        fields = '__all__'
        widgets = {
            'year': forms.TextInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-toggle': 'datetimepicker',
                'data-target': '#year',
                'value': datetime.now().year
            }),
            'month': forms.Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%;'
            }),
        }

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


class AssistanceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    date_joined = forms.DateField(input_formats=['%Y-%m-%d'], widget=forms.DateInput(format='%Y-%m-%d', attrs={
        'class': 'form-control datetimepicker-input',
        'id': 'date_joined',
        'value': datetime.now().strftime('%Y-%m-%d'),
        'data-toggle': 'datetimepicker',
        'data-target': '#date_joined'
    }), label='Fecha de asistencia')

    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
    }), label='Fecha de inicio y finalización')


class EventsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].widget.attrs['autofocus'] = True

    class Meta:
        model = Events
        fields = 'employee', 'event_type', 'date_joined', 'details'
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'event_type': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'details': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3})
        }
        exclude = ['start_date', 'end_date', 'start_time', 'end_time', 'state']

    date_joined = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }), label='Fecha y hora de registro')


class ProviderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Provider
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'ruc': forms.TextInput(attrs={'placeholder': 'Ingrese un número de ruc'}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Ingrese un teléfono celular'}),
            'address': forms.TextInput(attrs={'placeholder': 'Ingrese una dirección'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese un email'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                instace = super().save()
                data = instace.toJSON()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'code': forms.TextInput(attrs={'placeholder': 'Ingrese un código'}),
            'description': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
            'category': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'type': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'price': forms.TextInput(),
            'pvp': forms.TextInput(),
        }
        exclude = ['stock']

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class PurchaseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['provider'].queryset = Provider.objects.none()

    class Meta:
        model = Purchase
        fields = '__all__'
        widgets = {
            'number': forms.TextInput(attrs={'placeholder': 'Ingrese un número de factura', 'class': 'form-control', 'autocomplete': 'off'}),
            'provider': forms.Select(attrs={'class': 'custom-select select2'}),
            'payment_condition': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'date_joined': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'date_joined',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#date_joined'
            }),
            'end_credit': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'end_credit',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#end_credit'
            }),
            'subtotal': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off'
            }),
        }


class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'employee': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'type': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'date_joined': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'date_joined',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#date_joined'
            }),
            'date_attention': forms.TextInput(attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'date_attention',
                'value': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'data-toggle': 'datetimepicker',
                'data-target': '#date_attention'
            }),
            'subtotal': forms.TextInput(attrs={
                'class': 'form-control',
                'disabled': True
            }),
            'iva': forms.TextInput(attrs={
                'class': 'form-control',
                'disabled': True
            }),
            'total_iva': forms.TextInput(attrs={
                'class': 'form-control',
                'disabled': True
            }),
            'total': forms.TextInput(attrs={
                'class': 'form-control',
                'disabled': True
            }),
        }


class PackageForm(forms.Form):
    description = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese una descripción',
        'class': 'form-control',
        'autocomplete': 'off'
    }), label='Descripción')

    tariff = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;'
    }), queryset=Tariff.objects.none(), label='Tarifa')

    peso = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'disabled': True,
        'value': '0.00'
    }), label='Peso')

    condition = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;'
    }), queryset=Condition.objects.all(), label='Condición')

    size = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;'
    }), queryset=Size.objects.all(), label='Tamaño')

    amount = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'value': '0.00'
    }), label='Precio')


class ShippingRouteForm(forms.Form):
    date_joined = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'value': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'disabled': True
    }), label='Fecha de registro')

    status = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;'
    }), choices=STATUS_SENDING, label='Estado')

    comment = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese un nombre',
        'autocomplete': 'off',
    }), label='Comentario')
