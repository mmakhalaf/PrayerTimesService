from openpyxl import *

wb = load_workbook("../../../../tests/data/Shrewsbury_2016.xlsx", use_iterators=True);
print(wb.sheetnames);
sheet = wb['March'];
for row in sheet.rows:
    for cell in row:
        print("{}".format(cell.value));

# Algorithm
#
# Create a genric table structure to input to the algorithm
#  This could potentially mean the algorithm is not 'excel' dependent'
#  The table should contain strings (or None) where empty
#
# = Find prayer columns
# prayer_name_columns = []
# prayer_name_row = -1
# Go through each row,
#  For each cell in the row,
#   Find the prayer names (taking synonyms into account).
#   Store the indices (or range, if merged) of their columns in 'prayer_name_columns'
#   Store the current row index in 'prayer_name_row'
#   Once found, end the iteration
#
# = Find date rows
# date_range_rows = []
# date_range_column = -1
# Go through each column,
#  Look for sequential numbers starting from 1
#   The sequence should start from the row after which the prayers were found
#   Store the rows on which the dates are appearing
#   Store the current column index
#   Once found, end the iteration
#
#
# = Find Jamaa times
# prayer_times = []
# Store the end prayer times into an array of maps (key as prayer name, value as time)
# For each prayer in 'prayer_name_columns'
#  jamaa_column = -1
#  If single column, this is the jamaa column
#  If multiple,
#   look in the grid under the prayer name for the word jamaa (and its synonyms)
#  If not found, use the last column in the range if it has a sequence in the
#  rows under it
#  If still not found,
#   TODO What???
#  For each row in 'data_range_rows',
#   Add the time at the given cell into 'prayer_times'
#
