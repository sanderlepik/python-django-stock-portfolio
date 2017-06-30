from django.shortcuts import render
from yahoo_finance import Share
import time
from .models import Stocks
from .forms import StockForm


def update_stock_table(request):
    """
    function, that allows to add or remove stock options and displays them in portfolio
    
    :param request: POST request that defines weather to add or remove stock options to portfolio
    :return: index.html with context dictionary that has all the stock options that you have added to portfolio
    """

    stock_list = Stocks.objects.order_by('price')[:10]

    today_date = time.strftime("%d.%m.%Y %H:%M")

    if 'new_stock' in request.POST:

        if request.method == 'POST':
            form = StockForm(request.POST)

            if form.is_valid():
                new_stock = request.POST.get("new_stock", "")

                if not Stocks.objects.filter(symbol=new_stock.upper()):

                    try:
                        stock_object = Share(new_stock)
                        new_stock_name = stock_object.get_name()
                        new_stock_price = stock_object.get_price()
                        new_stock_change = stock_object.get_change()

                        stock_to_db = Stocks(symbol=new_stock.upper(),
                                             name=new_stock_name,
                                             price=new_stock_price,
                                             change=new_stock_change)
                        stock_to_db.save()

                        add_success_message = "Stock successfully added to portfolio!"

                        context = {
                            'stock_list': stock_list,
                            'today_date': today_date,
                            'add_success_message': add_success_message
                        }

                    except Exception:
                        pass
                        error_message = "Insert correct symbol!"

                        context = {
                            'stock_list': stock_list,
                            'today_date': today_date,
                            'error_message': error_message,
                        }

                else:
                    stock_exists_message = "Stock is already in your portfolio!"

                    context = {
                        'stock_list': stock_list,
                        'today_date': today_date,
                        'stock_exists_message': stock_exists_message,
                    }
                    return render(request, 'stockInformation/index.html', context)

        else:
            for stock in stock_list:
                stock_symbol = stock.symbol
                stock_object = Share(stock_symbol)
                stock.price = stock_object.get_price()
                stock.change = stock_object.get_change()
                stock.save()

                context = {
                    'stock_list': stock_list,
                    'today_date': today_date,
                }

        return render(request, 'stockInformation/index.html', context)

    elif 'remove_stock' in request.POST:

        if request.method == 'POST':
            symbol = request.POST.get("remove_stock", "")

            try:
                Stocks.objects.filter(symbol=symbol).delete()
                stock_list = Stocks.objects.order_by('price')[:10]

                delete_success_message = "Stock successfully removed from portfolio!"

                context = {
                    'stock_list': stock_list,
                    'today_date': today_date,
                    'delete_success_message': delete_success_message,
                }

            except Exception:
                remove_error_message = "Insert correct symbol!"

                context = {
                    'stock_list': stock_list,
                    'today_date': today_date,
                    'remove_error_message': remove_error_message,
                }

        return render(request, 'stockInformation/index.html', context)

    context = {
        'stock_list': stock_list,
        'today_date': today_date,
    }
    return render(request, 'stockInformation/index.html', context)

