import pymongo

from config import *


class DB:
	def __init__(self):
		self.client = pymongo.MongoClient(IP)
		self.db = self.client[DATABASE]
		self.col = self.db[TABELA]
				
	def inserir(self, dado):
		for i in dado:
			self.col.update({'id' : i['id']}, i, upsert=True);

	def pegar_dados(self, id=None):
		return self.col.find_one({'id': id}) if id else self.col.find({})
	def atualizar_telefone(self, id, telefones):
		self.col.find_one_and_update({'id':id}, {'$set': { 'dados_contato.telefone' : telefones} } )
	def pegar_total(self):
		return self.col.count()
