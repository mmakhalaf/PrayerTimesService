SELECT id, name, address, postcode, capacity, gender, ST_AsText(location)
FROM public."PrayerTimesAPI_mosque";
