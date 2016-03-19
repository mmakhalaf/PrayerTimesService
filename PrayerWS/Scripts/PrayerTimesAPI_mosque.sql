
--SELECT address, ST_AsText(ST_Transform(location::geometry, 3857)) FROM "PrayerTimesAPI_mosque"
--WHERE ST_DWITHIN(location, ST_Transform(ST_GeomFromText('SRID=3857;POINT(52.45 -1.9)'), 4326)::geography, .1);

--SELECT address, latitude, longitude, 70*ST_Distance(location, ST_Transform(ST_GeomFromText('SRID=3857;POINT(52.45 -1.9)'),4326))
--FROM "PrayerTimesAPI_mosque";

--SELECT name, address, postcode, latitude, longitude
--FROM "PrayerTimesAPI_mosque"
--WHERE ( 3959 * acos( cos( radians(52.45) ) * cos( radians( latitude ) ) * cos( radians( longitude ) - radians(-1.9) ) + sin( radians(52.45) ) * sin( radians( latitude ) ) ) ) < 1;

SELECT name, address, latitude, longitude,
ST_AsText(location),
ST_Distance(location,
            ST_GeomFromText('SRID=4326;POINT(52.45 -1.9)'))
FROM "PrayerTimesAPI_mosque";