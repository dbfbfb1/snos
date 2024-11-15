import datetime
import pprint
import smtplib
import sqlite3
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import telebot
from cryptopay import CryptoPay
from cryptopay import TESTNET
from cryptopay.types import Invoice
from telebot import types

bot = telebot.TeleBot('7584236727:AAGReJFPSrAGsbnlztiW2-HcGiz6YDyRwy0')
senders = {
    "bloody.snos@mail.ru": "B1iJdb8cLu45nKivsWRM"

}
help_text = f'''
    <strong>Наш ботнет — надёжное и быстрое решение для удаления аккаунтов, который постоянно обновляется.

Мы предлагаем мощность и интуитивно понятный интерфейс, доступный даже для новичков.

Наши низкие цены делают нас идеальным выбором для пользователей с ограниченным бюджетом.

Быстрая активация доступа сразу после покупки! Начните использовать преимущества ботнета без задержек.

Наши особенности:
 - Удобный интерфейс для простоты использования.
 - Высокая скорость сноса.
 - Значительная мощность для различных задач.</strong>
 
 Версия бота - 1.0
 Количество почт - 65
    '''
confirm_text_day = '''
Поздравляем с успешной подпиской! 🎉

Вы успешно оформили подписку на нашего сносера. Мы рады приветствовать вас! Вот что вам нужно знать:

Подробности вашей подписки:
- Тарифный план:  Сносер на 1 день
- Стоимость:  2$

Спасибо, что выбрали нас! Мы надеемся, что вы насладитесь преимуществами вашей подписки.

По вопросам обращаться к @sociaIov & @extradota

Чтобы подписка начала работать, перезапустите бота командой /start
'''

confirm_text_week = '''
Поздравляем с успешной подпиской! 🎉

Вы успешно оформили подписку на нашего сносера. Мы рады приветствовать вас! Вот что вам нужно знать:

Подробности вашей подписки:
- Тарифный план:  Сносер на 1 неделю
- Стоимость:  5$

Спасибо, что выбрали нас! Мы надеемся, что вы насладитесь преимуществами вашей подписки.

По вопросам обращаться к @sociaIov & @extradota

Чтобы подписка начала работать, перезапустите бота командой /start
'''

confirm_text_month = '''
Поздравляем с успешной подпиской! 🎉

Вы успешно оформили подписку на нашего сносера. Мы рады приветствовать вас! Вот что вам нужно знать:

Подробности вашей подписки:
- Тарифный план:  Сносер на 1 месяц
- Стоимость:  10$

Спасибо, что выбрали нас! Мы надеемся, что вы насладитесь преимуществами вашей подписки.

По вопросам обращаться к @sociaIov & @extradota

Чтобы подписка начала работать, перезапустите бота командой /start
'''

confirm_text_forever = '''
Поздравляем с успешной подпиской! 🎉

Вы успешно оформили подписку на нашего сносера. Мы рады приветствовать вас! Вот что вам нужно знать:

Подробности вашей подписки:
- Тарифный план:  Сносер навсегда
- Стоимость:  30$

Спасибо, что выбрали нас! Мы надеемся, что вы насладитесь преимуществами вашей подписки.

По вопросам обращаться к @sociaIov & @extradota

Чтобы подписка начала работать, перезапустите бота командой /start
'''
global username
global id
global register_time
global bool_subscribe
global balance
global quantity
db_file = "data__base.db"

receivers = ['sms@telegram.org',
             'dmca@telegram.org',
             'abuse@telegram.org',
             'sticker@telegram.org',
             'support@telegram.org',
             'snossocial@gmail.com'
             ]

API_KEY = "20003:AADJSeXxRnrO4MYZ6VLpvSkx7HXQy4R8VCk"
BOT_TOKEN = "7702354813:AAHx7Tn5eQrV0j-EOKlHx1CBQSMTOgvKlg0"

crypto_pay = cp = CryptoPay(API_KEY, TESTNET)
print("привет")
def create_table(db_file):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        user_id INTEGER UNIQUE,
        register_data TEXT
    )
    ''')

    cur.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cur.fetchall()]

    conn.commit()
    cur.close()
    conn.close()

    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    if 'subscribe_bool_day' not in columns:
        cur.execute('''
            ALTER TABLE users
            ADD COLUMN subscribe_bool_day INTEGER DEFAULT 0
        ''')
    else:
        print("Столбец subscribe_bool_day уже существует.")

    if 'subscribe_bool_week' not in columns:
        cur.execute('''
               ALTER TABLE users
               ADD COLUMN subscribe_bool_week INTEGER DEFAULT 0
           ''')
    else:
        print("Столбец subscribe_bool_week уже существует.")

    if 'subscribe_bool_month' not in columns:
        cur.execute('''
               ALTER TABLE users
               ADD COLUMN subscribe_bool_month INTEGER DEFAULT 0
           ''')
    else:
        print("Столбец subscribe_bool_month уже существует.")

    if 'subscribe_bool_forever' not in columns:
        cur.execute('''
               ALTER TABLE users
               ADD COLUMN subscribe_bool_forever INTEGER DEFAULT 0
           ''')
    else:
        print("Столбец subscribe_bool_forever уже существует.")

    if 'balance' not in columns:
        cur.execute('''
               ALTER TABLE users
               ADD COLUMN balance INTEGER DEFAULT 0
           ''')
    else:
        print("Столбец balance уже существует.")
    conn.commit()
    cur.close()
    conn.close()


def check_and_add_user(db_file, username, id, register_time):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    # Проверяем, существует ли пользователь по username или user_id
    cur.execute("SELECT * FROM users WHERE username = ? OR user_id = ?", (username, id))
    user = cur.fetchone()

    if user is not None:
        print(f"Пользователь с именем '{username}' или id '{id}' уже существует.")
    else:
        # Если пользователь не существует, добавляем его
        try:
            cur.execute("INSERT INTO users (username, user_id, register_data) VALUES (?, ?, ?)", (username, id, register_time))
            conn.commit()
            print(f"Пользователь '{username}' добавлен в базу данных.")
        except sqlite3.IntegrityError:
            print(f"Ошибка: пользователь с таким id '{id}' или именем '{username}' уже существует.")
        except Exception as e:
            print(f"Ошибка добавления пользователя: {e}")

    # Закрываем соединение
    cur.close()
    conn.close()




def get_invoice(invoice):
    get_invoice = invoice.paid_at
def create_invoice(amount: float, message) -> str:
    try:
        global invoice
        invoice = crypto_pay.create_invoice(asset='USDT', allow_anonymous=False, amount=amount, currency_type="crypto")
        pprint.pprint(invoice)
        username = message.from_user.username
        invoice.await_payment(user_id=message.from_user.id, message_id=message.message_id, username=username)
        return invoice.pay_url

    except Exception as e:
        print(f"Ошибка создания счета: {e}")
        return None

    conn.close()

def start_payment_process(chat_id, message):
    bot.send_photo(message.chat.id, photo=open('photo.jpg', 'rb'), caption="Пожалуйста, введите сумму счета")
    bot.register_next_step_handler_by_chat_id(chat_id, set_amount)


def set_amount(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id-1)
    try:
        amount = float(message.text)
        invoice_url = create_invoice(amount, message)
        if invoice_url:
            bot.send_photo(message.chat.id, photo=open('photo.jpg', 'rb'), caption=f"Новый одноразовый счет сгенерирован.\n\nДля оплаты воспользуйтесь ссылкой ниже\n\n{invoice_url}\n{invoice_url}\n{invoice_url}",
            parse_mode = 'html')
            print(get_invoice(invoice))
        else:
            bot.send_message(message.chat.id, "Не удалось создать счет.")
    except ValueError:
        bot.send_photo(message.chat.id, photo=open('photo.jpg', 'rb'),
                       caption="Ошибка при создании счета",
                       parse_mode='html')


@bot.message_handler(commands=['start'])
def command_start(message):
    id = message.from_user.id
    bot.delete_message(message.chat.id, message.message_id)
    username = message.from_user.username
    register_time = str(datetime.datetime.now().time())
    create_table(db_file)
    check_and_add_user(db_file, username, id, register_time)

    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    # Ищем пользователя по ID
    select_query = "SELECT subscribe_bool FROM users WHERE user_id = ?"
    cur.execute(select_query, (id,))
    result = cur.fetchone()

    if result:
        current_subscribe_bool = result[0]
    else:
        print("Пользователь не найден.")

    conn.commit()  # Сохраняем изменения в базе данных
    conn.close()
    markup = types.InlineKeyboardMarkup()
    main_button3 = types.InlineKeyboardButton('Информация о боте', callback_data="callback_main_button3")
    main_button1 = types.InlineKeyboardButton('Мой профиль', callback_data="callback_main_button1")
    if current_subscribe_bool == 0:
        main_button2 = types.InlineKeyboardButton('Подписка', callback_data="subscribe_button")
        markup.row(main_button2)
        markup.row(main_button1, main_button3)
    elif current_subscribe_bool == 1:
        button_snos = types.InlineKeyboardButton('Снос', callback_data="snos_button")
        markup.row(button_snos)
        markup.row(main_button1, main_button3)

    bot.send_photo(message.chat.id, photo=open('photo.jpg', 'rb'), caption="💻 Главное меню", reply_markup=markup)

@cp.polling_handler()
def handle_payment(
        invoice: Invoice,
        user_id: int,
        message_id: int,
        username: str # добавлен параметр username
) -> None:
    global balance
    balance = invoice.amount
    markup = types.InlineKeyboardMarkup()
    information_button_back = types.InlineKeyboardButton('Назад', callback_data='information_button_back_pay')
    markup.row(information_button_back)
    bot.send_photo(user_id, photo=open('photo.jpg', 'rb'),
                   caption=f"Вы оплатили счет на сумму: {invoice.amount} {invoice.asset}\nБлагодарим за оплату!",
                   reply_markup=markup)
    # Обновление баланса
    plus_user_balance(user_id, balance)
    return user_id# передаем username
def plus_user_balance(user_id: int, amount: float) -> None:
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    # Ищем пользователя по ID
    select_query = "SELECT balance FROM users WHERE user_id = ?"
    cur.execute(select_query, (user_id,))
    result = cur.fetchone()

    if result:
        current_balance = result[0]
        print(f"Текущий баланс пользователя с ID {user_id}: {current_balance}")

        # Суммируем новый баланс с текущим
        new_balance = (current_balance or 0) + amount

        update_query = "UPDATE users SET balance = ? WHERE user_id = ?"
        cur.execute(update_query, (new_balance, user_id))
        print(f"Баланс пользователя с ID {user_id} обновлен на {new_balance}.")
    else:
        print("Пользователь не найден.")

    conn.commit()  # Сохраняем изменения в базе данных
    conn.close()


def send_email(receiver, sender_email, sender_password, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Определение SMTP-сервера и порта
        if 'gmail.com' in sender_email:
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
        elif 'rambler.ru' in sender_email:
            smtp_server = 'smtp.rambler.ru'
            smtp_port = 587
        elif 'hotmail.com' in sender_email or 'outlook.com' in sender_email:
            smtp_server = 'smtp-mail.outlook.com'
            smtp_port = 587
        elif 'mail.ru' in sender_email:
            smtp_server = 'smtp.mail.ru'
            smtp_port = 587
        elif 'yandex.ru' in sender_email:
            smtp_server = 'smtp.yandex.ru'
            smtp_port = 587
        elif 'zoho.com' in sender_email:
            smtp_server = 'smtp.zoho.com'
            smtp_port = 587
        else:
            raise ValueError("Неподдерживаемый почтовый сервис")

        # Подключение и отправка письма
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver, msg.as_string())
        server.quit()

        return True
    except Exception as e:
        print(f"Произошла ошибка при отправке письма: {e}")
        return False

@bot.message_handler(func=lambda message: True)

def send_welcome(message: types.Message, data):
    bot.send_photo(message.chat.id, photo=open('photo.jpg', 'rb'), caption="Введите юзернейм человека")
    bot.register_next_step_handler(message, get_username, data)
def get_username(message: types.Message, data):
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)

    username = message.text
    bot.send_photo(message.chat.id, photo=open('photo.jpg', 'rb'), caption="Введите айди человека")

    bot.register_next_step_handler(message, get_id, username, data)

def get_id(message: types.Message, username, data):
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)
    print(data)
    if data == "session" or data == "virtual":
        id = message.text
        markup = types.InlineKeyboardMarkup()
        information_button_back = types.InlineKeyboardButton('Назад', callback_data='information_button_back')
        markup.row(information_button_back)
        bot.send_photo(message.chat.id, photo=open('photo.jpg', 'rb'), caption="Отлично, все данные собраны. Атака началась!", reply_markup=markup)
        sent_emails = 0
        comp_texts = {
            "session": f"3дравствуйте, уважаемая поддержка. Я случайно перешёл по ссылке, которая может быть фишинговой, и потерял доступ к своему аккаунту. Мой юзернейм - {username}, ID - {id}. Пожалуйста, помогите мне восстановить доступ или удалите аккаунт, если это возможно.",

            "virtual": f"Добрый день, поддержка Telegram! Я обратил внимание, что аккаунт с юзернеймом {username} и ID {id} использует виртуальный номер, который был приобретён через сервис по активации временных номеров. Этот номер не относится к владельцу аккаунта. Прошу вас рассмотреть эту ситуацию. Заранее спасибо!"
        }
        for i in range(10):
            for sender_email, sender_password in senders.items():
                for receiver in receivers:
                    comp_text = comp_texts[data]
                    comp_body = comp_text.format(username=username.strip(), id=id.strip())
                    send_email(receiver, sender_email, sender_password, 'Жалоба на аккаунт телеграм', comp_body)
                    print(f"Отправлено на {receiver} от {sender_email}!")
                    sent_emails += 1
                    time.sleep(3)
            print(sent_emails)
    else:
        id = message.text
        bot.send_photo(message.chat.id, photo=open('photo.jpg', 'rb'), caption="Введите ссылку на чат")
        bot.register_next_step_handler(message, get_chat_link, id, username, data)
def get_chat_link(message: types.Message, username, id, data):
    chat_link = message.text
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)
    bot.send_photo(message.chat.id, photo=open('photo.jpg', 'rb'), caption="Введите ссылку на нарушение")
    bot.register_next_step_handler(message, get_violation_link, chat_link, id, username, data)
def get_violation_link(message: types.Message, username, chat_link, id, data):
    violation_link = message.text
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)
    sent_emails = 0
    markup = types.InlineKeyboardMarkup()
    information_button_back = types.InlineKeyboardButton('Назад', callback_data='information_button_back')
    markup.row(information_button_back)
    bot.send_photo(message.chat.id, photo=open('photo.jpg', 'rb'), caption="Отлично, все данные собраны. Атака началась!", reply_markup=markup)
    comp_texts = {
        "nark": f"Здравствуйте, уважаемая поддержка Telegram. Я заметил пользователя с юзернеймом {username} и ID {id}, который может заниматься продажей запрещенных веществ. Ссылка на чат: {chat_link}, а ссылка на информацию о нарушении: {violation_link}. Прошу вас рассмотреть этот вопрос.",

        "curator": f"Здравствуйте, уважаемая поддержка Telegram. Обратил внимание на пользователя с юзернеймом {username} и ID {id}, который, кажется, привлекает людей в сомнительные дела. Ссылка на чат: {chat_link}, а ссылка на нарушения: {violation_link}. Буду благодарен за ваше внимание к этому вопросу.",

        "CPU": f"Здравствуйте, уважаемая поддержка Telegram. Я вижу, что пользователь с юзернеймом {username} и ID {id} может быть вовлечен в распространение неприемлемого контента с участием несовершеннолетних. Ссылка на чат: {chat_link}, а ссылка на нарушения: {violation_link}. Прошу вас проверить ситуацию.",

        "extortion": f"Здравствуйте, уважаемая поддержка Telegram. В чатах я обнаружил пользователя с юзернеймом {username} и ID {id}, который, похоже, вымогает личные фотографии у несовершеннолетних. Ссылка на чат: {chat_link}, а ссылка на нарушения: {violation_link}. Надеюсь, вы сможете рассмотреть этот вопрос.",

        "oppression_nation": f"Здравствуйте, уважаемая поддержка Telegram. Я заметил пользователя с юзернеймом {username} и ID {id}, который может разжигать конфликты и угнетать определенные группы. Ссылка на чат: {chat_link}, а ссылка на нарушения: {violation_link}. Прошу вас рассмотреть эту ситуацию.",

        "oppression_religion": f"Здравствуйте, уважаемая поддержка Telegram. Пользователь с юзернеймом {username} и ID {id} может разжигать напряженность в религиозных вопросах. Ссылка на чат: {chat_link}, а ссылка на нарушения: {violation_link}. Буду благодарен за ваше внимание к этому вопросу.",

        "dismemberment": f"Здравствуйте, уважаемая поддержка Telegram. Я нашел пользователя с юзернеймом {username} и ID {id}, который, похоже, распространяет жестокий контент. Ссылка на чат: {chat_link}, а ссылка на нарушения: {violation_link}. Прошу проверить эту ситуацию.",

        "flaying": f"Здравствуйте, уважаемая поддержка Telegram. Обратил внимание на пользователя с юзернеймом {username} и ID {id}, который может распространять шокирующие материалы о животных. Ссылка на чат: {chat_link}, а ссылка на нарушения: {violation_link}. Прошу вас обратиться к этому вопросу.",

        "pornography": f"Здравствуйте, уважаемая поддержка Telegram. Я заметил пользователя с юзернеймом {username} и ID {id}, который может распространять неприемлемый контент. Ссылка на чат: {chat_link}, а ссылка на нарушения: {violation_link}. Прошу вас рассмотреть это.",

        "pimp": f"Здравствуйте, уважаемая поддержка Telegram. Я заметил пользователя с юзернеймом {username} и ID {id}, который может предлагать сомнительные услуги. Ссылка на чат: {chat_link}, а ссылка на нарушения: {violation_link}. Прошу вас изучить данный случай.",

        "suicide": f"Здравствуйте, уважаемая поддержка Telegram. Я обнаружил пользователя с юзернеймом {username} и ID {id}, который отправляет сообщения, которые могут вызвать опасения по поводу самоубийства. Ссылка на чат: {chat_link}, а ссылка на нарушения: {violation_link}. Прошу вас обратить внимание на эту ситуацию.",

        "terrorist": f"Здравствуйте, уважаемая поддержка Telegram. Я нашел пользователя с юзернеймом {username} и ID {id}, который может отправлять сообщения с неприемлемым содержанием. Ссылка на чат: {chat_link}, а ссылка на нарушения: {violation_link}. Надеюсь, вы сможете рассмотреть этот вопрос.",

        "swat": f"Здравствуйте, уважаемая поддержка Telegram. Я заметил пользователя с юзернеймом {username} и ID {id}, который, возможно, угрожает раскрытием личной информации. Ссылка на чат: {chat_link}, а ссылка на нарушения: {violation_link}. Прошу вас рассмотреть ситуацию.",

        "kill": f"Здравствуйте, уважаемая поддержка Telegram. Я обнаружил пользователя с юзернеймом {username} и ID {id}, который может угрожать насилием. Ссылка на чат: {chat_link}, а ссылка на нарушения: {violation_link}. Прошу вас обратить внимание на эту ситуацию."
    }
    for i in range(10):

        for sender_email, sender_password in senders.items():
            for receiver in receivers:
                comp_text = comp_texts[data]
                comp_body = comp_text.format(username=username.strip(), id=id.strip(), chat_link=chat_link.strip(),
                                             violation_link=violation_link.strip())
                send_email(receiver, sender_email, sender_password, 'Жалоба на аккаунт телеграм', comp_body)
                print(f"Отправлено на {receiver} от {sender_email}!")
                sent_emails += 1
                time.sleep(3)
    print(sent_emails)

user_data = {}

# Шаблоны сообщений
comp_texts = {
    "channel_dox": "Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал, который распространяет личные данные невинных людей. Ссылка на канал - {channel_link}, ссылки на нарушения - {channel_violation}. Пожалуйста заблокируйте данный канал.",
    "channel_flaying": "Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который распространяет жестокое обращение с животными. Ссылка на канал - {channel_link}, ссылки на нарушения - {channel_violation}. Пожалуйста заблокируйте данный канал.",
    "channel_CPU": "Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который распространяет порнографию с участием несовершеннолетних. Ссылка на канал - {channel_link}, ссылки на нарушения - {channel_violation}. Пожалуйста заблокируйте данный канал.",
    "channel_price": "Здравствуйте, уважаемый модератор телеграмма. хочу пожаловаться вам на канал, который продает услуги доксинга, сваттинга. Ссылка на телеграмм канал: {channel_link} Ссылка на нарушение: {channel_violation} Просьба заблокировать данный канал.",
    "channel_dismemberment": "Здравствуйте, уважаемая поддержка Телеграмма. На вашей платформе я нашел канал который распространяет шокирующие кадры убийства людей. Ссылка на телеграмм канал: {channel_link} Ссылка на нарушение: {channel_violation} Просьба заблокировать данный канал.",
    "channel_casino": "Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который распространяет рулетки или же казино, которые запрещены на территории РФ статьей 171 УКРФ. Ссылка на телеграмм канал: {channel_link} Ссылка на нарушение: {channel_violation} Просьба заблокировать данный канал.",
    "channel_narko": "Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который пропагандирует продажу наркотических веществ, которые запрещены на территории РФ статьей 228.1 УКРФ. Ссылка на телеграмм канал: {channel_link} Ссылка на нарушение: {channel_violation} Просьба заблокировать данный канал.",
    "channel_terror": "Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который призывает людей к террору, что запрещено на территории РФ статьей 205.2 УКРФ. Ссылка на телеграмм канал: {channel_link} Ссылка на нарушение: {channel_violation} Просьба заблокировать данный канал.",
    "channel_suicide": "Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который призывает людей к суициду, что запрещено на территории РФ статьей 110.1 УКРФ. Ссылка на телеграмм канал: {channel_link} Ссылка на нарушение: {channel_violation} Просьба заблокировать данный канал.",
    "channel_hatred": "Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который разжигает ненависть в сторону определенных людей или же групп лиц. Ссылка на канал: {channel_link} Ссылка на нарушение: {channel_violation} Просьба заблокировать данный канал.",
    "channel_violence": "Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который пропагандирует насилие, что запрещено на территории РФ статьей 282 УКРФ. Ссылка на канал: {channel_link} Ссылка на нарушение: {channel_violation} Просьба заблокировать данный канал.",
    "channel_sell_CPU": "Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который занимается продажей детских интимных фото, что запрещено на территории РФ статьей 242.1 УКРФ. Ссылка на канал: {channel_link} Ссылка на нарушение: {channel_violation} Просьба заблокировать данный канал.",
    "channel_oppression_nation": "Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который пропагандирует угнетение нации, что запрещено на территории РФ статьей 282 УКРФ. Ссылка на канал: {channel_link} Ссылка на нарушение: {channel_violation} Просьба заблокировать данный канал.",
    "channel_oppression_religion": "Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который пропагандирует угнетение религии, что запрещено на территории РФ статьей 148 УКРФ. Ссылка на канал: {channel_link} Ссылка на нарушение: {channel_violation} Просьба заблокировать данный канал.",
    "channel_pornography": "Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который пропагандирует порнографические материалы. Ссылка на канал - {channel_link}, Ссылка на нарушение - {channel_violation}. Просьба заблокировать данный канал."
}

# Функция для получения ссылки на канал
def get_channel_link(message: types.Message, data):
    user_id = message.from_user.id
    user_data[user_id] = {'channel_link': None, 'channel_violation': None}

    bot.send_photo(message.chat.id, photo=open('photo.jpg', 'rb'), caption="Введите ссылку на канал")
    bot.register_next_step_handler(message, get_violation, user_id, data)

# Функция для получения ссылки на нарушение
def get_violation(message: types.Message, user_id, data):
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)

    user_data[user_id]['channel_link'] = message.text

    bot.send_photo(message.chat.id, photo=open('photo.jpg', 'rb'), caption="Введите ссылку на нарушение")
    bot.register_next_step_handler(message, get_good, user_id, data)

# Функция для получения дополнительных данных и отправки жалобы
def get_good(message: types.Message, user_id, data):
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)

    user_data[user_id]['channel_violation'] = message.text

    channel_link = user_data[user_id]['channel_link']
    channel_violation = user_data[user_id]['channel_violation']

    markup = types.InlineKeyboardMarkup()
    information_button_back = types.InlineKeyboardButton('Назад', callback_data='information_button_back')
    markup.row(information_button_back)

    bot.send_photo(message.chat.id, photo=open('photo.jpg', 'rb'), caption="Отлично, все данные собраны. Атака началась!", reply_markup=markup)

    comp_text = comp_texts.get(data, "Жалоба не найдена")
    comp_body = comp_text.format(channel_link=channel_link.strip(), channel_violation=channel_violation.strip())

    sent_emails = 0
    for i in range(10):
        for sender_email, sender_password in senders.items():
            for receiver in receivers:
                send_email(receiver, sender_email, sender_password, 'Жалоба на телеграм канал', comp_body)
                print(f"ОТПРАВЛЕНО НА {receiver} ОТ {sender_email}")
                sent_emails += 1
                time.sleep(5)
        print(sent_emails)
def minus_user_balance(user_id: int, amount: float) -> None:
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    # Ищем пользователя по ID
    select_query = "SELECT balance FROM users WHERE user_id = ?"
    cur.execute(select_query, (user_id,))
    result = cur.fetchone()

    if result:
        current_balance = result[0]
        print(f"Текущий баланс пользователя с ID {user_id}: {current_balance}")

        # Суммируем новый баланс с текущим
        new_balance = (current_balance or 0) - amount

        update_query = "UPDATE users SET balance = ? WHERE user_id = ?"
        cur.execute(update_query, (new_balance, user_id))
        print(f"Баланс пользователя с ID {user_id} обновлен на {new_balance}.")
    else:
        print("Пользователь не найден.")

    conn.commit()  # Сохраняем изменения в базе данных
    conn.close()


@bot.message_handler(commands=['help'])
def command_help(message):
    bot.delete_message(message.chat.id, message.message_id)
    markup = types.InlineKeyboardMarkup()
    information_button_back = types.InlineKeyboardButton('Назад', callback_data='information_button_back')
    markup.row(information_button_back)
    bot.send_photo(message.chat.id, photo=open('photo.jpg', 'rb'), caption="<strong>По всем вопросам обращайтесь к создателям\n\n\n@extradota</strong>", parse_mode='html', reply_markup=markup)


def get_user_balance(user_id: int) -> float:
    """
    Получить баланс пользователя по его ID.

    :param user_id: ID пользователя
    :return: Баланс пользователя или None, если пользователь не найден
    """
    # Открываем соединение с базой данных
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # SQL-запрос для получения значения balance
    select_query = "SELECT balance FROM users WHERE user_id = ?"

    cursor.execute(select_query, (user_id,))
    result = cursor.fetchone()

    # Проверяем результат и получаем баланс
    if result:
        balance = result[0]
        print(f"Баланс пользователя {user_id}: {balance}")
    else:
        print("Пользователь не найден.")
        balance = None

    # Закрытие соединения
    conn.close()

    return balance

@bot.callback_query_handler(func=lambda call: True)
def main_handle_query(callback):
    if callback.data == "information_button_back_pay":
        bot.delete_message(callback.message.chat.id, callback.message.message_id-1)
        command_start(callback.message)
    elif callback.data == "callback_main_button1":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        user_id = callback.from_user.id
        username = callback.from_user.username
        balance = get_user_balance(user_id)
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Запрос для получения даты регистрации пользователя по ID
        select_query = "SELECT register_data FROM users WHERE user_id = ?"

        # Выполнение запроса с передачей ID как параметра
        cursor.execute(select_query, (user_id,))

        # Извлечение результата
        result = cursor.fetchone()
        if result:
            register_time = result[0]
            print(f"Дата регистрации пользователя с ID {user_id}: {register_time}")
        else:
            register_time = None
            print("Пользователь не найден.")

        markup = types.InlineKeyboardMarkup()

        pay_balance_button = types.InlineKeyboardButton("Пополнить баланс", callback_data='pay_balance')
        information_button_back = types.InlineKeyboardButton('Назад', callback_data='information_button_back')

        markup.row(pay_balance_button, information_button_back)
        profile_text = f"Информация о вас: \n\nusername -> @{username} \nid -> {user_id} \nДата регистрации: {register_time[:8]} \nбаланс -> {balance}"

        bot.send_photo(callback.message.chat.id, photo=open('photo.jpg', 'rb'), caption=profile_text, reply_markup=markup)

    elif callback.data == "callback_main_button3":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        information_button_back = types.InlineKeyboardButton('Назад', callback_data='information_button_back')
        markup.row(information_button_back)
        bot.send_photo(callback.message.chat.id, photo=open('photo.jpg', 'rb'), caption=help_text, parse_mode='html', reply_markup=markup)

    elif callback.data == "subscribe_button":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        information_button_back = types.InlineKeyboardButton('Назад', callback_data='information_button_back')
        subscribe_button = types.InlineKeyboardButton('Купить подписку', callback_data='button_subscribe')
        markup.row(information_button_back, subscribe_button)
        subscribe_text = '''<strong>Подписка\n\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖\nВозможности сносера:\n1.Снос аккаунтов.\n2.Снос телеграмм каналов.\nБыстрая отправка писем.\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖\nЦены:\n\nПодписка на день - 2$\nПодписка на неделю - 5$\nПодписка на месяц - 10$\nПодписка навсегда - 30\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖</strong>
        '''
        bot.send_photo(callback.message.chat.id, photo=open('photo.jpg', 'rb'), caption=subscribe_text, parse_mode='html', reply_markup=markup)


    elif callback.data == "information_button_back":
        id = callback.from_user.id
        markup = types.InlineKeyboardMarkup()
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()

        # Ищем пользователя по ID
        select_query = "SELECT subscribe_bool FROM users WHERE user_id = ?"
        cur.execute(select_query, (id,))
        result = cur.fetchone()

        conn.commit()  # Сохраняем изменения в базе данных
        conn.close()
        if result:
            current_subscribe_bool = result[0]
        else:
            print("Пользователь не найден.")

        if current_subscribe_bool == 1:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
            button_snos = types.InlineKeyboardButton('Снос', callback_data="snos_button")
            main_button3 = types.InlineKeyboardButton('Информация о боте', callback_data="callback_main_button3")
            main_button1 = types.InlineKeyboardButton('Мой профиль', callback_data="callback_main_button1")
            markup.row(button_snos)
            markup.row(main_button1, main_button3)

        elif current_subscribe_bool == 0:
            command_start(callback.message)
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_photo(callback.message.chat.id, photo=open('photo.jpg', 'rb'), caption="💻 Главное меню", reply_markup=markup)

    elif callback.data == "button_subscribe":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        button_snos_account = types.InlineKeyboardButton("Подписка на день", callback_data='snos_day')
        button_snos_channel = types.InlineKeyboardButton("Подписка на неделю", callback_data='snos_week')
        information_button_back = types.InlineKeyboardButton('Назад', callback_data='information_button_back')
        markup.row(button_snos_channel, button_snos_account)
        markup.row(information_button_back)
        bot.send_photo(callback.message.chat.id, photo=open('photo.jpg', 'rb'), parse_mode='html', reply_markup=markup)

    elif callback.data == "pay_balance":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        global amount
        start_payment_process(callback.message.chat.id, callback.message)

    elif callback.data == "snos_week":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        user_id = callback.from_user.id
        balance = get_user_balance(user_id)
        if balance < 5:
            markup = types.InlineKeyboardMarkup()
            information_button_back = types.InlineKeyboardButton('Назад', callback_data='information_button_back')
            markup.row(information_button_back)
            bot.send_photo(callback.message.chat.id, photo=open('photo.jpg', 'rb'),
                           caption="У вас недостаточно средств",
                           parse_mode='html', reply_markup=markup)
        else:
            markup = types.InlineKeyboardMarkup()
            button_confirm = types.InlineKeyboardButton("Подтвердить", callback_data="confirm_button_week")
            information_button_back = types.InlineKeyboardButton('Назад', callback_data='information_button_back')
            markup.row(button_confirm)
            markup.row(information_button_back)
            bot.send_photo(callback.message.chat.id, photo=open('photo.jpg', 'rb'),
                           caption="Подтвердите выбор",
                           parse_mode='html', reply_markup=markup)

    elif callback.data == "snos_day":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        user_id = callback.from_user.id
        balance = get_user_balance(user_id)
        if balance < 2:
            markup = types.InlineKeyboardMarkup()
            information_button_back = types.InlineKeyboardButton('Назад', callback_data='information_button_back')
            markup.row(information_button_back)
            bot.send_photo(callback.message.chat.id, photo=open('photo.jpg', 'rb'),
                           caption="У вас недостаточно средств",
                           parse_mode='html', reply_markup=markup)
        else:
            markup = types.InlineKeyboardMarkup()
            button_confirm = types.InlineKeyboardButton("Подтвердить", callback_data="confirm_button_day")
            information_button_back = types.InlineKeyboardButton('Назад', callback_data='information_button_back')
            markup.row(button_confirm)
            markup.row(information_button_back)
            bot.send_photo(callback.message.chat.id, photo=open('photo.jpg', 'rb'),
                           caption="Подтвердите выбор",
                           parse_mode='html', reply_markup=markup)

    elif callback.data == "confirm_button_day":
        user_id = callback.from_user.id
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()

        # SQL-запрос для получения значения balance
        select_query = "SELECT subscribe_bool_day FROM users WHERE user_id = ?"

        cur.execute(select_query, (user_id,))
        result = cur.fetchone()

        if result:
            current_subscribe_bool_day = result[0]
        else:
            print("Пользователь не найден")

        if current_subscribe_bool_day == 1:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
            markup = types.InlineKeyboardMarkup()
            information_button_back = types.InlineKeyboardButton('Назад', callback_data='information_button_back')
            markup.row(information_button_back)
            bot.send_photo(callback.message.chat.id, photo=open('photo.jpg', 'rb'),
                           caption="Вы уже оформили подписку",
                           parse_mode='html', reply_markup=markup)
        else:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
            user_id = callback.from_user.id
            print(user_id)
            markup = types.InlineKeyboardMarkup()
            information_button_back = types.InlineKeyboardButton('Назад', callback_data='information_button_back')
            markup.row(information_button_back)
            bot.send_photo(callback.message.chat.id, photo=open('photo.jpg', 'rb'),
                           caption=confirm_text_day,
                           parse_mode='html', reply_markup=markup)
            minus_user_balance(user_id, 2)

            conn = sqlite3.connect(db_file)
            cur = conn.cursor()

            # SQL-запрос для получения значения balance
            select_query = "SELECT subscribe_bool_day FROM users WHERE user_id = ?"

            cur.execute(select_query, (user_id,))
            result = cur.fetchone()

            if result:
                current_subscribe_bool_day = result[0]
                print(f"Текущий значение подписки у пользователя с ID {user_id}: {current_subscribe_bool_day}")

                # Суммируем новый баланс с текущим
                new_subscribe_bool_day = (current_subscribe_bool_day or 0) + 1

                update_query = "UPDATE users SET subscribe_bool_day = ? WHERE user_id = ?"
                cur.execute(update_query, (new_subscribe_bool_day, user_id))
                print(f"значение подписки у пользователя с ID {user_id} обновлен на {new_subscribe_bool_day}.")
            else:
                print("Пользователь не найден.")
            conn.commit()  # Сохраняем изменения в базе данных
            conn.close()

            conn = sqlite3.connect(db_file)
            cur = conn.cursor()

            # SQL-запрос для получения значения balance
            select_query = "SELECT subscribe_bool FROM users WHERE user_id = ?"

            cur.execute(select_query, (user_id,))
            result = cur.fetchone()

        if result:
            current_subscribe_bool = result[0]
            print(f"Текущий значение подписки у пользователя с ID {user_id}: {current_subscribe_bool}")

            # Суммируем новый баланс с текущим
            new_subscribe_bool = (current_subscribe_bool or 0) + 1

            update_query = "UPDATE users SET subscribe_bool = ? WHERE user_id = ?"
            cur.execute(update_query, (new_subscribe_bool, user_id))
            print(f"значение подписки у пользователя с ID {user_id} обновлен на {new_subscribe_bool}.")
        else:
            print("Пользователь не найден.")
        conn.commit()  # Сохраняем изменения в базе данных
        conn.close()

    elif callback.data == "confirm_button_week":
        user_id = callback.from_user.id
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()

        # SQL-запрос для получения значения balance
        select_query = "SELECT subscribe_bool_week FROM users WHERE user_id = ?"

        cur.execute(select_query, (user_id,))
        result = cur.fetchone()

        if result:
            current_subscribe_bool_week = result[0]
        else:
            print("Пользователь не найден")

        if current_subscribe_bool_week == 1:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
            markup = types.InlineKeyboardMarkup()
            information_button_back = types.InlineKeyboardButton('Назад', callback_data='information_button_back')
            markup.row(information_button_back)
            bot.send_photo(callback.message.chat.id, photo=open('photo.jpg', 'rb'),
                           caption="Вы уже оформили подписку",
                           parse_mode='html', reply_markup=markup)
        else:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
            user_id = callback.from_user.id
            print(user_id)
            markup = types.InlineKeyboardMarkup()
            information_button_back = types.InlineKeyboardButton('Назад', callback_data='information_button_back')
            markup.row(information_button_back)
            bot.send_photo(callback.message.chat.id, photo=open('photo.jpg', 'rb'),
                           caption=confirm_text_week,
                           parse_mode='html', reply_markup=markup)
            minus_user_balance(user_id, 5)

            conn = sqlite3.connect(db_file)
            cur = conn.cursor()

            # SQL-запрос для получения значения balance
            select_query = "SELECT subscribe_bool_week FROM users WHERE user_id = ?"

            cur.execute(select_query, (user_id,))
            result = cur.fetchone()

            if result:
                current_subscribe_bool_week = result[0]
                print(f"Текущий значение подписки у пользователя с ID {user_id}: {current_subscribe_bool_week}")

                # Суммируем новый баланс с текущим
                new_subscribe_bool_week = (current_subscribe_bool_week or 0) + 1

                update_query = "UPDATE users SET subscribe_bool_week = ? WHERE user_id = ?"
                cur.execute(update_query, (new_subscribe_bool_week, user_id))
                print(f"значение подписки у пользователя с ID {user_id} обновлен на {new_subscribe_bool_week}.")
            else:
                print("Пользователь не найден.")
            conn.commit()  # Сохраняем изменения в базе данных
            conn.close()

            conn = sqlite3.connect(db_file)
            cur = conn.cursor()

            # SQL-запрос для получения значения balance
            select_query = "SELECT subscribe_bool FROM users WHERE user_id = ?"

            cur.execute(select_query, (user_id,))
            result = cur.fetchone()

        if result:
            current_subscribe_bool = result[0]
            print(f"Текущий значение подписки у пользователя с ID {user_id}: {current_subscribe_bool}")

            # Суммируем новый баланс с текущим
            new_subscribe_bool = (current_subscribe_bool or 0) + 1

            update_query = "UPDATE users SET subscribe_bool = ? WHERE user_id = ?"
            cur.execute(update_query, (new_subscribe_bool, user_id))
            print(f"значение подписки у пользователя с ID {user_id} обновлен на {new_subscribe_bool}.")
        else:
            print("Пользователь не найден.")
        conn.commit()  # Сохраняем изменения в базе данных
        conn.close()

    elif callback.data == "snos_button":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        snos_account_button = types.InlineKeyboardButton("Снос аккаунтов", callback_data="snos_account_data")
        snos_channel_button = types.InlineKeyboardButton("Снос каналов", callback_data="snos_channel_data")
        information_button_back = types.InlineKeyboardButton('Назад', callback_data='information_button_back')
        markup.row(snos_channel_button, snos_account_button)
        markup.row(information_button_back)
        bot.send_photo(callback.message.chat.id, photo=open('photo.jpg', 'rb'), caption="Выберите вариант сноса", parse_mode='html', reply_markup=markup)
    elif callback.data == "snos_channel_data":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        channel_button_dox = types.InlineKeyboardButton("С личными данными", callback_data="channel_dox")
        channel_button_flaying = types.InlineKeyboardButton("Живодерство", callback_data="channel_flaying")
        channel_button_CPU = types.InlineKeyboardButton("ЦП", callback_data="channel_CPU")
        channel_button_price = types.InlineKeyboardButton("Прайсы, био и т.д", callback_data="channel_price")
        channel_button_dismemberment = types.InlineKeyboardButton("Расчлененка", callback_data="channel_dismemberment")
        channel_button_casino = types.InlineKeyboardButton("Казино", callback_data="channel_casino")
        channel_button_narko = types.InlineKeyboardButton("Нарко-шоп", callback_data="channel_narko")
        channel_button_terror = types.InlineKeyboardButton("Призыв к террору", callback_data="channel_terror")
        channel_button_suicide = types.InlineKeyboardButton("Призыв к суициду", callback_data="channel_suicide")
        channel_button_hatred = types.InlineKeyboardButton("Разжигание ненависти", callback_data="channel_hatred")
        channel_button_violence = types.InlineKeyboardButton("Пропоганда насилия", callback_data="channel_violence")
        channel_button_sell_CPU = types.InlineKeyboardButton("Продажа ЦП", callback_data="channel_sell_CPU")
        channel_button_oppression_nation = types.InlineKeyboardButton("Угнетение нации", callback_data="channel_oppression_nation")
        channel_button_oppression_religion = types.InlineKeyboardButton("Угнетение религии", callback_data="channel_oppression_religion")
        channel_button_pornography = types.InlineKeyboardButton("С порнографии", callback_data="channel_pornography")
        information_button_back = types.InlineKeyboardButton('Назад', callback_data='information_button_back')

        markup.row(channel_button_dox, channel_button_flaying)
        markup.row(channel_button_CPU, channel_button_price)
        markup.row(channel_button_dismemberment, channel_button_casino)
        markup.row(channel_button_narko, channel_button_terror)
        markup.row(channel_button_suicide, channel_button_hatred)
        markup.row(channel_button_violence, channel_button_sell_CPU)
        markup.row(channel_button_oppression_nation, channel_button_oppression_religion)
        markup.row(channel_button_pornography)
        markup.row(information_button_back)
        bot.send_photo(callback.message.chat.id, photo=open('photo.jpg', 'rb'), caption="Выберите причину сноса",
                       parse_mode='html', reply_markup=markup)
    elif callback.data == "snos_account_data":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        account_button_spam = types.InlineKeyboardButton("Спам", callback_data="spam")
        account_button_dox = types.InlineKeyboardButton("Доксинг", callback_data="dox")
        account_button_troll = types.InlineKeyboardButton("Троллинг", callback_data="troll")
        account_button_nark = types.InlineKeyboardButton("Продажа/реклама наркотиков", callback_data="nark")
        account_button_curator = types.InlineKeyboardButton("Куратор в наркошопе", callback_data="curator")
        account_button_CPU = types.InlineKeyboardButton("Продажа цп", callback_data="CPU")
        account_button_extortion = types.InlineKeyboardButton("Сексуальное вымогательство", callback_data="extortion")
        account_button_oppression_nation = types.InlineKeyboardButton("Угнетение нации", callback_data="oppression_nation")
        account_button_oppression_religion = types.InlineKeyboardButton("Угнетение религии", callback_data="oppression_religion")
        account_button_dismemberment = types.InlineKeyboardButton("Распространение расчлененки", callback_data="dismemberment")
        account_button_flaying = types.InlineKeyboardButton("Распространение живодерства", callback_data="flaying")
        account_button_pornography = types.InlineKeyboardButton("Распространение порнографии", callback_data="pornography")
        account_button_pimp = types.InlineKeyboardButton("Продажа проституток", callback_data="pimp")
        account_button_suicide = types.InlineKeyboardButton("Призыв к суициду", callback_data="suicide")
        account_button_terrorist = types.InlineKeyboardButton("Призыв к террору", callback_data="terrorist")
        account_button_swat = types.InlineKeyboardButton("Угрозы сватом", callback_data="swat")
        account_button_kill = types.InlineKeyboardButton("Угрозы убийством", callback_data="kill")
        account_button_session = types.InlineKeyboardButton("Снос сессии", callback_data="session")
        account_button_virtual = types.InlineKeyboardButton("Виртуальный номер", callback_data="virtual")
        information_button_back = types.InlineKeyboardButton('Назад', callback_data='information_button_back')

        markup.row(account_button_spam, account_button_dox)
        markup.row(account_button_troll, account_button_nark)
        markup.row(account_button_curator, account_button_CPU)
        markup.row(account_button_extortion, account_button_oppression_nation)
        markup.row(account_button_oppression_religion, account_button_dismemberment)
        markup.row(account_button_flaying, account_button_pornography)
        markup.row(account_button_pimp, account_button_suicide)
        markup.row(account_button_terrorist, account_button_swat)
        markup.row(account_button_kill, account_button_session)
        markup.row(account_button_virtual)
        markup.row(information_button_back)
        bot.send_photo(callback.message.chat.id, photo=open('photo.jpg', 'rb'), caption="Выберите причину сноса", parse_mode='html', reply_markup=markup)
    elif callback.data == "channel_dox" or "channel_flaying" or "channel_CPU" or "channel_price" or "channel_dismemberment" or "channel_casino" or "channel_narko" or "channel_terror" or "channel_suicide" or "channel_hatred" or "channel_violence" or "channel_sell_CPU" or "channel_oppression_nation" or "channel_oppression_religion" or "channel_pornography":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        data = callback.data
        get_channel_link(callback.message, data)

    elif callback.data == "spam" or "dox" or "troll" or "nark" or "curator" or "CPU" or "extortion" or "oppression_nation" or "oppression_religion" or "dismemberment" or "flaying" or "pornography" or "pimp" or "suicide" or "terrorist" or "swat" or "kill":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        data = callback.data
    elif callback.data == "session" or "virtual":
        data = callback.data
        send_welcome_18(callback.message, data)

    else:
        bot.answer_callback_query(callback.id, "Неизвестный выбор")
    id = callback.from_user.id




crypto_pay.run_polling(bot.infinity_polling)
bot.polling()