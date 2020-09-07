import numpy as np
import struct
import itertools

def load_edf(file_name:str)->dict:
    """
    Load edf file and parse the data into header and binary raw data
    It returns data(numpy data) and head in dictionary
    All keys and values are string format axcept data
    
    Parameter
    ---------
    file_name : relative/absolute path of file
    """
    # load edf file and pare the data into header and data
    with open(file_name,'rb') as f:
        raw_data=f.read()
    header_end=raw_data.find(b'}\n')
    header_bin=raw_data[:header_end+1]
    data_bin=raw_data[header_end+2:]

    # header conversion
    rst=dict()

    header_str=header_bin.decode('utf-8').replace(" ","")
    for header_line in header_str.split()[1:-2]:
        try:
            key,val=header_line.split("=")
            rst[key]=val[:-1]
        except:
            print(f"Warning:Parsing fails for the line '{header_line}'")
        

    # data conversion
    while data_bin[0]==b' ' or data_bin[0]==b'\n':
        data_bin.pop(0)
    
    dim1=int(rst['Dim_1'])
    dim2=int(rst['Dim_2'])
    assert((len(data_bin)/dim1/dim2)==4)

    pix_mat=np.zeros((dim1,dim2))
    for (x,y) in itertools.product(range(dim1),range(dim2)):
        pix_mat[x,y]=max(0,struct.unpack('f',data_bin[4*(x+y*dim1):4*(x+y*dim1+1)])[0])

    rst['data']=pix_mat
    
    return rst

def edf_plotly(edf_dict:dict):
    '''
    simple edf data plotting using plotly graph
    '''
    import plotly.express as px
    
    fig=px.imshow(np.log10((edf_dict["data"]+1)))
    fig.show()

def edf_matplot(edf_dict:dict):
    '''
    simple edf data plotting using matplotlib graph
    '''
    import matplotlib.pyplot as plt
    
    plt.rcParams["figure.figsize"] = (int(edf_dict["Dim_2"])/20,int(edf_dict["Dim_1"])/20)
    plt.pcolor(np.log(np.add(edf_dict["data"],np.ones_like(edf_dict["data"]))))
    plt.show()
