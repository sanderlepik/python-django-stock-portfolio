from django import forms


class StockForm(forms.Form):
    new_stock = forms.CharField(label='new_stock', max_length=100)


class DeleteNewForm(forms.Form):
    remove_stock = forms.CharField(label='remove_stock', max_length=100)



