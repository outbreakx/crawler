import enum

# API DO SITE
API = { 
	'padrao' : 'https://www.zapimoveis.com.br/Busca/RetornarBuscaAssincrona/',
	'telefone' : 'https://www.zapimoveis.com.br/VerTelefone/Buscar/'
}

# ARQUIVOS
ARQUIVO_PROXY = 'proxies.txt'
ARQUIVO_USER_AGENT = 'user_agents.txt'

# THREADS: ATENÇÃO, MANTER PRÓXIMO DE 12 OU ABAIXO PREFERENCIALMENTE, acima disso, causa a ativação de alguns sistemas anti spam deles de forma mais ostensiva.
MAX_THREADS = 10

# HEADRERS DOS REQUESTS
headers = {
	'padrao' : {
		'content-type': 'application/x-www-form-urlencoded',
		'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
		'cookie': '_origemChamada=8mxSIGpu4zXvlmPJn50gaStfRLqD4EDsG+QlQeqKAZkvXk2a8hfaMfF2AJqw9LFagT1m7ZqBnCbUFMTpzk8aUA==; _locusu=IIUjpGZ+8CK8W3Q/iBTtr6uWADlnTp71VhjyWhFpEkCk/6UNH7Hzos+Pc+5bBp9QA9LM71QE5TGLvJ4dVNISp++BnpPGD1tefbNyg31+VxrS0HZaHQxm+UbKRQ+BI+X877TzQbZkw8i0OafiuLNqATkvZGrDLxcd87J4f5yTqTg=; uidNav=36973ed1-f387-4118-b942-643e0f24feb5; utag_main=v_id:0169e9685fef0082e8035b59841003065001e05d00bd0$_sn:12$_ss:1$_st:1554713500975$_pn:1%3Bexp-session$ses_id:1554711700975%3Bexp-session; __RequestVerificationToken=jzrQ0Z9KknBNujM04i4yOD6IZNN17y48kf_0kKwOi5yJO2sNXoNcmydK0Jl9iz-dTarztY8h9zCS-iUkyhuamydbksM1; localizacaoUsuario=%7B%22Coordenadas%22%3Anull%2C%22PermiteAutorizacao%22%3Afalse%2C%22Erro%22%3A1%2C%22MensagemErro%22%3A%22user%20did%20not%20share%20geolocation%20data%22%2C%22Accuracy%22%3Anull%7D; location=%7B%22ElementoHtml%22%3A%22%22%2C%22OrigemLocalidade%22%3A%22%22%2C%22IdLocalidade%22%3A%22ulAutosuggest%22%2C%22IdBoxExemplos%22%3A%22box-exemplos-autosuggest%22%2C%22IdBtnBusca%22%3A%22btnBuscar%22%2C%22OrigemChamada%22%3A%22home%22%7D; troca_transacao=false; exibicao=G; ResultadoBuscaVenda=true; _filbusc=V+1SgvBHHDdHR60BbqVe/RQrK42MSwOS44c3LaCFhZqno+l0Tqz9XWl4ZPIXzii1Kud1QGlNjUsqSc4tgCU2tK2oWnvWCQ6EwQQVixswGbQTYS1SglCtgJIGXdqa/II5Q+C0bS8leAf9B8tRMFJB2msTPqPWlgrIX12wB+HvVW69EnpwU2T8Et+ozlyHykmRi7gVB3rOms37LfV29YwqgODFdM8EIfJdZykP3JFhlZgTRVgyFlEpnDR3ZczQJiNE41usbcnLD2+LM63ZC8Ma5W+F3qbOMdEdWPsADQg06pu1LXQkOlwqdMGBDS/JwePIpHYLkqM8jyFdUwDBsTIXk3/1v4ZyekgmxbodDD5ocUSqCkp2Y0wHuIB1LjGwszvANLxLPONct0rgQz6Lu/MGKiXZ9sdG6xxUawr0GQvq7mrcVhqTxTlMnBLI6qyisyLpAM4azzpdYyFP9vEIJFlzrMdBe59TgMvxbs0DVKmGrtfmmDWLup6SN5b2Y8JwJUrxqhTXIOaI0AtzJZFI4BR6sWI6hdameneD4YBU05rXOuc=; transacao_caixabusca=Venda; _filalerta=V+1SgvBHHDdHR60BbqVe/RQrK42MSwOS44c3LaCFhZqno+l0Tqz9XWl4ZPIXzii1Kud1QGlNjUs8P6oTFEUCO/baC5CQsSrbilG6KLnSm1RycgD8Xs5pGjHQQCL585vLHQEHn5NX2RQqDMCs7ssXQ5AkbFKyazgYviSKiVSO4lRWGPJaEWkSQNqH9DcZy1VZiIhglGlw9DNecVMboK7lcxwMnvb+OA5rMINnAJt+Lv/oq9ps+jQEhcCVLmMROaApaFSeDGjt74pCr5a0SyQ+3Q==',
		'origin': 'https://www.zapimoveis.com.br',
		'referer': 'https://www.zapimoveis.com.br',		
		'x-requested-with': 'XMLHttpRequest'
	},
	'telefone' : {
		'content-type': 'application/x-www-form-urlencoded',
		'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
		'cookie': '_origemChamada=wHFwAKIPFZcq-HML1RF-mZkcxashEygK6LaaDXR4AuEBWLeTn1bKih53xCbhh-Ypw_6ngRHOab2OOij8QzmNMZCVrOc1; _locusu=IIUjpGZ+8CK8W3Q/iBTtr6uWADlnTp71VhjyWhFpEkCk/6UNH7Hzos+Pc+5bBp9QA9LM71QE5TGLvJ4dVNISp++BnpPGD1tefbNyg31+VxrS0HZaHQxm+UbKRQ+BI+X877TzQbZkw8i0OafiuLNqATkvZGrDLxcd87J4f5yTqTg=; uidNav=36973ed1-f387-4118-b942-643e0f24feb5; utag_main=v_id:0169e9685fef0082e8035b59841003065001e05d00bd0$_sn:12$_ss:1$_st:1554713500975$_pn:1%3Bexp-session$ses_id:1554711700975%3Bexp-session; __RequestVerificationToken=jzrQ0Z9KknBNujM04i4yOD6IZNN17y48kf_0kKwOi5yJO2sNXoNcmydK0Jl9iz-dTarztY8h9zCS-iUkyhuamydbksM1; localizacaoUsuario=%7B%22Coordenadas%22%3Anull%2C%22PermiteAutorizacao%22%3Afalse%2C%22Erro%22%3A1%2C%22MensagemErro%22%3A%22user%20did%20not%20share%20geolocation%20data%22%2C%22Accuracy%22%3Anull%7D; location=%7B%22ElementoHtml%22%3A%22%22%2C%22OrigemLocalidade%22%3A%22%22%2C%22IdLocalidade%22%3A%22ulAutosuggest%22%2C%22IdBoxExemplos%22%3A%22box-exemplos-autosuggest%22%2C%22IdBtnBusca%22%3A%22btnBuscar%22%2C%22OrigemChamada%22%3A%22home%22%7D; troca_transacao=false; exibicao=G; ResultadoBuscaVenda=true; _filbusc=V+1SgvBHHDdHR60BbqVe/RQrK42MSwOS44c3LaCFhZqno+l0Tqz9XWl4ZPIXzii1Kud1QGlNjUsqSc4tgCU2tK2oWnvWCQ6EwQQVixswGbQTYS1SglCtgJIGXdqa/II5Q+C0bS8leAf9B8tRMFJB2msTPqPWlgrIX12wB+HvVW69EnpwU2T8Et+ozlyHykmRi7gVB3rOms37LfV29YwqgODFdM8EIfJdZykP3JFhlZgTRVgyFlEpnDR3ZczQJiNE41usbcnLD2+LM63ZC8Ma5W+F3qbOMdEdWPsADQg06pu1LXQkOlwqdMGBDS/JwePIpHYLkqM8jyFdUwDBsTIXk3/1v4ZyekgmxbodDD5ocUSqCkp2Y0wHuIB1LjGwszvANLxLPONct0rgQz6Lu/MGKiXZ9sdG6xxUawr0GQvq7mrcVhqTxTlMnBLI6qyisyLpAM4azzpdYyFP9vEIJFlzrMdBe59TgMvxbs0DVKmGrtfmmDWLup6SN5b2Y8JwJUrxqhTXIOaI0AtzJZFI4BR6sWI6hdameneD4YBU05rXOuc=; transacao_caixabusca=Venda; _filalerta=V+1SgvBHHDdHR60BbqVe/RQrK42MSwOS44c3LaCFhZqno+l0Tqz9XWl4ZPIXzii1Kud1QGlNjUs8P6oTFEUCO/baC5CQsSrbilG6KLnSm1RycgD8Xs5pGjHQQCL585vLHQEHn5NX2RQqDMCs7ssXQ5AkbFKyazgYviSKiVSO4lRWGPJaEWkSQNqH9DcZy1VZiIhglGlw9DNecVMboK7lcxwMnvb+OA5rMINnAJt+Lv/oq9ps+jQEhcCVLmMROaApaFSeDGjt74pCr5a0SyQ+3Q=='
	}
}

# DEFINIÇÕES DE AÇÕES PARA BUSCA
class TipoAcao(enum.Enum):
	venda = 1,
	alugar = 2,
	lancamento = 3

class TipoResidencia(enum.Enum):
	todos = 'imoveis',
	apartamento_padrao = 'apartamentos',
	casa_de_condominio = 'casas-de-condominio',
	casa_de_vila = 'casas-de-vila',
	casa_padrao = 'casas',
	cobertura = 'cobertura',
	conjunto_mercial_sala = 'conjunto-comercial-sala',
	flat = 'flat',
	kitchenette = 'quitinetes',
	loft = 'loft',
	loteamento_condominio = 'loteamento-condominio',
	terreno_padrao = 'terreno-padrao',
	box_garagem = 'box-garagem',
	casa_comercial = 'casa-comercial',
	galpao_deposito = 'galpao-deposito-armazem',
	hotel = 'hotel',
	industria = 'industria',
	loja_shopping = 'loja-shopping--ct-comercial',
	loja_salao = 'loja-salao',
	motel = 'motel',
	pousada_chale = 'pousada-chale',
	predio_inteiro = 'predio-inteiro',
	studio = 'studio',
	chacara = 'chacaras',
	fazenda = 'fazendas'
	haras = 'haras',
	sitio = 'sitios'