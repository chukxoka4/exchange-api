#%%
from pip._vendor import requests
# %%
response = requests.get("https://api.exchangeratesapi.io/latest?base=USD")
print(response.status_code)
# %%
