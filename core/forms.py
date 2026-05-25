from django import forms
from publicacoes.models import Publicacao, MensagemPublicacao
from usuarios.models import Usuario


def aplicar_bootstrap(form):
    for field in form.fields.values():
        widget = field.widget

        if isinstance(widget, forms.CheckboxInput):
            widget.attrs.update({
                'class': 'form-check-input'
            })

        elif isinstance(widget, forms.Select):
            widget.attrs.update({
                'class': 'form-select'
            })

        else:
            widget.attrs.update({
                'class': 'form-control'
            })


class CadastroClienteForm(forms.Form):
    username = forms.CharField(label='Usuário', max_length=150)
    email = forms.EmailField(label='E-mail')

    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput
    )

    password_confirm = forms.CharField(
        label='Confirmar senha',
        widget=forms.PasswordInput
    )

    empresa = forms.CharField(label='Empresa', max_length=100)
    cnpj = forms.CharField(label='CNPJ', max_length=18)

    telefone_empresa = forms.CharField(
        label='Telefone da empresa',
        max_length=20,
        required=False
    )

    representante = forms.CharField(
        label='Seu nome / Representante',
        max_length=100
    )

    celular = forms.CharField(
        label='Celular',
        max_length=20,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_bootstrap(self)

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError('Este usuário já está em uso.')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está em uso.')

        return email

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_bootstrap(self)


class MateriaFormatadaForm(forms.ModelForm):
    class Meta:
        model = Publicacao
        fields = ['arquivo_formatado']

        labels = {
            'arquivo_formatado': 'Matéria formatada',
        }

        widgets = {
            'arquivo_formatado': forms.FileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_bootstrap(self)


class MensagemPublicacaoForm(forms.ModelForm):
    class Meta:
        model = MensagemPublicacao
        fields = ['texto']

        labels = {
            'texto': 'Mensagem',
        }

        widgets = {
            'texto': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_bootstrap(self)


class NovaPublicacaoForm(forms.ModelForm):
    class Meta:
        model = Publicacao
        fields = ['titulo', 'jornal', 'arquivo']

        labels = {
            'titulo': 'Título',
            'jornal': 'Jornal desejado',
            'arquivo': 'Texto',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_bootstrap(self)


class AdminPublicacaoForm(forms.ModelForm):
    class Meta:
        model = Publicacao
        fields = [
            'titulo',
            'funcionario_responsavel',
            'jornal',
            'data_publicacao',
            'tamanho',
            'valor',
        ]

        labels = {
            'titulo': 'Título',
            'funcionario_responsavel': 'Funcionário responsável',
            'jornal': 'Jornal',
            'data_publicacao': 'Data da publicação',
            'tamanho': 'Tamanho da publicação',
            'valor': 'Valor',
        }

        widgets = {
            'data_publicacao': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['funcionario_responsavel'].queryset = Usuario.objects.filter(
            tipo_usuario='funcionario',
            is_active=True
        )

        aplicar_bootstrap(self)


class MinhaContaForm(forms.Form):
    email = forms.EmailField(label='E-mail', required=False)

    telefone_empresa = forms.CharField(
        label='Telefone da empresa',
        max_length=20,
        required=False
    )

    celular = forms.CharField(
        label='Celular do representante',
        max_length=20,
        required=False
    )

    def __init__(self, *args, usuario=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.usuario = usuario

        if usuario:
            self.fields['email'].initial = usuario.email
            self.fields['celular'].initial = usuario.celular

            if usuario.empresa:
                self.fields['telefone_empresa'].initial = usuario.empresa.telefone

        aplicar_bootstrap(self)

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email and Usuario.objects.exclude(id=self.usuario.id).filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está em uso.')

        return email

    def save(self):
        usuario = self.usuario

        usuario.email = self.cleaned_data.get('email')
        usuario.celular = self.cleaned_data.get('celular')
        usuario.save()

        if usuario.empresa:
            usuario.empresa.telefone = self.cleaned_data.get('telefone_empresa')
            usuario.empresa.save()

        return usuario