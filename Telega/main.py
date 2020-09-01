# from telegram import Bot
# from telegram import Update
# from telegram.ext import CallbackContext
# from telegram.ext import CommandHandler
# from telegram.ext import ConversationHandler
# from telegram.ext import Updater
# from telegram.ext import Filters
# from telegram.ext import MessageHandler
#
# from Telega.validators import *
#
# NAME, GENDER, AGE = range(3)
#
#
# def start_handler(update: Update, context: CallbackContext):
#     update.message.reply_text(
#         text='Hello, what is your name?',
#     )
#
#     return NAME
#
#
# def name_handler(update: Update, context: CallbackContext):
#     # Получить имя
#     context.user_data[NAME] = update.message.text
#
#     genders = [f'{key} - {value}' for key, value in GENDER_MAP.items()]
#     genders = '\n'.join(genders)
#     update.message.reply_text(
#         f'''
# Gender?
# {genders}
# ''')
#     return GENDER
#
#
# def age_handler(update: Update, context: CallbackContext):
#
#     gender = validate_gender(text=update.message.text)
#     if gender is None:
#         update.message.reply_text('Input correct gender:')
#         return GENDER
#
#     context.user_data[GENDER] = gender
#
#     update.message.reply_text('Input your age: ')
#     return AGE
#
#
# def finish_handler(update: Update, context: CallbackContext):
#     # Получить возраст
#     age = validate_age(text=update.message.text)
#     if age is None:
#         update.message.reply_text('Input correct age!')
#         return AGE
#
#     context.user_data[AGE] = age
#
#     # TODO: save data into database
#
#     # Завершить диалог
#     update.message.reply_text(f'''
# Data saved!
# You: {context.user_data[NAME]}, gender: {gender_hru(context.user_data[GENDER])}, age: {context.user_data[AGE]}
# ''')
#     context.user_data.clear()
#     return ConversationHandler.END
#
#
# def cancel_handler(update: Update, context: CallbackContext):
#     """ Data lost!
#     """
#     update.message.reply_text('Cancel. Press /start to start again:)')
#     return ConversationHandler.END
#
#
# def echo_handler(update: Update, context: CallbackContext):
#     update.message.reply_text(
#         'Press /start to start:)',
#     )
#
#
# # def button_help_handler(update: Update, context: CallbackContext):
# #     update.message.reply_text(
# #         text='Hello, its help',
# #         reply_markup=ReplyKeyboardRemove(),
# #     )
#
# # def message_handler(update: Update, context: CallbackContext):
# #     text = update.message.text
# #     if text == button_help:
# #         return button_help_handler(update=update,context=context)
# #
# #     reply_markup = ReplyKeyboardMarkup(
# #         keyboard=[
# #             [
# #                 KeyboardButton(text=button_help),
# #             ],
# #         ],
# #         resize_keyboard=True
# #     )
# #
# #     update.message.reply_text(
# #         text='Hello, press the button',
# #         reply_markup=reply_markup,
# #     )
#
# def main():
#     print('Start')
#
#     bot = Bot(
#         token='1286048999:AAHn2LtAN5C5VjGvMo5WEi_dPqzoRmos1Jc',
#     )
#
#     updater = Updater(
#         bot=bot,
#         use_context=True,
#     )
#
#     conv_handler = ConversationHandler(
#         entry_points=[
#             CommandHandler('start', start_handler)
#         ],
#         states={
#             NAME: [
#                 MessageHandler(Filters.all, name_handler, pass_user_data=True)
#             ],
#             GENDER: [
#                 MessageHandler(Filters.all, age_handler, pass_user_data=True)
#             ],
#             AGE: [
#                 MessageHandler(Filters.all, finish_handler, pass_user_data=True)
#             ],
#         },
#         fallbacks=[
#             CommandHandler('cancel', cancel_handler)
#         ],
#     )
#
#     updater.dispatcher.add_handler(conv_handler)
#     updater.dispatcher.add_handler(
#         MessageHandler(filters=Filters.all, callback=echo_handler))
#
#     updater.start_polling()
#     updater.idle()
#
#     print('Finish')
#
#
# if __name__ == '__main__':
#     main()

import telebot
from telebot import types
import sqlite3
import secrets
from random import randint as rand
#from exps2 import exp
from links2 import link
from datetime import datetime
import pywaves as pw
import requests
import base58
from secret_phrase import *


def add_balance(id, amount, db, conn):
    sql = "UPDATE alco SET balance=? WHERE user_id=?"
    db.execute(sql, [float(balance(db, id)) + float(amount), id])
    conn.commit()


def new_user(msg):
    try:
        id = msg.chat.id
        start = msg.text
        conn = sqlite3.connect("gold_users.db")
        db = conn.cursor()
        sql = "SELECT user_id FROM alco"
        db.execute(sql)
        a = db.fetchall()
        sql = "SELECT used_id FROM banned"
        db.execute(sql)
        b = db.fetchall()
        dont_exist = True
        for i in range(len(a)):
            if id == a[i][0]:
                dont_exist = False
                break
        for i in range(len(b)):
            if id == b[i][0]:
                dont_exist = False
                bot.send_message(id, "Sorry, but you was banned")
                break
        if dont_exist:
            bot.send_message(id, exp["Hello!"][0], reply_markup=markup(0))
            ref = 0
            if len(start) > 6:
                try:
                    ref = int(start[7:])
                    sql = "SELECT user_id FROM alco"
                    db.execute(sql)
                    a = db.fetchall()
                    for i in range(len(a)):
                        if ref == a[i][0]:
                            add_balance(ref, 250, db, conn)
                            bot.send_message(ref, "affiliate bonus: +250")
                            db.execute("INSERT INTO alco VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                       [id, 250, None, 0, 0, 0, ref, None])
                except:
                    db.execute("INSERT INTO alco VALUES (?, ?, ?, ?, ?, ?, ?, ?)", [id, 250, None, 0, 0, 0, 0, None])
            else:
                db.execute("INSERT INTO alco VALUES (?, ?, ?, ?, ?, ?, ?, ?)", [id, 250, None, 0, 0, 0, 0, None])
            bot.send_message(354502298, "new user")
            conn.commit()
    except:
        pass


def write_bet(id, amount, db, conn):
    sql = "UPDATE alco SET current_number=? WHERE user_id=?"
    db.execute(sql, [float(amount), id])
    conn.commit()


def markup(lang):
    mark1 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    mark1.row(exp["make bet"][lang])
    mark1.row(exp["faucet"][lang])
    mark1.row(exp["balance"][lang])
    mark1.row(exp["settings"][lang])
    return mark1


def markup5(lang):
    mark5 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    mark5.row(exp["affiliate link"][lang])
    mark5.row(exp["language"][lang])
    mark5.row(exp["cancel"][lang])
    return mark5


def markup4(lang):
    mark4 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    #	mark4.row(exp["how it works"][lang])
    #	mark4.row(exp["claim"][lang])
    mark4.row(exp["cancel"][lang])
    return mark4


def bal_markup(lang):
    bmark = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    bmark.row(exp["deposit"][lang])
    bmark.row(exp["withdraw"][lang])
    bmark.row(exp["cancel"][lang])
    return bmark


def markup3(lang):
    mark3 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    mark3.row(exp["high"][lang])
    mark3.row(exp["low"][lang])
    mark3.row(exp["cancel"][lang])
    return mark3


def markup6(lang):
    mark6 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    #	mark4.row(exp["how it works"][lang])
    #	mark6.row(exp["link don't work"][lang])
    mark6.row(exp["cancel"][lang])
    return mark6


def markup8(lang):
    mark8 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    mark8.row(exp["check transactions"][lang])
    mark8.row(exp["my id"][lang], exp["deposit wallet"][lang])
    mark8.row(exp["cancel"][lang])
    return mark8


def balance(db, m_id):
    sql = "SELECT balance FROM alco WHERE user_id=?"
    db.execute(sql, [m_id])
    a = db.fetchall()
    return str(round(a[0][0], 8))


def beet(m_id, db, conn):
    sql = "SELECT current_number FROM alco WHERE user_id=?"
    db.execute(sql, [m_id])
    a = db.fetchall()
    return a[0][0]


def update_balance(amount, id, db, conn):
    sql = "UPDATE alco SET balance=? WHERE user_id=?"
    db.execute(sql, [float(balance(db, id)) + amount, id])
    conn.commit()


#	sql = "UPDATE alco SET balance=? WHERE user_id=900840378"
#	db.execute(sql, [float(balance(db, 900840378))-amount])
#	conn.commit()


def ban_user(his_id):
    conn = sqlite3.connect("gold_users.db")
    db = conn.cursor()
    sql = "DELETE FROM alco WHERE user_id=?"
    db.execute(sql, [his_id])
    db.execute("INSERT INTO banned VALUES (?)", [his_id])
    conn.commit()


def date_check(id, db, conn):
    date_now = int(datetime.utcnow().day)
    sql = "SELECT utc_date FROM date"
    db.execute(sql)
    date_was = db.fetchall()[0][0]
    if date_now != date_was:
        sql = "UPDATE date SET utc_date=?"
        db.execute(sql, [date_now])
        sql = "UPDATE alco SET date_check=?"
        db.execute(sql, [0])
        conn.commit()
    sql = "SELECT date_check FROM alco WHERE user_id=?"
    db.execute(sql, [id])
    dew = db.fetchall()[0][0]
    return dew


token = '1286048999:AAHn2LtAN5C5VjGvMo5WEi_dPqzoRmos1Jc'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def board(message):
    #	try:
    if True:
        new_user(message)
        try:
            print(message.chat.username + ": " + message.text)
        except:
            print(str(message.chat.id) + ": " + message.text)


#	except:
#		print("START ERROR")


markup2 = types.InlineKeyboardMarkup()
button1 = types.InlineKeyboardButton("\U0001F1F7" + "\U0001F1FA", callback_data="1")
button2 = types.InlineKeyboardButton("\U0001F1EC" + "\U0001F1E7", callback_data="0")
markup2.add(button1, button2)


@bot.callback_query_handler(func=lambda call: True)
def query_text(call):
    #	lst=list(users(call.message.chat.id)[0])
    conn = sqlite3.connect("gold_users.db")
    db = conn.cursor()
    sql = "UPDATE alco SET language=? WHERE user_id=?"
    db.execute(sql, [int(call.data), call.message.chat.id])
    conn.commit()
    if call.data == "0":  # en
        bot.send_message(call.message.chat.id, "Language successfully changed, bot is ready to go!",
                         reply_markup=markup(0))
    elif call.data == "1":  # ru
        bot.send_message(call.message.chat.id, "Язык успешно изменён, бот готов к использованию!",
                         reply_markup=markup(1))


@bot.message_handler(content_types=["text"])
# @bot.message_handler(regexp="text")
def repeat(message):
    id = message.chat.id
    set_zero1 = True
    set_zero2 = True
    set_zero3 = True

    try:
        print(message.chat.username + ": " + message.text)
    except:
        print(str(id) + ": " + message.text)

    conn = sqlite3.connect("gold_users.db")
    db = conn.cursor()

    sql = "SELECT used_id FROM banned"
    db.execute(sql)
    b = db.fetchall()
    not_banned = True
    for i in range(len(b)):
        if id == b[i][0]:
            bot.send_message(id, "Sorry, but you was banned")
            not_banned = False
            break
    #	try:
    if not_banned:

        #		conn=sqlite3.connect("gold_users.db")
        #		db=conn.cursor()
        try:
            text = message.text.lower()
            sql = "SELECT language FROM alco WHERE user_id=?"
            db.execute(sql, [id])
            lang = int(db.fetchall()[0][0])
            #		bot.send_message(354502298, lang)
            print(text)
            if text == exp["balance"][lang]:
                bot.send_message(id, exp["your balance"][lang] + ":\n" + balance(db, id), reply_markup=bal_markup(lang))
            elif text == exp["settings"][lang]:
                bot.send_message(id, exp["settings"][lang] + ":", reply_markup=markup5(lang))
            elif text == exp["language"][lang]:
                bot.send_message(id, exp["choose your language:"][lang], reply_markup=markup2)
            elif text == exp["make bet"][lang]:
                bot.send_message(id, exp["enter amount"][lang], reply_markup=markup4(lang))
            elif text == exp["cancel"][lang]:
                bot.send_message(id, exp["cancel"][lang], reply_markup=markup(lang))
            elif text == exp["affiliate link"][lang]:
                bot.send_message(id, exp["ref reward"][lang], reply_markup=markup(lang))
                bot.send_message(id, "t.me/goldmillion_dice_bot?start=" + str(id))
            elif text == exp["faucet"][lang]:
                print(1)
                aff = date_check(id, db, conn)
                if aff < 3:
                    rand_link = rand(0, len(link) - 1)
                    sql = "UPDATE alco SET faucet=? WHERE user_id=?"
                    db.execute(sql, [link[rand_link][1], id])
                    sql = "UPDATE alco SET date_check=? WHERE user_id=?"
                    db.execute(sql, [aff + 1, id])
                    conn.commit()
                    gif = open("animation.gif.mp4", "rb")
                    bot.send_document(id, gif)
                    bot.send_message(id, "[personal link](" + link[rand_link][0] + ")\n\n" + exp["your code:"][lang],
                                     parse_mode="Markdown", reply_markup=markup6(lang))
                    set_zero2 = False
                else:
                    bot.send_message(id, exp["try tomorrow"][lang], reply_markup=markup(lang))
            elif text == exp["withdraw"][lang]:
                sql = "UPDATE alco SET withdraw=? WHERE user_id=?"
                db.execute(sql, ["wait", id])
                conn.commit()
                set_zero3 = False
                bot.send_message(id, exp["your wallet"][lang], reply_markup=markup4(lang))
            elif text == exp["deposit"][lang]:
                bot.send_message(id, exp["deposit instruction"][lang], reply_markup=markup8(lang))
            elif text == exp["my id"][lang]:
                bot.send_message(id, str(id))
            elif text == exp["deposit wallet"][lang]:
                bot.send_message(id, "3PGQGQeq3gmFrKyUyyX38fyRmWYkvUcUD1C")
            elif text == exp["check transactions"][lang]:
                node_url = 'https://nodes.wavesnodes.com'
                address = '3PGQGQeq3gmFrKyUyyX38fyRmWYkvUcUD1C'
                limit = 1000
                sql = "SELECT after FROM date"
                db.execute(sql)
                before = db.fetchall()[0][0]
                transactions = requests.get(
                    f'{node_url}/transactions/address/{address}/limit/{limit}?before={before}').json()
                a = []
                for i in range(len(transactions[0])):
                    if transactions[0][i]["id"] != before:
                        if transactions[0][i]["type"] == 4 and transactions[0][i]["recipient"] == address and len(
                                transactions[0][i]["attachment"]) and transactions[0][i][
                            "assetId"] == "85Jc7CzxHBg9vNokztjyznpimvQv7AUJjxPDQ5Vywf2a":
                            try:
                                attachment = int(str(base58.b58decode(transactions[0][i]["attachment"]))[2:-1])
                                a += " "
                                a[len(a) - 1] = [attachment, transactions[0][i]["amount"] / 100000000]
                            except:
                                pass
                    else:
                        break
                check_send = True
                if len(a):
                    for i in range(len(a)):
                        try:
                            add_balance(a[i][0], a[i][1], db, conn)
                            if a[i][0] == int(id):
                                check_send = False
                            bot.send_message(a[i][0], "income transfer:\n+" + str(a[i][1]))
                            bot.send_message(a[i][0], exp["your balance"][lang] + ":\n" + balance(db, a[i][0]),
                                             reply_markup=bal_markup(lang))
                        except:
                            pass
                if check_send:
                    bot.send_message(id, exp["try later"][lang])
                sql = "UPDATE date SET after=?"
                db.execute(sql, [transactions[0][0]["id"]])
                conn.commit()




            elif text == exp["high"][lang] or text == exp["low"][lang]:
                try:
                    #			if True:
                    bet = beet(id, db, conn)
                    if bet > 0 and bet <= float(balance(db, id)):
                        if bet <= 1000000:
                            secret_number = secrets.randbelow(100)
                            if text == exp["high"][lang]:
                                if secret_number < 51:
                                    update_balance((-1) * bet, id, db, conn)
                                    bot.send_message(id, exp["lose"][lang] + "\n\n" + exp["your balance"][
                                        lang] + ":\n" + balance(db, id), reply_markup=markup(lang))
                                elif secret_number > 50:
                                    update_balance(bet, id, db, conn)
                                    bot.send_message(id, exp["win"][lang] + "\n\n" + exp["your balance"][
                                        lang] + ":\n" + balance(db, id), reply_markup=markup(lang))
                            elif text == exp["low"][lang]:
                                if secret_number > 48:
                                    update_balance((-1) * bet, id, db, conn)
                                    bot.send_message(id, exp["lose"][lang] + "\n\n" + exp["your balance"][
                                        lang] + ":\n" + balance(db, id), reply_markup=markup(lang))
                                elif secret_number < 49:
                                    update_balance(bet, id, db, conn)
                                    bot.send_message(id, exp["win"][lang] + "\n\n" + exp["your balance"][
                                        lang] + ":\n" + balance(db, id), reply_markup=markup(lang))
                            try:
                                add_balance(354502298, round(bet * 0.006, 8), db, conn)
                            except:
                                pass
                            try:
                                add_balance(972984750, round(bet * 0.006, 8), db, conn)
                            except:
                                pass
                            try:
                                add_balance(383025136, round(bet * 0.002, 8), db, conn)
                            except:
                                pass
                            try:
                                add_balance(849678522, round(bet * 0.002, 8), db, conn)
                            except:
                                pass
                            sql = "SELECT ref FROM alco WHERE user_id=?"
                            db.execute(sql, [id])
                            ref = db.fetchall()[0][0]
                            print(ref)
                            if ref != 0:
                                add_balance(ref, round(bet * 0.004, 8), db, conn)
                        else:
                            bot.send_message(id, "max bet: 1'000'000")
                    else:
                        bot.send_message(id, exp["incorrect amount"][lang], reply_markup=markup(lang))
                except:
                    bot.send_message(id, exp["enter amount of coins"][lang], reply_markup=markup(lang))

            elif text[:21] == 'admin_update_balance_' and (id == 354502298 or id == 972984750):
                add_balance(text[21:text.index("*")], text[text.index("*") + 1:], db, conn)
                bot.send_message(text[21:text.index("*")], "balance changed:\n" + text[text.index("*") + 1:])
            elif text[:11] == "admin_send_" and (id == 354502298 or id == 972984750):
                try:
                    conn = sqlite3.connect("gold_users.db")
                    cursor = conn.cursor()
                    sql = "SELECT user_id FROM alco"
                    cursor.execute(sql)
                    a = cursor.fetchall()
                    for i in range(len(a)):
                        try:
                            sql = "SELECT language FROM alco WHERE user_id=?"
                            db.execute(sql, [a[i][0]])
                            lang = int(db.fetchall()[0][0])
                            if lang == int(text[11]):
                                bot.send_message(int(a[i][0]), text[12:])
                        except:
                            print("нет(")
                except:
                    pass
            elif text[:10] == "admin_ban_" and (id == 354502298 or id == 972984750):
                ban_user(int(text[10:]))
                bot.send_message(int(text[10:]), "you was banned")
                bot.send_message(354502298, "user " + text[10:] + " was banned")
            elif text[:10] == "admin_air_" and (id == 354502298 or id == 972984750):
                try:
                    conn = sqlite3.connect("gold_users.db")
                    cursor = conn.cursor()
                    sql = "SELECT user_id FROM alco"
                    cursor.execute(sql)
                    a = cursor.fetchall()
                    for i in range(len(a)):
                        try:
                            add_balance(int(a[i][0]), text[10:], db, conn)
                            bot.send_message(int(a[i][0]), "balance changed:\n" + text[10:])
                        except:
                            print("нет(")
                except:
                    pass
            elif text[:7] == "admin5 " and id == 354502298:
                try:
                    sql = "UPDATE alco SET ref=? WHERE user_id=?"
                    db.execute(sql, [int(text[7:text.index("*")]), int(text[text.index("*") + 1:])])
                    conn.commit()
                    bot.send_message(int(text[7:text.index("*")]), "referral was added")
                    bot.send_message(354502298, "добавлено")
                except:
                    pass

            elif db.execute("SELECT withdraw FROM alco WHERE user_id=?", [id]).fetchall()[0][0] == "wait":
                try:
                    if pw.validateAddress(str(message.text)):
                        sql = "UPDATE alco SET withdraw=? WHERE user_id=?"
                        db.execute(sql, [str(message.text), id])
                        conn.commit()
                        set_zero3 = False
                        bot.send_message(id, exp["now enter amount:"][lang])
                        print(str(message.text))
                    else:
                        bot.send_message(id, "incorrect address")
                except:
                    bot.send_message(id, "incorrect address")


            else:
                try:
                    sql = "SELECT faucet FROM alco WHERE user_id=?"
                    db.execute(sql, [id])
                    if_num = db.fetchall()[0][0]
                    w_amount = None
                    if if_num == 0:
                        sql = "SELECT withdraw FROM alco WHERE user_id=?"
                        db.execute(sql, [id])
                        w_amount = db.fetchall()[0][0]
                        if w_amount == "wait":
                            w_amount = None
                    print(if_num)
                    print(w_amount)
                    if if_num != 0:
                        if str(if_num) == text:
                            add_balance(id, +3000, db, conn)
                            bot.send_message(354502298, "faucet")
                            bot.send_message(id, "balance changed:\n" + "+3000", reply_markup=markup(lang))
                            sql = "SELECT ref FROM alco WHERE user_id=?"
                            db.execute(sql, [id])
                            ref = db.fetchall()[0][0]
                            if ref != 0:
                                try:
                                    add_balance(ref, +1000, db, conn)
                                    bot.send_message(ref, "affiliate bonus:\n" + "+1000")
                                except:
                                    pass
                        else:
                            bot.send_message(id, exp["invalid code"][lang])
                    elif isinstance(w_amount, str):
                        if float(balance(db, id)) >= float(text) and float(text) > 5000:
                            try:
                                send_amount = int((float(text) - 5000) * 100000000)
                                bot.send_message(id, "wait a second...", reply_markup=None)
                                FDToken = pw.Asset("85Jc7CzxHBg9vNokztjyznpimvQv7AUJjxPDQ5Vywf2a")
                                myAddress = pw.Address(privateKey='secret_key')
                                recipient = pw.Address(str(w_amount))
                                myAddress.sendAsset(recipient, FDToken, send_amount,
                                                    attachment="payout from t.me/goldmillion_dice_bot")
                                add_balance(id, float(text) * (-1), db, conn)
                                bot.send_message(id, "success!", reply_markup=markup(lang))
                            except:
                                pass
                        else:
                            bot.send_message(id, "not enough coins")


                    else:
                        float(text)
                        write_bet(id, text, db, conn)
                        set_zero1 = False
                        bot.send_message(id, exp["bet: "][lang] + text, reply_markup=markup3(lang))
                except:
                    bot.send_message(id, exp["try again"][lang], reply_markup=markup(lang))

            if set_zero1:
                sql = "UPDATE alco SET current_number=? WHERE user_id=?"
                db.execute(sql, [None, id])
            if set_zero2:
                sql = "UPDATE alco SET faucet=? WHERE user_id=?"
                db.execute(sql, [0, id])
            if set_zero3:
                sql = "UPDATE alco SET withdraw=? WHERE user_id=?"
                db.execute(sql, [None, id])

            if set_zero1 or set_zero2 or set_zero3:
                conn.commit()
        except:
            pass


#	except:
#		print("error")

if __name__ == '__main__':
    bot.polling(none_stop=True)
