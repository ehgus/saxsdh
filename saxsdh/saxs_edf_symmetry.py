from glob import glob
import os

import numpy as np
import plotly.graph_objects as go
from saxsdh import load_edf


def dev_edf(edf_dict:dict)->float:
    data=edf_dict["data"]
    
    #split data into four qudrant spaces
    qudrants=[
        data[:19,:19],
        data[:19,38:19:-1],
        data[38:19:-1,:19],
        data[38:19:-1,38:19:-1]
    ]
    qudrants_log=list(map(lambda nparray: np.log(np.add(nparray,np.ones((19,19)))),qudrants))
    # why log?: to suppress noise of incident beam
    #return deviation
    return np.sum(np.std(qudrants_log,axis=0))


## represent graph

def sym_graph(dir_path:str,file_re='*.edf',table_out=False):
    '''
    graphically shows the symmetricity of saxs data

    table_out: should be implemented later
    '''
    # find files
    edf_files = glob(os.path.join(dir_path,file_re))
    if len(edf_files)==0: 
        print("No file is detected. Check your input")
        return
    #calculate deviations and stack data
    x_cor=[]
    y_cor=[]
    devs=[]
    best_score_loc=0
    for i,file_name in enumerate(edf_files):
        rst=load_edf(file_name)
        dev=dev_edf(rst)
        x_cor.append(float(rst['x']))
        y_cor.append(float(rst['z']))
        devs.append(dev)

        if devs[best_score_loc]>dev:
            best_score_loc=i

    #plot the result
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_cor,
        y=y_cor,
        text=devs,
        mode='markers',
        marker=dict(
            color=devs,
            size=20,
            showscale=True,
    )))
    fig.update_layout(
        annotations=[
            dict(
                x=x_cor[best_score_loc],
                y=y_cor[best_score_loc],
                text=edf_files[best_score_loc],
                showarrow=True
            )
        ]
    )
    fig.update_xaxes(title_text='x axis')
    fig.update_yaxes(title_text='z axis')
    fig.show()


## predict middle point(using machine learning)

def middle_saxs():
    '''
    predict the middel point(using machine learning later)
    '''
    print("This is not implemented now. Do not use this callable")
    pass