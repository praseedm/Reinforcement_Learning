import pickle

pkl_file = open('data.pkl', 'rb')
Q = pickle.load(pkl_file) 
print Q

