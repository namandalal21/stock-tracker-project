from urllib import request
from django.http import HttpResponse 
from django.shortcuts import render
from yahoo_fin.stock_info import * # type: ignore
import time
import queue
# Create your views here.
def stockPicker(request):
    stock_picker = tickers_nifty50()
    print(stock_picker)
    return render(request, 'mainapp/stockpicker.html',{'stockpicker':stock_picker})

import threading

def get_quote_thread(q, stock):
    result = get_quote_table(stock)
    q.put({stock: result})

def stocktracker(request):
    stockPicker = request.GET.getlist('stockpicker')
    print(stockPicker)
    data = {}
    available_stock = tickers_nifty50()
    start = time.time()
    q = queue.Queue()
    threads = []
    for i in stockPicker:
        if i in available_stock:
            thread = threading.Thread(target=get_quote_thread, args=(q, i))
            threads.append(thread)
            thread.start()
        else:
            return HttpResponse("Error")
    for thread in threads:
        thread.join()
    while not q.empty():
        result = q.get()
        data.update(result)
    end = time.time()
    time_taken = end - start
    print(time_taken)
    print(data)
    return render(request, 'mainapp/stocktracker.html',{'data': data})