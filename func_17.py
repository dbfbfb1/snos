from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import telebot
from telebot import types


bot = telebot.TeleBot('7702354813:AAHx7Tn5eQrV0j-EOKlHx1CBQSMTOgvKlg0')

@bot.message_handler(func=lambda message: True)

def send_welcome_17(message: types.Message, data):
    bot.send_message(message.chat.id, text='Введите юзернейм человека')
    bot.register_next_step_handler(message, get_username_17, data)

def get_username_17(message: types.Message, data):
    print(message.text)
    username = message.text
    # тут у вас то что ввел юзер
    bot.send_message(message.chat.id, text='Введите айди человека')
    bot.register_next_step_handler(message, get_id_17, username, data)


def get_id_17(message: types.Message, username, data):
    id = message.text
    bot.send_message(message.chat.id, text=f'Введите ссылку на чат')
    bot.register_next_step_handler(message, get_chat_link_17, id, username, data)


def get_chat_link_17(message: types.Message, username, id, data):
    chat_link = message.text
    bot.send_message(chat_id=message.chat.id, text=f'Введите ссылку на нарушение')
    bot.register_next_step_handler(message, get_violation_link_17, chat_link, id, username, data)

def send_email(receiver, sender_email, sender_password, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver
        msg['Subject'] = subject 
        msg.attach(MIMEText(body, 'plain'))  

        if 'gmail.com' in sender_email:
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
        elif 'protonmail.com' in sender_email:
            smtp_server = 'smtp.protonmail.com'
            smtp_port = 587
        elif 'mail.ru' in sender_email:
            smtp_server = 'smtp.mail.ru'
            smtp_port = 587
        elif 'rambler.ru' in sender_email or 'rambler.com' in sender_email:
            smtp_server = 'smtp.rambler.ru'
            smtp_port = 587  # SSL
        else:
            raise ValueError("Неподдерживаемый почтовый сервер.")

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  
        server.login(sender_email, sender_password) 
        server.sendmail(sender_email, receiver, msg.as_string())
        time.sleep(3)  
        server.quit()  

        return True

    except Exception as e:
        print(f"Ошибка при отправке электронной почты: {e}") 
        return False 

def get_violation_link_17(message: types.Message, username, chat_link, id, data):
    violation_link = message.text
    sent_emails = 0
    bot.send_message(message.chat.id, "Отлично, все данные собраны. Атака началась!")
    comp_texts = {
        "spam": f"Здравствуйте, уважаемая поддержка. На вашей платформе я нашел пользователя который отправляет много ненужных сообщений - СПАМ. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушения - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю.",
        "dox": f"Здравствуйте, уважаемая поддержка, на вашей платформе я нашел пользователя, который распространяет чужие данные без их согласия. его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение/нарушения - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его акккаунта.",
        "troll": f"Здравствуйте, уважаемая поддержка телеграм. Я нашел пользователя который открыто выражается нецензурной лексикой и спамит в чатах. его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение/нарушения - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его акккаунта.",
        "nark": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который продает и рекламирует наркотические вещества. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользоателю путем блокировки его аккаунта.",
        "curator": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который привлекает людей в сферу нарко-бизнеса. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировни его аккаунта.",
        "CPU": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который продает порнографические материалы с участием несовешеннолетних. Его юзернейм - {username}, его айди {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта.",
        "extortion": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который вымогает фото интимного характера у несовершенно летних, его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры к данному пользователю путем блокировки его аккаунта.",
        "oppression_nation": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который угнетает нацию и разжигает конфликты. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователб=ю путем блокировки его аккаунта.",
        "oppression_religion": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который угнетает религию и разжигает конфликты. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользоателю путем блокировки его аккаунта.",
        "dismemberment": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который распростроняет видео и фото шокирущего контента с убийством людей. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта.",
        "flaying": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который распростроняет видео и фото шокирующего контента с убийством животных. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта.",
        "pornography": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который распростроняет фото и видео порнографического типа. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта.",
        "pimp": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который продает услуги проституции. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта.",
        "suicide": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который отправляет сообщения которые приводят людей к суициду. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примине меры по отношению к данному пользователю путем блокировки его аккаунта.",
        "terrorist": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который отправляет сообщения с призывом к террризму. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта.",
        "swat": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который угрожает людям распростронением личной информации. Его юзернейи - {username}, его айди {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта.",
        "kill": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который угрожает людям расправой. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта."
    }
    for sender_email, sender_password in senders.items():
        for receiver in receivers:
            comp_text = comp_texts[data]
            comp_body = comp_text.format(username=username.strip(), id=id.strip(), chat_link=chat_link.strip(),
                                         violation_link=violation_link.strip())
            send_email(receiver, sender_email, sender_password, 'Жалоба на аккаунт телеграм', comp_body)
            print(f"Отправлено на {receiver} от {sender_email}!")
            sent_emails += 14888
            time.sleep(0.1)