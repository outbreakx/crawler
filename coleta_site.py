import requests
import urllib
import json  
import random
import os
import time

from bs4 import BeautifulSoup
import traceback


from constantes import *
from MongoProxies import *
from UserAgents import *

proxies = []
user_agents = []

mp = MongoProxies()
ua = UserAgents()

##
## @brief      pega as proxies do arquivo
##
## @return     lista de proxies
##
def pegar_proxies():
	return mp.getRandomProxy()


##
## @brief      pega os user agents do arquivo
##
## @return     lista de agentes
##
def pegar_user_agents():
	return ua.getRandomUserAgent()


##
## @brief      testa se uma proxy é válida
##
## @param      proxy  The proxy
##
## @return     nada
##
def testar_proxy(proxy):
	try:
		pro = {
			'https' : proxy
		}
		s = requests.Session()
		s.mount('http://', requests.adapters.HTTPAdapter(max_retries=1))

		s = s.get('https://www.google.com.br', proxies=pro)
		return True if s.status_code == 200 else False
	except Exception as e:
		print(e)
		return False



#atualizar_proxies()
proxies = pegar_proxies()
user_agents = pegar_user_agents()


def pegar_cookie():
	headers = {
		'user-agent': random.choice(user_agents)
	}
	proxy = {
		'http' : ''
	}
	req = None
	while not req:
		proxy['http'] = random.choice(proxies)
		req = requests.get('https://www.zapimoveis.com.br/', headers=headers, proxies = proxy)
	return req.headers['Set-Cookie']

##
## @brief      Class for coletar site.
##
class ColetarSite():
	def __init__(self, data):
		self.data = data	
		self.proxy_ = None


	def definir_data(self, data):
		self.data = data

	def pegar_pagina_total(self):
		obj = None
		try:
			obj = self.pegar_dados(self.data)
		except:
			pass

		if not obj:
			return 0
		return int(obj['Resultado']['QuantidadePaginas'])


	##
	## @brief      pegar todas as informações dos data fornecido
	##
	## @param      self  The object
	##
	## @return     os dados com base no data
	##
	def pegar_info(self):
		todos_dados = []
		#obj = json.load(open('data.txt',encoding='utf8'))	

		# pegamos a pagina.. mas não tem nada...
		
		pagina_id = self.data['hashFragment']['pagina'] 

		obj = None
		contador = 0
		while obj == None and contador < 10:
			try:
				obj = self.pegar_dados(self.data)
			except:
				pass
			contador += 1
		if obj and int(obj['Resultado']['QuantidadePaginas']) == 0:	
			#print('deu errado...')		
			return None
		if not obj:
			return None

		for item in obj['Resultado']['Resultado']:
			dados = {}
			dados['id'] = item['CodigoOfertaZAP']
			dados['url'] = item['UrlFicha']

			fotos = []

			for foto in item['Fotos']:
				fotos.append(foto['UrlImagemTamanhoG'])

			dados['fotos'] = fotos
			try:
				valor = int(item['Valor'].replace('R$','').replace('.',''))
			except:
				valor = 0

			dados['valor'] = valor
			try:
				iptu = int(item['ValorIPTU'].replace('R$','').replace('.',''))
			except:
				iptu = 0
			dados['iptu'] = iptu
			try:
				condominio = int(item['PrecoCondominio'].replace('R$','').replace('.',''))
			except:
				condominio = 0

			dados['condominio'] = condominio

			caracteristicas_principais = {}

			caracteristicas_principais['qt_quartos'] = max(int(item['QuantidadeQuartos']), int(item['QuantidadeQuartosMinima']))
			caracteristicas_principais['qt_suites'] = max(int(item['QuantidadeSuites']), int(item['QuantidadeSuitesMinima']))
			caracteristicas_principais['qt_vagas'] = max(int(item['QuantidadeVagas']), int(item['QuantidadeVagasMinima']))
			caracteristicas_principais['area_minima'] = item['AreaMinima']
			caracteristicas_principais['area_maxima'] = item['AreaMaxima']
			caracteristicas_principais['area'] = item["Area"]
			
			caracteristicas_principais['descricao'] = item['Observacao']

			dados['caracteristicas_principais'] = caracteristicas_principais


			localizacao = {}
			localizacao['cep'] = item['CEP']
			localizacao['endereco'] = item['Endereco']
			localizacao['numero'] = item['Numero']
			localizacao['estado'] = item['Estado']
			localizacao['cidade'] = item['CidadeOficial']
			localizacao['bairro'] = item['BairroOficial']

			dados['localizacao'] = localizacao

			dados_contato = {}
			dados_contato['nome'] = item['NomeAnunciante']
			
			try:
				dados_contato['email'] = item['ContatoCampanha']['Email'].split('|')
			except:
				dados_contato['email'] = []

			dados_contato['telefone'] = []	

			dados['transacao'] = item['Transacao']

			dados['dados_contato'] = dados_contato			
			todos_dados.append(dados)

		# caso queira salvar em json pra testes...
		'''
		with open('test/teste-{}.json'.format(pagina_id), 'w') as outfile:  
			json.dump(todos_dados, outfile, indent=4,sort_keys=True)
		'''
		
		
		return todos_dados


	##
	## @brief      pega o numero com base nos dados passados
	##
	## @param      self       The object
	## @param      id         o id
	## @param      transacao  o tipo de transação
	##
	## @return     os dados
	##
	def pegar_numero(self, id, transacao):
		data = {
			'parametros': {
				"ImovelID":id,
				"TipoOferta": 'CampanhaImovel',			
				"Transacao": transacao
			},
			'__RequestVerificationToken': '0rA02O2FYGLCXpeSEzuKMYZ9zzOJamFDqK6BgcpcbHx1S7Atqp-HlJU_kG2z52TXqmBo6Y6KJN_v_8fme23oitgeZIM1'

		}
		proxy = {
			'http' : ''
		}

		header = headers['telefone']

		header['user-agent'] = random.choice(user_agents)

		header['cookie'] = pegar_cookie()

		
		proxy['http'] = random.choice(proxies) if not self.proxy_ else self.proxy_

		# tento pegar os dados do telefone
		req = requests.post(API['telefone'],headers=header,data=urllib.parse.urlencode(data), proxies=proxy)
		obj = None
		# funcionou?
		if req.status_code == 200:
			obj = json.loads(req.text)
		# se tiver captcha or se deu errado
		if req.status_code == 500 or obj['CaptchaId']:
			# muda o tipo de oferta se o erro foi 500
			if not obj['CaptchaId']:
				data['TipoOferta'] = 'Imovel'

			# tenta dnv...
			req = requests.post(API['telefone'],headers=header,data=urllib.parse.urlencode(data),proxies=proxy)
			obj = json.loads(req.text)
			#print(obj)

			# tem captcha?
			if obj['CaptchaId']:
				#print('entrou')

				# tenta pegar o número trocando de proxies...
				while True:
					try:
						proxy['http'] = random.choice(proxies)
						header['cookie'] = pegar_cookie()
						req = requests.post(API['telefone'],headers=header,data=urllib.parse.urlencode(data))
						s = requests.Session()
						s.mount('https://', requests.adapters.HTTPAdapter(max_retries=1))
						req = s.post(API['telefone'],headers=header,data=urllib.parse.urlencode(data),proxies=proxy)
						obj = obj = json.loads(req.text)
						if not obj['CaptchaId'] or len(obj['CaptchaId'] ) == 0:
							#print(obj)
							self.proxy_ = proxy['http']
							#print('saiu')										
							break
						else:			
							#print('xdd')		
							time.sleep(random.choice([2,4,6]))	
					except Exception as e:
						#print(traceback.format_exc())
						pass			
		else:
			obj = json.loads(req.text)
		return {'status': req.status_code, 'data' : obj}


	##
	## @brief      pega os dados com base no data
	##
	## @param      self  The object
	## @param      data  dicionário contendo que coisa deve ser procurada.
	##
	## @return     os dados
	##
	def pegar_dados(self, data):
		proxy = {
			'http' : ''
		}
		header = headers['padrao']

		header['user-agent'] = random.choice(user_agents)

		req = None
		tentativas = 0
		

		# garante que vai tentar 50 vezes pegar os dados com proxies...
		while tentativas < 5:
			proxy['http'] = random.choice(proxies)
			header['cookie'] = pegar_cookie()
			s = requests.Session()
			s.mount('http://', requests.adapters.HTTPAdapter(max_retries=1))
			try:			
				req = s.post(API['padrao'],proxies = proxy, headers=header,data=urllib.parse.urlencode(data))
				if req.status_code == 200:
					break
			except:
				time.sleep(random.choice([2,4,6,8]))
				pass
			tentativas += 1
		obj = None
		if req:
			obj = json.loads(req.text)
		return obj