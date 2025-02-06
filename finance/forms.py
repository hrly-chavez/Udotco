# from django import forms
# from django.core.exceptions import ValidationError
# from shared.models import *

# class MaterialForm(forms.ModelForm):
#     class Meta:
#         model = Material
#         fields = ['mat_name', 'mat_quantity', 'mat_brand', 'mat_measurement', 'mat_category','mat_max_request']
#         labels = {
#             'mat_name' : 'Name',
#             'mat_quantity' : 'Quantity',
#             'mat_brand' :   'Brand',
#             'mat_measurement' : 'Measurement',
#             'mat_category' : 'Category',
#             'mat_max_request': 'Max Requestion',
#         }
#         widgets = {
#             'mat_measurement': forms.TextInput(attrs={'placeholder': 'Optional: Measurement'}),
#             'mat_name': forms.TextInput(attrs={'placeholder': 'Enter material name'}),
#             'mat_quantity': forms.NumberInput(attrs={'placeholder': 'Enter quantity'}),
#             'mat_category': forms.Select(attrs={'placeholder': 'Select Material Category'}),
#             'mat_max_request': forms.NumberInput(attrs={'placeholder':'Optional: Enter Value for Max Requesition'}) 
#         }

#     def clean_mat_quantity(self):
#         mat_quantity = self.cleaned_data.get('mat_quantity')
#         if mat_quantity <= 0:
#             raise ValidationError("* The quantity you entered is invalid. Please input a value of 1 or higher.")
#         return mat_quantity
    
    
# class MaterialOrderForm(forms.ModelForm):
#     class Meta:
#         model = Material_Order
#         fields = ['mat_odr_name', 'mat_odr_qty', 'mat_odr_brand', 'mat_odr_measurement']
#         labels = {
#             'mat_odr_name': 'Item Name',
#             'mat_odr_qty': 'Quantity',
#             'mat_odr_brand': 'Brand',
#             'mat_odr_measurement': 'Measurement / Size',
            
#         }
#         widgets = {
#             'mat_odr_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'mat_odr_qty': forms.NumberInput(attrs={'class': 'form-control'}),
#             'mat_odr_brand': forms.TextInput(attrs={'class': 'form-control'}),
#             'mat_odr_measurement': forms.TextInput(attrs={'class': 'form-control'}),
            
#         }

#     # Custom validation for 'mat_odr_qty' (Quantity)
#     def clean_mat_odr_qty(self):
#         quantity = self.cleaned_data.get('mat_odr_qty')

#         # Check if the quantity is less than or equal to 0
#         if quantity is None or quantity <= 0:
#             raise ValidationError(
#                 "The quantity you entered is invalid. Please input a value of 1 or higher."
#             )

#         return quantity



# class PurchaseOrderForm(forms.ModelForm):
#     class Meta:
#         model = Purchase_Order
#         fields = ['po_description', 'po_datemade', 'postat_id', 'sup_id', 'po_approved_by']
#         labels = {
#             'po_description': 'Description',
#             'po_datemade': 'Date Created',
#             'postat_id': 'Status',
#             'sup_id': 'Supplier',
#             'po_approved_by': 'Approved By',
#         }
#         widgets = {
#             'po_description': forms.Textarea(attrs={'class': 'form-control'}),
#             'po_datemade': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#             'postat_id': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),  # Make read-only in the UI
#             'sup_id': forms.Select(attrs={'class': 'form-control'}),
#             'po_approved_by': forms.Select(attrs={'class': 'form-control'}),
#         }

# class DateFilterForm(forms.Form):
#     start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))


# class MaterialRequestApprovalForm(forms.ModelForm):
#     class Meta:
#         model = Material_Requested
#         fields = ['mat_req_qty', 'mat_code']  

# class AcknowledgmentReceiptForm(forms.ModelForm):
#     item_approved_id = forms.ModelChoiceField(
#         queryset=Material_Approved.objects.select_related('mat_approved_code'),
#         widget=forms.Select(attrs={'class': 'form-control select2'}),
#         label="Approved Item"
#     )

#     class Meta:
#         model = Acknowledgment_Receipt
#         fields = ['ar_note', 'item_approved_id']  # Exclude ar_date_received, ar_date_receiver, and ar_status
#         labels = {
#             'ar_note': 'Note',
#             'item_approved_id': 'Approved Item',
#         }
#         widgets = {
#             'ar_note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['item_approved_id'].queryset = Material_Approved.objects.filter(
#             mat_req_id__mat_req_status='Approved'  # Ensure this condition matches your approval logic
#         ).select_related('mat_approved_code')
#         self.fields['item_approved_id'].label_from_instance = lambda obj: f"{obj.mat_approved_code.mat_name} - Quantity: {obj.mat_approved_qty}"


from django import forms
from django.core.exceptions import ValidationError
from shared.models import *
from django.forms import modelformset_factory
class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['mat_name', 'mat_quantity', 'mat_brand', 'mat_measurement', 'mat_category','mat_max_request']
        labels = {
            'mat_name' : 'Name',
            'mat_quantity' : 'Quantity',
            'mat_brand' :   'Brand',
            'mat_measurement' : 'Measurement',
            'mat_category' : 'Category',
            'mat_max_request': 'Max Requestion',
        }
        widgets = {
            'mat_measurement': forms.TextInput(attrs={'placeholder': 'Optional: Measurement'}),
            'mat_name': forms.TextInput(attrs={'placeholder': 'Enter material name'}),
            'mat_quantity': forms.NumberInput(attrs={'placeholder': 'Enter quantity'}),
            'mat_category': forms.Select(attrs={'placeholder': 'Select Material Category'}),
            'mat_max_request': forms.NumberInput(attrs={'placeholder':'Optional: Enter Value for Max Requesition'}) 
        }

    def clean_mat_quantity(self):
        mat_quantity = self.cleaned_data.get('mat_quantity')
        if mat_quantity <= 0:
            raise ValidationError("* The quantity you entered is invalid. Please input a value of 1 or higher.")
        return mat_quantity
    
class MaterialOrderForm(forms.ModelForm):

    class Meta:
        model = Material_Order
        fields = ['mat_odr_name', 'mat_odr_qty', 'mat_odr_brand', 'mat_odr_measurement', 'mat_category']
        labels = {
            'mat_odr_name': 'Item Name',
            'mat_odr_qty': 'Quantity',
            'mat_odr_brand': 'Brand',
            'mat_odr_measurement': 'Measurement / Size',
            'mat_category': 'Category',
        }
        widgets = {
            'mat_odr_name' : forms.TextInput(attrs={'class': 'form-control'}),
            'mat_odr_qty': forms.NumberInput(attrs={'class': 'form-control'}),
            'mat_odr_brand': forms.TextInput(attrs={'class': 'form-control'}),
            'mat_odr_measurement': forms.TextInput(attrs={'class': 'form-control'}),
            'mat_category': forms.Select(attrs={'class': 'form-control'}),
        }


    # Custom validation for 'mat_odr_qty' (Quantity)
    def clean_mat_odr_qty(self):
        quantity = self.cleaned_data.get('mat_odr_qty')

        if quantity is None or quantity <= 0:
            raise ValidationError(
                "The quantity you entered is invalid. Please input a value of 1 or higher."
            )

        return quantity
MaterialOrderFormSet = modelformset_factory(
    Material_Order,
    form=MaterialOrderForm,
    extra=1,  # Number of extra forms displayed
    can_delete=True,
)


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = Purchase_Order 
        fields = ['po_description', 'po_datemade', 'postat_id', 'sup_id', 'po_approved_by']
        labels = {
            'po_description': 'Description',
            'po_datemade': 'Date Created',
            'postat_id': 'Status',
            'sup_id': 'Supplier',
            'po_approved_by': 'Approved By',
        }
        widgets = {
            'po_description': forms.Textarea(attrs={'class': 'form-control'}),
            'po_datemade': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),    
            'postat_id': forms.HiddenInput(),   
            'sup_id': forms.Select(attrs={'class': 'form-control'}),
            'po_approved_by': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Pre-set the default status to "Waiting"
        if not self.instance.pk:  # Only set this for new instances
            self.fields['postat_id'].initial = Purchase_Order_Status.objects.get(postat_status="Waiting")
            
        # Filter employees to show only those in the Finance Department or with the role 'Operational Manager'
        self.fields['po_approved_by'].queryset = Employee.objects.filter(
            models.Q(dept_id__dept_name='Finance Department') | models.Q(emp_role='Operational Manager')
        )

    

class DateFilterForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

class MaterialRequestApprovalForm(forms.ModelForm):
    class Meta:
        model = Material_Requested
        fields = ['mat_req_qty', 'mat_code']  

class AcknowledgmentReceiptForm(forms.ModelForm):
        item_approved_id = forms.ModelChoiceField(
            queryset=Material_Approved.objects.select_related('mat_approved_code'),
            widget=forms.Select(attrs={'class': 'form-control select2'}),
            label="Approved Item"
        )

        class Meta:
            model = Acknowledgment_Receipt
            fields = ['ar_note', 'item_approved_id']  # Exclude ar_date_received, ar_date_receiver, and ar_status
            labels = {
                'ar_note': 'Note',
                'item_approved_id': 'Approved Item',
            }
            widgets = {
                'ar_note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['item_approved_id'].queryset = Material_Approved.objects.filter(
                mat_req_id__mat_req_status='Approved'  # Ensure this condition matches your approval logic
            ).select_related('mat_approved_code')
            self.fields['item_approved_id'].label_from_instance = lambda obj: f"{obj.mat_approved_code.mat_name} - Quantity: {obj.mat_approved_qty}"
