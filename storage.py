import pandas as pd


# Load data from storage implementation

clients = pd.read_csv('data/clients.csv')
products = pd.read_csv('data/products.csv')
sales = pd.read_csv('data/sales.csv')


# Append computed fields

sales['date'] = pd.to_datetime(sales['date'])

min_year = sales['date'].dt.year.min()
sales['week'] = sales['date'].dt.isocalendar().week + ((sales['date'].dt.isocalendar().year - min_year) * 53)

sales['discount_prc'] = sales['discount'] / (sales['discount'] + sales['price'])
sales['profit'] = (sales['price'] + 100 * sales['discount']) / (sales['discount'] + sales['price'])

sales = pd.merge(sales, products[['product_id', 'group']], on='product_id')


# utility functions

def list_groups():
    return list(products['group'].unique())


def list_product_names():
    return list(products['name'])