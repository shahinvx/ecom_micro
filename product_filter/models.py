from django.db import models

# Create your models here.


class FinalAmazonV2(models.Model):
    uniq_id = models.TextField(db_column='Uniq Id', blank=True, null=True)
    product_name = models.TextField(
        db_column='Product Name', blank=True, null=True)
    category = models.TextField(db_column='Category', blank=True, null=True)
    selling_price = models.FloatField(
        db_column='Selling Price', blank=True, null=True)
    image = models.TextField(db_column='Image', blank=True, null=True)
    stock = models.IntegerField(db_column='Stock', blank=True, null=True)
    model_number = models.TextField(
        db_column='Model Number', blank=True, null=True)
    variants = models.TextField(db_column='Variants', blank=True, null=True)
    about_product = models.TextField(
        db_column='About Product', blank=True, null=True)
    product_specification = models.TextField(
        db_column='Product Specification', blank=True, null=True)
    technical_details = models.TextField(
        db_column='Technical Details', blank=True, null=True)
    product_url = models.TextField(
        db_column='Product Url', blank=True, null=True)
    rating = models.IntegerField(db_column='Rating', blank=True, null=True)
    shiping = models.TextField(db_column='Shiping', blank=True, null=True)
    discount_percentage = models.IntegerField(
        db_column='discount percentage', blank=True, null=True)
    #id = models.AutoField(unique=True)

    # def __str__(self):
    #     return self.id

    class Meta:
        managed = True
        db_table = 'final_amazon_v2'
