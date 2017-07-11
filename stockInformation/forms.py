from django import forms


class AddStockForm(forms.Form):
    add_stock = forms.CharField(label='add_stock', max_length=10)
    stocks_bought = forms.IntegerField(label='stocks_bought')
    buying_price = forms.DecimalField(label='buying_price', min_value=0)


class RemoveStockForm(forms.Form):
    remove_stock = forms.CharField(label='remove_stock')

