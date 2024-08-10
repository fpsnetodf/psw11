from django.shortcuts import render, redirect
from .models import Empresas, Documento, Metricas
from django.contrib.messages import add_message , constants
from investidores.models import PropostaInvestimento
from django.http import HttpResponse


def empresarios(request):
   return render(request, "empresarios/empresarios.html")


def cadastrar_empresa(request):
 if not request.user.is_authenticated:
   return redirect("/logar/")
 if request.method == "GET":
   return render(request, 'empresarios/cadastrar_empresa.html', {'tempo_existencia': Empresas.tempo_existencia_choices, 'areas': Empresas.area_choices })
 elif request.method == "POST":
   nome = request.POST.get('nome')
   cnpj = request.POST.get('cnpj')
   site = request.POST.get('site')
   tempo_existencia = request.POST.get('tempo_existencia')
   descricao = request.POST.get('descricao')
   data_final = request.POST.get('data_final')
   percentual_equity = request.POST.get('percentual_equity')
   estagio = request.POST.get('estagio')
   area = request.POST.get('area')
   publico_alvo = request.POST.get('publico_alvo')
   valor = request.POST.get('valor')
   pitch = request.FILES.get('pitch')
   logo = request.FILES.get('logo')
   try:
      empresa = Empresas(
      user=request.user,
      nome=nome,
      cnpj=cnpj,
      site=site,
      tempo_existencia=tempo_existencia,
      descricao=descricao,
      data_final_captacao=data_final,
      percentual_equity=percentual_equity,
      estagio=estagio,
      area=area,
      publico_alvo=publico_alvo,
      valor=valor,
      pitch=pitch,
      logo=logo
      )
      empresa.save()
   except:
      add_message(request, constants.ERROR, 'Erro interno do sistema')
      return redirect('/empresarios/cadastrar_empresa')
 
 add_message(request, constants.SUCCESS, 'Empresa criada com sucesso')
 return redirect('/empresarios/cadastrar_empresa')


def listar_empresas(request):
   if not request.user.is_authenticated:
    # Todo lista o filtro das empresas
    return redirect("/logar/")
   if request.method == "GET":
      empresa = request.GET.get("empresa")      
      if empresa :
         empresas = Empresas.objects.filter(nome__icontains=empresa) 
      else:
         empresas = Empresas.objects.filter(user=request.user)
      # empresas = Empresas.objects.filter(nome__icontains=empresa) | Empresas.objects.filter(user=request.user)
      return render(request, 'empresarios/listar_empresas.html', {"empresas": empresas})
   

def empresa(request, id):
   empresa = Empresas.objects.get(id=id)
   if empresa.user != request.user:
      add_message(request, constants.ERROR, "Essa empresa não é sua!!")
      return redirect(f"/empresa/{id}") 
   
   if request.method == "GET":
      documentos = Documento.objects.filter(empresa=empresa) 
      proposta_investimentos = PropostaInvestimento.objects.filter(empresa=empresa)
      percentual_vendido = 0
      free = int(empresa.valuation()* 0.001)
      print("free", free)
      for pi in proposta_investimentos:
         print(pi)
         if pi.status == "PA":
            percentual_vendido += pi.percentual
         print("vendido % ",percentual_vendido)
      proposta_investimentos_enviada = proposta_investimentos.filter(status='PE') 
      return render(request, "empresarios/empresa.html", {"empresa" : empresa, "documentos": documentos, "proposta_investimentos_enviada": proposta_investimentos_enviada, "percentual_vendido": int(percentual_vendido) })
      
def add_doc(request, id):
   empresa = Empresas.objects.get(id=id)
   titulo = request.POST.get('titulo')
   arquivo = request.FILES.get('arquivo')
   extensao = arquivo.name.split('.')
    
   if empresa.user != request.user:
      add_message(request, constants.ERROR, "Essa empresa não é sua!!")
      return redirect(f"/empresa/{id}")

   if extensao[1] != 'pdf':
      add_message(request, constants.ERROR, "Envie apenas PDF's")        
      return redirect(f'/empresa/{empresa.id}')
    
   if not arquivo:
      add_message(request, constants.ERROR, "Envie um arquivo")
      return redirect(f'/empresa/{empresa.id}')
        
   documento = Documento(
   empresa=empresa,
   titulo=titulo,
   arquivo=arquivo
    )
   documento.save()
   add_message(request, constants.SUCCESS, "Arquivo cadastrado com sucesso")
   return redirect(f'/empresa/{empresa.id}')


def excluir_dc(request, id):
   documento = Documento.objects.get(id=id)
   if documento.empresa.user != request.user:
      add_message(request, constants.ERROR, "Esse documento não é seu")
      return redirect(f'/empresa/{empresa.id}')
   
   documento.delete()
   add_message(request, constants.SUCCESS, "Documento excluído com sucesso")
   return redirect(f'/empresa/{documento.empresa.id}')


def add_metrica(request, id):
    empresa = Empresas.objects.get(id=id)
    titulo = request.POST.get('titulo')
    valor = request.POST.get('valor')
    
    metrica = Metricas(
        empresa=empresa,
        titulo=titulo,
        valor=valor
    )
    metrica.save()

    add_message(request, constants.SUCCESS, "Métrica cadastrada com sucesso")
    return redirect(f'/empresa/{empresa.id}')


def gerenciar_proposta(request, id):
   acao = request.GET.get("acao")
   return HttpResponse(acao)
 
 

   