from django import forms

class ProductForm(forms.Form):
    product = forms.CharField(max_length=30)
    price = forms.CharField(max_length=10)

    def clean(self):
        cleaned_data = super(ProductForm, self).clean()
        product = cleaned_data.get('product')
        price = cleaned_data.get('price')
        if not product and not price:
            raise forms.ValidationError('You have to write something!')

class SearchProductForm(forms.Form):
    productID = forms.CharField(max_length=30)
    priceGet = forms.CharField(max_length=10, required=False)

    def clean(self):
        cleaned_data = super(SearchProductForm, self).clean()
        product = cleaned_data.get('productID')
        price = cleaned_data.get('priceGet')
        if not product:
            raise forms.ValidationError('You have to write a product!')
