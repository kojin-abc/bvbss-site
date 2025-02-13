from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import Game

class LoginForm(AuthenticationForm):
    def __init__(self, request = ..., *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class GameForm(forms.Form):
    opp_name= forms.CharField(label='対戦相手', widget=forms.TextInput(attrs={'class':'form-control'}), \
            min_length=1, max_length=10)

class GameResultForm(forms.Form):
    score0_0 = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','style':"text-align:center"}), \
                                max_value = 5, min_value=0, label=None)
    score0_1 = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','style':"text-align:center"}), \
                                max_value = 5, min_value=0, label=None)
    score1_0 = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','style':"text-align:center"}), \
                                max_value = 99, min_value=0, label=None)
    score1_1 = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','style':"text-align:center"}), \
                                max_value = 99, min_value=0, label=None)
    score2_0 = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','style':"text-align:center"}), \
                                max_value = 99, min_value=0, label=None, required=False)
    score2_1 = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','style':"text-align:center"}), \
                                max_value = 99, min_value=0, label=None, required=False)
    score3_0 = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','style':"text-align:center"}), \
                                max_value = 99, min_value=0, label=None, required=False)
    score3_1 = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','style':"text-align:center"}), \
                                max_value = 99, min_value=0, label=None, required=False)
    score4_0 = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','style':"text-align:center"}), \
                                max_value = 99, min_value=0, label=None, required=False)
    score4_1 = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','style':"text-align:center"}), \
                                max_value = 99, min_value=0, label=None, required=False)
    score5_0 = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','style':"text-align:center"}), \
                                max_value = 99, min_value=0, label=None, required=False)
    score5_1 = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','style':"text-align:center"}), \
                                max_value = 99, min_value=0, label=None, required=False)
    
class ServeForm(forms.Form):
    serve_label = ""
    serve_0 = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','style':"text-align:center"}), \
                                max_value = 99, min_value=0, label=None)
    serve_1 = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','style':"text-align:center"}), \
                                max_value = 99, min_value=0, label=None)
    serve_2 = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','style':"text-align:center"}), \
                                max_value = 99, min_value=0, label=None)
    serve_3 = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','style':"text-align:center"}), \
                                max_value = 99, min_value=0, label=None)
    serve_4 = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','style':"text-align:center"}), \
                                max_value = 99, min_value=0, label=None)
    serve_5 = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','style':"text-align:center"}), \
                                max_value = 99, min_value=0, label=None)
    
class TermForm(forms.Form):
    from_date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','style':"text-align:center"}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','style':"text-align:center"}))

