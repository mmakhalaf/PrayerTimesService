# Each prayer can't be spelt in various ways
# These classes abstracts the prayer name and allow each to be synonyms
# We'll assume everything is lowercase (and lower the case of incoming)

##### #########################################################################
class PrayerName:
    """Base class to represent a prayer name, with all its variants"""

    def __init__(self):
    ### ###############
        self.name = "";
        self.num = -1;
        self.aliases = [];
    
    def ContainsPrayer(self, txt):
    ### ##########################
        """Return True if 'txt' contains one of the synonyms"""
        txt = str.lower(txt);
        for syn in self.aliases:
            if txt.find(syn) != -1:
                return True;
        return False;


##### #########################################################################
class FajrPrayerName(PrayerName):
    name = "fajr";
    jamaa = name + "_jamaa";

    def __init__(self):
    ### ###############
        self.name = FajrPrayerName.name;
        self.num = 1;
        self.aliases = ["fajr", 
                        "fagr"];
        
##### #########################################################################
class DuhrPrayerName(PrayerName):
    name = "duhr";
    jamaa = name + "_jamaa";

    def __init__(self):
    ### ###############
        self.name = DuhrPrayerName.name;
        self.num = 2;
        self.aliases = ["duhr",
                        "dohr", 
                        "dohor", 
                        "zuhr", 
                        "zohr", 
                        "zohar"];
        
##### #########################################################################
class AsrPrayerName(PrayerName):
    name = "asr";
    jamaa = name + "_jamaa";

    def __init__(self):
    ### ###############
        self.name = AsrPrayerName.name;
        self.num = 3;
        self.aliases = ["asr",
                        "asar"];
        
##### #########################################################################
class MaghribPrayerName(PrayerName):
    name = "maghrib";
    jamaa = name + "_jamaa";

    def __init__(self):
    ### ###############
        self.name = MaghribPrayerName.name;
        self.num = 4;
        self.aliases = ["magreb", 
                        "magrib", 
                        "maghreb", 
                        "maghrib"];
        
##### #########################################################################
class IshaPrayerName(PrayerName):
    name = "ishaa";
    jamaa = name + "_jamaa";

    def __init__(self):
    ### ###############
        self.name = IshaPrayerName.name;
        self.num = 5;
        self.aliases = ["isha", 
                        "ishaa"];

        
###############################################################################

prayers = (FajrPrayerName(),
            DuhrPrayerName(),
            AsrPrayerName(),
            MaghribPrayerName(),
            IshaPrayerName());

def ContainsPrayerName(content):
### ############################
    """Returns the actual prayer name object if any found in the input."""
    if content is None:
        return None;
    for p in prayers:
        if p.ContainsPrayer(content):
            return p;
    return None;

def ContainsJamaat(content):
### ########################
    """Returns whether the given text contains something indicative of jamaa"""
    if content is None:
        return False;

    content = str.lower(content);
    jamat_syn = ["jamat",
                 "jamaa",
                 "jamaat",
                 "jama"];

    for syn in jamat_syn:
        if content.find(syn) != -1:
            return True;

    return False;