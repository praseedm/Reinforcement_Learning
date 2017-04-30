
import ma_Gui
import threading
import time
import csv
import pickle
import os

discount = 0.8
actions = ma_Gui.actions
states = []
Q = {}



for i in range(ma_Gui.x):
    for j in range(ma_Gui.y):
        states.append((i, j))


def init_Q() :
	for state in states:
		temp = {}
		for action in actions:
			temp[action] = 0.1
		Q[state] = temp

#Read Q
if os.path.isfile('ma_data.pkl'):
	pkl_file = open('ma_data.pkl', 'rb')
	Q = pickle.load(pkl_file) 
	#print Q[(0,4)] 
	print "READ\n" 
else :
	init_Q()
	print "Initialize\n" 

for wall in ma_Gui.walls:
	temp = {}
	for action in actions:
		temp[action] = -1
	Q[wall] = temp  

for (i, j, c, w) in ma_Gui.specials:
    for action in actions:
        Q[(i, j)][action] = w
        


def do_action(action):
    s = ma_Gui.player
    r = -ma_Gui.score
    if action == actions[0]:
        ma_Gui.try_move(0, -1)
    elif action == actions[1]:
        ma_Gui.try_move(0, 1)
    elif action == actions[2]:
        ma_Gui.try_move(-1, 0)
    elif action == actions[3]:
        ma_Gui.try_move(1, 0)
    else:
        return
    s2 = ma_Gui.player
    r += ma_Gui.score
    return s, action, r, s2

def ma_do_action(action):
    s = ma_Gui.ma_player
    r = -ma_Gui.ma_score
    if action == actions[0]:
        ma_Gui.ma_try_move(0, -1)
    elif action == actions[1]:
        ma_Gui.ma_try_move(0, 1)
    elif action == actions[2]:
        ma_Gui.ma_try_move(-1, 0)
    elif action == actions[3]:
        ma_Gui.ma_try_move(1, 0)
    else:
        return
    s2 = ma_Gui.ma_player
    r += ma_Gui.ma_score
    return s, action, r, s2    

#Find Optimal action for a state
def max_Q(s):
    val = None
    act = None
    for a, q in Q[s].items():
        if val is None or (q > val):
            val = q
            act = a
    return act, val


def inc_Q(s, a, alpha, inc):
    Q[s][a] *= 1 - alpha
    Q[s][a] += alpha * inc
    
    
def printq():
	pkl_file = open('ma_data.pkl', 'wb+')
	pickle.dump(Q, pkl_file)
	target = open('ma_dict_2.csv', 'wb')
	writer = csv.writer(target)
	for i in Q.keys():
		writer.writerow([i,Q[i]])
	target.close();
	
		     


def run():
    global discount
    time.sleep(1)
    alpha = 1
    t = 1
    count = 0
    ff = 0
    
    printq()
    
    while True:
    	i= 0
    	ff += 1
        # Pick  action
        s = ma_Gui.player
        #print Q[(0,4)] 
        max_act, max_val = max_Q(s)
        (s, a, r, s2) = do_action(max_act)
        
		
        # Update Q
        max_act, max_val = max_Q(s2)
        inc_Q(s, a, alpha, r + discount * max_val)
        printq()

        #  restarted
        t += 1.0
        if ma_Gui.has_restarted():
        	count += 1
        	ma_Gui.restart_game()
        	time.sleep(0.01)
        	t = 1.0
        	print "\nIteration = " , count
        	'''if count == 2 :
        		break'''
            

        # Update the learning rate
        alpha = pow(t, -0.1)

        # SLEEP.
        time.sleep(0.01)
        

def magent():
    global discount
    time.sleep(1)
    alpha = 1
    t = 1
    count = 0
    ff = 0
    while True:
        # explore agent
        agent2 = ma_Gui.ma_player
        #pick action
        max_act, max_val = max_Q(agent2)
        (s, a, r, s2) = ma_do_action(max_act)

        # Update Q
        max_act, max_val = max_Q(s2)
        inc_Q(s, a, alpha, r + discount * max_val)
        printq()

        #  restarted
        t += 1.0
        if ma_Gui.ma_has_restarted():
            count += 1
            ma_Gui.ma_restart_game()
            time.sleep(0.01)
            t = 1.0
            print "\nIteration = " , count
            '''if count == 2 :
                break'''
            

        # Update the learning rate
        alpha = pow(t, -0.1)

        # SLEEP.
        time.sleep(0.1)

t_multi = threading.Thread(target=magent)
t_multi.daemon = True

t = threading.Thread(target=run)
t.daemon = True
t.start()
t_multi.start()
ma_Gui.start_game()
