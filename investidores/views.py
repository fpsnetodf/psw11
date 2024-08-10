from django.shortcuts import render, redirect
from empresarios.models import Empresas, Documento
from .models import PropostaInvestimento
from django.contrib.messages import add_message, constants
from django.http import Http404

# Create your views here.
def sugestao(request):   
    areas = Empresas.area_choices
    if request.method == "GET":   
        return render(request, 'investidores/sugestao.html', {'areas': areas})
    elif request.method == "POST":
        tipo = request.POST.get('tipo')
        area = request.POST.getlist('area')
        valor = request.POST.get('valor')

        if tipo == 'C':
            empresas = Empresas.objects.filter(tempo_existencia='+5').filter(estagio="E")
        elif tipo == 'D':
            empresas = Empresas.objects.filter(tempo_existencia__in=['-6', '+6', '+1']).exclude(estagio="E")
        
        empresas = empresas.filter(area__in=area)
        
        empresas_selecionadas = []
        for empresa in empresas:
            percentual = (float(valor) * 100) / float(empresa.valuation())
            if percentual >= 1:
                empresas_selecionadas.append(empresa)

        return render(request, 'investidores/sugestao.html', {'empresas': empresas_selecionadas, 'areas': areas})


def ver_empresa(request, id):
    empresa = Empresas.objects.get(id=id)
    documentos = Documento.objects.filter(empresa=empresa)
    return render(request, 'investidores/ver_empresa.html', {'empresa': empresa, "documentos": documentos})


def realizar_proposta(request, id):
    valor = request.POST.get('valor')
    percentual = request.POST.get('percentual')
    empresa = Empresas.objects.get(id=id)

    propostas_aceitas = PropostaInvestimento.objects.filter(empresa=empresa).filter(status='PA')
    total = 0

    for pa in propostas_aceitas:
        total = total + pa.percentual

    if total + int(percentual)  > empresa.percentual_equity:
        add_message(request, constants.WARNING, 'O percentual solicitado ultrapassa o percentual máximo.')
        return redirect(f'/ver_empresa/{id}')


    valuation =  int(valor) * int(percentual) / 100
    print(valuation)

    if valuation < int(empresa.valuation())/2 :
        add_message(request, constants.WARNING, f'Seu valuation proposto foi R${valuation} e deve ser no mínimo R${empresa.valuation()/2}')
        return redirect(f'/ver_empresa/{id}')

    pi = PropostaInvestimento(
        valor = valor,
        percentual = percentual,
        empresa = empresa,
        investidor = request.user,
    )

    pi.save()

    #add_message(request, constants.SUCCESS, f'Proposta enviada com sucesso')
    return redirect(f'/assinar_contrato/{pi.id}')


def assinar_contrato(request, id):
    pi = PropostaInvestimento.objects.get(id=id)
    if pi.status != "AS":
        raise Http404()
    
    if request.method == "GET":
        return render(request, 'investidores/assinar_contrato.html', {'id': id})
    elif request.method == "POST":
        selfie = request.FILES.get('selfie')
        rg = request.FILES.get('rg')
        print(request.FILES)
        

        pi.selfie = selfie
        pi.rg = rg
        pi.status = 'PE'
        pi.save()

        add_message(request, constants.SUCCESS, f'Contrato assinado com sucesso, sua proposta foi enviada a empresa.')
        return redirect(f'/ver_empresa/{pi.empresa.id}')
