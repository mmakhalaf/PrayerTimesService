# Each prayer can't be spelt in various ways
# These classes abstracts the prayer name and allow each to be synonyms
# We'll assume everything is lowercase (and lower the case of incoming)

class PrayerName:
    """Base class to represent a prayer name, with all its variants"""

    def __init__(self):
        self.names = [];
    
    def IsPrayer(self, syn):
        syn = str.lower(syn);
        if syn in self.names:
            return True;
        else:
            return False;

class FajrPrayerName(PrayerName):
    name = "fajr";
    def __init__(self):
        self.names = ["fajr", "fagr"];

class DuhrPrayerName(PrayerName):
    name = "duhr";
    def __init__(self):
        self.names = ["duhr", "dohr", "dohor", "zuhr"];

class AsrPrayerName(PrayerName):
    name = "asr";
    def __init__(self):
        self.names = ["asr"];

class MaghribPrayerName(PrayerName):
    name = "maghrib";
    def __init__(self):
        self.names = ["magreb", "magrib", "maghreb", "maghrib"];

class IshaPrayerName(PrayerName):
    name = "isha";
    def __init__(self):
        self.names = ["isha", "ishaa"];
