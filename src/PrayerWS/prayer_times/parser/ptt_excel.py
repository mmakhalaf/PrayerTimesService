from ptt_parser import PrayerTimeParser, PrayerColumn;
from ptt_prayer_names import *
from openpyxl import *



class PrayerTimeExcelParser(PrayerTimeParser):
    """Read in Excel files and convert the data to our list of lists cell representation"""
    def __init__(self):
        return super().__init__();

    def ImportFromFile(self, filename):
        self.data = [];
        
        wb = None;
        try:
            wb = load_workbook(filename, use_iterators=True);
        except BaseException:
            raise ImportError("Failed to read file");

        sheet = wb.active;
        
        for row in sheet.rows:
            self.data.append([]);
            for cell in row:
                self.data[len(self.data)-1].append(cell.value);
            
        return self.ImportFromData();

if __name__ == "__main__":
    imp = PrayerTimeExcelParser();
    ptimes = imp.ImportFromFile("../../tests/data/Excel/test.xlsx");
