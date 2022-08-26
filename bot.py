from ast import parse
import encodings
from encodings.utf_8 import encode
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

import requests as re
from bs4 import BeautifulSoup
import csv

# especifica a qual bot o código se refere (dentro dos parênteses está o token do bot)
updater = Updater("5589909898:AAGo3Bwcy2hZ6P6DrM0FSbQDxlg24tGptok",
                  use_context=True)

# mensagem de boas vindas que aparece quando o usuário iniciar a interação com o bot


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "O BSI_unirio_bot te dá boas vindas! Digite /ajuda para ver os comandos disponíveis.")

# mensagem com os comandos que o bot aceita (ex.: calendario, horarios...)
# A ALTERAR


def ajuda(update: Update, context: CallbackContext):
    update.message.reply_text("Your Message")


# mensagem que aparece se usuário digitar comando inválido
def desconhecido(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Desculpe, '%s' não é um comando válido." % update.message.text)

# mensagem que aparece se o usuário digitar algo que não é um comando
def texto_desconhecido(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Desculpe, eu não entendi, você falou: '%s'" % update.message.text)


# mensagem com o calendário academico
def calendario_mensagem(update: Update, context: CallbackContext):
    try:
        with open('calendario.csv', encoding='utf-8') as arq:
            leitor = csv.reader(arq, delimiter=',')
            lista_do_csv = list(leitor) # transforma o arquivo lido em uma lista
        lista_do_csv = [': '.join(linha) for linha in lista_do_csv]
        update.message.reply_text('\n\n'.join(lista_do_csv), parse_mode='html')
    except:
        update.message.reply_text('Calendario não atualizado. Digite /atualiza_calendario para obtê-lo')
        

# funcao para guardar os dados lidos do HTML em um arquivo csv
def atualiza_calendario(update: Update, context: CallbackContext):
    update.message.reply_text('Aguarde alguns segundos enquanto o calendario atualiza...')
    with open('calendario.csv', 'w', encoding='UTF8', newline='') as arq:
        escritor = csv.writer(arq)
        for linha in retorna_lista_datas():
            escritor.writerow(linha)
    update.message.reply_text('Calendario atualizado com sucesso! Digite /calendario para vê-lo')


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


# se usuário digitar o que está no primeiro parâmetro, a função do segundo parâmetro é rodada
updater.dispatcher.add_handler(CommandHandler('start', start))

updater.dispatcher.add_handler(CommandHandler('ajuda', ajuda))

updater.dispatcher.add_handler(
    CommandHandler('calendario', calendario_mensagem))

updater.dispatcher.add_handler(CommandHandler(
    'atualiza_calendario', atualiza_calendario))

updater.dispatcher.add_handler(MessageHandler(Filters.text, desconhecido))

updater.dispatcher.add_handler(MessageHandler(
    Filters.command, desconhecido))  # filtra comandos desconhecidos

updater.dispatcher.add_handler(MessageHandler(
    Filters.text, texto_desconhecido))  # filtra mensagens desconhecidas

updater.start_polling()
