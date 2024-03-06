import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

for file_res in os.listdir("results"):

    if ".csv" not in file_res:
        continue

    file_res_open = pd.read_csv("results/" + file_res, sep = ";", index_col = False)

    row_names = list(file_res_open["var"])

    print(row_names)
    print(file_res_open.columns)

    dict_vals = dict()

    use_cols = []

    for ix in range(len(row_names)):
        dict_vals[row_names[ix]] = dict()
        for colname in list(file_res_open.columns):
            if colname == "var":
                continue
            if colname not in use_cols:
                use_cols.append(colname)
            dict_vals[row_names[ix]][colname] = float(str(file_res_open[colname][ix]).replace(",", "."))

    print(dict_vals)
 
    numrows = 0
    for ix_row in range(len(dict_vals.keys())):
        rowname = list(dict_vals.keys())[ix_row]  
        if "size" in rowname or "ratio" in rowname:
            numrows += 1

    plt.figure(figsize = (10, 5), dpi = 80)
    plt.rcParams.update({'font.size': 22}) 
    for ix_row in range(len(dict_vals.keys())):
        rowname = list(dict_vals.keys())[ix_row] 
        if "size" in rowname or "ratio" in rowname:
            x_vals = [i * (numrows + 1) + ix_row - int(numrows // 2) for i in range(len(list(dict_vals[rowname].values())))] 
            plt.bar(x_vals, list(dict_vals[rowname].values()), label = rowname, zorder = 2)
            for i in range(len(x_vals)):
                if i == 0:
                    yoff = 0.2 * max(list(dict_vals[rowname].values()))
                else:
                    yoff = 35
                if list(dict_vals[rowname].values())[i] < 0:
                    yoff = 0.7 * max(list(dict_vals[rowname].values()))
                add_str = " " + rowname.split("(")[-1].replace(")", "")
                if "%" in add_str:
                    add_str = "%"
                plt.text(x_vals[i] - 1.65, list(dict_vals[rowname].values())[i] + yoff, str(list(dict_vals[rowname].values())[i]) + add_str)
    
    plt.xticks([i * (numrows + 1) for i in range(len(list(dict_vals[rowname].values())))], use_cols)

    title = "Size comparison with ratio\n"

    if "larger" in file_res:
        title += "Larger buffer"
    if "smaller" in file_res:
        title += "Smaller buffer"
    if "with_" not in file_res:
        title += "No BWT"
        
    plt.title(title)
    plt.xlim(-2.7, 10)
    plt.ylim(-350, 1000)
    plt.xlabel("Image size")
    plt.grid(axis = 'y')  
    plt.legend(ncol = 1, loc = "upper left")
    plt.savefig("results/" + file_res.replace(".csv", "_") + "size_comparison.png", bbox_inches = "tight")
    plt.close()
    
    for ix_row in range(len(dict_vals.keys())):
        rowname = list(dict_vals.keys())[ix_row] 
        if "time" in rowname:
            plt.figure(figsize = (10, 5), dpi = 80)
            plt.rcParams.update({'font.size': 22}) 
            x_vals = [i for i in range(len(list(dict_vals[rowname].values())))] 
            plt.bar(x_vals, list(dict_vals[rowname].values()), label = rowname, zorder = 2)
            for i in range(len(x_vals)):
                yoff = 0.02 * max(list(dict_vals[rowname].values()))
                add_str = " " + rowname.split("(")[-1].replace(")", "")
                plt.text(x_vals[i] - 0.3, list(dict_vals[rowname].values())[i] + yoff, str(list(dict_vals[rowname].values())[i]) + add_str)
    
            plt.xticks([i for i in range(len(list(dict_vals[rowname].values())))], use_cols)

            title = rowname.capitalize() + "\n"

            if "larger" in file_res:
                title += "Larger buffer"
            if "smaller" in file_res:
                title += "Smaller buffer"
            if "with_" not in file_res:
                title += "No BWT"
                
            plt.title(title)
            plt.ylim(0, max(list(dict_vals[rowname].values())) * 1.1)
            plt.xlabel("Image size")
            plt.grid(axis = 'y')   
            plt.savefig("results/" + file_res.replace(".csv", "_") + rowname + ".png", bbox_inches = "tight")
            plt.close()

    cs_vals = dict()

    for s in dict_vals["compression time (ms)"]:
        cs_vals[s] = np.round(dict_vals["size before (kB)"][s] / dict_vals["compression time (ms)"][s] * 1000, 2)
        print(s, cs_vals[s])

    plt.figure(figsize = (10, 5), dpi = 80)
    plt.rcParams.update({'font.size': 22}) 
    x_vals = [i for i in range(len(list(cs_vals.values())))] 
    plt.bar(x_vals, list(cs_vals.values()), label = rowname, zorder = 2)
    for i in range(len(x_vals)):
        yoff = 0.02 * max(list(cs_vals.values()))
        add_str = " kB/s"
        plt.text(x_vals[i] - 0.3, list(cs_vals.values())[i] + yoff, str(list(cs_vals.values())[i]) + add_str)

    plt.xticks([i for i in range(len(cs_vals.values()))], use_cols)

    title = "Compression speed (kB/s)\n"

    if "larger" in file_res:
        title += "Larger buffer"
    if "smaller" in file_res:
        title += "Smaller buffer"
    if "with_" not in file_res:
        title += "No BWT"
        
    plt.title(title)
    plt.ylim(0, max(list(cs_vals.values())) * 1.1)
    plt.xlabel("Image size")
    plt.grid(axis = 'y')   
    plt.savefig("results/" + file_res.replace(".csv", "_") + "cs_vals.png", bbox_inches = "tight")
    plt.close()

    ds_vals = dict()

    for s in dict_vals["decompression time (ms)"]:
        ds_vals[s] = np.round(dict_vals["size after (kB)"][s] / dict_vals["decompression time (ms)"][s] * 1000, 2)
        print(s, ds_vals[s])

    plt.figure(figsize = (10, 5), dpi = 80)
    plt.rcParams.update({'font.size': 22}) 
    x_vals = [i for i in range(len(list(ds_vals.values())))] 
    plt.bar(x_vals, list(ds_vals.values()), label = rowname, zorder = 2)
    for i in range(len(x_vals)):
        yoff = 0.02 * max(list(ds_vals.values()))
        add_str = " kB/s"
        plt.text(x_vals[i] - 0.3, list(ds_vals.values())[i] + yoff, str(list(ds_vals.values())[i]) + add_str)

    plt.xticks([i for i in range(len(ds_vals.values()))], use_cols)

    title = "Decompression speed (kB/s)\n"

    if "larger" in file_res:
        title += "Larger buffer"
    if "smaller" in file_res:
        title += "Smaller buffer"
    if "with_" not in file_res:
        title += "No BWT"
        
    plt.title(title)
    plt.ylim(0, max(list(ds_vals.values())) * 1.1)
    plt.xlabel("Image size")
    plt.grid(axis = 'y')   
    plt.savefig("results/" + file_res.replace(".csv", "_") + "ds_vals.png", bbox_inches = "tight")
    plt.close()