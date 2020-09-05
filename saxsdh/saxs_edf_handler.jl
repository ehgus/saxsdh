

using Plots

function load_edf(file_name::String)::Dict
    """
    Load edf file and parse the data into header and binary raw data
    It returns Array and head in dictionary
    All keys and values are string format axcept data
    
    Parameter
    ---------
    file_name : relative/absolute path of file
    """
    #laod edf files and parse the data into header and data
    rst=Dict()
    open(file_name,"r") do io
        #parse header
        @assert readline(io)=="{"
        while (content=readline(io))!="}"
            re_rst=match(r"\A(?<key>\w+)\s*=\s*(?<val>.+)\s*;\Z",content)
            if re_rst===nothing
                continue
            end
            rst[re_rst["key"]]=re_rst["val"]
        end
        #parse data
        dim1=parse(Int64,rst["Dim_1"])
        dim2=parse(Int64,rst["Dim_2"])

        pix_mat=zeros(Float32,dim1,dim2)
        for j=1:dim2
            for i=1:dim1
                pix_mat[i,j]=read(io,Float32)
            end
        end
        @assert eof(io)
        rst["data"]=pix_mat
    end
    return rst
end;

function edf_plot(edf_dict::Dict)
    plotly()
    heatmap(
        1:size(rst["data"],2),
        1:size(rst["data"],1),
        log.(2 .+rst["data"]),
        xlabel="x axis", ylabel="z axis",
        title=edf_dict["title"])
end;

#rst=load_edf("/home/ubundo/Desktop/saxsdh_julia/example_data/mapping_0_00001.edf")
#edf_plot(rst)
