#!/usr/bin/env python3
#v1 07/23/21
#v2 03/13/23 
#v3 05/31/24

import csv
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import time
from matplotlib import cm
import numpy as np

###################
####IMPORTANT######
'''it is necessary to use python 3.6 or earlier and pandas v.1.1 or earlier
so it is recomended to create an anaconda environment 
e.g., mamba create -n alandscapes -c bioconda python=3.6 pandas=1.1 biopython numpy matplotlib'''
###################
###################

#DIVSUM_SPLITER. searches for the 'Div' string and creates a new table (file.csv)

def divsum_splitter(file): 
    
    file_modif = file.split('.')[0]
    with open(file) as file, open( file_modif + '.csv', 'w') as modif:    
        orig_table = csv.reader(file)
        for row in orig_table:
            for index in row:
                if 'Div' in index:
                    file_csv = csv.writer(modif)
                    file_csv.writerow(row)
                    for row in orig_table:
                        csv.writer(modif)
                        file_csv.writerow(row)
    return file_modif + '.csv'



#CSV_PERCENTAGE_SORTER. Gets a csv file from divsum_splitter and generates as output a csv file with sorted (descending) sats by % of abundance, and the total % of sats in the library. 
def csv_percentage_sorter(file, bp_number):
       
    file = divsum_splitter(file)
    df = pd.read_csv(file, delim_whitespace=True)
    
    #If the df comes with another first column name rather than 'Div', it will be rename it to 'Div' as a divsum file index
    print('df index was renamed as "Div"')
    df = df.rename(columns = {df.columns[0]:'Div'})
   
    
    df = df.set_index('Div').div(bp_number).multiply(100)
    
    ## Adds a row of total abundance scores * 100 
    #df = df*100
    df = (df).append(df.sum(numeric_only = True), ignore_index = True)
    
    #Reset the index to Div
    df = df.reset_index()
    df = df.rename(columns = {'index': 'Div'}).set_index('Div')
    df = df.sort_values(by = df.last_valid_index(), axis = 1, ascending=False)
    
    ##print the total percentage of sats
    total_sats = df.loc[df.last_valid_index()].sum()
    print()
    print("The total ammount of sats represents {} % of the library {}\n".format(round(total_sats,2), file))
    
    #drops last row before exporting
    df = df.drop(labels = df.last_valid_index())
    return df

#NAMES_SORTER


#LANDSCAPES_SPECIES_PLOTTER. Takes a dataframe from landscapes_csv_generator and output a landscape plot for the species
def landscapes_species_plotter(df, lolim_sat, uplim_sat, plot_name):
        
    #df = df.set_index('Div')  #set 'Div' as index
    #df = df.loc[:, df.columns[:]]  #columns[inf_limit:up_limit] == number of sats to plot
    df = df.loc[:50, df.columns[lolim_sat:uplim_sat]]
    
    #plot by using % df from csv_percentage_sorter
    plot = df.plot.bar(stacked = True, figsize = (25,20), cmap = color_map, fontsize = 40, rot = 45)
    plot.legend(loc=[1.01,0.01],ncol=4)
    #move x labels to the top
    plot.xaxis.tick_top()
    plt.xticks(np.arange(0, 50, 5))
    plt.xticks(fontsize = 25)
    plt.yticks(fontsize = 25)
    plt.ylabel(ylabel= 'Abundance (%)', fontsize = 30)
    plt.xlabel(xlabel= 'Divergence (%)', fontsize = 30)
    
    plt.savefig(plot_name, bbox_inches='tight')
    

#LANDSCAPES_SATS_PLOTTER. Takes a dataframe from landscapes_cvs_generator and output a landscape subplot for each sat o selected sats
def landscapes_sats_plotter(df, lolim_sat, uplim_sat, plot_name):
    ##some validation
    if uplim_sat != None and lolim_sat != None:
        if lolim_sat > uplim_sat: #check the sat number input
            print()
            print('Please check sat numbers inputs. The input should be lower sat number/upper sat number')
            return
        lim_val = int(len(df.columns))
        if uplim_sat > lim_val:
            print()
            print('Please check the choosen upper sat number as it is higher than the elements in the dataframe')
            return
    
    #df = df.set_index('Div') #set Div as index
    df = df.loc[:, df.columns[lolim_sat:uplim_sat]] #choose the number of Sats [lowlim:uplim]  
        
    #set the sats_list used for the plot
    file_list = list(df.columns)

    #set heigh of the plot with sats numbers(columns) ~3 inches per graph
    h = 3*len(file_list)
    sat_num = len(file_list)
    #two sats per line + 1
    sat_rows = sat_num//2 + 1
    
    #if the sats input is between 200 and 400 the graph will be splitted into two!
    if sat_num > 200:
        df1 = df.loc[:, df.columns[:200]]
        df2 = df.loc[:, df.columns[201:]]
        print('Too many elements (>200)! The dataframe will be splitted into two (df1 and df2) and plotted in two different files')
        print()
        print('Plotting a total of {} sats (from {} to {})'.format(len(file_list), lolim_sat, uplim_sat))
        #print('This will take about {}~{} secs...'.format(len(sats_list)*0.85, len(sats_list)*0.95)) #about 0.85-0.95 sec per sat
        time0 = time.time()
        
        
        #Resize of the plot with sats numbers(columns) ~3 inches per graph
        h = 3*len(file_list)//2
        sat_num = len(file_list)//2
        #two sats per line + 1
        sat_rows = sat_num + 1
        
        print("Plotting df1...")
        df1.plot.bar(stacked = True, xlabel = 'Kimura %', ylabel = 'Abundance to bases', figsize = (20,h), fontsize = 8, rot = 0, width = 1.0, alpha = 0.8, subplots = True, xticks = range(0,70,5), layout = (sat_rows,2))
        plt.tight_layout()
        plt.savefig('df1_' + plot_name, bbox_inches='tight')
        print("Ok", "filename:", "df1_" + plot_name)
        print("Plotting df2...")
        df2.plot.bar(stacked = True, xlabel = 'Kimura %', ylabel = 'Abundance to bases', figsize = (20,h), fontsize = 8, rot = 0, width = 1.0, alpha = 0.8, subplots = True, xticks = range(0,70,5), cmap = color_map, layout = (sat_rows,2))
        plt.xticks(fontsize = 8)
        plt.yticks(fontsize = 8)
        plt.savefig('df2_' + plot_name, bbox_inches='tight')
        print("Ok", "filename:", "df2_" + plot_name)
        
        print(round(time.time()-time0, 2), 'secs')
        #quit
        return
    
    
    
    
    #If Sats number is below 200
    #some parameters: x,ylabel: x,y-axis names; figsize = (weight,height); rot = rotation angle of x axis labels; edgecolor = line color of columns; width = of columns; alpha = transparency for colors; subplots = divide plots for each column (sat); layout = (rows,columns) for output
    
    print()
    print('Plotting a total of {} sats (from {} to {})'.format(len(file_list), lolim_sat, uplim_sat))
    #print('This will take about {} secs...'.format(len(sats_list)*0.7)) #about 0.65-0.75 sec per sat
    time0 = time.time()
        
    plot = df.plot.bar(stacked = True, xlabel = 'Kimura %', ylabel = 'Abundance to bases', figsize = (20,h), fontsize = 8, rot = 0, width = 1.0, alpha = 0.8, subplots = True, xticks = range(0,70,5), cmap = color_map, layout = (sat_rows,2))

    plt.tight_layout()
    plt.savefig(plot_name, bbox_inches='tight')
    
    print("The plot includes {} elements. Thanks!".format(sat_num))
    print(round(time.time()-time0, 2), 'secs')


####LANDSCAPE_SATS_PLOTTER WITH LIST

def landscapes_list_plotter(df, list, plot_name):
    #set the sats_list used for the plot
    df_list = df[list]

    #df = df.set_index('Div') #set Div as index
    #df = df.loc[:, df.columns[list] #choose the list Sats

    #set heigh of the plot with sats numbers(columns) ~3 inches per graph
    h = 3*len(list)
    sat_num = len(list)
    #two sats per line + 1
    sat_rows = sat_num//2 + 1

    print()
    print('Plotting a total of {} sats'.format(len(list)))

    time0 = time.time()

    plot = df_list.plot.bar(stacked = True, xlabel = 'Kimura %', ylabel = 'Abundance to bases', figsize = (20,h), fontsize = 8, rot = 0, width = 1.0, alpha = 0.8, subplots = True, xticks = range(0,70,5), cmap = color_map, layout = (sat_rows,2))

    plt.tight_layout()
    plt.savefig(plot_name, bbox_inches='tight')

    print("The plot includes {} elements. Thanks!".format(sat_num))
    print(round(time.time()-time0, 2), 'secs')













#DFS_SORTER. Given two dfs (df1 and df2), check and sort df2 by df1.     
def dfs_sorter(df1, df2):
    #create a variable for missing elements if dfs are not equal in content
    missing_elements = df2.columns.difference(df1.columns).values #df2 elements that are not present in df1
    missing_elements2 = df1.columns.difference(df2.columns).values #df1 elements that are not present in df2
    
    # Check if the size of df1 = df2 
    if len(df1.columns) != len(df2.columns):
        print()
        print('Warning. The number of elements in both dataframes are different!')
        print()
        if len(df1.columns) < len(df2.columns):
            #get number of different elements
            elements = (len(df2.columns) - len(df1.columns))
            #get missing elements' name/s
            missing_elements = df2.columns.difference(df1.columns).values
            
            print('Warning. The df2 has {} more elements than df1, possible cause: low abundance elements that were not detected in df1.'.format(elements))
            print('Check the element/s {} in df1'.format(missing_elements))
            print()
            reply = input('This should not be a problem. This/these element/s will be automatically removed when sorting both dfs. Type **yes** to proceed or **no** to cancel and exit: ')
            if reply == 'yes':
                df2 = df2[df1.columns]
                print()
                print('\033[1m' + 'The df2 was sorted according to the df1 and the {} element/s {} removed...'.format(elements, missing_elements))
            else:
                return
    
        else: 
            #get missing elements' name/s
            missing_elements = df1.columns.difference(df2.columns).values
            elements = (len(df1.columns) - len(df2.columns))
            print('Warning. The df1 has {} more elements than df2, possible cause: low abundance elements not detected in df2.'.format(elements))
            print('Check the element/s {} in df2'.format(missing_elements))
            print()
            reply = input('This should not be a problem. This/these element/s will be automatically removed when sorting both dfs. Type **yes** to proceed or **no** to cancel and exit: ') 
            if reply == 'yes':
                df1 = df1[df2.columns]
                print()
                print('\033[1m' + 'The df1 was sorted according to the df2, and the {} element/s {} removed...'.format(elements, missing_elements))
            else:
                return
            
        
    elif len(missing_elements) != 0 or len(missing_elements2) != 0: #check and delete not sharing elements between both dfs
            
            print('Both dfs selections have different element contents. Element/s {} in df2 is/are not present in df1. Element/s {} in df1 is/are not present in df2. In order to continue it is necessary to eliminate them.'.format(missing_elements, missing_elements2))
            reply = input('Type **yes** to proceed or **no** to cancel and exit: ')  
            if reply == 'yes':
                print('\nRemember. Sorted dfs will include a lower number of elements!\n')
                for element in missing_elements:
                    df2 = df2.drop(labels = element, axis=1)
                for element in missing_elements2:
                    df1 = df1.drop(labels = element, axis=1)
                
                #and finaly sort!!!
                df1 = df1[df2.columns]
            else:
                return
    #Both dfs numbers are ok to sort!
    else:
        
        df1 = df1[df2.columns]
    
    return df1, df2

    
#ABUNDANCE_SUBTRACTER. Given two dataframes(dfs), this function will sort both dfs with the dfs_sorter function and returns the subtraction df1 - df2 abundance. Before sorting it checks if the size of df1 = df2. If they have different number of elements, the one with higher score can be arranged with the other that has less score. 

def abundance_subtracter(df1, df2, plot_name):
    df1, df2 = dfs_sorter(df1, df2)
    
    #subtraction
    dfsus = df1.subtract(df2)

    #making plot
    print()
    print('\033[0m' + 'plotting...\n')
    plot = dfsus.plot.bar(stacked = True, xlabel = '% Kimura', ylabel = '% Abundance', figsize = (25,20), cmap = color_map, fontsize = 8, rot = 45)
    plot.legend(loc=[1.01,0.01],ncol=4)
    #move x labels to the top
    plot.xaxis.tick_top()
    plot.axhline(c = 'gray', ls = '--')

    plt.savefig(plot_name, bbox_inches='tight')
    
    print('\nDone, thanks!\n')
    return dfsus
    

#ABUNDANCE_RATIO. Given two dfs (df1, df2), gets a sorted abundance ratio list per element between df1/df2.
def abundance_ratio(df1, df2, csv_name):
    # Adds a final row of total abundance scores per df
    df1 = df1.append(df1.sum(numeric_only = True), ignore_index = True)
    df2 = df2.append(df2.sum(numeric_only = True), ignore_index = True)
    
    #sorts df1 and df2 with the dfs_sorter function
    df1, df2 = dfs_sorter(df1, df2)
   
    # select last rows of both dfs that content the total abundance
    df1 = df1.iloc[-1]
    df2 = df2.iloc[-1]
    
    #get abundance ratio between df1/df2 and sort values in descending order
    ab_ratio = (df1/df2).sort_values(ascending = False)
    
    #exports a csv file
    ab_ratio.to_csv(csv_name)
    print('The abundance ratio between df1 and df2 was exported in {}'.format(csv_name))
    
#FINAL_KIMURA.Import a divsum file and return a kimura dataframe(df_k)    
def final_kimura(kimura_divsum):
    kimura_modif = kimura_divsum.split('.')[0] + '_final_kimura.csv'
    with open(kimura_divsum) as file:    
        df_k = pd.read_csv(file, delimiter = '\t', header = 4)
        return df_k


#FINAL_AB_KIMURA.Importes a dataframe_abundance (df_ab) from csv_percentage_sorter, transpose and sort df_k names by df_ab. returns a abundance_kimura dataframe and csv file with the input name (default = abundance_kimura.csv)

def final_ab_kimura(df_ab, df_k, ab_k_filename = 'abundance_kimura.csv'):
    #removes the second table by dropping NAs values, remove the Class column, and set Reapeat column as index.
    df_k = df_k.dropna().drop(labels = 'Repeat', axis = 1).set_index('Class')
    #Removes the remaining first column (with------ values)
    df_k = df_k.drop(df_k.index[0])
    #add abundance sum per element
    df_ab = df_ab.append(df_ab.sum(numeric_only = True), ignore_index = True)
    #pick last row  with total elelements and transpose
    df_ab = df_ab.iloc[-1].transpose()
    #set reset_index in df_ab
    df_ab = df_ab.reset_index().set_index('index')
    #rename the sum column
    df_ab.columns.values[-1] = 'Abundance%'
    #sort df_k by df_ab names
    df_k = df_k.reindex(df_ab.index)
    df_ab_k = df_ab.join(df_k['Kimura%'])
    #exports the final combined df
    df_ab_k.to_csv(ab_k_filename)
    print(df_ab_k)
    print()
    print('Table was exported as **', ab_k_filename, '** file')
    return df_ab_k

def sat_lister(file_list):
    with open(file_list) as file:
        list = file.read().split(',')
        list = [element.replace('\n','') for element in list]
        list = [element.strip(' ') for element in list] 
    return list



####MAIN FUNCTION####

if __name__ == "__main__":
    
    

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="\n========================\n   ANALYZE LANDSCAPES \n========================\nFor any bug/s, suggestions and comments, please contact me!\n ~~~Juan Martin Ferro, ferrojm@gmail.com~~~\n\nPlot landscapes from a RepeatMasker output file (divsum). \n1) Calculate and sort (descending) sats by % of abundance giving a csv file as output, and the total % of sats in the library. \n2) Plot a species sats landscape or individual landscapes for all (or selected) sats. \n3) Given two dataframes (df1 and df2), checks and sort df2 by df1, and get their subtracted abundance (df1 - df2). Before sorting, it checks size and content of both df1 and df2. If they have different number of elements, the one with higher score will be arranged with the one with less score (you will be asked before proceeding). \n4) Given two dataframes (df1, df2), it gets a sorted abundance ratio list per element between df1/df2. \n5) Takes two files as input (abundance_per_fam and kimura_per_fam), returns a sorted csv file\n========================\n Some examples \n========================\n##for plotting species landscape##\nAnalyzeLandscapes.py -i file.divsum -b bp_number -m lsp \n##for individual landscape sats##\nAnalyzeLandscapes.py -i file.divsum -b bp_number -m lstp\n##for individual landscape sats, setting sats range##\nAnalyzeLandscapes.py -i file.divsum -b bp_number -m lstp -l lower_sat_limit higher_sat_limit \n##for subtractive (two files)##\nAnalyzeLandscapes.py -i file1.divsum -b bp_number1 -i2 file2.divsum -b2 bp_number2 -m abs -csv ")
    
    #Arguments
    parser.add_argument("-i", "--input", type = str, required = True, help = "a divsum input file" )
    parser.add_argument("-m", "--mode", type = str, required = True, choices = ["dvs", "ps","lsp", "lstp", "dfs", "abs", "abr", "ak","lslp"], help = "dvs: divsum splitter. returns an abundance csv table by sat family; ps: percentage sorter. sort sats by their abundance percentage;\n lsp: landscape species plotter. plots a landscape for the species; lstp: landscape sats plotter. plot sats in individual landscapes (optional: range limits); dfs: dataframes sorter. sort a df2 by df1 in a .csv; abs: abundance subtracter. given two dfs (df1, df2), calculate and plot (df1 - df2) abundance; abr: abundance ratio. given two dfs (df1, df2), gets a sorted abundance ratio list.csv per element between df1/df2; ak: abundance & kimura. given one df (df_divsum) returns an abundance & Kimura df (file.csv) per element family; lslp: plot a sat list (comma separated list)")
    parser.add_argument("-b", "--bp_number", type = int, default = 0, help = "The number of base paires of the RMasker input fasta to get abundance percentages per element")
    parser.add_argument("-n", "--name", type = str, help ="The output plot name and format (e.g., plot.pdf, plot.png, plot.svg) [default .png]")
    parser.add_argument("-l", "--sat_lim", type = int, default = [None,None], nargs = 2, help = "for plotting with limited elements [-l lower higher]")      
    parser.add_argument("-i2", "--second_input", type = str, help = "a second divsum input file" )
    parser.add_argument("-b2", "--bp_number_second_input", type = int, default = 0, help = "The total pair base number of a second input")
    #parser.add_argument("-k", "--kimura_file", type = str, help = "divsum input file with Kimura-2-parameters per family" )
    parser.add_argument("-csv", "--to_csv", action = 'store_true', help = "if set, exports output dfs to csv file")
    parser.add_argument("-r", "--range_sats", type = int, default = 0, help ="A single number/range of elements only used for abudance subtracter")
    parser.add_argument("-list", "--sats_list", type = str, help ="give a list (comma separated list) of sats to plot (used only with mode -m lslp)")
    
    args = parser.parse_args()
    bp_number = args.bp_number
    plot_name = args.name
    file = args.input
    mode = args.mode
    lolim_sat, uplim_sat = args.sat_lim
    file2 = args.second_input
    bp_number2 = args.bp_number_second_input
    #kimura_fam_divsum = args.kimura_file
    csv_export = args.to_csv
    range_sats = args.range_sats
    file_list = args.sats_list
    
    color_map = plt.cm.get_cmap('nipy_spectral')
    #modes selector 
    #DVS
    if mode == "dvs": # divsum_splitter
        divsum_splitter(file)
    
    #PS
    elif mode == "ps": #percentage_sorter
        if bp_number == 0:
            print("For [ps] argument [-b, -bp_number] value is needed!")
        else:
            df = csv_percentage_sorter(file, bp_number)
            if csv_export:
                csv_name = file.split('.')[0] + '_sorted.csv'
                df.to_csv(csv_name)
                print('The df was stored with the name {}'.format(csv_name))
    #LSP
    elif mode == "lsp":
        df = csv_percentage_sorter(file, bp_number)
        #checks if file has extension or not
        if plot_name == None: #no name
            plot_name = file + '_sp_landscape.png'
            csv_name = file + '_sp_landscape.csv'
        elif len(plot_name.split('.')) == 1: #no extension
            plot_name = plot_name + '_sp_landscape.png'
            csv_name = plot_name + '_sp_landscape.csv'
        else:
            plot_name = plot_name.split('.')[0] + '_sp_landscape.' + plot_name.split('.')[1]
            csv_name = plot_name.split('.')[0] + '.csv'
        
       
        
        landscapes_species_plotter(df,lolim_sat, uplim_sat, plot_name)
        if csv_export:
            df.to_csv(csv_name)
            print('The df was stored with the name {}'.format(csv_name))
        print('The plot was named as {}'.format(plot_name))
        
    
    #LSTP
    elif mode == "lstp":
        df = csv_percentage_sorter(file, bp_number)
        #checks if file has extension or not
        if plot_name == None: #no name
            plot_name = file + '_sat_landscape.png'
            csv_name = file + '_sat_landscape.csv'
        elif len(plot_name.split('.')) == 1: #no extension
            plot_name = plot_name + '_sat_landscape.png' 
            csv_name = plot_name + '_sat_landscape.csv'
        else:
            plot_name = plot_name.split('.')[0] + '_sat_landscape.' + plot_name.split('.')[1]
            csv_name = plot_name.split('.')[0] + '.csv'
        
        
        
        landscapes_sats_plotter(df, lolim_sat, uplim_sat, plot_name)
        if csv_export:
            df.to_csv(csv_name)
            print('The df was stored with the name {}'.format(csv_name))
        print('The plot was named as {}'.format(plot_name))
    ###LSLP
    elif mode == "lslp":
        df_list = csv_percentage_sorter(file, bp_number)
        list = sat_lister(file_list)
        plot_name = file + '_sat_list.png'
        landscapes_list_plotter(df_list, list, plot_name)
        print('The plot was named as {}'.format(plot_name))

    #DFS    
    elif mode == "dfs":
        df1 = csv_percentage_sorter(file, bp_number)
        df2 = csv_percentage_sorter(file2, bp_number2)
        dfs_sorter(df1,df2)
    
    #ABS 
    elif mode == "abs":
        df1 = csv_percentage_sorter(file, bp_number)
        df2 = csv_percentage_sorter(file2, bp_number2)
        
        #if there is an input list of sats
        if file_list != None: #there is an input list
            list = sat_lister(file_list)
            df1 = df1[list]
            df2 = df2[list]  
           
        #checks if file has extension or not
        if plot_name == None: #no name
            plot_name = file + '_ab_sub_df1_df2.png'
            csv_name = file + '_ab_sub_df1_df2.csv'
        elif len(plot_name.split('.')) == 1: #no extension
            plot_name = plot_name + '_ab_sub_df1_df2.png'
            csv_name = plot_name + '.csv'
        else:
            plot_name = plot_name.split('.')[0] + '_ab_sub_df1_df2.' + plot_name.split('.')[1]
            csv_name = plot_name.split('.')[0] + '.csv'
        
        
        #choose number of sats to plot from the most abundant        
        if range_sats > 0:                                    
            df1 = df1.loc[:, df1.columns[0:range_sats]] #choose the number of Sats [lowlim:uplim]
            df2 = df2.loc[:, df2.columns[0:range_sats]] #choose the number of Sats [lowlim:uplim] 
            df1, df2 = dfs_sorter(df1,df2)
            
                
        dfsus = abundance_subtracter(df1, df2, plot_name)
        
        if csv_export:
            dfsus.to_csv(csv_name)
            print('The df was stored with the name {}'.format(csv_name))
        print('The plot was named as {}'.format(plot_name))
        
    #ABR        
    elif mode == "abr":
        df1 = csv_percentage_sorter(file, bp_number)
        df2 = csv_percentage_sorter(file2, bp_number2)
        ###se busca la interseccion de columnas df1 df2
        shared_columns = df1.columns.intersection(df2.columns)
        df1 = df1.loc[:,shared_columns]
        df2 = df2.loc[:,shared_columns]
        
        csv_name = args.name        
        abundance_ratio(df1, df2, csv_name = 'ab_ratio_df1_df2.csv')
        ###
    #AK
    elif mode == "ak":
        df_ab = csv_percentage_sorter(file, bp_number)
        df_k = final_kimura(file)
        ab_k_filename = args.name
        final_ab_kimura(df_ab, df_k, ab_k_filename = 'abundance_kimura.csv')
     
    
    
#functions(arguments)

##divsum_splitter(file)
##csv_percentage_sorter(file, bp_number)
##landscapes_species_plotter(df, plot_name)
##landscapes_sats_plotter(df, plot_name, lolim_sat=None, uplim_sat=None)..........Tupples>lolim_sat=None, uplim_sat=None
##dfs_sorter(df1, df2)
##abundance_subtracter(df1, df2, plot_name ='ab_sub_df1_df2.png')
##abundance_ratio(df1, df2, csv_name = 'ab_ratio_df1_df2.csv')
##final_kimura(kimura_fam_divsum)
##final_ab_kimura(df_ab, df_k, ab_k_filename = 'abundance_kimura.csv'):




