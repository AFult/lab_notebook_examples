import numpy as np
import matplotlib.pyplot as plt

# labels bars on graphs
def autolabel(rects, axes, counts, negative = False, ax=''):
    for rect, count in zip(rects, counts):
        
        height = float(rect.get_height())
        ymin, ymax = axes.get_ylim()
        fc = rect.get_facecolor()
        
        if negative == True:
            height = -height
            
        if float(height) / ymax < .2:
            loc_h = 2*height
            loc_c = loc_h * .85
            if float(height) / ymax < .1:
                loc_h = .1 * ymax
                loc_c = .07 * ymax
        else:
            loc_h = .55 * height
            loc_c = loc_h * .85
            
            
        if height < 10:
            text = '%.2f' % float(height)
        else:
            text = '%d' % int(height)    
        
        if fc == (0,0,0,1) and float(height) / ymax > .2:
            tc = 'w'
        else:
            tc = 'k'


        ax.text(rect.get_x() + rect.get_width()/2., loc_h,
                text,
                color = tc,
                ha = 'center', va = 'bottom')
        ax.text(rect.get_x() + rect.get_width()/2., loc_c,
                'n = %d' % int(count),
                color=tc,
                ha = 'center', va = 'bottom')

# builds each bar graph 
def bar(df, ylim = False, ylabel = 'seconds to indifference point', ax=''):

    hatch = ['','/','///','','','']
    color = ['w','w','w','k','.75','.4']
    
    x = np.arange(len(df))
    error_config = {'ecolor':'0.3'}
    bar_width = 0.35
    opacity = 0.4

    bars = ax.bar(x + .15, df['mean'], yerr = df['sem'],
                 error_kw = error_config)
    
    for bar, h, c in zip(bars,hatch,color):
        bar.set_hatch(h)
        bar.set_color(c)
        bar.set_edgecolor('k')

    ax.set_xticks(x + bar_width + .15)
    ax.set_xticklabels([g for g in df.index])
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_ylabel(ylabel, fontsize=15)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_xticklabels(df.index, rotation=45)
    ax.xaxis.set_ticks_position('none')
    if ylim is not False:
        ax.set_ylim(ylim)
        autolabel(bars, ax, df['count'], negative = True, ax=ax)
    else:
        autolabel(bars, ax, df['count'], ax=ax)
        
def histo(df_dict, interest, bins=20, normed=True, ax=''):
    
    hatch = ['','/','///','','','']
    color = ['w','w','w','k','.75','.4']
    
    for group, key in zip(df_dict.values(), df_dict.keys()):
        ax.hist(group[interest], normed=normed, alpha=.5, bins=bins, label=key)

    ax.legend()