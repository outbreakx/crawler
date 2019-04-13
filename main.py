from gerenciar_coleta import *
from config import VERSAO
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

acao = TipoAcao.lancamento
tipo = TipoResidencia.apartamento_padrao
onde = None
qnt_quartos = None
qnt_suites = None
qnt_vagas = None
area_util_minima = None
area_util_maxima = None

# pagina de inicio da procura...
pagina_inicial = 1
# se tiver -1, ele vai pesquisar todas as paginas com os parâmetros passados...
pagina_final = -1

# criamos a instancia de coleta
gerenciar = GerenciarColeta(acao=acao, tipo=tipo,onde=onde,qnt_quartos=qnt_quartos,qnt_suites=qnt_suites,qnt_vagas=qnt_vagas,area_util_minima=area_util_minima,area_util_maxima=area_util_maxima)
# iniciamos a coleta !
gerenciar.rodar(pagina_inicial=pagina_inicial,pagina_final=pagina_final)