# IMPORTS

# from telegram_bot_calendar import WYearTelegramCalendar, STEP
import psycopg2
import telebot
from telebot import types
import requests
import json
from Singleton import Singleton
from datetime import date
from datetime import timedelta
# IMPORTS




ids_dict=Singleton()
bot=telebot.TeleBot('6493099407:AAEhqGdCO9WxUv0tjDn0eSh_6QG3vL3nn_c')
metric_post_api_key='eaf94a6b-a946-497d-888f-0d5f89cb2ae5'
leader_client_id='fce7f1d5-c662-4f8a-bf44-0915e81687e9'
leader_client_secret='kFpy0P3obIC6UPuafXC664gL41zo2P7n'
redirect_url='duskxd.pythonanywhere.com/auth'
get_access_token_url='https://apps.leader-id.ru/api/v1/oauth/token'
current_date_for_events = date.today()
last_date_for_events = date.today() + timedelta(days=14)
get_hot_point_events_url=('https://apps.leader-id.ru/api/v1/events/search?paginationPage=1&paginationSize=15&sort'
                          f'=popularity&dateFrom={current_date_for_events}&dateTo={last_date_for_events}&formats=&onlyActual=1&placeIds[]=1034')
create_events_url='https://leader-id.ru/events/'
moderator_id=1700929284
back_button_statement = ''



main_menu=types.ReplyKeyboardMarkup(row_width=2 , resize_keyboard=True)
menu1=types.KeyboardButton('Эксперты')
menu2=types.KeyboardButton('Новости')
menu3=types.KeyboardButton('Сайт')
menu4=types.KeyboardButton('Подать заявку на акселератор')
menu5=types.KeyboardButton('Записаться на мероприятие')
menu6=types.KeyboardButton('Техническая поддержка')
main_menu.add(menu1, menu2, menu3, menu4, menu5, menu6)

conn=psycopg2.connect(
    dbname="ppbot",
    user="postgres",
    password="DaS3VLQZ@IOp",
    host="127.0.0.1",
    port="5432"

)


def check_moder_status(user_id):
    cur=conn.cursor()
    cur.execute('SELECT status FROM admin_users WHERE user_id = %s', (user_id,))
    status=cur.fetchone()[0]
    cur.close()
    return status


@bot.message_handler(commands=['admin'])
def admin_panel(message):
    user_id=message.from_user.id
    if check_moder_status(user_id):

        buttons=types.ReplyKeyboardMarkup(resize_keyboard=True)
        items1=types.KeyboardButton('Посмотреть все запросы')
        items2=types.KeyboardButton('Сделать рассылку')
        items3=types.KeyboardButton('Меню')
        buttons.add(items1, items2, items3)
        msg=bot.send_message(message.chat.id, "Ты админ", reply_markup=buttons)
        bot.register_next_step_handler(msg, select_reqs)
    else:
        bot.reply_to(message, "Ты не админ")


def select_reqs(message):
    if message.text == 'Меню':
        bot.send_message(message.chat.id, f'Меню', reply_markup=main_menu)
    elif message.text == 'Сделать рассылку':
        msg = bot.send_message(message.chat.id, 'Напишите сообщение, которое хотите разослать пользователям')
        bot.register_next_step_handler(msg, sending_events)
    elif message.text == 'Посмотреть все запросы':
        cursor=conn.cursor()
        cursor.execute("SELECT req_text, req_id, user_id, req_user_chat_id FROM req_queue WHERE req_status = false")
        rows=cursor.fetchall()
        conn.commit()
        cursor.close()
        iterator=1

        for row in rows:
            ids_dict.add_id(iterator, int(row[3]))
            req_text=str(row[0])
            req_id=str(row[1])
            bot.send_message(message.chat.id, f'Активный запрос №{req_id}, text:{req_text}, ')
            iterator+=1
        msg=bot.send_message(message.chat.id, 'Напишите номер запроса, который хотите обработать')
        bot.register_next_step_handler(msg, get_req_id)


def get_req_id(message):
    request_id=message.text
    cursor=conn.cursor()
    cursor.execute("SELECT req_user_chat_id FROM req_queue WHERE req_id = %s", request_id)
    user_chat_id=cursor.fetchone()
    cursor.close()

    message=bot.send_message(message.chat.id, f'Напишите ответ пользователю')
    bot.register_next_step_handler(message, handle_messages, user_chat_id)

def sending_events(message):
    cur=conn.cursor()
    cur.execute('SELECT user_chat_id FROM users')
    chat_id_list=cur.fetchall()
    for ids in chat_id_list:
        chat_id=int(ids[0])
        bot.send_message(chat_id, f'{message.text}')

def handle_messages(message, user_chat_id):
    buttons=types.ReplyKeyboardMarkup(resize_keyboard=True)
    items1=types.KeyboardButton('Удалить запрос')
    back=types.KeyboardButton('Меню')
    buttons.add(items1, back)
    bot.send_message(int(user_chat_id[0]), message.text, reply_markup=buttons)


@bot.message_handler(commands=['news'])
def news(message):
    bot.send_message(message.chat.id, 'https://sbi.tusur.ru/#news')


@bot.message_handler(commands=['site', 'website'])
def site(message):
    bot.send_message(message.chat.id, 'https://sbi.tusur.ru')


@bot.message_handler(commands=['expert', 'expertlist', 'experts'])
def expert_areas(message):
    buttons=types.ReplyKeyboardMarkup(resize_keyboard=True)
    items1=types.KeyboardButton('Рынок и маркетинг')
    items2=types.KeyboardButton('Интеллектуальная собственность')
    items3=types.KeyboardButton('Юридические и бухгалтерские вопросы')
    items4=types.KeyboardButton('Технические вопросы по IT')
    items5=types.KeyboardButton('Экспертиза CustDev')
    items6=types.KeyboardButton('Инвестиции')
    back=types.KeyboardButton('Меню')
    buttons.add(items1, items2, items3, items4, items5, items6, back)
    bot.send_message(message.chat.id, 'Эксперты', reply_markup=buttons)


# def events_search(): cur_date = datetime.date.today() last_date = cur_date + datetime.timedelta(days=3) #return
# requests.get(f'https://apps.leader-id.ru/api/v1/events/search?dateFrom={cur_date}&dateTo={last_date}&placeIds[
# ]=1034&onlyWithActuralRegistration=0&participationFormat=person&onlyOffline=0&paginationPage=1&paginationSize=20')

@bot.message_handler(commands=['start'])
def start(message):
    cur = conn.cursor()
    cur.execute('INSERT INTO users (user_id, user_chat_id, user_name) VALUES (%s, %s, %s) ON CONFLICT (user_id) DO NOTHING',
                (message.from_user.id, message.chat.id, message.from_user.first_name))
    conn.commit()
    cur.close()
    bot.send_message(message.chat.id, f'Здарова, {message.from_user.first_name}!', reply_markup=main_menu)


@bot.message_handler(commands=['help'])
def start(message):
    bot.send_message(message.chat.id, f'Вот список команд бота:\n/expertlist\n/news\n/site\n/website\n')


@bot.message_handler(content_types=['text'])
def func_message(message):
    if message.chat.type == 'private':
        if message.text == "акселерация" or message.text == "аксель" or message.text == "акс":
            bot.send_message(message.chat.id,
                             'Акселератор - это программа по развитию предпринимательских талантов среди молодежи')
        elif message.text == "как подать заявку":
            bot.send_message(message.chat.id,
                             'Для того, чтобы подать заявку на акселерационную программу нужно собрать команду и '
                             'придумать идею для проекта. Подать можно здесь: ('
                             'https://startup-poligon.ru/accelerator)')
        elif message.text == "Удалить запрос":
            cur=conn.cursor()
            delete_row_id=message.from_user.id
            cur.execute("DELETE FROM req_queue WHERE user_id = %s", (delete_row_id,))
            conn.commit()
            bot.send_message(message.chat.id, f"Запрос удален")
        elif message.text == 'Эксперты':
            buttons=types.ReplyKeyboardMarkup(resize_keyboard=True)
            items1=types.KeyboardButton('Рынок и маркетинг')
            items2=types.KeyboardButton('Интеллектуальная собственность')
            items3=types.KeyboardButton('Юридические и бухгалтерские вопросы')
            items4=types.KeyboardButton('Технические вопросы по IT')
            items5=types.KeyboardButton('Экспертиза CustDev')
            items6=types.KeyboardButton('Инвестиции')
            back=types.KeyboardButton('Меню')
            buttons.add(items1, items2, items3, items4, items5, items6, back)
            bot.send_message(message.chat.id, 'Эксперты', reply_markup=buttons)
        elif message.text == 'Техническая поддержка':
            buttons=types.ReplyKeyboardMarkup(resize_keyboard=True)
            back=types.KeyboardButton('Меню')
            buttons.add(back)
            msg=bot.send_message(message.chat.id, 'Напишите ваш вопрос', reply_markup=buttons)
            bot.register_next_step_handler(msg, put_message_db)
        elif message.text == 'Подать заявку на акселератор':
            bot.send_message(message.chat.id,
                             f'Подать заявку на акселерацию можно тут:\nhttps://startup-poligon.ru/accelerator')
        # https: // startup - poligon.ru / accelerator
        elif message.text == 'Новости':
            buttons=types.ReplyKeyboardMarkup(resize_keyboard=True)
            items1=types.KeyboardButton('Новости СБИ ТУСУР')
            back=types.KeyboardButton('Меню')
            buttons.add(items1, back)
            bot.send_message(message.chat.id, 'Новости', reply_markup=buttons)
        elif message.text == 'Сайт':
            site(message)
        elif message.text == 'Новости СБИ ТУСУР':
            bot.send_message(message.chat.id, 'https://sbi.tusur.ru/#news')
        elif message.text == 'Меню':
            bot.send_message(message.chat.id, f'Меню', reply_markup=main_menu)
        elif message.text == 'Записаться на мероприятие':
            cur=conn.cursor()
            cur.execute('SELECT token_date FROM access_token')
            access_token_date = cur.fetchone()[0]
            cur.close()
            date_difference = date.today() - access_token_date
            if date_difference.days < 14:
                cur=conn.cursor()
                cur.execute('SELECT access_token FROM access_token')
                access_token = cur.fetchone()[0]
                cur.close()
                events_headers={'Authorization': f'Bearer {access_token}'}
                try:
                    get_events_response=requests.get(get_hot_point_events_url, headers=events_headers)
                except Exception:
                    bot.send_message(message.chat.id, 'Не удалось получить список мероприятий')
                if get_events_response.status_code == 200:
                    events=get_events_response.json()
                    events_ids=[event["id"] for event in events["items"]]
                    if len(events_ids)>0:
                        bot.send_message(message.chat.id, 'Вот список доступных мероприятий:')
                        for event in events_ids:
                            bot.send_message(message.chat.id, f'{create_events_url}{event}')
                    else:
                        bot.send_message(message.chat.id, 'Нет мероприятий на ближайшее время')
                else:
                    bot.send_message(message.chat.id, 'Ошибка в получении мероприятий')
            else:
                cur = conn.cursor()
                cur.execute('SELECT refresh_token FROM access_token')
                refresh_token = cur.fetchone()[0]
                refresh_data = {
                    'client_id': leader_client_id,
                    'client_secret': leader_client_secret,
                    'grant_type': 'refresh_token',
                    'refresh_token': refresh_token
                }
                try:
                    refresh_response=requests.post(get_access_token_url, json=refresh_data)
                except Exception:
                    bot.send_message(message.chat.id, 'Не удалось подключиться к Leader-id')
                if refresh_response.status_code == 200:
                    access_token=refresh_response.json()['access_token']
                    refresh_token=refresh_response.json()['refresh_token']
                    current_date = date.today()
                    cur=conn.cursor()
                    cur.execute(f'UPDATE access_token SET access_token = %s, refresh_token = %s, token_date = %s', (str(access_token), str(refresh_token), current_date))
                    conn.commit()
                    cur.close()

                    events_headers={'Authorization': f'Bearer {access_token}'}
                    try:
                        get_events_response=requests.get(get_hot_point_events_url, headers=events_headers)
                    except Exception:
                        bot.send_message(message.chat.id, 'Не удалось получить доступ к leader-id, попробуйте позже '
                                                          'или обратитесь в тех. поддержку')
                    if get_events_response.status_code == 200:
                        events=get_events_response.json()
                        events_ids=[event["id"] for event in events["items"]]
                        bot.send_message(message.chat.id, 'Вот список доступных мероприятий:')
                        for event in events_ids:
                            bot.send_message(message.chat.id, f'{create_events_url}{event}')
                    else:
                        bot.send_message(message.chat.id, f'Ошибка в получении мероприятий')
                else:
                    bot.send_message(message.chat.id, 'Ошибка аутентификации')
        elif message.text == 'Глеб Садыков':
            buttons=types.ReplyKeyboardMarkup(resize_keyboard=True)
            back_experts=types.KeyboardButton('Меню')
            buttons.add(back_experts)
            bot.send_message(message.chat.id,
                             f'Глеб Садыков: руководитель акселерационной программы, ментор. telegram id - @Nixxxy.\nДля записи на встречу с данным экспертом перейдите по ссылке: https://calendly.com/likhachevvasilii/vasilii-likhachev-meeting',
                             reply_markup=buttons)
        elif message.text == 'Валерия Цибульникова':
            buttons=types.ReplyKeyboardMarkup(resize_keyboard=True)
            items1=types.KeyboardButton('Записаться на встречу')
            back_experts=types.KeyboardButton('Меню')
            buttons.add(items1, back_experts)
            bot.send_message(message.chat.id,
                             f'Валерия Цибульникова: продвижение продукта. telegram id - @Valeriya_Ts70',
                             reply_markup=buttons)
        elif message.text == 'Мария Брусянина':
            buttons=types.ReplyKeyboardMarkup(resize_keyboard=True)
            items1=types.KeyboardButton('Записаться на встречу')
            back_experts=types.KeyboardButton('Меню')
            buttons.add(items1, back_experts)
            bot.send_message(message.chat.id,
                             f'Мария Брусянина: анализ рынка. telegram id - @Maria_brusyanina',
                             reply_markup=buttons)
        elif message.text == 'Валентина Мельникова':
            buttons=types.ReplyKeyboardMarkup(resize_keyboard=True)
            items1=types.KeyboardButton('Записаться на встречу')
            back_experts=types.KeyboardButton('Меню')
            buttons.add(items1, back_experts)
            bot.send_message(message.chat.id,
                             f'Валентина Мельникова: ???. telegram id - @Valentina_Melnikowa',  # Nyzhna informaciya
                             reply_markup=buttons)
        elif message.text == 'Галина Волкова':
            buttons=types.ReplyKeyboardMarkup(resize_keyboard=True)
            items1=types.KeyboardButton('Записаться на встречу')
            back_experts=types.KeyboardButton('Меню')
            buttons.add(items1, back_experts)
            bot.send_message(message.chat.id,
                             f'Галина Волкова: Директор центра бухгалтерских услуг'
                             f' "Баланс-Т". telegram id - @V1902gv',
                             reply_markup=buttons)
        elif message.text == 'Роман Кульшин':
            buttons=types.ReplyKeyboardMarkup(resize_keyboard=True)
            items1=types.KeyboardButton('Записаться на встречу')
            back_experts=types.KeyboardButton('Меню')
            buttons.add(items1, back_experts)
            bot.send_message(message.chat.id, f'Роман Кульшин: трекер, преприниматель,'
                                              f' резидент СБИ ТУСУР. telegram '
                                              f'id - @RomanGramor', reply_markup=buttons)
        elif message.text == 'Рынок и маркетинг':
            buttons=types.ReplyKeyboardMarkup(resize_keyboard=True)
            items1=types.KeyboardButton('Валерия Цибульникова')
            items2=types.KeyboardButton('Мария Брусянина')

            back_expertmenu=types.KeyboardButton('Меню')
            buttons.add(items1, items2, back_expertmenu)
            bot.send_message(message.chat.id, 'Рынок и маркетинг', reply_markup=buttons)
        elif message.text == 'Интеллектуальная собственность':
            buttons=types.ReplyKeyboardMarkup(resize_keyboard=True)
            items1=types.KeyboardButton('Валентина Мельникова')
            back_expertmenu=types.KeyboardButton('Меню')
            buttons.add(items1, back_expertmenu)
            bot.send_message(message.chat.id, 'Интеллектуальная собственность', reply_markup=buttons)
        elif message.text == 'Юридические и бухгалтерские вопросы':
            buttons=types.ReplyKeyboardMarkup(resize_keyboard=True)
            items1=types.KeyboardButton('Галина Волкова')

            back_expertmenu=types.KeyboardButton('Меню')
            buttons.add(items1, back_expertmenu)
            bot.send_message(message.chat.id, 'Юридические и бухгалтерские вопросы', reply_markup=buttons)
        elif message.text == 'Технические вопросы по IT':
            buttons=types.ReplyKeyboardMarkup(resize_keyboard=True)
            items1=types.KeyboardButton('Роман Кульшин')

            back_expertmenu=types.KeyboardButton('Меню')
            buttons.add(items1, back_expertmenu)
            bot.send_message(message.chat.id, 'Технические вопросы по IT', reply_markup=buttons)
        elif message.text == 'Экспертиза CustDev':
            buttons=types.ReplyKeyboardMarkup(resize_keyboard=True)
            items1=types.KeyboardButton('Глеб Садыков')

            back_expertmenu=types.KeyboardButton('Меню')
            buttons.add(items1, back_expertmenu)
            bot.send_message(message.chat.id, 'Экспертиза CustDev', reply_markup=buttons)
        elif message.text == 'Инвестиции':
            buttons=types.ReplyKeyboardMarkup(resize_keyboard=True)
            items1=types.KeyboardButton('Глеб Садыков')

            back_expertmenu=types.KeyboardButton('Меню')
            buttons.add(items1, back_expertmenu)
            bot.send_message(message.chat.id, 'Инвестиции', reply_markup=buttons)
        else:
            bot.send_message(message.chat.id, 'Данное сообщение не распознано, обратитесь в тех. поддержку')
def put_message_db(message):
    if message.text == "Меню":
        bot.send_message(message.chat.id, f'Меню', reply_markup=main_menu)
    else:
        cursor=conn.cursor()
        cursor.execute("INSERT INTO req_queue (user_id, req_text, req_user_chat_id) VALUES (%s, %s, %s)",
                       (message.from_user.id, message.text, message.chat.id))
        conn.commit()
        cursor.close()
        bot.send_message(message.chat.id, 'Ваш вопрос принят')
        bot.send_message(message.chat.id, f'Меню', reply_markup=main_menu)


bot.infinity_polling()
