from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import ProductForm, SearchProductForm
import consul
import json
import requests

# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

def elements(request):
    #getting consul service for use the redis api
    consul_service = consul.Consul(host='consul')
    #get service_api
    consul_service_api = consul_service.catalog.service('service_api')
    #get info about service_api
    json_service_str = consul_service_api[1]
    json_service = json.dumps(json_service_str[0])
    data_service = json.loads(json_service)
    #set the url to use de api from consul
    url = "http://"+data_service["ServiceAddress"]+":"+str(data_service["ServicePort"])
    #print(fetch_products.json())
    if request.method == 'POST':
        if '_add' in request.POST:
            form = ProductForm(request.POST)
            if form.is_valid():
                product = form.cleaned_data['product']
                price = form.cleaned_data['price']
                payload = {"key":product,"value":price}
                post_product = requests.post(url+"/api/product", json=payload)
                print(post_product.json())
                search = SearchProductForm()
                pass
            search = SearchProductForm()
        elif '_search' in request.POST:
            search = SearchProductForm(request.POST)
            if search.is_valid():
                product = search.cleaned_data['productID']
                get_product = requests.get(url+"/api/product/"+product)
                print(get_product.json())
                search = SearchProductForm(initial={'productID':product,'priceGet':get_product.json()})
                pass
            form = ProductForm()
    else:
        form = ProductForm()
        search = SearchProductForm()
    #get all products
    fetch_products = requests.get(url+"/api/all")
    return render(request, 'elements.html', {'form': form,'search': search, 'fetch_products': fetch_products.json()})
