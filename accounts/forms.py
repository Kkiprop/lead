from django import forms

class EmailForm(forms.Form):
    to_email = forms.CharField(
        label='Recipient Email',
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'investor@example.com, founder@fund.com'}),
        help_text='Use one email or separate multiple addresses with commas.',
    )
    subject = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea)

    def clean_to_email(self):
        raw_value = self.cleaned_data['to_email']
        recipients = [item.strip() for item in raw_value.replace(';', ',').split(',') if item.strip()]
        if not recipients:
            raise forms.ValidationError('Enter at least one recipient email address.')

        validator = forms.EmailField().clean
        for recipient in recipients:
            validator(recipient)

        return recipients


class InvestorSearchForm(forms.Form):
    query = forms.CharField(
        label='Search investors',
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Try: Venture capital firms in Nairobi',
            }
        ),
    )


class DashboardEmailForm(forms.Form):
    subject = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 8}))
