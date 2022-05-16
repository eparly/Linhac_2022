#import libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

import pandas as pd
import math
import scipy.interpolate as sci

#import data
data = pd.read_csv(r'C:\Users\13432\Documents\LINHAC_2022_data.csv')
img = plt.imread(r'C:\Users\13432\Pictures\hockeyrink.png')
rebound = []
saves = []
shot1 = []
shot2 = []
multi_coords = []
xG = []
nan = float("nan")
rebound_check = False

#function finds the average xg of list of shots
def avg_tup(shot):
    s = 0
    for i in range(len(shot)):
        a = shot[i][2]
        s+=a
    s=s/len(shot)
    
    
    return s
   
#function sorts list of shots based on xg     

def sort_tuple(shot, k):
    shot.sort(key = lambda x: x[k])
    return shot

#creates a plot showing pre-rebound shot based on rebound xg
def plot_rebounds(shot):
    x = []
    y = []
    xg = []
    
    for i in range(len(shot)):
        x.append(shot[i][3])
        y.append(shot[i][4])
        xg.append(shot[i][2])
        
    ax=plt.axes()
    ax.set_title("pre-rebound shot based on rebound xg")
    
    plt.hexbin(x, y, xg, (5,5))
    plt.colorbar()
    plt.show()
    

#creates an smooth heat map of rebound xg based on distance to net of original shot
def xg_inter(shot):
    
    x2 = []
    y2 = []
    xg = []
        
    for i in range(len(shot)):
        x2.append(shot[i][3])
        y2.append(shot[i][4])
        xg.append(shot[i][2])
        
  
    #setting boundaries
    xnew_edges, ynew_edges = np.mgrid[25:100:93j, -45:45:93j]
    xnew = xnew_edges[:-1, :-1] + np.diff(xnew_edges[:2, 0])[0] / 2
    ynew = ynew_edges[:-1, :-1] + np.diff(ynew_edges[0, :2])[0] / 2
    
    #evaluating the data
    tck = sci.bisplrep(x2, y2, xg, s = 0)
    znew = sci.bisplev(xnew[:, 0], ynew[:, 0], tck)
    
    #plotting data
    plt.figure()
    ax = plt.axes()
    ax.imshow(img, extent = [25, 100, -45, 45])
    n = mpl.colors.Normalize()
    lims = dict(cmap = 'RdBu_r', vmin = 0, vmax = 1)
    plt.pcolormesh(xnew_edges, ynew_edges, znew, shading = 'flat', alpha = 0.2, **lims)
    plt.colorbar()
    plt.title('Xg of rebound shot based on original shot location')
    plt.show()
    

    return    

#creates plot of xg based on location, as well as shot frequency
def plot_xy(shot):
    x2 = []
    y2 = []
    xg = []
        
    for i in range(len(shot)):
        x2.append(shot[i][0])
        y2.append(shot[i][1])
        xg.append(shot[i][2])
      
        
      
    ax = plt.axes()
    ax.set_title("xg based on location")
    plt.hexbin(x2, y2, xg, (5,5))
    plt.colorbar()
    plt.show()
    
    ax = plt.axes()
    ax.set_title("shot frequency")
    plt.hist2d(x2, y2, bins = (8, 10), cmap = 'inferno', range = ([30,90],[-40, 40]))
    plt.colorbar()
    plt.show()

    

#cleans and sorts the data into different lists    
def rebound_shots(data):
    i=0
  
    while (i!=76038):
        
        rebound_check = False
        possession_change = False
        #checking for possession changes
        while((data["teaminpossession"][i]==data["teaminpossession"][i+1]) or (math.isnan(data["teaminpossession"][i]))):
            if (data["eventname"][i]=="shot" and data["xadjcoord"][i]>25 and rebound_check ==False):
                #records shot data
                original_x = data["xadjcoord"][i]
                original_y = data["yadjcoord"][i]
                original_xg = data["xg"][i]
                shot1.append((data["xadjcoord"][i], data["yadjcoord"][i], data['xg'][i]))
      
        #creates list of all rebound locations
            if data["eventname"][i]=="rebound": 
                rebound.append((data["xadjcoord"][i], data["yadjcoord"][i]))
                rebound_check = True
                
            #checks for second chances and records any extra shots
            if rebound_check == True:
                if data["eventname"][i]=="shot" and data["xadjcoord"][i]>25:
                    shot2.append((data["xadjcoord"][i], data["yadjcoord"][i], data['xg'][i], original_x, original_y, original_xg))
            i+=1
            possession_change = True
        
        
        if (possession_change == False):
            i+=1
           


rebound_shots(data)
sort_tuple(shot2, 2)
plot_xy(shot1)
plot_xy(shot2)
plot_rebounds(shot2)
xg_inter(shot2)





       
        



