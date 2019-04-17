from gerenciar_coleta import *
from config import VERSAO
from constantes import *
print('versão: {}'.format(VERSAO))

# usagem
# ação => é o tipo do de ação que imovel está(venda,compra,lançamento...)
# tipo => é o tipo de residência.. você pode ver todos os tipos no arquivo constantes.py
# onde => é a localidade.. ela segue o padrão do site que é: estado + região, exemplo: sp + zona-sul
# pagina => é a pagina inicial que você pode initializar... podendo tbm só chamar no método rodar.
# qnt_quartos => quantos quartos a residencia tem
# qnt_suites => quantas suites a residencia tem
# qnt_vagas => quantas vagas de estacionamento a residencia tem
# area_util_minima => é o espaço em metros mínimo da residência.
# area_util_maxima => é o espaço ém metros máximo da residência



import requests
import urllib
import json

data = {
	'tipoOferta': 'Imovel',
	'paginaAtual': 1,
	'pathName': '/venda/apartamentos/mg+belo-horizonte/',
	'hashFragment': { "filtrodormitorios":"1;","pagina":"1"}
}
header = headers['padrao']
req = requests.post(API['padrao'],headers=header,data=urllib.parse.urlencode(data))
data = json.loads(req.text)

with open('data.json', 'w') as outfile:
    json.dump(data, outfile,indent=4)





# variáveis de configuração !

acao = TipoAcao.venda
tipo = TipoResidencia.apartamento_padrao
onde = 'mg+belo-horizonte' # estado + cidade
qnt_quartos = 1
qnt_suites = None
qnt_vagas = None
area_util_minima = None
area_util_maxima = None

# pagina de inicio da procura...
pagina_inicial = 1
# se tiver -1, ele vai pesquisar todas as paginas com os parâmetros passados...
pagina_final = -1 # vamos pegar 5 páginas

# criamos a instancia de coleta
gerenciar = GerenciarColeta(acao=acao, tipo=tipo,onde=onde,qnt_quartos=qnt_quartos,qnt_suites=qnt_suites,qnt_vagas=qnt_vagas,area_util_minima=area_util_minima,area_util_maxima=area_util_maxima)
# iniciamos a coleta !
gerenciar.rodar(pagina_inicial=pagina_inicial,pagina_final=pagina_final)

