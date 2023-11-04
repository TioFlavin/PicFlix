import telebot
import json
from telebot import types

TOKEN = '6499682913:AAHcTt6H_ZxroGDSF5qt0PhosbpeHcOUzxo'
bot = telebot.TeleBot(TOKEN)

admin_id = '5479757526'

@bot.message_handler(commands=['start'])
def saudacao(message):
    bot.send_message(message.chat.id, "Bem-vindo ao seu bot de códigos! Use o comando /codigo para ver os códigos. do Sketchware")

@bot.message_handler(commands=['enviar'])
def enviar_codigo(message):
    if str(message.chat.id) == admin_id:
        bot.send_message(message.chat.id, "Por favor, envie o nome do código:")
        bot.register_next_step_handler(message, receber_nome_codigo)
    else:
        bot.send_message(message.chat.id, "Você não tem permissão para usar este comando.")

def receber_nome_codigo(message):
    nome_codigo = message.text
    bot.send_message(message.chat.id, f"Você deseja enviar um código chamado '{nome_codigo}'? Envie o código agora.")
    bot.register_next_step_handler(message, receber_codigo, nome_codigo)

def receber_codigo(message, nome_codigo):
    codigo = message.text
    try:
        with open('dados.json', 'r') as json_file:
            dados = json.load(json_file)
    except FileNotFoundError:
        dados = {}

    dados[nome_codigo] = codigo

    with open('dados.json', 'w') as json_file:
        json.dump(dados, json_file, indent=4)

    bot.send_message(message.chat.id, f"Código '{nome_codigo}' salvo com sucesso!")

# Manipulador para o comando /codigo
@bot.message_handler(commands=['codigo'])
def listar_codigos(message):
    try:
        with open('dados.json', 'r') as json_file:
            dados = json.load(json_file)

        if not dados:
            bot.send_message(message.chat.id, "Não há códigos na lista.")
        else:
            buttons = []
            for nome_codigo in dados:
                buttons.append(types.KeyboardButton(nome_codigo))

            # Dividir os botões em 3 colunas
            markup = types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True, resize_keyboard=True)
            markup.add(*buttons)

            bot.send_message(message.chat.id, "Escolha um código:", reply_markup=markup)
            bot.register_next_step_handler(message, enviar_codigo_selecionado, dados)
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Nenhum código encontrado.")

# Função para enviar o código selecionado
def enviar_codigo_selecionado(message, dados):
    codigo_selecionado = message.text
    if codigo_selecionado in dados:
        bot.send_message(message.chat.id, f"Código '{codigo_selecionado}':\n\n```\n{dados[codigo_selecionado]}\n```", parse_mode="Markdown", reply_markup=types.ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, "Código não encontrado.", reply_markup=types.ReplyKeyboardRemove())
        
        
@bot.message_handler(commands=['remove'])
def remover_codigo(message):
    if str(message.chat.id) == admin_id:
        try:
            with open('dados.json', 'r') as json_file:
                dados = json.load(json_file)

            buttons = []
            for nome_codigo in dados:
                buttons.append(types.KeyboardButton(nome_codigo))

            markup = types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True, resize_keyboard=True)
            markup.add(*buttons)

            bot.send_message(message.chat.id, "Escolha um código para remover:", reply_markup=markup)
            bot.register_next_step_handler(message, remover_codigo_nome, dados)
        except FileNotFoundError:
            bot.send_message(message.chat.id, "Nenhum código encontrado.")
    else:
        bot.send_message(message.chat.id, "Você não tem permissão para usar este comando.")

def remover_codigo_nome(message, dados):
    codigo_selecionado = message.text
    if codigo_selecionado in dados:
        del dados[codigo_selecionado]
        with open('dados.json', 'w') as json_file:
            json.dump(dados, json_file, indent=4)
        bot.send_message(message.chat.id, f"Código '{codigo_selecionado}' foi removido com sucesso.", reply_markup=types.ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, "Código não encontrado.", reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(commands=['help'])
def ajuda(message):
    if str(message.chat.id) == admin_id:
        bot.send_message(message.chat.id, "Aqui estão os comandos disponíveis:\n\n/enviar - Enviar um novo código\n/codigo - Listar códigos disponíveis\n/remove - Remover um código\n/help - Mostrar esta mensagem de ajuda")
    else:
        bot.send_message(message.chat.id, "Você não tem permissão para usar este comando.")

if __name__ == '__main__':
    bot.polling()