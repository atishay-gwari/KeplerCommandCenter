from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Upload(models.Model):
    user_name = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    file=models.FileField()
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    public=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user_name}, {self.file}"


class Csv(models.Model):
    user_name = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    file=models.FileField()
    activated=models.BooleanField(default=False)
    updated_at=models.DateTimeField(auto_now_add=True)
    date=models.DateField(auto_now=False,auto_now_add=False)
    def __str__(self):
        return f"{self.user_name}, {self.file}"
    class Meta:
        verbose_name_plural = "Csv"
    
class CovertedToDB(models.Model):
    Monitering_Date=models.DateField(auto_now=False,null=True,blank=True,auto_now_add=False)
    user_name = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    
    
    Circle=models.CharField(max_length=100,null=True,blank=True)
    City=models.CharField(max_length=100,null=True,blank=True)
    Component=models.CharField(max_length=100,null=True,blank=True)
    Date=models.CharField(max_length=100,null=True,blank=True)
    Hour=models.IntegerField(null=True,blank=True)
    Total_Customers=models.IntegerField(null=True,blank=True)
    Anomal=models.CharField(max_length=100,null=True,blank=True)
    Ratio_Date=models.IntegerField(null=True,blank=True)
    Ratio_Voice=models.IntegerField(null=True,blank=True)
    Ratio_HSI=models.IntegerField(null=True,blank=True)
    cluster_issue=models.CharField(max_length=100,null=True,blank=True)
    Data_Volume=models.IntegerField(null=True,blank=True)
    Data_Volume_Formula=models.IntegerField(null=True,blank=True)
    Data_Volume_mean=models.IntegerField(null=True,blank=True)
    Data_Volume_std=models.IntegerField(null=True,blank=True)
    Voice_Affected_Users=models.IntegerField(null=True,blank=True)
    Voice_Affected_Users_Formula=models.IntegerField(null=True,blank=True)
    Voice_Affected_Users_mean=models.IntegerField(null=True,blank=True)
    Voice_Affected_Users_std=models.IntegerField(null=True,blank=True)
    HSI_Affected_Users=models.IntegerField(null=True,blank=True)
    HSI_Affected_Users_Formula=models.IntegerField(null=True,blank=True)
    HSI_Affected_Users_mean=models.IntegerField(null=True,blank=True)
    HSI_Affected_Users_std=models.IntegerField(null=True,blank=True)
    Data_Change=models.FloatField(null=True,blank=True)
    Voice_Change=models.FloatField(null=True,blank=True)
    HSI_Change=models.FloatField(null=True,blank=True)
    num_grids=models.IntegerField(null=True,blank=True)
    num_cells=models.IntegerField(null=True,blank=True)
    num_sectors=models.IntegerField(null=True,blank=True)
    Indoor_Freqency_850=models.IntegerField(null=True,blank=True)
    Indoor_Freqency_1800=models.IntegerField(null=True,blank=True)
    Indoor_Freqency_2300=models.IntegerField(null=True,blank=True)
    prb_20=models.IntegerField(null=True,blank=True)
    prb_70_90=models.IntegerField(null=True,blank=True)
    prb_90=models.IntegerField(null=True,blank=True)
    prb_20_per=models.FloatField(null=True,blank=True)
    prb_70_90_per=models.FloatField(null=True,blank=True)
    prb_90_per=models.FloatField(null=True,blank=True)
    area=models.FloatField(null=True,blank=True)                              
    month=models.IntegerField(null=True,blank=True)                               
    week=models.IntegerField(null=True,blank=True)                                 
    total_users_data_complaints=models.IntegerField(null=True,blank=True)          
    total_users_vvm_complaints=models.IntegerField(null=True,blank=True)          
    total_users_covergae_complaints=models.IntegerField(null=True,blank=True)      
    total_users_other_complaints=models.IntegerField(null=True,blank=True)         
    totla_upc_generated=models.IntegerField(null=True,blank=True)                  
    Polygon=models.CharField(max_length=100,null=True,blank=True)                             
    lat=models.FloatField(null=True,blank=True)                                
    lon=models.FloatField(null=True,blank=True)                               


    def __str__(self):
        return f"{self.user_name}, {self.Circle}, {self.City}, {self.Component}, {self.Date}, {self.Hour}, {self.Total_Customers}"
    
    class Meta:
        verbose_name_plural = "CovertedToDB"