import pickle
import os

dynamic_walls = {0:[(1, 1), (1, 2), (2, 2) , (3,0) , (4,2) ], 1: [(1, 1), (1,3), (1,4), (1, 2), (2, 2) , (3,0) , (4,2)]}

walli = 0
print "test : ",dynamic_walls[0]

'''if os.path.isfile('ma_data.pkl'):
    pkl_file = open('ma_data.pkl', 'rb')
    Q = pickle.load(pkl_file) 
    #print Q[(0,4)] 
    print "READ\n",Q'''

