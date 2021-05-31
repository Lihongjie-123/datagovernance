from django.db import models


class StatisticsDataInfo(models.Model):
    # id = models.AutoField(primary_key=True)
    primary_id = models.TextField(primary_key=True)
    interface_type = models.TextField()
    data = models.TextField()
    import_time = models.DateTimeField()

    class Meta(object):
        db_table = "statistics_data_info"
