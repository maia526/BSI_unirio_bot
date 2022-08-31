from ast import parse
from encodings.utf_8 import encode
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from datetime import datetime
import requests as re
from bs4 import BeautifulSoup
import csv

# especifica a qual bot o código se refere (dentro dos parênteses está o token do bot)
updater = Updater("5589909898:AAGo3Bwcy2hZ6P6DrM0FSbQDxlg24tGptok",
                  use_context=True)


# mensagem de boas vindas que aparece quando o usuário iniciar a interação com o bot
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "O BSI_unirio_bot te dá boas vindas! Acesse o menu ou apenas digite / para ver comandos.")


# enviando o fluxograma
def envia_fluxograma(update: Update, context: CallbackContext):
    update.message.reply_photo(
        'https://bsi.uniriotec.br/wp-content/uploads/sites/31/2020/06/fluxograma.png')


# capivara
def capivara(update: Update, context: CallbackContext):
    update.message.reply_photo(
        'https://pbs.twimg.com/media/FOkigT_XwAgQAM_?format=jpg&name=small')


# mensagem com os horarios por período
def horarios(update: Update, context:CallbackContext):
    with open('horarios.txt', encoding='utf-8') as arq:
        linhas = arq.readlines()
        update.message.reply_text(''.join(linhas), parse_mode='html')


# mensagem com o calendário academico
def calendario_mensagem(update: Update, context: CallbackContext):
    try:
        with open('calendario.csv', encoding='utf-8') as arq:
            leitor = csv.reader(arq, delimiter=',')
            # transforma o arquivo lido em uma lista
            lista_do_csv = list(leitor)
        lista_do_csv = [': '.join(linha) for linha in lista_do_csv]
        update.message.reply_text('\n\n'.join(lista_do_csv), parse_mode='html')
    except:
        update.message.reply_text(
            'Calendario não atualizado. Digite /atualiza_calendario para obtê-lo')


# funcao para guardar os dados lidos do HTML em um arquivo csv
def atualiza_calendario(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Aguarde alguns segundos enquanto o calendario atualiza...')
    with open('calendario.csv', 'w', encoding='UTF8', newline='') as arq:
        escritor = csv.writer(arq)
        for linha in retorna_lista_datas():
            escritor.writerow(linha)
    update.message.reply_text(
        'Calendario atualizado com sucesso! Digite /calendario para vê-lo')


def retorna_lista_datas():
    url = 'http://www.unirio.br/prograd/calendario-academico'
    r = re.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # segunda tabela é sobre o segundo período
    tabela = soup.findAll('table')[1]
    dados = tabela.findAll('td')  # todas as entradas de dados da tabela
    resultado = []  # lista de strings das linhas da tabela
    for i in range(0, len(dados), 2):
        resultado.append(
            ['<b>'+dados[i].text + '</b>', dados[i + 1].text.strip().strip()])
    # cada elemento da lista é uma linha da tabela
    return resultado


# retorna quandos dias faltam para o fim de 2022.2
def countdown(update: Update, context: CallbackContext):
    final = datetime.strptime('2023-02-13', '%Y-%m-%d')
    hoje = datetime.now()
    timedelta = final - hoje
    update.message.reply_text(
        f"Faltam {timedelta.days} dias para o fim de 2022.2!")


# se usuário digitar o que está no primeiro parâmetro, a função do segundo parâmetro é rodada
updater.dispatcher.add_handler(CommandHandler('start', start))

# envia calendario academico, se houver arquivo .csv
updater.dispatcher.add_handler(
    CommandHandler('calendario', calendario_mensagem))

# atualiza ou cria arquivo .csv com o calendario
updater.dispatcher.add_handler(CommandHandler(
    'atualiza_calendario', atualiza_calendario))

# envia o fluxograma
updater.dispatcher.add_handler(CommandHandler('fluxograma', envia_fluxograma))

# envia quantos dias faltam para o último dia do período
updater.dispatcher.add_handler(CommandHandler('falta', countdown))

# envia capivara
updater.dispatcher.add_handler(CommandHandler('capivara', capivara))

# envia horarios
updater.dispatcher.add_handler(CommandHandler('horarios', horarios))

updater.start_polling()
