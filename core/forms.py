# hakaton2025/core/forms.py

from django import forms
from .models import ReuniaoAcessivel, AnaliseFeedback

class ReuniaoForm(forms.ModelForm):
    class Meta:
        model = ReuniaoAcessivel
        fields = ['titulo', 'data_reuniao', 'arquivo_audio', 'participantes']
        widgets = {
            'data_reuniao': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Daily de Planejamento'}),
            'arquivo_audio': forms.FileInput(attrs={'class': 'form-control'}),
            'participantes': forms.SelectMultiple(attrs={'class': 'form-control'})
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = AnaliseFeedback
        fields = ['texto_original']
        widgets = {
            'texto_original': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4,
                'placeholder': 'Digite o feedback aqui para análise de viés...',
                # Atributos HTMX para "mágica" em tempo real:
                'hx-post': '/checar-feedback/',  # Chama a URL de análise
                'hx-trigger': 'keyup changed delay:1s',  # Espera 1s após parar de digitar
                'hx-target': '#resultado-analise',  # Onde o resultado vai aparecer
                'hx-swap': 'innerHTML'
            })
        }

        # Adicione esta classe no final do arquivo core/forms.py

class TradutorForm(forms.Form):
    texto_complexo = forms.CharField(
        label="Cole o texto difícil aqui (E-mail, Comunicado, etc)",
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 5, 
            'placeholder': 'Ex: Prezado time, o budget para o Q3 sofreu um churn...'
        })
    )