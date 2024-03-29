import threading 
import time
import sys

from constantes import *
from coleta_site import ColetarSite
from config import *
from db import DB


def update_progress(progress,message):
	length = 30
	block = int(round(length*progress))
	msg = "\r{0}: [{1}] {2}%".format(message, "#"*block + "-"*(length-block), round(progress*100, CASAS_DECIMAIS))
	if progress >= 1: 
		msg += " TERMINOU!\r\n"
	sys.stdout.write(msg)
	sys.stdout.flush()

##
## @brief      função para gerar intervalos
##
## @param      l     range
## @param      n     tamanho do intervalo
##
## @return     lista contendo os intervalos
##
def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))


class Test(threading.Thread):
	def __init__(self,paginas,ref):
		threading.Thread.__init__(self)
		self.paginas = paginas
		self.ref = ref
		self.db = DB()
		self.concluido = 0
		self.total = len(self.paginas)
	def run(self):
		total = 0
		xd = 0
		for pagina in self.paginas:
			cs = ColetarSite(self.ref.gerar_data(pagina))	
			dados = cs.pegar_info()
			if not dados:
				tentativas = 0
				while not dados and tentativas < 10:
					cs = ColetarSite(self.ref.gerar_data(pagina))	
					dados = cs.pegar_info()
					tentativas += 1
			if dados:
				self.db.inserir(dados)
				total += 1
				xd += len(dados)
			else:
				#print('não coletou a página:' + str(pagina))
				pass
			self.concluido += 1
		#print('inseriu {} paginas com {} dados'.format(total,xd))
		


##
## @brief      Class for gerenciar coleta.
##
class GerenciarColeta():

	##
	## @brief      Constructs the object.
	##
	## @param      self              The object
	## @param      acao              The acao
	## @param      tipo              The tipo
	## @param      onde              The onde
	## @param      pagina            The pagina
	## @param      qnt_quartos       The qnt quartos
	## @param      qnt_suites        The qnt suites
	## @param      area_util_minima  The area utility minima
	## @param      area_util_maxima  The area utility maxima
	##
	def __init__(self,acao = TipoAcao.venda, tipo = TipoResidencia.todos, onde=None, pagina=1, qnt_quartos=None,qnt_suites=None,qnt_vagas=None,area_util_minima=None,area_util_maxima=None):

		self.acao = acao
		self.tipo = tipo		
		self.onde = onde

		# parâmetros de busca!
		self.parametros_de_busca = {
			'filtrodormitorios':'',
			'filtrosuites':'',
			'filtrovagas':'',
			'areautilminima':'',
			'areautilmaxima':'',
			'pagina':'1'		
		}		

		if qnt_quartos:
			self.definir_quartos(qnt_quartos)
		if qnt_suites:						
			self.definir_suites(qnt_suites)
		if qnt_vagas:
			self.definir_vagas(qnt_vagas)
		if area_util_minima:
			self.definir_area_util_minima(area_util_minima)
		if area_util_maxima:						
			self.definir_area_util_maxima(area_util_maxima)
		if pagina:
			self.definir_pagina(pagina)

	##
	## @brief      gera a data a ser enviada
	##
	## @param      self    The object
	## @param      pagina  The pagina
	##
	## @return     data a ser enviada
	##
	def gerar_data(self, pagina=-1):
		tmp = self.parametros_de_busca
		if pagina != -1:
			tmp['pagina'] = pagina
		data = {
			'tipoOferta': self.pegar_oferta(),	
			'pathName': '/' + self.pegar_acao() + self.pegar_tipo() + self.pegar_onde(),
			'hashFragment': tmp,
			'formato': 'Galeria',
		}		
		return data


	##
	## @brief      pega o tipo de oferta
	##
	## @param      self  The object
	##
	## @return     a oferta
	##
	def pegar_oferta(self):
		if self.acao == TipoAcao.lancamento:
			return 2
		elif self.acao == TipoAcao.venda:
			return 1
		else:
			return 'Imovel'


	##
	## @brief      defini a pagina
	##
	## @param      self  The object
	## @param      val   The value
	##
	##
	def definir_pagina(self,val):
		self.parametros_de_busca['pagina'] = str(val)

	##
	## @brief      pega a pagina
	##
	## @param      self  The object
	##
	## @return     a pagina
	##
	def pegar_pagina(self):
		return int(self.parametros_de_busca['pagina'])

	##
	## @brief      pega a ação
	##
	## @param      self  The object
	##
	## @return    retorna a ação
	##
	def pegar_acao(self):
		if TipoAcao.venda == self.acao:
			return 'venda/'			
		elif TipoAcao.alugar == self.acao:
			return 'aluguel/'
		elif TipoAcao.lancamento == self.acao:
			return'lancamentos/'
		else:
			return None

	##
	## @brief      pega o tipo 
	##
	## @param      self  The object
	##
	## @return     o tipo
	##
	def pegar_tipo(self):
		return str(self.tipo.value[0]) + '/'

	##
	## @brief      define o numero de quartos
	##
	## @param      self  The object
	## @param      val   o numero de quartos
	##
	##
	def definir_quartos(self, val):
		if val > 4:
			self.parametros_de_busca['filtrodormitorios'] = '4;'
		elif val < 0:
			self.parametros_de_busca['filtrodormitorios'] = ''
		else:
			self.parametros_de_busca['filtrodormitorios'] = str(val) + ';'
	
	##
	## @brief      define o numero de suites
	##
	## @param      self  The object
	## @param      val   o numero de suites
	##
	##
	def definir_suites(self,val):
		if val > 4:
			self.parametros_de_busca['filtrosuites'] = '4;'
		elif val < 0:
			self.parametros_de_busca['filtrosuites'] = ''
		else:
			self.parametros_de_busca['filtrosuites'] = str(val) + ';'

	def definir_vagas(self,val):
		if val > 4:
			self.parametros_de_busca['filtrovagas'] = '4;'
		elif val < 0:
			self.parametros_de_busca['filtrovagas'] = ''
		else:
			self.parametros_de_busca['filtrovagas'] = str(val) + ';'

	##
	## @brief      define o numero de metros minimos
	##
	## @param      self  The object
	## @param      val   o numero de metros minimos
	##
	##
	def definir_area_util_minima(self,val):
		self.parametros_de_busca['areautilminima'] = str(val)

	##
	## @brief      define o numero de metros maximos
	##
	## @param      self  The object
	## @param      val   o numero de metros maximos
	##
	##
	def definir_area_util_maxima(self,val):
		self.parametros_de_busca['areautilmaxima'] = str(val)

	##
	## @brief      define o lugar de pesquisa
	##
	## @param      self  The object
	## @param      val  o lugar de pesquisa
	##
	##
	def definir_onde(self,val):
		self.onde = val


	##
	## @brief      pega o lugar de pesquisa formatado
	##
	## @param      self  The object
	##
	## @return     lugar de pesquisa formtado
	##
	def pegar_onde(self):
		return self.onde.replace(' ','+') + '/' if self.onde else ''


	##
	## @brief      roda o programa para os intervalos
	##
	## @param      self     The object
	## @param      paginas  The paginas
	## @param      id       The identifier
	##
	## @return     { description_of_the_return_value }
	##
	def rodar_intervalo(self, paginas):
		#cria a instancia da db
		db = DB()
		# pra cada página coletar as informações...
		#total_dados = []
		
		for pagina in paginas:			
			cs = ColetarSite(self.gerar_data(pagina))	
			dados = cs.pegar_info()
			if not dados:
				tentativas = 0
				while not dados and tentativas < 10:
					cs = ColetarSite(self.gerar_data(pagina))	
					dados = cs.pegar_info()
					tentativas += 1

			if dados:
				# insere os dados..				
				#print('coletou os dados da página atual: ' + str(pagina))
				db.inserir(dados)
	##
	## @brief      o quantidade que cada thread vai processar
	##
	## @param      self  The object
	## @param      val   The value
	##
	## @return     { description_of_the_return_value }
	##
	def pegar_taxa_incremento(self, val):
		if val < MAX_THREADS:
			return 1
		elif val < 50:
			return 2

		div = 3
		while True:
			res = int(val/div)
			if res >= MAX_THREADS:
				div += 1
			else:
				break
		return div

	def pegar_concluidos(self, arr):
		cnt = 0
		for item in arr:
			cnt += item.concluido
		return cnt


	##
	## @brief      rodar a coleta com base em intervalos
	##
	## @param      self            The object
	## @param      pagina_inicial  pagina inicial
	## @param      pagina_final    pagina final
	##
	##
	def rodar(self, pagina_inicial = 1, pagina_final = -1):
		# uma instancia de coleta de dados
		cs = ColetarSite(self.gerar_data(pagina_inicial))	
		if pagina_final == -1:
			pagina_final = cs.pegar_pagina_total()

		if pagina_final == 0 or pagina_final < -1:
			print("não foi possível pegar a página final...")
			return False
		else:
			pagina_final += 1

		
		increase_rate = self.pegar_taxa_incremento(pagina_final - pagina_inicial)
		threads = []
		total_paginas = 0		
		for chunk in chunks(range(pagina_inicial, pagina_final), increase_rate):			
			thread = Test(chunk, self)
			thread.start()
			threads.append(thread)
			total_paginas += len(chunk)	

		l = total_paginas

		#print('total de threads:{}'.format(l))
		update_progress(0, "Progresso:")

		while True:
			total_concluido = self.pegar_concluidos(threads)
			update_progress(total_concluido/l, "Progresso:")
			if total_concluido == total_paginas:
				break
			time.sleep(1)

