from django.shortcuts import render
from yahoo_finance import Share
import time
from .models import Stocks
from .forms import StockForm


def update_stock_table(request):
    """
    function, that allows to add or remove stock options and displays them in portfolio
    
    Another possibility: https://query.yahooapis.com/v1/public/yql?q=select%20Ask%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22GOOGL%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=
    
    :param request: POST request that defines weather to add or remove stock options to portfolio
    :return: index.html with context dictionary that has all the stock options that you have added to portfolio
    """

    stock_list = Stocks.objects.order_by('price')[:10]

    today_date = time.strftime("%d.%m.%Y %H:%M")

    if 'new_stock' in request.POST:

        if request.method == 'POST':
            form = StockForm(request.POST)

            if form.is_valid():  # form validation
                new_stock = request.POST.get("new_stock", "")

                if not Stocks.objects.filter(symbol=new_stock.upper()):  # stock not already in portfolio

                    try:  # try to add stock to portfolio
                        stock_object = Share(new_stock)
                        new_stock_name = stock_object.get_name()
                        new_stock_price = stock_object.get_price()
                        new_stock_change = stock_object.get_change()
                        stocks_owned = form.cleaned_data['stocks_bought']
                        buying_price = form.cleaned_data['buying_price']

                        stock_to_db = Stocks(symbol=new_stock.upper(),
                                             name=new_stock_name,
                                             price=new_stock_price,
                                             change=new_stock_change,
                                             stocks_owned=stocks_owned,
                                             buying_price=buying_price,
                                             balance=0
                                             )
                        stock_to_db.save()

                        add_success_message = "Stock successfully added to portfolio!"

                        stock = Stocks.objects.get(symbol=new_stock)
                        stocks = stock.stocks_owned
                        bprice = stock.buying_price
                        price = stock.price
                        balance = (stocks * price) - (stocks * bprice)
                        stock.balance = balance
                        stock.save()

                        context = {
                            'stock_list': stock_list,
                            'today_date': today_date,
                            'add_success_message': add_success_message,
                        }
                        return render(request, 'stockInformation/index.html', context)

                    except Exception:  # if symbol is not correct
                        pass
                        error_message = "Insert correct symbol!"

                        context = {
                            'stock_list': stock_list,
                            'today_date': today_date,
                            'error_message': error_message,
                        }
                        return render(request, 'stockInformation/index.html', context)

                else:  # if symbol is already in your portfolio
                    stock_exists_message = "Stock is already in your portfolio!"

                    context = {
                        'stock_list': stock_list,
                        'today_date': today_date,
                        'stock_exists_message': stock_exists_message,
                    }
                    return render(request, 'stockInformation/index.html', context)

            else:  # if form was incorrectly filled in
                error_message = "Invalid form!"

                context = {
                    'stock_list': stock_list,
                    'today_date': today_date,
                    'error_message': error_message,
                }
                return render(request, 'stockInformation/index.html', context)

    elif 'remove_stock' in request.POST:  # if user was trying to remove stock from portfolio

        if request.method == 'POST':
            symbol = request.POST.get("remove_stock", "")

            if Stocks.objects.filter(symbol=symbol).count() > 0:  # if inserted stock is in portfolio

                Stocks.objects.filter(symbol=symbol).delete()
                stock_list = Stocks.objects.order_by('price')[:10]

                delete_success_message = "Stock successfully removed from portfolio!"

                context = {
                    'stock_list': stock_list,
                    'today_date': today_date,
                    'delete_success_message': delete_success_message,
                }
                return render(request, 'stockInformation/index.html', context)

            else:  # if user entered stock symbol that is not in portfolio or is invalid
                remove_error_message = "Insert correct symbol!"

                context = {
                    'stock_list': stock_list,
                    'today_date': today_date,
                    'remove_error_message': remove_error_message,
                }
                return render(request, 'stockInformation/index.html', context)

    else:  # if there was no POST request - the whole portfolio should be updated

        stocks = Stocks.objects.all()

        for stock in stocks:
            stock_object = Share(stock.symbol)

            stock.price = stock_object.get_price()
            stock.change = stock_object.get_change()

            stock.save(update_fields=['price', 'change'])

        context = {
            'stock_list': stock_list,
            'today_date': today_date
            # 'values': [['january', 1.62], ['february', 1.66], ['march', 1.69], ['april', 1.62],
            # ['may', 1.58], ['june', 1.72], ['july', 1.75],
            # ['august', 1.75], ['september', 1.75], ['october', 1.75], ['november', 1.75], ['december', 1.75]]
        }
        return render(request, 'stockInformation/index.html', context)


