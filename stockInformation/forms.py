from django import forms


class StockForm(forms.Form):
    new_stock = forms.CharField(label='new_stock', max_length=10)
    stocks_bought = forms.IntegerField(label='stocks_bought')
    buying_price = forms.DecimalField(label='buying_price', min_value=0)


class DeleteNewForm(forms.Form):
    remove_stock = forms.IntegerField(label='remove_stock')



