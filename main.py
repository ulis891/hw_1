from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler

TOKEN = '**********:***********************************'
bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(update.effective_chat.id,
                             f"Hello {update.effective_user.first_name}!")
    context.bot.send_message(update.effective_chat.id,
                             f"Введите, что будем делать:\n/r\t(записать новый контакт)\n/w\t(прочитать справочник)\n"
                             f"для записи добавьте через пробел 4 аргумента где:\n"
                             f"1 - фамилия\n"
                             f"2 - имя\n"
                             f"3 - телефон\n"
                             f"4 - описание")


def log(surname, name, tel, description):
    count = 0
    with open('DataBase/csvDB.csv', 'r', encoding='utf-8') as file:
        for row in file:
            count += 1
    with open('DataBase/csvDB.csv', 'a+', encoding='utf-8') as log:
        log.write(f'{count};{surname};{name};{tel};{description}\n')

    with open('DataBase/txtDB.txt', 'a+', encoding='utf-8') as file:
        file.write(f'{count}: surname: {surname}\nname: {name}\ntel: {tel}\ndescription: {description}\n\n')


def new_contact(update, context):

    surname, name, tel, description = context.args
    log(surname, name, tel, description)
    context.bot.send_message(update.effective_chat.id, f"Контакт {surname} записан")


def read(update, context):
    data_list = []
    data_text = ''
    action = context.args[0]
    print(action)
    if action == 'txt':
        with open('DataBase/txtDB.txt', encoding='utf-8') as file:
            for row in file:
                data_text += row
            data_all_list = data_text.split('\n')
            for i in range(0, len(data_all_list), 5):
                data_list.append(data_all_list[i:i + 5])
            for i in range(len(data_list)):
                context.bot.send_message(update.effective_chat.id, f'{data_list[i]}')
    elif action == 'csv':
        with open('DataBase/csvDB.csv',encoding='utf-8') as file:
            for row in file:
                context.bot.send_message(update.effective_chat.id, row)
    else:
        context.bot.send_message(update.effective_chat.id, 'Непонятно')


start_handler = CommandHandler('start', start)
write_handler = CommandHandler("w", new_contact)
read_handler = CommandHandler("r", read)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(write_handler)
dispatcher.add_handler(read_handler)

updater.start_polling()
updater.idle()
