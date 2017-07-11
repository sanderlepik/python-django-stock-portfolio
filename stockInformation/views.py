from django.shortcuts import render
from yahoo_finance import Share
import time
import decimal
import logging
from .models import Stocks
from .forms import AddStockForm


# CREATING LOGGER
logger = logging.getLogger('LOG')
logger.setLevel(logging.INFO)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


def update_stock_table(request):
    """
    function, that allows to add or remove stock options and displays them in portfolio
    
    Another possibility: https://query.yahooapis.com/v1/public/yql?q=select%20Ask%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22GOOGL%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=
    
    :param request: POST request that defines weather to add or remove stock options to portfolio
    :return: stocks.html with context dictionary that has all the stock options that you have added to portfolio
    """

    stock_list = Stocks.objects.order_by('price')[:10]

    today_date = time.strftime("%d.%m.%Y %H:%M")

    if 'add_stock' in request.POST:

            form = AddStockForm(request.POST)

            if form.is_valid():  # form validation
                new_stock = request.POST.get("add_stock", "")

                if not Stocks.objects.filter(symbol=new_stock.upper()):  # stock not already in portfolio

                    logger.info('Adding ' + new_stock.upper() + ' to stock portfolio')

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
                        return render(request, 'stockInformation/stocks.html', context)

                    except Exception:  # if symbol is not correct
                        pass
                        error_message = "Insert correct symbol!"

                        context = {
                            'stock_list': stock_list,
                            'today_date': today_date,
                            'error_message': error_message,
                        }
                        return render(request, 'stockInformation/stocks.html', context)

                else:  # if symbol is already in your portfolio
                    stock_exists_message = "Stock is already in your portfolio!"

                    context = {
                        'stock_list': stock_list,
                        'today_date': today_date,
                        'stock_exists_message': stock_exists_message,
                    }
                    return render(request, 'stockInformation/stocks.html', context)

            else:  # if form was incorrectly filled in
                error_message = "Invalid form!"

                context = {
                    'stock_list': stock_list,
                    'today_date': today_date,
                    'error_message': error_message,
                }
                return render(request, 'stockInformation/stocks.html', context)

    elif 'remove_stock' in request.POST:  # if user was trying to remove stock from portfolio

        symbol = str(request.POST.get('stock_symbol'))

        if Stocks.objects.filter(symbol=symbol).count() > 0:  # if inserted stock is in portfolio

            logger.info('Removing ' + symbol + ' from stock portfolio')

            Stocks.objects.filter(symbol=symbol).delete()
            stock_list = Stocks.objects.order_by('price')[:10]

            delete_success_message = "Stock successfully removed from portfolio!"

            context = {
                'stock_list': stock_list,
                'today_date': today_date,
                'delete_success_message': delete_success_message,
            }
            return render(request, 'stockInformation/stocks.html', context)

    else:  # if there was no POST request - the whole portfolio should be updated

        stocks = Stocks.objects.all()  # This returns queryset

        for stock in stocks:
            stock_object = Share(stock.symbol)

            stock.price = decimal.Decimal(stock_object.get_price())
            stock.change = stock_object.get_change()

            balance = (stock.stocks_owned * stock.price) - (stock.stocks_owned * stock.buying_price)
            stock.balance = balance

            stock.save(update_fields=['price', 'change', 'balance'])  # do not create new object in db,
            # update current lines

        context = {
            'stock_list': stock_list,
            'today_date': today_date
        }

        logger.info('Refreshing stock list')

        return render(request, 'stockInformation/stocks.html', context)


def crowdfunding(request):
    context = {
    }

    return render(request, 'stockInformation/crowdfunding.html', context)