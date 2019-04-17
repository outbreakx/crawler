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
MAX_THREADS = 9

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
		'cookie' : 'origemChamada=8mxSIGpu4zXvlmPJn50gaStfRLqD4EDsG+QlQeqKAZkvXk2a8hfaMfF2AJqw9LFagT1m7ZqBnCbUFMTpzk8aUA==; _locusu=IIUjpGZ+8CK8W3Q/iBTtr6uWADlnTp71VhjyWhFpEkCk/6UNH7Hzos+Pc+5bBp9QA9LM71QE5TGLvJ4dVNISp++BnpPGD1tefbNyg31+VxrS0HZaHQxm+UbKRQ+BI+X877TzQbZkw8i0OafiuLNqATkvZGrDLxcd87J4f5yTqTg=; uidNav=d4e9fd9c-5941-4fd7-8d34-1e6ff5d43544; location=%7B%22ElementoHtml%22%3A%22%22%2C%22OrigemLocalidade%22%3A%22%22%2C%22IdLocalidade%22%3A%22ulAutosuggest%22%2C%22IdBoxExemplos%22%3A%22box-exemplos-autosuggest%22%2C%22IdBtnBusca%22%3A%22btnBuscar%22%2C%22OrigemChamada%22%3A%22home%22%7D; [object Object]; localizacaoUsuario=%7B%22Coordenadas%22%3Anull%2C%22PermiteAutorizacao%22%3Afalse%2C%22Erro%22%3A1%2C%22MensagemErro%22%3A%22user%20did%20not%20share%20geolocation%20data%22%2C%22Accuracy%22%3Anull%7D; __RequestVerificationToken=i2BL5LrZIp09XTCpmYqNS1IX3FwgcaY4wFawnTve0X8I8r53n40qQxKNBDkvk7e4glAQV6INsyEHRxJ_jfnQ4l6sPbE1; origemDivLocalidade=caixabusca; EstadosModal=%5B%7B%22id%22%3A%22SP%22%2C%22text%22%3A%22Sao%20Paulo%22%7D%2C%7B%22id%22%3A%22RJ%22%2C%22text%22%3A%22Rio%20de%20Janeiro%22%7D%2C%7B%22id%22%3A%22MG%22%2C%22text%22%3A%22Minas%20Gerais%22%7D%2C%7B%22id%22%3A%22AC%22%2C%22text%22%3A%22Acre%22%7D%2C%7B%22id%22%3A%22AL%22%2C%22text%22%3A%22Alagoas%22%7D%2C%7B%22id%22%3A%22AP%22%2C%22text%22%3A%22Amapa%22%7D%2C%7B%22id%22%3A%22AM%22%2C%22text%22%3A%22Amazonas%22%7D%2C%7B%22id%22%3A%22BA%22%2C%22text%22%3A%22Bahia%22%7D%2C%7B%22id%22%3A%22CE%22%2C%22text%22%3A%22Ceara%22%7D%2C%7B%22id%22%3A%22DF%22%2C%22text%22%3A%22Distrito%20Federal%22%7D%2C%7B%22id%22%3A%22ES%22%2C%22text%22%3A%22Espirito%20Santo%22%7D%2C%7B%22id%22%3A%22GO%22%2C%22text%22%3A%22Goias%22%7D%2C%7B%22id%22%3A%22IN%22%2C%22text%22%3A%22Internacional%22%7D%2C%7B%22id%22%3A%22MA%22%2C%22text%22%3A%22Maranhao%22%7D%2C%7B%22id%22%3A%22MT%22%2C%22text%22%3A%22Mato%20Grosso%22%7D%2C%7B%22id%22%3A%22MS%22%2C%22text%22%3A%22Mato%20Grosso%20do%20Sul%22%7D%2C%7B%22id%22%3A%22PA%22%2C%22text%22%3A%22Para%22%7D%2C%7B%22id%22%3A%22PB%22%2C%22text%22%3A%22Paraiba%22%7D%2C%7B%22id%22%3A%22PR%22%2C%22text%22%3A%22Parana%22%7D%2C%7B%22id%22%3A%22PE%22%2C%22text%22%3A%22Pernambuco%22%7D%2C%7B%22id%22%3A%22PI%22%2C%22text%22%3A%22Piaui%22%7D%2C%7B%22id%22%3A%22RN%22%2C%22text%22%3A%22Rio%20Grande%20do%20Norte%22%7D%2C%7B%22id%22%3A%22RS%22%2C%22text%22%3A%22Rio%20Grande%20do%20Sul%22%7D%2C%7B%22id%22%3A%22RO%22%2C%22text%22%3A%22Rondonia%22%7D%2C%7B%22id%22%3A%22RR%22%2C%22text%22%3A%22Roraima%22%7D%2C%7B%22id%22%3A%22SC%22%2C%22text%22%3A%22Santa%20Catarina%22%7D%2C%7B%22id%22%3A%22SE%22%2C%22text%22%3A%22Sergipe%22%7D%2C%7B%22id%22%3A%22TO%22%2C%22text%22%3A%22Tocantins%22%7D%5D; CidadeLocalidadeModal=%5B%7B%22id%22%3A%22Zona%7CSAO%20PAULO%22%2C%22text%22%3A%22Capital%22%7D%2C%7B%22id%22%3A%22Bairro%7CAldeia%20da%20Serra%22%2C%22text%22%3A%22Aldeia%20da%20Serra%22%7D%2C%7B%22id%22%3A%22Bairro%7CAlphaville%20e%20Tambor%C3%A9%22%2C%22text%22%3A%22Alphaville%20e%20Tambor%C3%A9%22%7D%2C%7B%22id%22%3A%22Cidade%7CGrande%20S%C3%A3o%20Paulo%22%2C%22text%22%3A%22Grande%20S%C3%A3o%20Paulo%22%7D%2C%7B%22id%22%3A%22Bairro%7CGranja%20Vianna%20e%20Raposo%20Tavares%22%2C%22text%22%3A%22Granja%20Vianna%20e%20Raposo%20Tavares%22%7D%2C%7B%22id%22%3A%22Cidade%7CInterior%20de%20S%C3%A3o%20Paulo%22%2C%22text%22%3A%22Interior%20de%20S%C3%A3o%20Paulo%22%7D%2C%7B%22id%22%3A%22Cidade%7CLitoral%20Norte%22%2C%22text%22%3A%22Litoral%20Norte%22%7D%2C%7B%22id%22%3A%22Cidade%7CLitoral%20Sul%22%2C%22text%22%3A%22Litoral%20Sul%22%7D%2C%7B%22id%22%3A%22Cidade%7CRegi%C3%A3o%20de%20Campinas%22%2C%22text%22%3A%22Regi%C3%A3o%20de%20Campinas%22%7D%2C%7B%22id%22%3A%22Cidade%7CRegi%C3%A3o%20de%20Ribeir%C3%A3o%20Preto%22%2C%22text%22%3A%22Regi%C3%A3o%20de%20Ribeir%C3%A3o%20Preto%22%7D%2C%7B%22id%22%3A%22Cidade%7CRegi%C3%A3o%20de%20Sorocaba%22%2C%22text%22%3A%22Regi%C3%A3o%20de%20Sorocaba%22%7D%2C%7B%22id%22%3A%22Cidade%7CRegi%C3%A3o%20do%20ABC%22%2C%22text%22%3A%22Regi%C3%A3o%20do%20Abc%22%7D%2C%7B%22id%22%3A%22Cidade%7CVale%20do%20Para%C3%ADba%22%2C%22text%22%3A%22Vale%20do%20Para%C3%ADba%22%7D%5D; exibicao=L; utag_main=v_id:016a0e5e2f4300126852b1458c3603073001e06b0086e$_sn:5$_ss:0$_st:1555511796435$_pn:3%3Bexp-session$ses_id:1555509788737%3Bexp-session; transacao_caixabusca=locacao; troca_transacao=true; resultadoZeroTag=false; ResultadoBuscaVenda=true; _filbusc=V+1SgvBHHDd6wyl+X5/A4uhLRiSc586aPSg3qSikI+JtgAGmfaYYYiShOkVK6D0DaXhk8hfOKLWIs7LArKMyzmsFB52OCmNYYf3j1gixvt6B8HlrHnKQ3bkfXMY7XSo47JAlHijtIrEHh2Q0CzeOHmDwllq6K17aHCc6mjgJpfjdrZSmOlo9+Qj5ABHmRZkCyIxvqr4CNTspl8tp1/FuO6fzdvg5/okFnfTpmPjxcVB1xQ3r+G7P2WUZUBhZfcWb7uF1EunNXdlEV6JfeYwfXcg9OXKAsaC9dpfyXABCnvci5Jrw24HBxItwISoowij6fK4IxKTDebTX1TwfBcHMt9d5CqEoylWly58crCL681MF6WkL5vsRYtuGLSBDfDah8oXPIdwrvYXEx7U44dXArZOGo65bbMNPSktjadLoc/AblcFH/lEgY7lMQ6L8Tn8rhmGo08z+irOY0K8bKup01DMHzAEAYyGVcVdJhB3r0zoao41KJdZprQp78ojT7jYbD18trJ2+/Mt9sQ0dZTuiw3LJbWcfUFWt1QOXweC0+9BgnBnVN2M3rsv8FnnMe3tR7wa5SLxd0u5e/Eyo/SqkNO5K0MH+G0ih2TTaRJeOEeEb7qf054T5GLKxd/FooKs96nVH8pLfMATt3YByjq4V7UKvlrRLJD7d; _filalerta=V+1SgvBHHDd6wyl+X5/A4uhLRiSc586aPSg3qSikI+JtgAGmfaYYYiShOkVK6D0DaXhk8hfOKLUanTdDlQpNWmsFB52OCmNYnGpNlkRUYZrIjG+qvgI1O1iVzaidOGjmoKyz59hXh3AmXnQm+MnPww61ZQCHQ7UfcnIA/F7OaRox0EAi+fObyx0BB5+TV9kUKgzArO7LF0POgbsvEZl4iADsR5pCdBD7cbHIOcDGXJbUQdHxwJUe0CQs1W23/C3rS9AgFITXuBfoq9ps+jQEhcCVLmMROaApaFSeDGjt74plkUbG3J9vQA==; rec_nav_hist=%5B%2219181813%22%5D; tran_last_list=Locacao',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'

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