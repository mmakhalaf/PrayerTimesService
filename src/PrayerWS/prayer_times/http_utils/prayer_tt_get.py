import datetime;
import calendar;

##### #########################################################################
class PTTGetRequest:
    """Parses the request for getting the time table"""

    ## Parameters
    parMosqueId = "mosqueid";
    parNumDays = "ndays";
    parMonth = "month";
    ##

    def __init__(self):
    ### ###############
        self.mosque_id = None;
        self.start_date = datetime.date.today();
        self.end_date = None;
        
    def Process(self, params):
    ### ######################
        """
        Extract query information from the map
        """
        # Get the mosque ID
        try:
            self.mosque_id = int(float(params[PTTGetRequest.parMosqueId]));
        except Exception as e:
            return False, "No mosque ID or invalid ID was provided.";

        # Use a duration (in days)
        try:
            num_days = int(float(params[PTTGetRequest.parNumDays]));
            if num_days > 0:
                self.end_date = self.start_date + datetime.timedelta(days=num_days);
                return True, None;
        except Exception as e:
            pass;

        # Use a month
        try:
            month = int(float(params[PTTGetRequest.parMonth]));
            if month < 1 or month > 12:
                return;
            
            # We can't query times in the past, so do so for the future
            year = self.start_date.year;
            if month < self.start_date.month:
                year += 1;

            range = calendar.monthrange(year, month);
            self.start_date = datetime.date(year, month, range[0]);
            self.end_date = datetime.date(year, month, range[1]);
        except Exception as e:
            return False, "No date range could be determined.";

        return True, None;
