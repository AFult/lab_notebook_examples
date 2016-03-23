import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import re
from collections import defaultdict, OrderedDict

# seperate group label and subject ID into tuple (subject number, group)
def group_id_split(string):
        if '-' in string:
            match_group = re.search(r'\w+-\w+', string)
        else:
            match_group = re.search(r'[a-z,A-Z]+', string)
        if '.' in string:
            match_num = re.search(r'\d+\.\d+', string)
        else:
            match_num = re.search(r'\d+', string)
        return (match_num.group(), match_group.group())


# returns a list. Each list item contains values for each subjects number, group,
# timepoint for 50% indifference point, k value, average slope of real values,
# and average slope of the fitted curve.
# ceiling blocks any values greater than a choosen integer or float from being used in the analysis
# arbitrary determines if values greater than the ceiling will be set at ceiling or ignored from analysis
def idp_frame(df, crit=50, extra_ceiling = [60, 300], ec_names=['v50_ceil60', 'v50_ceil300'], arb = True):
    
    ind = pd.DataFrame(columns = ['group','k', 'STD_DEV_ERR_on_params','a','v50_ceilNONE'])
    
    if arb == True:
        for name in ec_names:
            ind[name] = ''
    
    idpls = []
    
    
    for column in df.columns:
        num, gr = group_id_split(column)
        idpls.append((num, gr, df[column]))
    for n, gr, sub in idpls:
        hyper_f = lambda d, k: sub[0] / (1 + (k * d))
        k, pcov = curve_fit(hyper_f, np.array(sub.index), np.array(sub))
        idp = (((sub[0] / crit) - 1) / k)
        perr = np.sqrt(np.diag(pcov))
        a = sub[0]
        
        if idp > 0:
            ind = ind.append(pd.Series(OrderedDict(group= str(gr),
                                                   k= float(k),
                                                   STD_DEV_ERR_on_params= float(perr),
                                                   a= float(a),
                                                   v50_ceilNONE= float(idp)), 
                                                   name=n)
                            )
        
            if arb == True:
                for ceil, name in zip(extra_ceiling, ec_names):
                    new_idp = 0
                    if idp > ceil:
                        new_idp = ceil
                        ind.loc[n:n,name:name] = new_idp
                    else:
                        ind.loc[n:n,name:name] = idp
                    
    return ind
            
# returns a dataframe with each groups mean, sem, and count of for
# a value of interest from another dataframe of individual subject data
def by_group(df,IV_interest, DV_interest):
    grouped = df.groupby(IV_interest, sort = False)
    mean  = grouped[DV_interest].mean()
    sem   = grouped[DV_interest].sem()
    count = grouped[DV_interest].count()
    frame = pd.concat([mean, sem, count], axis=1)
    frame.columns = ['mean', 'sem', 'count']
    return frame

def gb_groups(df):
    numgr = [(group_id_split(index)) for index in df.T.index]
    sers = pd.DataFrame({'group':[i[1] for i in numgr]}, index = df.T.index)
    aggr = pd.concat([sers, df.T], axis=1)
    aggr_gb = aggr.groupby('group', sort = False)
    g = aggr_gb.mean().T
    g_sem = aggr_gb.sem().T
    return g, g_sem