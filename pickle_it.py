import pickle
from database import data

with open('export.p', 'wb') as FILE:
    pickle.dump(data, FILE)
