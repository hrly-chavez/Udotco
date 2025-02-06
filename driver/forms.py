from django import forms
from shared.models import JobOrder

class JobOrderForm(forms.ModelForm):
    class Meta:
        model = JobOrder
        fields = [
            'j_o_date_requested',
            'j_o_work_description',
            'j_o_bus_unit_num',
        ]
        widgets = {
            'j_o_date_requested': forms.DateInput(attrs={'type': 'date', 'readonly': 'readonly'}),
            'j_o_work_description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['j_o_date_requested'].required = False  # Make it not required if read-only

   