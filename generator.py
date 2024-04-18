from datetime import datetime
import pandas as pd
import numpy as np


YEARS = 3
PRODUCTS = 20
CLIENTS = 50
OUTLIER_PROB = 1e-5
SALES_RAISE_TREND = 0.1


# load data
products = pd.DataFrame(
    columns=['product_id', 'name', 'group'],
    data=[[i, f'pr{i}', f'grp{i % 5}'] for i in range(PRODUCTS)]
)

clients = pd.DataFrame(
    columns=['client_id', 'name'],
    data=[[i, f'cli'] for i in range(CLIENTS)]
)

sales_data = []

out_k = 500
sid = 0
bid = 0

print('generating data..')

for day in range(1, 365 * YEARS + 1):
    for client_id in clients['client_id']:
        if np.random.random() > 0.5:
            continue

        for bill_i in range(np.random.randint(1, 3)):
            bid += 1
            for product_id in products['product_id']:

                price = np.random.randint(100, 200)
                discount = np.random.randint(10, 50)

                pdr = discount / price

                if np.random.random() > 0.2 + pdr * 0.6 + 0.3 * (product_id in [1, 2]):
                    continue

                quantity = round(np.random.randint(1, 5) + SALES_RAISE_TREND * day)
                # simulate outliers
                if np.random.random() > (1 - OUTLIER_PROB):
                    quantity = round(quantity * out_k)

                date = datetime.strptime(f'{2020 + day // 366}-{day % 365 + 1:03}', "%Y-%j").strftime("%m-%d-%Y")

                sid += 1
                sales_data.append([sid, client_id, product_id, bid, discount, price, date, quantity])

print('done')

sales = pd.DataFrame(
    columns=['sale_id', 'client_id', 'product_id', 'bill_id', 'discount', 'price', 'date', 'quantity'],
    data=sales_data
)

clients.to_csv('data/clients.csv', index=False)
products.to_csv('data/products.csv', index=False)
sales.to_csv('data/sales.csv', index=False)