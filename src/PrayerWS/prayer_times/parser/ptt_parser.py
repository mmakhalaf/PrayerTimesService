from prayer_times.parser.ptt_prayer_names import *
import sys
import time
from itertools import groupby


# Algorithm
#
# = Find prayer columns
# Return the result as
#  prayer_name_columns_indices = []
#  prayer_name_row_index = -1
# 
# = Find Jamaa columns
# Return the columns containing the jamaa prayer
#  prayer_times = []
#
# = Extract times from jamaa column
#

##### #########################################################################
class ParsingError(Exception):
    """Exception thrown while parsing"""
    def __init__(self, value):
    ### ######################
        self.value = value;
    def __str__(self):
    ### ##############
        return repr(self.value);
    

##### #########################################################################
class PrayerColumn:
    """Represents a prayer column"""
    def __init__(self, cell, row_idx, col_idx, prayer_name):
    ### ####################################################
        self.text = cell;
        self.row_idx = row_idx;
        self.col_idx = col_idx;
        self.prayer_name = prayer_name;

    def GetPrayerName(self):
    ### ####################
        return self.prayer_name.name;

    def __str__(self):
    ### ##############
        str = "Coordinates: {}, {}.\nText: {}.\nPrayer Name: {}.";
        return str.format(self.row_idx, self.col_idx, self.text, self.GetPrayerName());
        

##### #########################################################################
class PrayerTimeParser:

    def __init__(self):
    ### ###############
        self.data = [];
        self.use_jamaa_fieldnames = False;

    def ImportFromFile(self, filename):
    ### ###############################
        """
        Implement this class to populate 'data' and then return the result
        of the base class function ImportFromData()
        """ 
        raise ParsingError("Calling abstract class");

    def ImportFromData(self):
    ### #####################
        if len(self.data) == 0:
            raise ParsingError("No data to parse");

        '''
        for row in self.data:
            for c in row:
                print(c, end=" ");
            print("");
        '''

        # Get the columns containing the prayer names
        prayer_cols = self.__findPrayerNames();
        '''
        for pcol in prayer_cols:
            print("===\n{}".format(str(pcol)));
        '''

        # Return a the column list of the jamat times
        prayer_cols = self.__filterPrayerColumns(prayer_cols);
        '''
        for pcol in prayer_cols:
            print("===\n{}".format(str(pcol)));
        '''

        prayer_times = self.__extractPrayerTimes(prayer_cols);

        prayer_times_list = self.__reformatPrayerTimeTable(prayer_times);

        return prayer_times_list;

    def __findPrayerNames(self):
    ### ########################
        """Return a list of column indices and the row they belong to"""
        
        # prayer_name_columns = []
        # prayer_name_row = -1
        # Go through each row,
        #  For each cell in the row,
        #   Find the prayer names (taking synonyms into account).
        #    Account for prayer name duplicates on the same row (one actual and one for jamaa)
        #   Store the indices (or range, if merged) of their columns in 'prayer_name_columns'
        #   Store the current row index in 'prayer_name_row'
        #   Once the row is found, end the iteration
        
        prayer_cols = [];

        r_idx = -1;
        for row in self.data:
            r_idx += 1;
            c_idx = -1;
            for cell in row:
                c_idx += 1;
                if cell == None:
                    continue;
                pname = ContainsPrayerName(str(cell));
                if pname != None:
                    prayer_cols.append(PrayerColumn(cell, r_idx, c_idx, pname));
        
        return prayer_cols;

    def __filterPrayerColumns(self, prayer_cols):
    ### #########################################
        """Filter the given column list to only those containing the Jamat prayer"""

        # Throw an error if there are fewer than 5 columns
        # Assume the names occur on the same row
        # 
        siz = len(prayer_cols);
        
        if len(prayer_cols) > 0:
            r = prayer_cols[0].row_idx;
            for pcol in prayer_cols:
                if pcol.row_idx != r:
                    #TODO Can this be handled differently???
                    raise ParsingError("Prayer names are not on the same row");
        
        if siz < 5:
            raise ParsingError("Not enough prayer columns");
        
        # Group the columns by prayer, ensure they're sorted by row index in ascending
        # order.
        #
        # For each group,
        #  Get the range of columns for the prayer
        #  If there is only in the range, this is the jamat
        #  For each column, starting from the row under the prayer name, check if jamaa column
        
        # Create a new list ordered by row and grouped by prayer
        new_prayer_cols = [];
        jamaa_prayer_cols = [];
        prayer_cols.sort(key=lambda x: x.col_idx);
        for k, g in groupby(prayer_cols, lambda c : c.prayer_name.name):
            for pcol in g:
                new_prayer_cols.append(pcol);
        
        num_cols = len(self.data[new_prayer_cols[0].row_idx]);
        for pname_idx in range(0, len(new_prayer_cols)):

            # Find the start and end column of a prayer
            curr_p = new_prayer_cols[pname_idx];
            min_col = curr_p.col_idx;
            max_col = curr_p.col_idx;

            if pname_idx < len(new_prayer_cols)-1:
                for pname_idx_2 in range(pname_idx,len(new_prayer_cols)):
                    next_p = new_prayer_cols[pname_idx_2];
                    if curr_p.GetPrayerName() != next_p.GetPrayerName():
                        max_col = next_p.col_idx;
                        break;
            else:
                max_col = num_cols;

            # Go through each cell between the max and min columns
            # on and under the given row
            r_idx = curr_p.row_idx;
            for r_idx in range(curr_p.row_idx, len(self.data)):
                found = False;
                for c_idx in range(min_col, max_col):
                    if ContainsJamaat(str(self.data[r_idx][c_idx])) or \
                                        min_col == max_col-1:
                        jamaa_prayer_cols.append(PrayerColumn(curr_p.GetPrayerName(), r_idx, c_idx, curr_p.prayer_name));
                        found = True;
                        break;
                if found:
                    break;
            
        return jamaa_prayer_cols;

    def __extractPrayerTimes(self, jamaa_cols):
    ### #######################################
        """Given a column, return a list of the jamaa prayer times under it."""

        prayer_times = {};

        time_formats = ("%I:%M",
                        "%I:%M %p",
                        "%I:%M:%S",
                        "%I:%M:%S %p");

        for jam_col in jamaa_cols:
            s_row = jam_col.row_idx;
            ls = [];
            is_first = True;
            for row_idx in range(s_row, len(self.data)):
                val = self.data[row_idx][jam_col.col_idx];
                t = None;
                if val is not None:
                    val = str(val).strip();
                    for tf in time_formats:
                        try:
                            t = time.strptime(val, tf);
                            break;
                        except ValueError:
                            continue;

                if t == None:
                    if is_first == False:
                        ls.append(ls[len(ls)-1]);
                    continue;
                
                if is_first:
                    is_first = False;

                ls.append(time.strftime("%I:%M", t));
            prayer_times[jam_col.GetPrayerName()] = ls;

        # Validate the number of times are the same for all prayers
        n = len(prayer_times[FajrPrayerName.name]);
        for k in prayer_times:
            if len(prayer_times[k]) != n:
                raise ParsingError("The number of prayer times extracted for all prayers is not the same");

        return prayer_times;

    def __reformatPrayerTimeTable(self, prayer_times):
    ### ##############################################
        """
        Given a map prayer_times {fajr: [list_of_times]},
        convert it to an array [{fajr: time, duhr: time}, {}, ...]
        """

        month_time = [];

        num_days = len(prayer_times[FajrPrayerName.name]);

        prayer_names_jamaa = [FajrPrayerName.jamaa,
                        DuhrPrayerName.jamaa,
                        AsrPrayerName.jamaa,
                        MaghribPrayerName.jamaa,
                        IshaPrayerName.jamaa];

        prayer_names = [FajrPrayerName.name,
                        DuhrPrayerName.name,
                        AsrPrayerName.name,
                        MaghribPrayerName.name,
                        IshaPrayerName.name];

        for i in range(0, num_days):
            day_time = {};
            for pi in range(0, len(prayer_names)):
                if self.use_jamaa_fieldnames:
                    day_time[prayer_names_jamaa[pi]] = prayer_times[prayer_names[pi]][i];
                else:
                    day_time[prayer_names[pi]] = prayer_times[prayer_names[pi]][i];
            month_time.append(day_time);

        return month_time;

