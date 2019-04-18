#from gerenciar_coleta import *
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



# variáveis de configuração !
'''
acao = TipoAcao.venda
tipo = TipoResidencia.apartamento_padrao
onde = 'mg+belo-horizonte' # estado + cidade
qnt_quartos = None
qnt_suites = None
qnt_vagas = None
area_util_minima = None
area_util_maxima = None

# pagina de inicio da procura...
pagina_inicial = 1
# se tiver -1, ele vai pesquisar todas as paginas com os parâmetros passados...
pagina_final = 1

# criamos a instancia de coleta
gerenciar = GerenciarColeta(acao=acao, tipo=tipo,onde=onde,qnt_quartos=qnt_quartos,qnt_suites=qnt_suites,qnt_vagas=qnt_vagas,area_util_minima=area_util_minima,area_util_maxima=area_util_maxima)
# iniciamos a coleta !
gerenciar.rodar(pagina_inicial=pagina_inicial,pagina_final=pagina_final)
'''

import requests
import urllib
import json
def pegar_num(id, transacao):
	data = {
		'parametros': {
			"ImovelID": id,
			"TipoOferta": 'CampanhaImovel',			
			"Transacao": transacao
		},
		'__RequestVerificationToken': 'EYbyU3njELw8HXGwBrgvwFWb0yEnAXik9CTUowNx-yagjLTg04otZc4VSe4AWEJoCgeNrAxfLhW1KKfyw5kundOKmVk1'
	}
	header = headers['telefone']
	#header['cookie'] = pegar_cookie()
	proxy = {
		'http' : ''
	}

	req = None
	try:
		req = requests.post(API['telefone'],headers=header,data=urllib.parse.urlencode(data))
	except:
		pass
	if not req or req.status_code != 200:
		data['parametros']['TipoOferta'] = 'Imovel'
		try:
			req = requests.post(API['telefone'],headers=header,data=urllib.parse.urlencode(data))
		except Exception as e:
			print(e)
			pass

	if not req:
		return None

	if req.status_code == 404:
		return None

	res = json.loads(req.text)

	if res['CaptchaId']:
		tentativas = 0
		while tentativas < 5:
			
			try:
				req = requests.post(API['telefone'],data=urllib.parse.urlencode(data), headers=header)
			except:
				pass
			if req and req.status_code == 200:
				res = json.loads(req.text)
				if not res['CaptchaId']:
					break
			else:
				tentativas += 1
				time.sleep(random.choice([2,4,6]))
	return res

print(pegar_num('21252430', 'Venda'))