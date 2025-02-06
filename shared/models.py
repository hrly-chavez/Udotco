# # from django.db import models
# # from django.utils.timezone import now
# # from django.contrib.auth.hashers import make_password
# # from django.apps import apps

# # # Create your models here.
# # class Bus(models.Model): 
# #     # bus_unit_num = models.IntegerField(primary_key=True)
# #     bus_unit_num = models.CharField(primary_key=True)
# #     bus_license_plate_number = models.CharField(max_length=10)
# #     bus_chassis_num = models.CharField(max_length=10)
# #     bus_engine_num = models.CharField(max_length=10)
# #     bus_year_model = models.IntegerField(null=True, blank=True)
# #     bus_tag_num = models.CharField(max_length=10)

# #     def __str__(self) -> str:
# #         return str(self.bus_unit_num) if self.bus_unit_num else "No Bus unit num"
    
# # class Material(models.Model):
# #     mat_code = models.AutoField(primary_key=True)  
# #     mat_name = models.CharField(max_length=200)
# #     mat_quantity = models.IntegerField()
# #     mat_brand = models.CharField(max_length=200, default='generic') 
# #     mat_measurement = models.CharField(max_length=200, null=True, blank=True)  
# #     mat_category = models.ForeignKey('Material_Category',on_delete=models.CASCADE,db_constraint=True)
# #     mat_max_request = models.PositiveIntegerField(null=True,blank=True)
# #     updated_at = models.DateTimeField(auto_now=True)

# #     def __str__(self):
# #         return f"{self.mat_name} ,{self.mat_code}, {self.mat_category}"
    
# # class Material_Category(models.Model):
# #     mat_category_id = models.AutoField(primary_key=True)
# #     mat_name = models.CharField(max_length=200)

# #     def __str__(self):
# #         return f"{self.mat_name}"

# # class Department(models.Model):
# #     dept_id = models.AutoField(primary_key=True)
# #     dept_name = models.CharField(max_length=200)
# #     dept_descript = models.TextField(null=True, blank=True)

# #     def __str__(self):
# #         return f"{self.dept_id}, {self.dept_name}"
    
# # class Employee(models.Model):
# #     emp_id = models.AutoField(primary_key=True)
# #     emp_fname = models.CharField(max_length=100)
# #     emp_initial = models.CharField(max_length=1, null=True, blank=True)
# #     emp_lname = models.CharField(max_length=100)
# #     emp_suffix = models.CharField(max_length=10, null=True, blank=True)
# #     emp_date_of_birth = models.DateField()
# #     emp_sex = models.CharField(max_length=6)
# #     emp_address = models.CharField(max_length=200)
# #     emp_role = models.CharField(max_length=100, null=True, blank=True)
# #     emp_contact_num = models.CharField(max_length=11)
# #     dept_id = models.ForeignKey(Department, on_delete=models.CASCADE, db_constraint=True)
# #     emp_image = models.ImageField(upload_to='employee_images/', null=True, blank=True)

# #     def __str__(self):
# #         return f"{self.emp_fname}, {self.emp_lname} ({self.dept_id.dept_name})"

# # class Purchase_Order_Status(models.Model):
# #     STATUS_CHOICES = [
# #         ('Waiting', 'Waiting'),
# #         ('Ongoing', 'Ongoing'),
# #         ('Done', 'Done'),
# #     ]
# #     postat_id = models.AutoField(primary_key=True)
# #     postat_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Waiting')

# #     def __str__(self):
# #         return self.postat_status
  
# # class Supplier(models.Model):
# #     sup_id = models.AutoField(primary_key=True)
# #     sup_name =models.CharField(max_length=300)
# #     sup_descript=models.TextField(null=True, blank=True)

# #     def __str__(self):
# #         return f"{self.sup_name} "
    
# # class Material_Order_Category(models.Model):
# #     mat_odr_cat_id = models.AutoField(primary_key=True)
# #     mat_odr_cat_name = models.CharField(max_length=100)

# #     def __str__(self):
# #         return f"{self.mat_odr_cat_name}"
    
# # def get_default_material_order_category():
# #     # Try to fetch the first category, or create a new one if none exists
# #     return Material_Order_Category.objects.first() or Material_Order_Category.objects.create(mat_odr_cat_name="Default Category")

# # class Purchase_Order(models.Model):
# #     po_num = models.AutoField(primary_key=True)
# #     po_approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL,null=True,blank=True)
# #     po_description = models.TextField(null=True, blank=True)
# #     po_datemade = models.DateField(default=now)
# #     postat_id = models.ForeignKey(Purchase_Order_Status, on_delete=models.SET_NULL, null=True,blank=True)
# #     sup_id = models.ForeignKey(Supplier, on_delete=models.SET_NULL,null=True, blank=True)
# #     mat_odr_id = models.ForeignKey(Material_Order_Category, on_delete=models.CASCADE,db_constraint=True, default= get_default_material_order_category, null =True,blank=True)
    
# # class Material_Order(models.Model):
# #     mat_odr_id = models.AutoField(primary_key=True)
# #     mat_odr_name = models.CharField(max_length=100)
# #     mat_odr_qty = models.IntegerField()
# #     mat_odr_brand = models.CharField(max_length=100, null=True, blank=True)
# #     mat_odr_measurement = models.CharField(null=True, blank=True)
# #     mat_category = models.ForeignKey(Material_Order_Category,on_delete=models.CASCADE, db_constraint=True,null=True,blank=True)
# #     purchase_order = models.ForeignKey(Purchase_Order, on_delete=models.CASCADE)
    
    
# #     def __str__(self):
# #         return f"{self.mat_odr_name}, {self.mat_odr_qty}"

# # class Material_Used(models.Model):
# #     mat_used_id = models.AutoField(primary_key=True)
# #     mat_used_name = models.CharField(max_length=200)
# #     mat_used_qty = models.IntegerField()
# #     mat_used_brand = models.CharField(max_length=200, null=True, blank=True)
# #     mat_used_measurement =models.CharField(max_length=200, null=True, blank=True)

# # class JobOrder(models.Model):
# #     STATUS_CHOICES = [
# #         ('Pending', 'Pending'),
# #         ('In Progress', 'In Progress'),
# #         ('Completed', 'Completed'),
# #     ]
# #     j_o_number = models.AutoField(primary_key=True)
# #     j_o_date_requested = models.DateField(default=now)
# #     j_o_work_description = models.TextField(null=True,blank=True)
# #     j_o_date_completed = models.DateField(null=True, blank=True)
# #     j_o_checked_by = models.ForeignKey(Employee, related_name='checked_by', on_delete=models.SET_NULL, null=True, blank=True)
# #     j_o_approved_by = models.ForeignKey(Employee, related_name='approved_by', on_delete=models.SET_NULL, null=True, blank=True)
# #     j_o_status =  models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
# #     j_o_bus_unit_num = models.ForeignKey(Bus, on_delete=models.CASCADE)
# #     mat_used_id = models.ForeignKey(Material_Used,on_delete=models.SET_NULL,null=True,blank=True)

# #     def __str__(self):
# #         return f"Job Order #{self.j_o_number} - {self.j_o_work_description[:30]}"  
    
# # class Material_Requested(models.Model):
# #     mat_req_id = models.AutoField(primary_key=True)
# #     mat_req_qty = models.PositiveIntegerField()
# #     mat_code = models.ForeignKey('Material', on_delete=models.CASCADE, db_constraint=True)
# #     item_req_num = models.ForeignKey('Item_Request', on_delete=models.CASCADE, db_constraint=True)
    
# #     # Add a status field to track approval status of each material request
# #     mat_req_status = models.CharField(max_length=20, choices=[
# #         ('Pending', 'Pending'),
# #         ('Approved', 'Approved'),
# #         ('Denied', 'Denied')
# #     ], default='Pending')

# #     def __str__(self):
# #         return f"{self.item_req_num} {self.mat_req_qty}"


# # class Item_Request(models.Model):
# #     IR_STAT_CHOICES = [
# #         ('Waiting', 'Waiting'),
# #         ('Ongoing', 'Ongoing'),
# #         ('Done', 'Done'),
# #     ]
# #     item_req_num = models.AutoField(primary_key=True)
# #     item_req_approved_by = models.ForeignKey('Employee', on_delete=models.CASCADE, db_constraint=True)
# #     item_req_date_requested = models.DateField(default=now)
# #     item_req_description = models.TextField(null=True, blank=True)
# #     item_req_status =  models.CharField(max_length=10, choices = IR_STAT_CHOICES, default='Waiting')
# #     bus_unit_num = models.ForeignKey(Bus, on_delete=models.CASCADE, db_constraint=True)
# #     mat_req_id = models.ForeignKey(Material_Requested,on_delete=models.SET_NULL,null=True,blank=True)
    
# #     def __str__(self):
# #         return f"{self.item_req_num} {self.mat_req_id}"
# #     def update_status(self):
# #         material_requests = self.material_requested_set.all()  # Fetch related materials

# #         if all(mat.mat_req_status in ['Approved', 'Denied'] for mat in material_requests):
# #             self.item_req_status = 'Done'
# #         elif any(mat.mat_req_status in ['Approved', 'Denied'] for mat in material_requests):
# #             self.item_req_status = 'Ongoing'
# #         else:
# #             self.item_req_status = 'Waiting'
# #         self.save()

# # class Acknowledgment_Receipt(models.Model):
# #     status_choices = [ 
# #         ('Pending', 'Pending'),
# #         ('Ongoing', 'Ongoing'),
# #         ('Delivered', 'Delivered'),
# #     ]
# #     ar_num = models.AutoField(primary_key=True)
# #     ar_date_made = models.DateTimeField(default=now)
# #     ar_date_received = models.DateField(null=True, blank=True)
# #     ar_date_receiver = models.ForeignKey(Employee, on_delete=models.CASCADE,null=True, blank=True)
# #     ar_status = models.CharField(max_length=20,choices=status_choices, default='Pending')
# #     ar_note = models.TextField()
# #     item_approved_id = models.ForeignKey('Material_Approved', on_delete=models.CASCADE, db_constraint=True)
    
# # class Material_Approved(models.Model):
# #     mat_approved_id = models.AutoField(primary_key=True)
# #     mat_req_id = models.ForeignKey(Material_Requested, on_delete=models.CASCADE, related_name='approved_materials')
# #     ir_num = models.ForeignKey(Item_Request, on_delete=models.CASCADE)
# #     mat_approved_qty = models.PositiveIntegerField()  # Approved quantity
# #     mat_approved_code = models.ForeignKey(Material, on_delete=models.SET_NULL,null=True,blank=True)  # Material code
# #     date_approved = models.DateTimeField(auto_now_add=True)
# #     ar_num = models.ForeignKey(Acknowledgment_Receipt, on_delete=models.CASCADE, null=True, blank=True)  
# #     is_acknowledged = models.BooleanField(default=False)
# #     def __str__(self):
# #         return f"Approved Material: {self.mat_approved_code.mat_name} - {self.mat_approved_qty}"

# # class Accounts(models.Model):
# #     user_id = models.OneToOneField( 
# #         'Employee', 
# #         on_delete=models.CASCADE, 
# #         db_constraint=True, 
# #         primary_key=True
# #     )
# #     username = models.CharField(
# #         max_length=150, 
# #         unique=True, 
# #         null=False, 
# #         blank=False
# #     )  # Adding a unique username field
# #     password = models.CharField(max_length=128)  # Storing hashed passwords

# #     def save(self, *args, **kwargs):
# #         # Hash the password before saving
# #         if not self.pk and self.password:  # Only hash if it's a new instance
# #             self.password = make_password(self.password)
# #         super().save(*args, **kwargs)

# #     def __str__(self):  
# #         return f"Username: {self.username}, User ID: {self.user_id}"
    
# from django.db import models
# from django.utils.timezone import now
# from django.contrib.auth.hashers import make_password
# from django.apps import apps
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# # Create your models here.
# class Bus(models.Model): 
#     bus_unit_num = models.CharField(primary_key=True)
#     bus_license_plate_number = models.CharField(max_length=10)
#     bus_chassis_num = models.CharField(max_length=10)
#     bus_engine_num = models.CharField(max_length=10)
#     bus_year_model = models.IntegerField(null=True, blank=True)
#     bus_tag_num = models.CharField(max_length=10)

#     def __str__(self) -> str:
#         return str(self.bus_unit_num) if self.bus_unit_num else "No Bus unit num"
    
# class Material(models.Model):
#     mat_code = models.AutoField(primary_key=True)  
#     mat_name = models.CharField(max_length=200)
#     mat_quantity = models.IntegerField() 
#     mat_brand = models.CharField(max_length=200, default='generic') 
#     mat_measurement = models.CharField(max_length=200, null=True, blank=True)  
#     mat_category = models.ForeignKey('Material_Category',on_delete=models.CASCADE,db_constraint=True)
#     mat_max_request = models.PositiveIntegerField(null=True,blank=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.mat_name} ,{self.mat_code}, {self.mat_category}"
    
# class Material_Category(models.Model):
#     mat_category_id = models.AutoField(primary_key=True)
#     mat_name = models.CharField(max_length=200)

#     def __str__(self):
#         return f"{self.mat_name}"

# class Department(models.Model):
#     dept_id = models.AutoField(primary_key=True)
#     dept_name = models.CharField(max_length=200)
#     dept_descript = models.TextField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.dept_id}, {self.dept_name}"
    
# class Employee(models.Model):
#     emp_id = models.AutoField(primary_key=True)
#     emp_fname = models.CharField(max_length=100)
#     emp_initial = models.CharField(max_length=1, null=True, blank=True)
#     emp_lname = models.CharField(max_length=100)
#     emp_suffix = models.CharField(max_length=10, null=True, blank=True)
#     emp_date_of_birth = models.DateField()
#     emp_sex = models.CharField(max_length=6)
#     emp_address = models.CharField(max_length=200)
#     emp_role = models.CharField(max_length=100, null=True, blank=True)
#     emp_contact_num = models.CharField(max_length=11)
#     dept_id = models.ForeignKey(Department, on_delete=models.CASCADE, db_constraint=True)
#     emp_image = models.ImageField(upload_to='employee_images/', null=True, blank=True)

#     def __str__(self):
#         return f"{self.emp_fname}, {self.emp_lname} ({self.dept_id.dept_name})"

# class Purchase_Order_Status(models.Model):
#     STATUS_CHOICES = [
#         ('Waiting', 'Waiting'),
#         ('Ongoing', 'Ongoing'),
#         ('Done', 'Done'),
#     ]
#     postat_id = models.AutoField(primary_key=True)
#     postat_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Waiting')

#     def __str__(self):
#         return self.postat_status
  
# class Supplier(models.Model):
#     sup_id = models.AutoField(primary_key=True)
#     sup_name =models.CharField(max_length=300)
#     sup_descript=models.TextField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.sup_name} "
    
# class Material_Order_Category(models.Model):
#     mat_odr_cat_id = models.AutoField(primary_key=True)
#     mat_odr_cat_name = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.mat_odr_cat_name}"
    
# def get_default_material_order_category():
#     # Try to fetch the first category, or create a new one if none exists
#     return Material_Order_Category.objects.first() or Material_Order_Category.objects.create(mat_odr_cat_name="Default Category")

# class Purchase_Order(models.Model):
#     po_num = models.AutoField(primary_key=True)
#     po_approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL,null=True,blank=True)
#     po_description = models.TextField(null=True, blank=True)
#     po_datemade = models.DateField(default=now)
#     postat_id = models.ForeignKey(Purchase_Order_Status, on_delete=models.SET_NULL, null=True,blank=True)
#     sup_id = models.ForeignKey(Supplier, on_delete=models.SET_NULL,null=True, blank=True)
#     mat_odr_id = models.ForeignKey(Material_Order_Category, on_delete=models.CASCADE,db_constraint=True, default= get_default_material_order_category, null =True,blank=True)
    
# class Material_Order(models.Model):
#     mat_odr_id = models.AutoField(primary_key=True)
#     mat_odr_name = models.CharField(max_length=100)
#     mat_odr_qty = models.IntegerField()
#     mat_odr_brand = models.CharField(max_length=100, null=True, blank=True,default='Generic')
#     mat_odr_measurement = models.CharField(null=True, blank=True)
#     mat_category = models.ForeignKey(Material_Category,on_delete=models.CASCADE)
#     mat_odr_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Denied', 'Denied')], default='Pending')
#     item_req_num = models.ForeignKey('Item_Request', on_delete=models.SET_NULL, null=True, blank=True, db_constraint=True)
    
#     def __str__(self):
#         return f"{self.mat_odr_name}"

# class Material_Used(models.Model):
#     mat_used_id = models.AutoField(primary_key=True)
#     mat_used_name = models.CharField(max_length=200)
#     mat_used_qty = models.IntegerField()
#     mat_used_brand = models.CharField(max_length=200, null=True, blank=True)
#     mat_used_measurement =models.CharField(max_length=200, null=True, blank=True)

# class JobOrder(models.Model):
#     STATUS_CHOICES = [
#         ('Pending', 'Pending'),
#         ('In Progress', 'In Progress'),
#         ('Completed', 'Completed'),
#     ]
#     j_o_number = models.AutoField(primary_key=True)
#     j_o_date_requested = models.DateField(default=now)
#     j_o_work_description = models.TextField()
#     j_o_date_completed = models.DateField(null=True, blank=True)
#     j_o_checked_by = models.ForeignKey(Employee, related_name='checked_by', on_delete=models.SET_NULL, null=True, blank=True)
#     j_o_approved_by = models.ForeignKey(Employee, related_name='approved_by', on_delete=models.SET_NULL, null=True, blank=True)
#     j_o_status =  models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
#     j_o_bus_unit_num = models.ForeignKey(Bus, on_delete=models.CASCADE)
#     mat_used_id = models.ForeignKey(Material_Used,on_delete=models.SET_NULL,null=True,blank=True)
    

#     def __str__(self):
#         return f"Job Order #{self.j_o_number} - {self.j_o_work_description[:30]}"  
    
# class Material_Requested(models.Model):
#     mat_req_id = models.AutoField(primary_key=True)
#     mat_req_qty = models.PositiveIntegerField()
#     mat_code = models.ForeignKey('Material', on_delete=models.CASCADE, db_constraint=True)
#     item_req_num = models.ForeignKey('Item_Request', on_delete=models.CASCADE, db_constraint=True,related_name='material_requests')
#     mat_req_status = models.CharField(max_length=20, choices=[
#         ('Pending', 'Pending'),
#         ('Approved', 'Approved'),
#         ('Denied', 'Denied')
#     ], default='Pending')

#     def __str__(self):
#         return f"{self.item_req_num} {self.mat_req_qty}"

# class Item_Request(models.Model):
#     IR_STAT_CHOICES = [
#         ('Waiting', 'Waiting'),
#         ('Ongoing', 'Ongoing'),
#         ('Done', 'Done'),
#     ]
#     item_req_num = models.AutoField(primary_key=True)
#     item_req_approved_by = models.ForeignKey('Employee', on_delete=models.CASCADE, db_constraint=True, null=True, blank=True)
#     item_req_date_requested = models.DateField(default=now)
#     item_req_description = models.TextField(null=True, blank=True)
#     item_req_status = models.CharField(max_length=10, choices=IR_STAT_CHOICES, default='Waiting')
#     bus_unit_num = models.ForeignKey(Bus, on_delete=models.CASCADE, db_constraint=True)
#     mat_req_id = models.ForeignKey(Material_Requested, on_delete=models.SET_NULL, null=True, blank=True)
#     job_order = models.ForeignKey('JobOrder', on_delete=models.SET_NULL, null=True, blank=True, db_constraint=True)
#     mat_odr_id = models.ForeignKey(Material_Order, on_delete=models.SET_NULL, null=True, blank=True, db_constraint=True)

#     def __str__(self):
#         job_order_id = self.job_order.j_o_number if self.job_order else 'No Job Order'
#         return f"{self.item_req_num} - Job Order: {job_order_id}"


#     def update_status(self):
#         material_requests = self.material_requests.all()
#         total = material_requests.count()
#         resolved = material_requests.filter(mat_req_status__in=['Approved', 'Denied']).count()

#         if resolved == total and total > 0:
#             self.item_req_status = 'Done'
#         elif resolved > 0:
#             self.item_req_status = 'Ongoing'
#         else:
#             self.item_req_status = 'Waiting'

#         self.save()

# @receiver(post_save, sender=Material_Requested)
# def update_item_request_status(sender, instance, **kwargs):
#     if instance.item_req_num:
#         instance.item_req_num.update_status()

# class Acknowledgment_Receipt(models.Model):
#     status_choices = [ 
#         ('Pending', 'Pending'),
#         ('Ongoing', 'Ongoing'),
#         ('Delivered', 'Delivered'),
#     ]
#     ar_num = models.AutoField(primary_key=True)
#     ar_date_made = models.DateTimeField(default=now)
#     ar_date_received = models.DateField(null=True, blank=True)
#     ar_date_receiver = models.ForeignKey(Employee, on_delete=models.CASCADE,null=True, blank=True)
#     ar_status = models.CharField(max_length=20,choices=status_choices, default='Pending')
#     ar_note = models.TextField()
#     item_approved_id = models.ForeignKey('Material_Approved', on_delete=models.CASCADE, db_constraint=True)
    
# class Material_Approved(models.Model):
#     mat_approved_id = models.AutoField(primary_key=True)
#     mat_req_id = models.ForeignKey(Material_Requested, on_delete=models.CASCADE, related_name='approved_materials')
#     ir_num = models.ForeignKey(Item_Request, on_delete=models.CASCADE)
#     mat_approved_qty = models.PositiveIntegerField()  # Approved quantity
#     mat_approved_code = models.ForeignKey(Material, on_delete=models.SET_NULL,null=True,blank=True)  # Material code
#     date_approved = models.DateTimeField(auto_now_add=True)
#     ar_num = models.ForeignKey(Acknowledgment_Receipt, on_delete=models.CASCADE, null=True, blank=True)  
#     is_acknowledged = models.BooleanField(default=False)
#     def __str__(self):
#         return f"Approved Material: {self.mat_approved_code.mat_name} - {self.mat_approved_qty}"
    

# class Accounts(models.Model):
#     user_id = models.OneToOneField( 
#         'Employee', 
#         on_delete=models.CASCADE, 
#         db_constraint=True, 
#         primary_key=True
#     )
#     username = models.CharField(
#         max_length=150, 
#         unique=True, 
#         null=False, 
#         blank=False
#     )  # Adding a unique username field
#     password = models.CharField(max_length=128)  # Storing hashed passwords

#     def save(self, *args, **kwargs):
#         # Hash the password before saving
#         if not self.pk and self.password:  # Only hash if it's a new instance
#             self.password = make_password(self.password)
#         super().save(*args, **kwargs)

#     def __str__(self):  
#         return f"Username: {self.username}, User ID: {self.user_id}"


from django.db import models
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password
from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Bus(models.Model): 
    bus_unit_num = models.CharField(primary_key=True)
    bus_license_plate_number = models.CharField(max_length=10)
    bus_chassis_num = models.CharField(max_length=10)
    bus_engine_num = models.CharField(max_length=10)
    bus_year_model = models.IntegerField(null=True, blank=True)
    bus_tag_num = models.CharField(max_length=10)

    def __str__(self) -> str:
        return str(self.bus_unit_num) if self.bus_unit_num else "No Bus unit num"
    
class Material(models.Model):
    mat_code = models.AutoField(primary_key=True)  
    mat_name = models.CharField(max_length=200)
    mat_quantity = models.IntegerField()
    mat_brand = models.CharField(max_length=200, default='generic') 
    mat_measurement = models.CharField(max_length=200, null=True, blank=True)  
    mat_category = models.ForeignKey('Material_Category',on_delete=models.CASCADE,db_constraint=True)
    mat_max_request = models.PositiveIntegerField(null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.mat_name} ,{self.mat_code}, {self.mat_category}"
    
class Material_Category(models.Model):
    mat_category_id = models.AutoField(primary_key=True)
    mat_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.mat_name}"

class Department(models.Model):
    dept_id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=200)
    dept_descript = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.dept_id}, {self.dept_name}"
    
class Employee(models.Model):
    emp_id = models.AutoField(primary_key=True)
    emp_fname = models.CharField(max_length=100)
    emp_initial = models.CharField(max_length=1, null=True, blank=True)
    emp_lname = models.CharField(max_length=100)
    emp_suffix = models.CharField(max_length=10, null=True, blank=True)
    emp_date_of_birth = models.DateField()
    emp_sex = models.CharField(max_length=6)
    emp_address = models.CharField(max_length=200)
    emp_role = models.CharField(max_length=100, null=True, blank=True)
    emp_contact_num = models.CharField(max_length=11)
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE, db_constraint=True)
    emp_image = models.ImageField(upload_to='employee_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.emp_fname}, {self.emp_lname} ({self.dept_id.dept_name})"

class Purchase_Order_Status(models.Model):
    STATUS_CHOICES = [
        ('Waiting', 'Waiting'),
        ('Ongoing', 'Ongoing'),
        ('Done', 'Done'),
    ]
    postat_id = models.AutoField(primary_key=True)
    postat_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Waiting')

    def __str__(self):
        return self.postat_status
  
class Supplier(models.Model):
    sup_id = models.AutoField(primary_key=True)
    sup_name =models.CharField(max_length=300)
    sup_descript=models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.sup_name} "
    
class Material_Order_Category(models.Model):
    mat_odr_cat_id = models.AutoField(primary_key=True)
    mat_odr_cat_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.mat_odr_cat_name}"
    
def get_default_material_order_category():
    # Try to fetch the first category, or create a new one if none exists
    return Material_Order_Category.objects.first() or Material_Order_Category.objects.create(mat_odr_cat_name="Default Category")


class Purchase_Order(models.Model):
    po_num = models.AutoField(primary_key=True)
    po_approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    po_description = models.TextField(null=True, blank=True)
    po_datemade = models.DateField(default=now)
    postat_id = models.ForeignKey(Purchase_Order_Status, on_delete=models.SET_NULL, null=True, blank=True)
    sup_id = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"PO {self.po_num}"

class Material_Order(models.Model):
    mat_odr_id = models.AutoField(primary_key=True)
    mat_odr_name = models.CharField(max_length=100)
    mat_odr_qty = models.IntegerField()
    mat_odr_brand = models.CharField(max_length=100, null=True, blank=True, default='Generic')
    mat_odr_measurement = models.CharField(max_length=100,null=True, blank=True)
    mat_category = models.ForeignKey(Material_Category, on_delete=models.CASCADE)
    mat_odr_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Denied', 'Denied')], default='Pending')
    item_req_num = models.ForeignKey('Item_Request', on_delete=models.SET_NULL, null=True, blank=True, db_constraint=True)
    purchase_order = models.ForeignKey(Purchase_Order, on_delete=models.SET_NULL, null=True, blank=True, related_name="material_orders", db_constraint=True)
    linked_to_po = models.BooleanField(default=False) 
    
    def __str__(self):
        return f"{self.mat_odr_name}"
   
    

 

# class Material_Used(models.Model):
#     mat_used_id = models.AutoField(primary_key=True)
#     mat_used_name = models.CharField(max_length=200)
#     mat_used_qty = models.IntegerField()
#     mat_used_brand = models.CharField(max_length=200, null=True, blank=True)
#     mat_used_measurement =models.CharField(max_length=200, null=True, blank=True)

class Material_Used(models.Model):
    mat_used_id = models.AutoField(primary_key=True)
    mat_used_name = models.CharField(max_length=200)
    mat_used_qty = models.IntegerField()
    mat_used_brand = models.CharField(max_length=200, null=True, blank=True)
    mat_used_measurement =models.CharField(max_length=200, null=True, blank=True)
    mat_req_id = models.IntegerField(null=True, blank=True)  # Allows null values
    mat_odr = models.ForeignKey(Material_Order, on_delete=models.CASCADE, null=True, blank=True)


class JobOrder(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    j_o_number = models.AutoField(primary_key=True)
    j_o_date_requested = models.DateField(default=now)
    j_o_work_description = models.TextField()
    j_o_date_completed = models.DateField(null=True, blank=True)
    j_o_checked_by = models.ForeignKey(Employee, related_name='checked_by', on_delete=models.SET_NULL, null=True, blank=True)
    j_o_approved_by = models.ForeignKey(Employee, related_name='approved_by', on_delete=models.SET_NULL, null=True, blank=True)
    j_o_status =  models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    j_o_bus_unit_num = models.ForeignKey(Bus, on_delete=models.CASCADE)
    mat_used_id = models.ForeignKey(Material_Used,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return f"Job Order #{self.j_o_number} - {self.j_o_work_description[:30]}"  
    
class Material_Requested(models.Model):
    mat_req_id = models.AutoField(primary_key=True)
    mat_req_qty = models.PositiveIntegerField()
    mat_code = models.ForeignKey('Material', on_delete=models.CASCADE, db_constraint=True)
    item_req_num = models.ForeignKey('Item_Request', on_delete=models.CASCADE, db_constraint=True,related_name='material_requests')
    mat_req_status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Denied', 'Denied')
    ], default='Pending')

    def __str__(self):
        return f"{self.item_req_num} {self.mat_req_qty}"

class Item_Request(models.Model):
    IR_STAT_CHOICES = [
        ('Waiting', 'Waiting'),
        ('Ongoing', 'Ongoing'),
        ('Done', 'Done'),
    ]
    item_req_num = models.AutoField(primary_key=True)
    item_req_approved_by = models.ForeignKey('Employee', on_delete=models.CASCADE, db_constraint=True, null=True, blank=True)  # Make this field optional
    item_req_date_requested = models.DateField(default=now)
    item_req_description = models.TextField(null=True, blank=True)
    item_req_status =  models.CharField(max_length=10, choices=IR_STAT_CHOICES, default='Waiting')
    bus_unit_num = models.ForeignKey(Bus, on_delete=models.CASCADE, db_constraint=True)
    mat_req_id = models.ForeignKey(Material_Requested, on_delete=models.SET_NULL, null=True, blank=True)
    job_order = models.ForeignKey('JobOrder', on_delete=models.SET_NULL, null=True, blank=True, db_constraint=True)
    mat_odr_id = models.ForeignKey(Material_Order, on_delete=models.SET_NULL, null=True, blank=True, db_constraint=True)

    def __str__(self): 
        return f"{self.item_req_num} - {self.bus_unit_num}"

    def update_status(self):
        material_requests = self.material_requests.all()
        total = material_requests.count()
        resolved = material_requests.filter(mat_req_status__in=['Approved', 'Denied']).count()

        if resolved == total and total > 0:
            self.item_req_status = 'Done'
        elif resolved > 0:
            self.item_req_status = 'Ongoing'
        else:
            self.item_req_status = 'Waiting'

        self.save()

@receiver(post_save, sender=Material_Requested)
def update_item_request_status(sender, instance, **kwargs):
    if instance.item_req_num:
        instance.item_req_num.update_status()

class Acknowledgment_Receipt(models.Model):
    status_choices = [ 
        ('Pending', 'Pending'),
        ('Ongoing', 'Ongoing'),
        ('Delivered', 'Delivered'),
    ]
    ar_num = models.AutoField(primary_key=True)
    ar_date_made = models.DateTimeField(default=now)
    ar_date_received = models.DateField(null=True, blank=True)
    ar_date_receiver = models.ForeignKey(Employee, on_delete=models.CASCADE,null=True, blank=True)
    ar_status = models.CharField(max_length=20,choices=status_choices, default='Pending')
    ar_note = models.TextField()
    item_approved_id = models.ForeignKey('Material_Approved', on_delete=models.CASCADE, db_constraint=True)
    
class Material_Approved(models.Model):
    mat_approved_id = models.AutoField(primary_key=True)
    mat_req_id = models.ForeignKey(Material_Requested, on_delete=models.CASCADE, related_name='approved_materials')
    ir_num = models.ForeignKey(Item_Request, on_delete=models.CASCADE)
    mat_approved_qty = models.PositiveIntegerField()  # Approved quantity
    mat_approved_code = models.ForeignKey(Material, on_delete=models.SET_NULL,null=True,blank=True)  # Material code
    date_approved = models.DateTimeField(auto_now_add=True)
    ar_num = models.ForeignKey(Acknowledgment_Receipt, on_delete=models.CASCADE, null=True, blank=True)  
    is_acknowledged = models.BooleanField(default=False)
    def __str__(self):
        return f"Approved Material: {self.mat_approved_code.mat_name} - {self.mat_approved_qty}"
    
class Accounts(models.Model):
    user_id = models.OneToOneField( 
        'Employee', 
        on_delete=models.CASCADE, 
        db_constraint=True, 
        primary_key=True
    )
    username = models.CharField(
        max_length=150, 
        unique=True, 
        null=False, 
        blank=False
    )  # Adding a unique username field
    password = models.CharField(max_length=128)  # Storing hashed passwords

    def save(self, *args, **kwargs):
        # Hash the password before saving
        if not self.pk and self.password:  # Only hash if it's a new instance
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):  
        return f"Username: {self.username}, User ID: {self.user_id}"