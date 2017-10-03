# PrayerTimesService
DJango web service for providing mosques' prayer times.

Provides,
- Read content of http://www.mosquedirectory.co.uk/ into a PostgreSQL database
- A simple (unsecure) web server,
  - List all mosques
  - Search for mosques based on some criteria
  - Upload prayer times for an Excel file (tries to be flexible)
