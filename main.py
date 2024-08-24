from selenium import webdriver
from selenium.webdriver.common.by import By
from time import strftime as st
import json


# opt = webdriver.EdgeOptions()
# opt.add_argument("headless")
link = "https://pt.wikipedia.org/wiki/Laureados_com_o_Nobel_por_pa%C3%ADs"
driver = webdriver.Edge()#options=opt)#"msedgedriver.exe")
driver.get(link)
dados_detalhados = {}
paises = []
anos = []


def exportar_dados():
	global dados_detalhados
	data = f"{st('%Y')}{st('%m')}{st('%d')}{st('%H')}{st('%M')}"
	arq = open(f"{data}.json", "w")
	arq.write(json.dumps(dados_detalhados, indent=4))
	arq.close()


def tratar_dados(pais, dds):
	global dados_detalhados
	lista_ganhadores = dds.split("\n")
	dados_detalhados[pais] = {}
	for num_ganhador, ganhador in enumerate(lista_ganhadores):
		if len(ganhador.split(',')) < 3:
			continue
		nome = ganhador.split(",")[0]
		categoria = ganhador.split(",")[1]
		ano = ganhador.split(",")[2]

		dados_detalhados[pais][num_ganhador] = {}
		dados_detalhados[pais][num_ganhador]["nome"] = nome
		dados_detalhados[pais][num_ganhador]["categoria"] = categoria
		dados_detalhados[pais][num_ganhador]["ano"] = ano


def pegando_dados():
	global paises
	num_pais = 1
	acabou = False
	while not acabou:
		# Pegando o nome dos paises que possuem Prêmios Nobel
		try:
			pais = driver.find_element(By.XPATH, f'//*[@id="mw-content-text"]/div[1]/div[{num_pais}]').text
		except:
			acabou = True
		else:
			if "ver também" in pais.lower():
				acabou = True
			print(pais)
			paises.append(pais)

		# Pegando as informações dos ganhadores do Prêmio Nobel
		try:
			dados = driver.find_element(By.XPATH, f'//*[@id="mw-content-text"]/div[1]/ol[{num_pais}]').text
		except:
			acabou = True
		else:
			tratar_dados(pais, dados)


		num_pais += 1

pegando_dados()
exportar_dados()


# num_pais = 1
# while True:
# 	if not pegando_paises(num_pais):
# 		break
# 	num_pais += 1

# pais = 3
# pais_nome = driver.find_element(By.XPATH, f'//*[@id="mw-content-text"]/div[1]/div[{pais}]').text
# pais_premios = driver.find_element(By.XPATH, f'//*[@id="mw-content-text"]/div[1]/ol[{pais}]').text
# print(f'{pais_nome}')
# print(f'{pais_premios.split("\n")}')


driver.quit()

# //*[@id="mw-content-text"]/div[1]/div[2] > Pais
# //*[@id="mw-content-text"]/div[1]/div[3]
# //*[@id="mw-content-text"]/div[1]/ol[2] > Premios
# //*[@id="mw-content-text"]/div[1]/ol[3]

# Albânia
# ['Ferid Murad, Fisiologia ou Medicina, 1998. nasc. Whiting, EUA', 
#  'Madre Teresa de Calcutá, Paz, 1979. nasc. Uskub, Império Otomano, hoje Skopje, Macedónia do Norte']