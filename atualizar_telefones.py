import pymongo
import pprint
import random
import requests
import urllib
import traceback
import time
from db import DB

from constantes import *
from MongoProxies import *
from UserAgents import *


db = DB()


data = db.pegar_dados()

contador = 0

proxies = []
user_agents = []
proxy_ = None

mp = MongoProxies()
ua = UserAgents()

def pegar_proxies():
	return mp.getRandomProxy()


def pegar_user_agents():
	data = []
	with open('user_agents.txt', encoding='utf8') as f:
		data = []
		for x in f.readlines():
			if len(x) > 0:
				data.append(x.strip())
	return data

proxies = pegar_proxies()
user_agents = pegar_user_agents()



def pegar_numero(id, transacao):
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
	ua =  random.choice(user_agents)
	
	req = None

	global proxy_

		
	proxy['http'] = random.choice(proxies) if not proxy_ else proxy_

	# tento pegar os dados do telefone
	try:
		req = requests.post(API['telefone'],headers=header,data=urllib.parse.urlencode(data), proxies=proxy)
	except:
		pass
	obj = None
	# funcionou?
	if req and req.status_code == 200:
		obj = json.loads(req.text)
	# testa imovel..
	if req and req.status_code == 500:
		data['TipoOferta'] = 'Imovel'
		try:
			req = requests.post(API['telefone'],headers=header,data=urllib.parse.urlencode(data),proxies=proxy)
		except:
			pass

	# se tiver captcha or se deu errado
	if not obj or obj['CaptchaId']:
		if req.status_code == 200:
			obj = json.loads(req.text)
		# tenta pegar o número trocando de proxies...
		tentativas = 0
		while tentativas < 15:
			try:
				proxy['http'] = random.choice(proxies)
				header['user-agent'] = random.choice(user_agents)
				req = requests.post(API['telefone'],headers=header,data=urllib.parse.urlencode(data))
				s = requests.Session()
				s.mount('https://', requests.adapters.HTTPAdapter(max_retries=1))
				req = s.post(API['telefone'],headers=header,data=urllib.parse.urlencode(data),proxies=proxy)
				if req.status_code == 200:
					obj = json.loads(req.text)
				if obj and (not obj['CaptchaId'] or len(obj['CaptchaId'] ) == 0):					
					proxy_ = proxy['http']														
					break
				else:
					
					time.sleep(random.choice([2,4,6]))
					if req.status_code == 403:
						data['TipoOferta'] = 'CampanhaImovel'
			except Exception as e:
				print(traceback.format_exc())
				time.sleep(random.choice([2,4,6]))
				pass	
			tentativas += 1		
	else:
		obj = json.loads(req.text)
	return obj

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()


l = db.pegar_total()
nao_coletados = []



for i, item in  enumerate(data):
	dados = db.pegar_dados(item['id'])
	#checamos se existe já algum telefone para esse id, então pulamos para o próximo id.
	if len(dados['dados_contato']['telefone']) > 0:
		continue
	nao_coletados.append(item)


l = len(nao_coletados)
printProgressBar(0, l, prefix = 'Progresso:', suffix = 'Completo', length = 50)
for i,item in enumerate(nao_coletados):
	tmp = pegar_numero(item['id'],item['transacao'])

	telefones = []
	if tmp:					
		if 'Telefones' in tmp and tmp['CaptchaId'] == None:														
			for telefone in tmp['Telefones']:
				if telefone['DDD']:
					telefones.append(telefone['DDD'] + telefone['Numero'])
	db.atualizar_telefone(item['id'], telefones)
	printProgressBar(i + 1, l, prefix = 'Progresso:', suffix = 'Completo', length = 50)