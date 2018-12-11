import inspect
import sys
import numpy as np
import math
import matplotlib.pyplot as plt
'''
Raise a "not defined" exception as a reminder 
'''
its = 0
def _raise_not_defined():
    print "Method not implemented: %s" % inspect.stack()[1][3]
    sys.exit(1)

'''
Kalman 2D
'''
def kalman2d(data):
    estimated = list()
    # Your code starts here 
    # You should remove _raise_not_defined() after you complete your code
    # Your code ends here 
    #_raise_not_defined()
    I = 1.1*np.matrix(np.eye(2))
    Q= np.matrix([[.0001,.00002],[.00002,.0001]])
    R= np.matrix([[.01,.005],[.005,.02]])
    g= np.random.normal(0, .1,2)
    w = np.multiply(g,Q)
    v = np.multiply(g,R)

    for x in xrange(0,len(data)):
        u=[data[x][0],data[x][1]]
        z=[data[x][2],data[x][3]]
        x_k=z-v
        x_k_1=x_k-u+w;
        temp = np.array(np.multiply(x_k_1,I)).flatten()
        estimated.append([temp[0],temp[3]])
    print(estimated)
    return estimated


'''
Plotting
'''
def plot(data, output):
    # Your code starts here
    # You should remove _raise_not_defined() after you complete your code
    # Your code ends here
    tempx = []
    tempy = []
    temp1x = []
    temp1y = []
    for x in range(0,len(data)):
        plt.plot(data[x][2],data[x][3],'bo')
        tempx.append(data[x][2])
        tempy.append(data[x][3])
        plt.plot(output[x][0],output[x][1],'ro')
        temp1x.append(output[x][0])
        temp1y.append(output[x][1])
    plt.plot(tempx,tempy,'b-')
    plt.plot(temp1x,temp1y,'r-')
    plt.axis([1, 10, -3, 2])
    plt.ylabel('Y')
    plt.xlabel('X')
    plt.show()



    return

'''
Kalman 2D 
'''
def kalman2d_shoot(ux, uy, ox, oy, reset=False):
    decision = (0, 0, False)
    global its 
    its +=1
    fire = False;
    I = np.matrix(np.eye(2))
    #Q= np.matrix([[.0001,.00002],[.00002,.0001]])
    R= np.matrix([[.01,.005],[.005,.02]])
    g= np.random.normal(0, .1,2)
    w = 0#= np.multiply(g,Q)
    v = np.multiply(g,R)
        
    u=[ux,uy]
    z=[ox,oy]
        
    x_k=z-v
    x_k_1=x_k-u+w;
        
    tempx = np.array(np.multiply(x_k,I)).flatten()
    tempk_1 = np.array(np.multiply(x_k_1,I)).flatten()

    z = math.fabs(tempx[0])-math.fabs(tempk_1[0])  
    if(math.fabs(z) <= .5 or its ==200):
        fire = True;

    decision=(tempx[0],tempx[3],fire)
    return decision

'''
Kalman 2D 
'''
def kalman2d_adv_shoot(ux, uy, ox, oy, reset=False):
    decision = (0, 0, False)
    # Your code starts here 
    # Your code ends here 
    _raise_not_defined()
    return decision


