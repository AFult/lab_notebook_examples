
import numpy as np
import pandas as pd
import scipy.stats
from random import shuffle


# Python Functions for permutation based statistics

def permuted_f(arg_list, num_permutes = 0):
    #determine f before permutations
    f_org, p_org = scipy.stats.f_oneway(*arg_list)
    
    #name vars
    counter = 0
    alldata = np.concatenate(arg_list)
    al_lens = [len(x) for x in arg_list]
    al_ranges = [(sum(al_lens[0:x]), sum(al_lens[0:x]) + al_lens[x]) for x in range(0,len(al_lens))]
    df1 = len(arg_list) - 1
    df2 = len(alldata) - len(arg_list)
    
    #loop through number of permutations, shuffle all data and 
    #allocate shuffled data to groups of same length of n
    for i in xrange(0, num_permutes):
        np.random.shuffle(alldata)
        new_order = [alldata[al_ranges[x][0]:al_ranges[x][1]] for x in range(len(al_ranges))]
        f_new, p_new = scipy.stats.f_oneway(*new_order)
        if abs(f_new) > abs(f_org):
            counter += 1
            
    real_p = float(counter) / num_permutes
    
    report = 'F(%s, %s) = %s, p = %s' % (df1, df2, f_org, real_p)
    
    return (report, real_p)

def permute_t_ls(array1, array2, numperms = 10000):
    
    alldata = np.concatenate((array1, array2))
    all_len = len(alldata)
    t_list = []
    
    for i in xrange(numperms):
        np.random.shuffle(alldata)
        g1 = alldata[0:len(array1)]
        g2 = alldata[len(array1):]
        t, p = scipy.stats.ttest_ind(g1, g2, equal_var=False)
        t_list.append(t)
    
    return t_list

def perm_mc_ttests(arg_list, nperms = 1000, labels = [0,1,2,3,4,5]):
    t_all = []
    real_t = []
    tp_list = []
    
    df_t = pd.DataFrame(index=labels, columns=labels[1:])
    df_p = df_t.copy()

    for x in range(len(arg_list)):
        for y in range(x+1,len(arg_list)):
            t_all.append(permute_t_ls(arg_list[x],
                                      arg_list[y], 
                                      numperms = nperms))
            t, p = scipy.stats.ttest_ind(arg_list[x],
                                         arg_list[y],
                                         equal_var=False)
            real_t.append((x, y, t))

    t_all = np.concatenate(t_all)
    for x, y, t in real_t:
    
        count = 0
    
        for i in t_all:
            if abs(t) < abs(i):
                count += 1
    
        real_p = float(count) / len(t_all)
    
        tp_list.append((x, y, t, real_p))
    
    for x,y,t,p in tp_list:
        df_t.iloc[x][y-1] = t
        df_p.iloc[x][y-1] = p
    
    return (df_t, df_p)