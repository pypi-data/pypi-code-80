import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import string, math
import warnings
from itertools import product

# custom errors 
class Error(Exception):
    pass
class PlateMapError(Error):
    pass
class HeaderError(PlateMapError):
    pass

# headers
header_names = {'Well ID': {'dtype':str, 'long':True, 'short_row': False, 'short_col':False},
                'Row': {'dtype':str, 'long':False, 'short_row': True, 'short_col':True},
                'Start': {'dtype':str, 'long':False, 'short_row': True, 'short_col':True},
                'End': {'dtype':str, 'long':False, 'short_row': True, 'short_col':True},
                'Type': {'dtype':str, 'long':True, 'short_row': True, 'short_col':True},
                'Contents': {'dtype':str, 'long':True, 'short_row': True, 'short_col':True},
                'Compound': {'dtype':str, 'long':True, 'short_row': True, 'short_col':True},
                'Protein': {'dtype':str, 'long':True, 'short_row': True, 'short_col':True},
                'Concentration': {'dtype':float, 'long':True, 'short_row': True, 'short_col':True},
                'Concentration Units':{'dtype':str, 'long':True, 'short_row': True, 'short_col':True},
                 'Valid':{'dtype':bool, 'long':True, 'short_row': False, 'short_col':False}
               }

# we need to reference well plate dimensions  
wells = {6:(2, 3), 12:(3, 4), 24:(4, 6), 48:(6, 8), 96:(8, 12), 384:(16, 24)} # dictionary of well sizes  


def empty_map(size=96, valid=True, header_type='long'):
    """Generates an empty platemap of defined size that is used as the template when generating the filled plate maps from csv file. 
    
    :param size: Size of well plate, default = 96 
    :type size: int
    :param valid: Validates every well - 'True' sets every well as valid, 'False' wells will not be used for analysis, default = True
    :type valid: bool
    :param header_type: Type of headers used to create the df (e.g. 'long', 'short_row'), must be the same as in header_names dictionary, defaults to 'long'
    :type header_type: str
    :return: Pandas Dataframe of an empty plate map
    :rtype: pandas df
    """
    headers = [x for x in header_names.keys() if header_names[x][header_type]]   # create list of headers
    
    row_letters = list(string.ascii_uppercase)[0: wells[size][0]]   # create a list of row letters for a given size
    col_numbers = list(np.arange(1, wells[size][1] + 1).astype(str))   # create a list of column numbers for a given size
    well_ids = ['%s%s' % (item[0], item[1]) for item in product(row_letters, col_numbers)]   # create a list of well ids from row letters and column numbers
    
    empty_df = pd.DataFrame(index=well_ids, columns=headers)   # create the platemap data frame
    empty_df['Valid'] = valid   # set 'Valid' as True to every well
    
    if 'Type' in empty_df.columns:   # set the deafult value of 'Type' column as 'empty'
        empty_df['Type'] = 'empty'
    
    # empty_df.drop(labels='Well ID', axis=1, inplace=True)   # remove the redundant 'Well ID' column created from the header_names dict
    return empty_df

# PLATE DF GENERATION FROM LONG HAND MAP
def plate_map(file, size=96, valid=True):
    """Returns a dataframe from a 'long' plate map csv file that defines each and every well from a well plate of defined size
    
    Each defined well in the csv file corresponds to a row of the dataframe. The index is set to the Well ID's of the well plate, e.g. "A1". Dataframe contains headers such as 'Well ID', 'Compound', 'Protein', 'Concentration', 'Concentration Units', 'Contents', 'Type' and 'Valid'. The csv file contains headers on line 2 and a well ID in the first column for every well in the plate.
    An example csv template can be found here: 'long map example.csv'
    
    :param size: Size of well plate - 6, 12, 24, 48, 96 or 384, default = 96 
    :type size: int
    :param valid: Validates every well - 'True' sets every well as valid, 'False' wells will not be used for analysis, default = True
    :type valid: bool
    :return: Pandas Dataframe of a defined plate map
    """
    try:   # substitute values w/ new plate map
        data_types = {i[0]: i[1]['dtype'] for i in header_names.items()}   # dictionary with data types
        
        df = pd.read_csv(file, skiprows = 1, dtype = data_types, skipinitialspace = True)   # create the platemap df from csv file
        headers = [x for x in header_names.keys() if header_names[x]['long']]   # list of pre-defined headers from header_names dict
        
        if set(list(df.columns)) != set(headers):   # if headers in imported platemap are different than pre-defined headers, raise error
            raise HeaderError("Wrong headers!")

        df = df.set_index(df['Well ID'])   # set index to Well ID

        # check there are no repeats
        if len(df.index.unique()) != len(df.index):
            raise PlateMapError("Check your plate map!")

        # correct typos due to capitalisation and trailing spaces
        if 'Type' in df.columns:    
            df['Type'] = df['Type'].str.lower()
        
        # correct typos due to trailing spaces
        str_cols = [x for x in header_names.keys() if header_names[x]['dtype'] == str]
        df[str_cols] = df[str_cols].stack(dropna=False).str.rstrip().unstack()

        temp = empty_map(size=size, valid=valid, header_type='long')   # define an empty plate map
        temp.update(df)   # insert imported plate map into the empty plate map

        return temp
    
    except HeaderError: 
        print("Headers in csv file are incorrect.\nUse: {}".format(headers))
    except PlateMapError:
        print("Check your plate map! Incorrect number of wells.")

# PLATE DF GENERATION FROM SHORT HAND MAP
def short_map(file, size=96, valid=True):
    """Returns a dataframe from a 'short' plate map csv file that defines each and every well from a well plate of defined size
    
    Contains the columns 'Well ID', 'Compound', 'Protein', 'Concentration', 'Concentration Units', 'Contents', 'Type' and 'Valid'. Each defined well in the csv file corresponds to a row of the dataframe. The index is set to the Well ID's of the well plate, e.g. "A1". 
    
    :param size: Size of well plate - 6, 12, 24, 48, 96 or 384, default = 96 
    :type size: int
    :param valid: Validates every well - 'True' sets every well as valid, 'False' wells will not be used for analysis, default = True
    :type valid: bool
    :return: Pandas Dataframe of a defined plate map
    """
    try:
        # read in short map 
        df = pd.read_csv(file, skiprows = 1, skipinitialspace = True)   
        headers = [x for x in header_names.keys() if header_names[x]['short_row']]   # list of suitable headers taken from the header_names dictionary
        
        if set(list(df.columns)) != set(headers):   # if headers in imported platemap are different than pre-defined headers, raise error
            raise HeaderError("Wrong headers!")
            
        # generate empty dataframe to append with each duplicated row
        filleddf = pd.DataFrame()

        # iterate down rows of short map to create duplicates that correspond to every 'filled' well plate
        for i in range(len(df.index)):
            row = df.iloc[i]
            # generate temporary dataframe for each row
            temp = pd.DataFrame()
            # duplicate rows according to difference in start and end and add to temp dataframe
            temp = temp.append([row]*(row['End']-row['Start'] +1), ignore_index = True)
            # update column coordinates using index of appended dataframe
            temp['Column']= (temp['Start'])+temp.index
            # concatenate column and row coordinates to form empty well ID
            temp['ID']= temp['Row'] + temp['Column'].astype('str')
            # set index to well ID
            temp.set_index('ID', inplace = True)
            # add generated rows to new dataframe
            filleddf = filleddf.append(temp)

            # check there are no repeats
            if len(filleddf.index.unique()) != len(filleddf.index):
                raise PlateMapError("Check your plate map! Incorrect number of wells.")

        # insert filled df into empty plate map to include empty rows 
        finalmap = empty_map(size=size, valid=valid, header_type='short_row')
        finalmap.update(filleddf)
        # # update data types to prevent future problems
        # finalmap['Column'] = finalmap['Column'].astype(int)
        # correct typos due to capitalisation and trailing spaces
        finalmap['Type'] = finalmap['Type'].str.lower()
        str_cols = [x for x in header_names.keys() if (header_names[x]['dtype'] == str) and 
                    (header_names[x]['short_row'])]
        finalmap[str_cols] = finalmap[str_cols].stack(dropna=False).str.rstrip().unstack()
        return finalmap
    
    except HeaderError:
        print("Headers in csv file are incorrect.\nUse: {}".format(headers))
    except PlateMapError:
        print("Check your plate map! Incorrect number of wells.")
        
# The next 3 functions are used to simplify 'visualise' function that follows: 

# hatches are defined to clearly show invalidated wells
hatchdict = {"True":("", 'black'), "False":("//////", 'red')}

# fontsize will scale font size of visualisaiton to the well plate size (avoids overlapping text)
def fontsize(sizeby, plate_size, **kwargs): 
    """Returns a font size defined by the length of the string and size of the well plate
    
    Larger well plate and/or longer string = smaller font size.
    
    :param sizeby: String that requires a corresponding font size
    :type sizeby: String or list of strings
    :param plate_size: Scalable integer, the size of the well plate
    :var plate_size: Larger value corresponds with smaller fontsize, size of well plate is used in the following instances of the function
    :type plate_size: int
    :param **kwargs: The str_len (int) is accepted as a keyword argument, it is the length of the string to be displayed on the platemap, used only if the formatting is scientific notation or percentage.
    :return: float corresponding to a scaled font size 
    :rtype: float
    """
    if 'str_len' in kwargs and kwargs['str_len'] != None:    # if value is to be displayed in scientific notation or percentage, use str_len to determine its fontsize instead of determinig its legth
        return (8 - math.log10(kwargs['str_len'])*2 - math.log10(plate_size)*1.5) 
    else:     # previous functionality
        return (8 - math.log10(len(str(sizeby)))*2 - math.log10(plate_size)*1.5)

# adds labels according to label stipulations (avoids excessive if statements in the visualise function)
def labelwell(platemap, labelby, iterrange, **kwargs):
    """Returns label for each row of a stipulated column.
    
    Used to return the appropriate, formatted label from a specified platemap at every well. Empty wells will always return 'empty', wells without a label will return a blank string.  
    
    :param platemap: Platemap that contains the required labels
    :type platemap: pandas dataframe
    :param labelby: Dataframe column to label by, for example 'Compound', 'Protein', 'Concentration', 'Concentration Units', 'Contents' or 'Type'
    :type labelby: str
    :param iterrange: Number of instances to itterate over, typically the size of the platemap
    :type iterrange: int
    :param **kwargs: The str_format (str) is accepted as a keyword argument, it determines whether the value is to be displayed in scientific notation or percentage 1 d.p.
    :return: string corresponding to the value located in column labelby and row iterrange of the platemap
    :rtype: str
    """
    if 'str_format' in kwargs and kwargs['str_format'] == 'scinot':   # if scinot parameter is true, format the value in scientific notation 
        return "%.2E" % (platemap[labelby].iloc[iterrange])
    elif 'str_format' in kwargs and kwargs['str_format'] == 'percent':
        return "%.1f" % (platemap[labelby].iloc[iterrange])
    else:   # get the value from 'labelby' column and 'iterrange' row
        return str(platemap[labelby].iloc[iterrange]).replace(" ", "\n")

    
def get_colour_dict(platemap, colorby, cmap, **kwargs):
    """Returns a dictionary of colours for all values that are to be plotted on the platemap.
    
    Wellcolour generates an array of either uniformely spaced values between 0 and 1 for categorical data (e.g. 'Type', 'Protein Name') or 
    an array of values normalised to the range 0 to 1 for non-categorical data (e.g. intensity, anisotropy, etc.). For each value in the array,
    a cololur is chosen from the colour map. Colour maps with a continuous range of colours are recommended for non-categorical data.

    :param platemap: Platemap that contains the required labels
    :type platemap: pandas df
    :param colorby: Data frame column to colour code, for example 'Compound', 'Protein', 'Concentration', 'Concentration Units', 'Contents' or 'Type'
    :type colorby: str
    :param cmap: Colour map that generates a customisable list of colours
    :type cmap: str
    :param **kwargs: The following keyword arguments are accepted: categorical (bool) - if False, the values from colorby column are normalised to
    the range 0 to 1, otherwise a uniformely spaced array represning the values is created, blank_yellow (bool) - if True, the 'blank' values
    are excluded from the array so that colors are not assigned for values in blank wells, and scale (str) - determines whether the non-categorical data is scaled linearly or logarithmically
    :return: Dictionary of string labels and their corresponding colours
    :rtype: dict
    """
    cmap = plt.get_cmap(cmap)   # get the colourmap object
    if 'categorical' in kwargs and kwargs['categorical'] == False:   # non-categorical data
        
        if 'blank_yellow' in kwargs and kwargs['blank_yellow'] == True:   # blank wells are coloured yellow
            vals = platemap[platemap['Type'] != 'blank'][colorby].dropna().to_numpy()   # create numpy array of the 'colorby' values except of blanks
        else:   # include blanks in the vals array so that colours are also generated for them
            vals = platemap[colorby].dropna().to_numpy()
        
        types = vals.astype(str)   # convert the data values to strings that will be keys of colourdict
        if 'scale' in kwargs and kwargs['scale'] == 'log':   
            if np.any(vals<=0):   # return warning if the scaling is logarithmic but data contains non-positive values
                warnings.warn('The logarithmic scale could not be used becasue the data contains values less than or equal to 0. The default linear scale was used instead.', RuntimeWarning)
            else:
                vals = np.log10(vals)   # take log10 of the values for logarythmic scaling

        norm = (vals - np.min(vals)) / (np.max(vals) - np.min(vals))   # normalise the data values to the range 0 to 1
        colors = cmap(norm)    # for each normalised data value get a numerical value repesenting the colour
        
    else:   # functionality for categorical data
        types = [str(i) for i in list(platemap[colorby].unique())]   # unique strings in the defined column are used as the list of labels, converted to strings to avoid errors
        colors = cmap(np.linspace(0, 1, len(types)))   # get equally spaced colour values
    
    colordict = dict(zip(types, colors))  
    return colordict
    

def wellcolour(colordict, platemap, colorby, iterrange, **kwargs):
    """Returns a unique colour for each label or defined condition.

    :param colordict: Dictionary of string labels and their corresponding colours
    :type colordict: dict
    :param platemap: Platemap that contains the required labels
    :type platemap: pandas df
    :param colorby: Data frame column to colour code, for example 'Compound', 'Protein', 'Concentration', 'Concentration Units', 'Contents' or 'Type'
    :type colorby: str
    :param iterrange: Number of instances to itterate over, typically the size of the platemap
    :type iterrange: int
    :param **kwargs: The function accepts the following keyword arguments: 'blank_yellow' (bool) which sets the well colour to yellow if the 'Type' is blank and 'to_plot' (str or list of str)
    :return: RGB array of a colour that corresponds to a unique label
    :rtype: numpy array
    """
    color = colordict.get(str(platemap[colorby].iloc[iterrange]))   # get a colour from the dictionary
    colordict['nan'] = 'yellow'

    if 'to_plot' in kwargs:   
        color = colordict.get(str(platemap[colorby].loc[to_plot[iterrange]]))
    if 'blank_yellow' in kwargs and kwargs['blank_yellow'] == True and platemap['Type'].iloc[iterrange] == 'blank':
        color = 'yellow'   # define colour as yellow, if colourdict contains colurs for blank wells, it will be overwritten
    
    return color

def visualise(platemap, title="", size=96, export=False, cmap='Paired', colorby='Type', labelby='Type', dpi=150, **kwargs):
    """Returns a visual representation of the plate map.
    
    The label and colour for each well can be customised to be a variable, for example 'Compound', 'Protein', 'Concentration', 'Concentration Units', 'Contents' or 'Type'. The size of the plate map used to generate the figure can be either 6, 12, 24, 48, 96 or 384. 
    
    :param platemap: Plate map to plot
    :type platemap: pandas dataframe
    :param size: Size of platemap, 6, 12, 24, 48, 96 or 384, default = 96
    :type size: int    
    :param export: If 'True' a .png file of the figure is saved, default = False
    :type export: bool
    :param title: Sets the title of the figure, optional
    :type title: str
    :param cmap: Sets the colormap for the color-coding, default = 'Paired'
    :type cmap: str
    :param colorby: Chooses the parameter to color code by, for example 'Type', 'Contents', 'Concentration', 'Compound', 'Protein', 'Concentration Units', default = 'Type'
    :type colorby: str
    :param labelby: Chooses the parameter to label code by, for example 'Type', 'Contents', 'Concentration', 'Compound', 'Protein', 'Concentration Units', default = 'Type'
    :type labelby: str
    :param dpi: Size of the figure, default = 150
    :type dpi: int 
    :param **kwargs: Keyword arguments passed to the 'wellcolour' and 'get_colour_dict' functions: str_len, str_format, categorical, blank_yellow and scale
    :return: Visual representation of the plate map.
    :rtype: figure
    """
    try:
        fig = plt.figure(dpi = dpi)
        # define well plate grid according to size of well plate 
        # an extra row and column is added to the grid to house axes labels
        grid = gridspec.GridSpec((wells[size])[0]+1, (wells[size])[1]+1, wspace=0.1, hspace=0.1, figure=fig)

        # plot row labels in extra row
        for i in range(1, (wells[size])[0]+1):
            ax = plt.subplot(grid[i, 0])
            ax.axis('off')
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.text(0.5, 0.5, list(string.ascii_uppercase)[i-1], size=8, ha="center", va="center")

        # plot column labels in extra column
        for i in range(1, (wells[size])[1]+1):
            ax = plt.subplot(grid[0, i])
            ax.axis('off')
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.text(0.5, 0.5, list(range(1, (wells[size])[1]+1))[i-1], size=8, ha="center", va="center")
        
        indexes = list(platemap.index)  # list of well ids
        # create a list of tuples, each one containing a row number corresponding to a specified row letter  and col number for all well ids so that there is no need to iterate over the 'Row' and 'Column' columns which are absent in flu_ani platemaps
        coords = [(ord(item[0].lower()) - 96, int(item[1:])) for item in indexes]
        colordict = get_colour_dict(platemap, colorby, cmap, **kwargs)   # get the dictionary with colours

        # plot plate types in grid, color code and label
        for i, coord in enumerate(coords):   # iterate over each tuple (effectively well id) in coords 
            ax = plt.subplot(grid[coord[0], coord[1]])
            ax.axis('off')
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            
            # Well colour coding  
            if platemap['Type'].iloc[i] == 'empty':
                ax.add_artist(plt.Circle((0.5, 0.5), 0.49, edgecolor='black', fill=False, lw=0.5))
                # LABELS #
                # add 'empty' label
                ax.text(0.5, 0.5, 'empty', size=str(fontsize(sizeby='empty', plate_size=size, **kwargs)), wrap=True, ha="center", va="center")

            else:
                ax.add_artist(plt.Circle((0.5, 0.5), 0.49, facecolor=wellcolour(colordict, platemap, colorby, i, **kwargs), edgecolor=hatchdict[str(platemap['Valid'].iloc[i])][1], lw=0.5, hatch = hatchdict[str(platemap['Valid'].iloc[i])][0]))

                # LABELS 
                # nan option allows a blank label if there is nothing stipulated for this label condition
                if str(platemap[labelby].iloc[i]) != 'nan':
                    ax.text(0.5, 0.5, labelwell(platemap, labelby, i, **kwargs), size=str(fontsize(sizeby=platemap[labelby].iloc[i], plate_size=size, **kwargs)), wrap=True, ha="center", va="center")
                    
        plt.suptitle(f"{title}")   # add the figure title

        if export == True:   # option to save the figure as .png file at matplotlib's default file path
            plt.savefig(f"{title}_map.png")
    
    except:
        print('error!')

def visualise_all_series(x, y, platemap, share_y, size = 96, title = " ", export = False, cmap = 'Dark2_r',
             colorby = 'Type', labelby = 'Type', dpi = 200):
    """Returns a plot for each series, the location on the grid corresponding to the location of each assay on the well plate.
    :param x: Data to be plotted on x axis, length of data must equal length of the platemap
    :type x: List of floats or dataframe column
    :param y: Data to be plotted on y axis, length of data must equal length of the platemap
    :type y: List of floats or dataframe column
    :param platemap: Plate map to plot
    :type platemap: pandas dataframe
    :param share_y: 'True' sets y axis the same for all plots
    :type share_y: bool
    :param size: Size of platemap, 6, 12, 24, 48, 96 or 384, default = 96
    :type size: int    
    :param export: If 'True' a .png file of the figure is saved, default = False
    :type export: bool
    :param title: Sets the title of the figure, optional
    :type title: str
    :param cmap: Sets the colormap for the color-coding, default = 'Dark2_r'
    :type cmap: str
    :param colorby: Chooses the parameter to color code by, for example 'Type', 'Contents', 'Concentration', 'Compound', 'Protein', 'Concentration Units', default = 'Type'
    :type colorby: str
    :param labelby: Chooses the parameter to label code by, for example 'Type', 'Contents', 'Concentration', 'Compound', 'Protein', 'Concentration Units', default = 'Type'
    :type labelby: str
    :param dpi: Size of the figure, default = 200
    :type dpi: int
    :return: Figure of plotted data for each well of the well plate described in the plate map and the x and y series.
    :rtype: figure
    """
    
    fig = plt.figure(dpi = dpi)
    # define well plate grid according to size of well plate 
    # an extra row and column is added to the grid to house axes labels
    grid = gridspec.GridSpec((wells[size])[0]+1, (wells[size])[1]+1, wspace=0.1, hspace=0.1, figure = fig)
    colordict = get_colour_dict(platemap, colorby, cmap)   # get the dictionary with colours

    # calculate y min and y max for share y axis
    ymin = y.min().min()
    ymax = y.max().max() + 0.2*y.max().max()
    # plot row labels in extra row
    for i in range(1, (wells[size])[0]+1):
        ax = plt.subplot(grid[i, 0])
        ax.axis('off')
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.text(0.5, 0.5, list(string.ascii_uppercase)[i-1], size = 10, ha = "center", va="center")
        
    # plot column labels in extra column
    for i in range(1, (wells[size])[1]+1):
        ax = plt.subplot(grid[0, i])
        ax.axis('off')
        ax.text(0.5, 0.5, list(range(1, (wells[size])[1]+1))[i-1], size = 8, ha = "center", va="center")
    
    indexes = list(platemap.index)  # list of well ids
    # create a list of tuples, each one containing a row number corresponding to a specified row letter  and col number for all well ids so that there is no need to iterate over the 'Row' and 'Column' columns which are absent in flu_ani platemaps
    coords = [(ord(item[0].lower()) - 96, int(item[1:])) for item in indexes]

    # plot plate types in grid, color code and label
    for i, coord in enumerate(coords):   # iterate over each tuple (effectively well id) in coords 
        # color code
        ax = plt.subplot(grid[coord[0], coord[1]])
        ax.axis('off')
        # set axes
        if share_y == True:
            plt.ylim([ymin, ymax])
        
        ax.plot(x.iloc[i], y.iloc[i], lw=0.5, color=wellcolour(colordict, platemap, colorby, i), label=labelwell(platemap, labelby, i))
        
        if platemap['Valid'].iloc[i] == False:
            ax.plot([x.iloc[i, 0], x.iloc[i, -1]], [y.iloc[i, 0]-(y.iloc[i, 0]*0.2), y.iloc[i, -1]+(y.iloc[i, -1]*0.05)], color='red')
        
                
        # add label for each well
        legend = ax.legend(fontsize = str(fontsize(sizeby = platemap[labelby].iloc[i], plate_size = size)),
                 frameon = False, markerscale = 0, loc='upper right', bbox_to_anchor=(1.0, 1.0))
        
        # remove legend line (keeps only the label text)
        for item in legend.legendHandles:
            item.set_visible(False)

    fig.suptitle('{}'.format(title))
    
    # provides option to save well plate figure 
    if export == True:
        plt.savefig('{}_map.png'.format(title))
        
        
def wellcolour2(platemap, colorby, cmap, iterrange, to_plot):
    """Returns a unique colour for each label or defined condition.
    
    Wellcolour2 generates a dictionary of colours for each unique label. This can be used to colour code figures to a defined label. 
    This function is different to wellcolour in that colours are located by loc instead of iloc.
    
    :param platemap: Platemap that contains the required labels
    :type platemap: pandas dataframe
    :param colorby: Dataframe column to colour code, insert header name, for example 'Compound', 'Protein', 'Concentration', 'Concentration Units', 'Contents' or 'Type', default = 'Type'
    :type colorby: str
    :type cmap: Colour map that generates a customisable list of colours
    :param iterrange: Number of instances to itterate over, typically the size of the platemap
    :type iterrange: int
    :param to_plot: Wells to plot
    :type to_plot: str or list of str
    :return: RGB array of a colour that corresponds to a unique label
    :rtype: numpy array
    """
    colordict = get_colour_dict(platemap, colorby, cmap)   # get the dictionary with colours
    return wellcolour(colordict, platemap, colorby, iterrange, to_plot)

def invalidate_wells(platemap, wells, valid=False):
    """Returns updated plate map with specified wells invalidated.
    
    :param platemap: Plate map to use
    :type platemap: pandas dataframe
    :param wells: Well or wells to invalidate, e.g. ["A1", "B1", "C1"]
    :type wells: string or list of strings
    :param valid: Sets the stipulated well 'True' or 'False', default = False
    :type valid: bool
    :return: Returns updated plate map
    :rtype: pandas dataframe
    """
    platemap.loc[wells, 'Valid'] = valid 
    return platemap

def invalidate_rows(platemap, rows, valid=False):
    """Returns updated plate map with specified rows invalidated.
    
    :param platemap: Plate map to use
    :type platemap: pandas dataframe
    :param rows: Rows to invalidate, e.g. ("A", "B", "C")   
    :type rows: string or tuple of strings                             
    :param valid: Sets the stipulated row or rows 'True' or 'False', default = False
    :type valid: bool
    :return: Returns updated plate map
    :rtype: pandas dataframe
    """ 
    platemap.loc[platemap.index.str.startswith(rows), 'Valid'] = valid
    return platemap

def invalidate_cols(platemap, cols, valid=False):
    """Returns updated plate map with specified columns invalidated.
    
    :param platemap: Plate map to use
    :type platemap: pandas dataframe
    :param wells: Columns to invalidate, e.g. [1, 2, 3]
    :type wells: int or list of ints
    :param valid: Sets the stipulated column or columns 'True' or 'False', default = False
    :type valid: bool
    :return: Returns updated plate map
    :rtype: pandas dataframe
    """
    if type(cols) == int:   # convert cols to a list because cols must be an iterable object to allow for list comprehension 
        cols = [cols]

    all_ids = list(platemap.index)   # create a list of all well ids from platemap indexes
    inval_ids = [item for item in all_ids if int(item[1:]) in cols]   # list of well ids to be invalidated based on the columns from 'cols' parameter
    platemap.loc[inval_ids, 'Valid'] = valid
    return platemap
