from django import forms
from shared.models import *
from django.core.exceptions import ValidationError
from datetime import date

# class EmployeeForm(forms.ModelForm):  # For adding employees
#     class Meta:
#         model = Employee
#         fields = [
#             'emp_fname', 'emp_lname', 'emp_initial', 'emp_suffix',
#             'emp_date_of_birth', 'emp_sex', 'emp_address',
#             'emp_contact_num', 'emp_role', 'dept_id', 'emp_image'
#         ]
#         widgets = {
#             'emp_fname': forms.TextInput(attrs={'placeholder': 'Enter first name'}),
#             'emp_lname': forms.TextInput(attrs={'placeholder': 'Enter last name'}),
#             'emp_initial': forms.TextInput(attrs={'placeholder': 'Optional: Middle Initial'}),
#             'emp_suffix': forms.TextInput(attrs={'placeholder': 'Optional: Suffix'}),
#             'emp_date_of_birth': forms.DateInput(
#                 attrs={
#                     'type': 'date',
#                     'onfocus': "setDefaultDate(this)"  # Add a JavaScript function
#                 }
#             ),

#             'emp_sex': forms.Select(choices=[
#                 ('', 'Select...'),
#                 ('Male', 'Male'),
#                 ('Female', 'Female')
#             ]),
#             'emp_address': forms.TextInput(attrs={'placeholder': 'Enter address'}),
#             'emp_contact_num': forms.TextInput(attrs={'placeholder': 'Enter contact number'}),
#             'emp_role': forms.TextInput(attrs={'placeholder': 'Optional: Role'}),
#             'dept_id': forms.Select(attrs={'placeholder': 'Select department'}),
#             'emp_image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
#         }

class EmployeeForm(forms.ModelForm):  # For adding employees
    class Meta:
        model = Employee
        fields = [
            'emp_fname', 'emp_lname', 'emp_initial', 'emp_suffix',
            'emp_date_of_birth', 'emp_sex', 'emp_address',
            'emp_contact_num', 'emp_role', 'dept_id', 'emp_image'
        ]
        widgets = {
            'emp_fname': forms.TextInput(attrs={'placeholder': 'Enter first name'}),
            'emp_lname': forms.TextInput(attrs={'placeholder': 'Enter last name'}),
            'emp_initial': forms.TextInput(attrs={'placeholder': 'Optional: Middle Initial'}),
            'emp_suffix': forms.TextInput(attrs={'placeholder': 'Optional: Suffix'}),
            'emp_date_of_birth': forms.DateInput(
                attrs={'type': 'date', 'onfocus': "setDefaultDate(this)"}
            ),
            'emp_sex': forms.Select(choices=[
                ('', 'Select...'),
                ('Male', 'Male'),
                ('Female', 'Female')
            ]),
            'emp_address': forms.TextInput(attrs={'placeholder': 'Enter address'}),
            'emp_contact_num': forms.TextInput(attrs={'placeholder': 'Enter contact number'}),
            'emp_role': forms.TextInput(attrs={'placeholder': 'Optional: Role'}),
            'dept_id': forms.Select(attrs={'placeholder': 'Select department'}),
            'emp_image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

    def clean_emp_date_of_birth(self):
        emp_date_of_birth = self.cleaned_data.get('emp_date_of_birth')
        if emp_date_of_birth and emp_date_of_birth > date.today():
            raise forms.ValidationError("Date of birth cannot be in the future.")
        return emp_date_of_birth

class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = [
            'bus_unit_num',
            'bus_license_plate_number',
            'bus_chassis_num',
            'bus_engine_num',
            'bus_year_model',
            'bus_tag_num',
        ]

    def __init__(self, *args, **kwargs):
        edit_mode = kwargs.pop('edit_mode', False)
        super().__init__(*args, **kwargs)

        if edit_mode:
            # Make bus_unit_num readonly during edit
            self.fields['bus_unit_num'].widget.attrs['readonly'] = True
            self.fields['bus_unit_num'].required = False
            self.fields['bus_unit_num'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        else:
            # Ensure bus_unit_num is required when adding
            self.fields['bus_unit_num'].required = True

    def clean_bus_unit_num(self):
        bus_unit_num = self.cleaned_data.get('bus_unit_num')

        if not bus_unit_num:
            raise ValidationError("Bus Unit Number is required.")

        if not self.instance.pk:
            # Adding a new bus, ensure uniqueness
            if Bus.objects.filter(bus_unit_num=bus_unit_num).exists():
                raise ValidationError("Bus Unit Number must be unique.")
        else:
            # Editing, ensure uniqueness excluding current instance
            if Bus.objects.filter(bus_unit_num=bus_unit_num).exclude(pk=self.instance.pk).exists():
                raise ValidationError("Bus Unit Number must be unique.")

        return bus_unit_num

    def clean(self):
        cleaned_data = super().clean()

        if self.instance and self.instance.pk:
            # Skip uniqueness check for bus_unit_num if editing
            cleaned_data.pop('bus_unit_num', None)

        # Check for negative numbers in bus_year_model or other fields if needed
        bus_year_model = cleaned_data.get('bus_year_model')

        if bus_year_model and bus_year_model < 0:
            self.add_error('bus_year_model', "Bus Year Model cannot be negative.")

        license_plate = cleaned_data.get('bus_license_plate_number')
        chassis_num = cleaned_data.get('bus_chassis_num')
        engine_num = cleaned_data.get('bus_engine_num')
        tag_num = cleaned_data.get('bus_tag_num')

        # Check for uniqueness of other fields
        if license_plate and Bus.objects.filter(bus_license_plate_number=license_plate).exclude(pk=self.instance.pk).exists():
            self.add_error('bus_license_plate_number', "License Plate Number must be unique.")
        if chassis_num and Bus.objects.filter(bus_chassis_num=chassis_num).exclude(pk=self.instance.pk).exists():
            self.add_error('bus_chassis_num', "Chassis Number must be unique.")
        if engine_num and Bus.objects.filter(bus_engine_num=engine_num).exclude(pk=self.instance.pk).exists():
            self.add_error('bus_engine_num', "Engine Number must be unique.")
        if tag_num and Bus.objects.filter(bus_tag_num=tag_num).exclude(pk=self.instance.pk).exists():
            self.add_error('bus_tag_num', "Tag Number must be unique.")

        return cleaned_data



class AccountsForm(forms.ModelForm):
    class Meta:
        model = Accounts
        fields = ['user_id', 'username', 'password']

    def __init__(self, *args, **kwargs):
        # Fetch the current user_id from kwargs if available
        self.current_user_id = kwargs.pop('current_user_id', None)
        super().__init__(*args, **kwargs)

        # Get all employees who don't have accounts
        existing_accounts = Accounts.objects.all().values_list('user_id', flat=True)
        available_employees = Employee.objects.exclude(emp_id__in=existing_accounts)

        # Add the current user_id back to the queryset if it exists
        if self.current_user_id:
            available_employees = available_employees | Employee.objects.filter(emp_id=self.current_user_id)

        # Filter employees to only include those in allowed departments
        allowed_departments = ['I.T. Department', 'Finance Department', 'Vehicle Maintenance Department', 'Transportation Department']
        
        # Filter the employees by department name in the Department model
        # This will check the dept_name field in Department through the ForeignKey
        available_employees = available_employees.filter(dept_id__dept_name__in=allowed_departments)

        # Populate the user_id dropdown with filtered employees
        self.fields['user_id'].queryset = available_employees

    def clean_user_id(self):
        user_id = self.cleaned_data.get('user_id')
        if not user_id:
            raise forms.ValidationError("Please select a valid employee.")
        return user_id


class DateFilterForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))