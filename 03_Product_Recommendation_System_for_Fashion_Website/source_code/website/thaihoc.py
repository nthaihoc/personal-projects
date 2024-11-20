import numpy as np
import sqlite3
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class CF:
    def __init__(self, table_product, table_orders, index):
        self.table_product = table_product
        self.table_orders = table_orders
        self.cnx = sqlite3.connect(r'H:\My Drive\SOURCE CODE\PYTHON\project-recommentdation-systems\instance\database.sqlite3')
        self.orders_df = None
        self.product_df = None
        self.index = index

    def load_data(self):
        query = f'SELECT * FROM {self.table_product}'
        self.product_df = pd.read_sql_query(query, self.cnx)

        query = f'SELECT * FROM \"{self.table_orders}\"'
        self.orders_df = pd.read_sql_query(query, self.cnx)
    
    def process_dataframe(self):
        self.orders_df = self.orders_df.drop(['id',"price", "status", "payment_id"], axis=1)
        self.orders_df = self.orders_df.rename(columns={"customer_link" : "User-ID", "product_link" : 'Product-ID', "quantity" : "Quantity"})
        self.orders_df = self.orders_df[["User-ID", "Product-ID", "Quantity"]]

        self.product_df = self.product_df.drop(["flash_sale", "date_added"], axis=1)
        self.product_df = self.product_df.rename(columns={"id" : "Product-ID", "product_name" : "Name"})

    def train_data(self):
        self.dummy_train = self.orders_df.copy()
        self.dummy_train['Quantity'] = self.dummy_train['Quantity'].apply(lambda x: 0 if x > 0 else 1)
        self.dummy_train = self.dummy_train.pivot_table(index="User-ID", columns="Product-ID", values="Quantity").fillna(1)

    def caculate_similarity(self):
        countings_with_name = self.orders_df.merge(self.product_df, on="Product-ID")
        self.datasets = countings_with_name.pivot_table(index="User-ID", columns="Product-ID", values="Quantity").fillna(0)
        self.user_similarity = cosine_similarity(self.datasets)
        self.user_similarity[np.isnan(self.user_similarity)] = 0

    def predict_user(self):
        self.user_predicted_ratings = np.dot(self.user_similarity, self.datasets)
        self.user_final_ratings = np.multiply(self.user_predicted_ratings, self.dummy_train)

    def recomment(self):
        prod_comment = self.user_final_ratings.iloc[self.index].sort_values(ascending = False)[0:5].index
        data = []
        for i in prod_comment:
            recomment = []
            product_items = self.product_df[self.product_df["Product-ID"] == i]
            recomment.extend(list(product_items.drop_duplicates("Product-ID")["Name"].values))
            recomment.extend(list(product_items.drop_duplicates("Product-ID")["current_price"].values))
            recomment.extend(list(product_items.drop_duplicates("Product-ID")["previous_price"].values))
            recomment.extend(list(product_items.drop_duplicates("Product-ID")["product_picture"].values))
            recomment.extend(list(product_items.drop_duplicates("Product-ID")["in_stock"].values))
            data.append(recomment)
        return data
    
    def recommentdation_systems(self):
        self.load_data()
        self.process_dataframe()
        self.train_data()
        self.caculate_similarity()
        self.predict_user()
        return self.recomment()

a = CF("Product", "Order", 1)
rcm = a.recommentdation_systems()
print(rcm)
