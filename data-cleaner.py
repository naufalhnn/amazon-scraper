import pandas as pd

data = pd.read_csv('amazonscraper/output.csv', encoding='utf-8')
data['title'] = data['title'].str.strip()
data['price'] = data['price'].str.strip()
data['url'] = data['url'].str.strip()
data.to_excel('products.xlsx', index=False)
