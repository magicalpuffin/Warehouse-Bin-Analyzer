import pandas as pd

# Had to manually set the decimals in the package because small volumes resulted in 0
# Changing the value in py3dbp.main for didn't work for some reason
import py3dbp
py3dbp.main.DEFAULT_NUMBER_OF_DECIMALS = 9
from decimal import Decimal

# Currently these functions were just imported from the previous project and made to be functional
# Should consider other bin packing optimization packages

def get_solution_bin(packer):
    """
    Finds the best bin that packed the items based on packing object. Will pick bin with smallest volume. \n
    Defaults to the largest bin if packing failed. Outputs bin and true false status. \n
    """
    # Finds the smallest volume bin that fits all items by looping through in order until one fits all items
    # Will default to largest bin if none can be found
    # Determines if the items were packed or not in pack_status
    bestbin = packer.bins[-1]
    pack_status = False
    for b in packer.bins:
        if len(b.unfitted_items) == 0:
            bestbin = b
            pack_status = True
            break
    return bestbin, pack_status

def get_excess_vol_weight(bin):
    """
    Takes a bin and finds the extra volume and weight left by the fitted items
    """
    total_item_vol = Decimal(0)
    total_item_weight = Decimal(0)
    for i in bin.items:
        total_item_vol = total_item_vol + i.get_volume()
        total_item_weight = total_item_weight + i.weight

    vol_diff = bin.get_volume() - total_item_vol
    weight_diff = bin.max_weight - total_item_weight
    vol_util = total_item_vol / bin.get_volume()
    weight_util = total_item_weight / bin.max_weight

    return vol_diff, weight_diff, vol_util, weight_util

def pack_SO(df, bin_df):
    """
    Determines the best bin to pack a shipping order. \n
    Designed to be used with an apply function on a dataframe grouped by SO.\n
    Parameters: \n
        df: Dataframe of a single shipping order. Item name assumed as index. Items have quantity and dimensions.\n
        bin_df: Dataframe of bins to be used during packing. Change the default so it works with apply. \n
                I don't know if there is a better way.\n
    Returns: \n
        output_sr: Series with different output parameters
    """
    # Prepares and runs packer object
    # ----
    # Initialized packer object. From the py3dbp package.
    packer = py3dbp.Packer()

    # Loops through each item in SO. Will add items to packer multiple times based on quantity.
    # Index should be the item name.
    for index, row in df.iterrows():
        for i in range(int(row["quantity"])):
            packer.add_item(py3dbp.Item(index, row["item_length"], row["item_width"], row["item_height"], row["item_weight"]))

    # Loops though each bins and adds them into the packer object
    # I want to switch this to use indexes but it breaks the package for some reason
    for index, row in bin_df.iterrows():
        packer.add_bin(py3dbp.Bin(row["bin_name"], row["bin_length"], row["bin_width"], row["bin_height"], row["bin_weight"]))
    
    # Packer evaluates how well items are packed in each bin
    packer.pack(number_of_decimals= 9)
    # ----
    # Interpret the packed results
    # Note that values from packer use the Decimal module
    bestbin, pack_status = get_solution_bin(packer)
    vol_diff, weight_diff, vol_util, weight_util = get_excess_vol_weight(bestbin)
    bin_name = bestbin.name
    # ----
    # Output series in order to automatically create a dataframe from the apply function
    # packer and bestbin are included for debugging purposes
    output_sr = pd.Series({'Pack_Status': pack_status, 
                           'Bin_Name': bin_name, 
                           'Volume_Difference': vol_diff, 
                           'Weight_Difference': weight_diff,
                           'Volume_Utilization': vol_util,
                           'Weight_Utilization': weight_util})
    return output_sr