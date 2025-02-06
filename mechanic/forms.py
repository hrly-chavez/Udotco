from django import forms
import json
from django.core.exceptions import ValidationError
from shared.models import *

# Form for Item Request details
class ItemRequestForm(forms.ModelForm):
    class Meta:
        model = Item_Request
        fields = [
            'item_req_approved_by',
            'item_req_date_requested',
            'item_req_description',
            'item_req_status',
            'bus_unit_num',  # Bus unit field
        ]
        labels = {
            'item_req_approved_by': 'Approved By',
            'item_req_date_requested': 'Date Requested',
            'item_req_description': 'Description',
            'item_req_status': 'Status',
            'bus_unit_num': 'Bus Unit',
        }
        widgets = {
            'item_req_approved_by': forms.Select(attrs={'class': 'form-select', 'readonly': True}),
            'item_req_date_requested': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'item_req_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'item_req_status': forms.Select(attrs={'class': 'form-select', 'disabled': 'disabled'}),  # Disabled for read-only
            'bus_unit_num': forms.Select(attrs={'class': 'form-select', 'disabled': 'disabled'}),  # Disabled for read-only
        }

    def __init__(self, *args, **kwargs):
        job_order = kwargs.pop('job_order', None)
        super(ItemRequestForm, self).__init__(*args, **kwargs)

        # Set default value for item_req_status
        self.fields['item_req_status'].initial = 'Waiting'
        self.fields['item_req_status'].required = False  # Make sure the field is not required in the form

        if job_order:
            # Prepopulate the bus_unit_num field with the actual Bus object from the job order
            self.fields['bus_unit_num'].initial = job_order.j_o_bus_unit_num  # Using the Bus object here
            self.fields['bus_unit_num'].queryset = Bus.objects.filter(bus_unit_num=job_order.j_o_bus_unit_num.bus_unit_num)

            # Prepopulate item_req_approved_by with the mechanic assigned to the job order
            if job_order.j_o_checked_by:
                self.fields['item_req_approved_by'].initial = job_order.j_o_checked_by


        # Optional: Add a fallback to include all employees if no 'Manager' found
        if not self.fields['item_req_approved_by'].queryset.exists():
            self.fields['item_req_approved_by'].queryset = Employee.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        materials = self.data.get('materials', '[]')
        materials = json.loads(materials)

        for material in materials:
            material_id = material["material_id"]
            requested_qty = int(material["quantity"])

            try:
                material_instance = Material.objects.get(pk=material_id)
            except Material.DoesNotExist:
                raise ValidationError(f"Material with ID {material_id} does not exist.")

            # Validate against available quantity
            if requested_qty > material_instance.mat_quantity:
                raise ValidationError(
                    f"Requested quantity for material {material_instance.mat_name} exceeds available stock ({material_instance.mat_quantity})."
                )

            # Validate against max requestable quantity
            if requested_qty > material_instance.mat_max_request:
                raise ValidationError(
                    f"Requested quantity for material {material_instance.mat_name} exceeds maximum requestable limit ({material_instance.mat_max_request})."
                )

        return cleaned_data