import hashlib
import pandas as pd
import os
data_dir = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data"))


class Auth:

    def authenticate(self, username, password):
        df_account = pd.read_csv(os.path.join(data_dir, "account.csv"))
        user = df_account.loc[df_account["username"] == username]
        hashed_password = hashlib.sha256(
            password.encode('utf-8')).hexdigest()
        if hashed_password == user['password']:
            print('Password matched')
            return True
        return False

    def get_user(self, username):
        df_account = pd.read_csv(os.path.join(data_dir, "account.csv"))
        user = df_account.loc[df_account["username"] == username]
        for _, row in user.iterrows():
            return {
                "username": row["username"],
                "password": row["password"],
            }

    def insert_user(self, data):
        try:
            df_account = pd.read_csv(os.path.join(data_dir, "account.csv"))
            df_insert_data = pd.DataFrame([data])
            print(df_insert_data)
            df_account = pd.concat(
                [df_account, df_insert_data], ignore_index=True)
            df_account.to_csv(os.path.join(
                data_dir, "account.csv"), index=False)
        except Exception as e:
            print(e)
            return False
        return True
