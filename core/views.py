from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from publicacoes.models import Publicacao, MensagemPublicacao
from usuarios.models import Usuario, Empresa
from .forms import CadastroClienteForm, StatusPublicacaoForm, MateriaFormatadaForm, MensagemPublicacaoForm, NovaPublicacaoForm, AdminPublicacaoForm, MinhaContaForm 
from django.contrib import messages


def home(request):
    return render(request, 'core/home.html')

@login_required
def dashboard(request):
    usuario = request.user
    nova_publicacao_form = None
    status_filtro = request.GET.get('status')

    if usuario.tipo_usuario == 'admin':
        publicacoes = Publicacao.objects.all()

    elif usuario.tipo_usuario == 'funcionario':
        publicacoes = Publicacao.objects.filter(
            funcionario_responsavel=usuario
        )

    else:
        publicacoes = Publicacao.objects.filter(
            cliente=usuario.empresa
        )

        nova_publicacao_form = NovaPublicacaoForm()

        if request.method == 'POST':
            acao = request.POST.get('acao')

            if acao == 'nova_publicacao':
                nova_publicacao_form = NovaPublicacaoForm(
                    request.POST,
                    request.FILES
                )

                if nova_publicacao_form.is_valid():
                    publicacao = nova_publicacao_form.save(commit=False)
                    publicacao.cliente = usuario.empresa
                    publicacao.status = 'pendente'
                    publicacao.save()

                    return redirect('detalhe_publicacao', id=publicacao.id)
    
    if status_filtro:
        publicacoes = publicacoes.filter(status=status_filtro)

    return render(request, 'core/dashboard.html', {
        'publicacoes': publicacoes,
        'nova_publicacao_form': nova_publicacao_form,
        'status_filtro': status_filtro,
        'status_opcoes': Publicacao.STATUS,
    })

def cadastro_cliente(request):
    if request.method == 'POST':
        form = CadastroClienteForm(request.POST)

        if form.is_valid():
            cnpj = form.cleaned_data['cnpj']

            empresa, criada = Empresa.objects.get_or_create(
                cnpj=cnpj,
                defaults={
                    'nome': form.cleaned_data['empresa'],
                    'telefone': form.cleaned_data['telefone_empresa'],
                }
            )

            Usuario.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                tipo_usuario='cliente',
                empresa=empresa,
                representante=form.cleaned_data['representante'],
                celular=form.cleaned_data['celular'],
                is_active=True,
                is_staff=False,
            )

            return redirect('login')

    else:
        form = CadastroClienteForm()

    return render(request, 'core/cadastro.html', {'form': form})

@login_required
def detalhe_publicacao(request, id):
    publicacao = get_object_or_404(Publicacao, id=id)
    usuario = request.user

    if usuario.tipo_usuario == 'cliente' and publicacao.cliente != usuario.empresa:
        return redirect('dashboard')

    if usuario.tipo_usuario == 'funcionario' and publicacao.funcionario_responsavel != usuario:
        return redirect('dashboard')

    status_form = StatusPublicacaoForm(instance=publicacao)
    materia_form = MateriaFormatadaForm(instance=publicacao)
    mensagem_form = MensagemPublicacaoForm()
    admin_form = AdminPublicacaoForm(instance=publicacao)

    if request.method == 'POST':
        acao = request.POST.get('acao')

        if acao == 'atualizar_status' and usuario.tipo_usuario == 'admin':
            status_form = StatusPublicacaoForm(request.POST, instance=publicacao)

            if status_form.is_valid():
                status_form.save()
                return redirect('detalhe_publicacao', id=publicacao.id)

        elif acao == 'enviar_mensagem' and usuario.tipo_usuario in ['admin', 'cliente']:
            mensagem_form = MensagemPublicacaoForm(request.POST)

            if mensagem_form.is_valid():
                mensagem = mensagem_form.save(commit=False)
                mensagem.publicacao = publicacao
                mensagem.autor = usuario
                mensagem.save()
                messages.success(request, 'Mensagem enviada com sucesso.')
                return redirect('detalhe_publicacao', id=publicacao.id)

        elif acao == 'confirmar_publicacao' and usuario.tipo_usuario == 'cliente':
            if publicacao.status == 'aguardando_aprovacao':
                publicacao.status = 'aprovado'
                publicacao.save()
                messages.success(request, 'Publicidade solicitada com sucesso.')
                return redirect('detalhe_publicacao', id=publicacao.id)

        elif acao == 'upload_materia' and usuario.tipo_usuario == 'funcionario':
            materia_form = MateriaFormatadaForm(
                request.POST,
                request.FILES,
                instance=publicacao
            )

            if materia_form.is_valid():
                materia_form.save()
                messages.success(request, 'Matéria formatada enviada com sucesso.')
                return redirect('detalhe_publicacao', id=publicacao.id)
        
        elif acao == 'editar_publicacao' and usuario.tipo_usuario == 'admin':
            admin_form = AdminPublicacaoForm(
                request.POST,
                instance=publicacao
            )

            if admin_form.is_valid():
                admin_form.save()
                messages.success(request, 'Dados da publicidade atualizados com sucesso.')
                return redirect('detalhe_publicacao', id=publicacao.id)

    mensagens = publicacao.mensagens.all()

    return render(request, 'core/detalhe_publicacao.html', {
        'publicacao': publicacao,
        'status_form': status_form,
        'materia_form': materia_form,
        'mensagem_form': mensagem_form,
        'mensagens': mensagens,
        'admin_form': admin_form,
    })

@login_required
def minha_conta(request):
    if request.user.tipo_usuario != 'cliente':
        return render(request, 'core/minha_conta.html')

    if request.method == 'POST':
        form = MinhaContaForm(
            request.POST,
            usuario=request.user
        )

        if form.is_valid():
            form.save()
            messages.success(request, 'Dados da conta atualizados com sucesso.')
            return redirect('minha_conta')

    else:
        form = MinhaContaForm(usuario=request.user)

    return render(request, 'core/minha_conta.html', {
        'form': form
    })