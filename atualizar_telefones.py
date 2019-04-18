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
from config import *

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



def update_progress(progress,message):
	length = 30
	block = int(round(length*progress))
	msg = "\r{0}: [{1}] {2}%".format(message, "#"*block + "-"*(length-block), round(progress*100, CASAS_DECIMAIS))
	if progress >= 1: 
		msg += " TERMINOU!\r\n"
	sys.stdout.write(msg)
	sys.stdout.flush()



def pegar_num(id, transacao):
	data = {
		'parametros': {
			"ImovelID": id,
			"TipoOferta": 'Imovel',			
			"Transacao": transacao
		},
		'__RequestVerificationToken': 'EYbyU3njELw8HXGwBrgvwFWb0yEnAXik9CTUowNx-yagjLTg04otZc4VSe4AWEJoCgeNrAxfLhW1KKfyw5kundOKmVk1'
	}
	header = headers['telefone']
	#header['cookie'] = pegar_cookie()
	proxy = {
		'http' : ''
	}
	proxy['http'] = pegar_proxies()

	req = None
	try:
		req = requests.post(API['telefone'],headers=header,data=urllib.parse.urlencode(data),proxies = proxy)
	except:
		pass
	if not req or req.status_code != 200:
		data['parametros']['TipoOferta'] = 'CampanhaImovel'
		try:
			req = requests.post(API['telefone'],headers=header,data=urllib.parse.urlencode(data),proxies = proxy)
		except:
			pass

	if req.status_code == 404:
		return None

	res = None

	if req.status_code == 403 or req.status_code == 200:

		if req.status_code == 200:
			res = json.loads(req.text)
			if not res['CaptchaId']:
				return res

		tentativas = 0
		while tentativas < 5:
			header['user-agent'] = random.choice(user_agents)
			proxy['http'] = pegar_proxies()
			try:
				req = requests.post(API['telefone'],headers=header,data=urllib.parse.urlencode(data),proxies = proxy)
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


l = db.pegar_total()
nao_coletados = []


for i, item in  enumerate(data):
	#checamos se existe já algum telefone para esse id, então pulamos para o próximo id.
	if len(item['dados_contato']['telefone']) > 0:
		continue

	nao_coletados.append(item)

l = len(nao_coletados)

update_progress(0, "Progresso:")
for i, item in enumerate(nao_coletados):
	tmp = pegar_num(item['id'], item['transacao'])

	if tmp:
		telefones = []
		if 'Telefones' in tmp and tmp['CaptchaId'] == None and len(tmp['Telefones']):														
			for telefone in tmp['Telefones']:
				if telefone['DDD']:
					telefones.append(telefone['DDD'] + telefone['Numero'])
			db.atualizar_telefone(item['id'], telefones)

	update_progress((i + 1)/l, "Progresso:")
	time.sleep(1)