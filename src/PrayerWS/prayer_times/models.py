from django.db import models

from mosques.models import Mosque

class PrayerTimes(models.Model):
    id = models.AutoField(primary_key=True);
    mosque = models.ForeignKey(Mosque, on_delete=models.CASCADE);
    date = models.DateField();
    fajr_jamaa = models.TimeField();
    duhr_jamaa = models.TimeField();
    asr_jamaa = models.TimeField();
    maghrib_jamaa = models.TimeField();
    ishaa_jamaa = models.TimeField();

    class Meta:
        ordering = ('id',);
        app_label = 'prayer_times';