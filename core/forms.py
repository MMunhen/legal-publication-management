from django import forms
from publicacoes.models import Publicacao, MensagemPublicacao
from usuarios.models import Usuario


class CadastroClienteForm(forms.Form):
    username = forms.CharField(label='Usuário', max_length=150)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Confirmar senha', widget=forms.PasswordInput)

    empresa = forms.CharField(label='Empresa', max_length=100)
    cnpj = forms.CharField(label='CNPJ', max_length=18)
    telefone = forms.CharField(label='Telefone', max_length=20, required=False)
    representante = forms.CharField(label='Representante', max_length=100)

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('As senhas não coincidem.')

        return cleaned_data
    
class StatusPublicacaoForm(forms.ModelForm):
    class Meta:
        model = Publicacao
        fields = ['status']


class MateriaFormatadaForm(forms.ModelForm):
    class Meta:
        model = Publicacao
        fields = ['arquivo_formatado']


class MensagemPublicacaoForm(forms.ModelForm):
    class Meta:
        model = MensagemPublicacao
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 3})
        }

class NovaPublicacaoForm(forms.ModelForm):
    class Meta:
        model = Publicacao
        fields = ['titulo', 'jornal', 'arquivo']

        labels = {
            'titulo': 'Título',
            'jornal': 'Jornal desejado',
            'arquivo': 'Texto',
        }


class AdminPublicacaoForm(forms.ModelForm):
    class Meta:
        model = Publicacao
        fields = [
            'titulo',
            'funcionario_responsavel',
            'jornal',
            'data_publicacao',
            'valor_definido',
            'valor',
        ]

        labels = {
            'titulo': 'Título',
            'funcionario_responsavel': 'Funcionário responsável',
            'jornal': 'Jornal',
            'data_publicacao': 'Data da publicação',
            'valor_definido': 'Valor definido',
            'valor': 'Valor',
        }

        widgets = {
            'data_publicacao': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['funcionario_responsavel'].queryset = Usuario.objects.filter(
            tipo_usuario__in=['funcionario']
        )