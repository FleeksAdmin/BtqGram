from telethon import TelegramClient, events
from colorama import Fore, Style, init
import os
import asyncio
import pyfiglet
from PIL import Image
import requests
from io import BytesIO

# Инициализация colorama
init()

# Ваши данные
api_id = '20716443'
api_hash = 'e5fefd8855258209a2968b62ebca7583'
phone_number = 'YOUR_PHONE_NUMBER'  # Ваш номер телефона в международном формате

client = TelegramClient('session_name', api_id, api_hash)

async def send_message(entity, text):
    await client.send_message(entity, text)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_pepe():
    # Виведемо зображення жаби Пепе
    pepe_url = "https://i.imgur.com/7X58l0A.png"  # URL зображення Пепе
    response = requests.get(pepe_url)
    img = Image.open(BytesIO(response.content))
    img.show()  # Відкрити зображення

async def main():
    await client.start(phone_number)

    # Слушатель для получения удалённых сообщений
    @client.on(events.MessageDeleted)
    async def handler(event):
        chat_id = event.chat_id
        deleted_messages = event.messages
        for message_id in deleted_messages:
            try:
                message = await client.get_messages(chat_id, ids=message_id)
                deleted_message_text = message.text
            except Exception as e:
                deleted_message_text = "Сообщение не найдено или удалено"
            
            saved_messages = await client.get_entity('me')  # Сохранённые сообщения
            await send_message(saved_messages, f"Удалённое сообщение в чате {chat_id}: {deleted_message_text}")

    clear_screen()
    
    # Выводим баннер
    print(Fore.RED + Style.BRIGHT + 'BTQGRAM' + Style.RESET_ALL)
    
    # Используем pyfiglet для создания ASCII-арта
    cvss_art = pyfiglet.figlet_format("CVSS")
    print(Fore.RED + Style.BRIGHT + cvss_art + Style.RESET_ALL)
    
    print(Style.BRIGHT + "ART" + Style.RESET_ALL)

    # Виводимо жабу Пепе
    display_pepe()
    
    # Основное меню
    print(Fore.RED + Style.BRIGHT + "1. НАПИСАТЬ ЧЕЛУ (ЮЗ)" + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + "2. НАПИСАТЬ ЧЕЛУ (ЛИСТ)" + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + "3. ПОИСК" + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + "4. ЗАБЛОКИРОВАТЬ (ЛИСТ)" + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + "5. ЗАБЛОКИРОВАТЬ (ЮЗ)" + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + "ВЫБЕРИТЕ ОПЦИЮ:" + Style.RESET_ALL)

    while True:
        option = input("Ваш выбор: ")
        if option == '1':
            user = input("Введите ID пользователя: ")
            text = input("Введите сообщение для отправки: ")
            await send_message(user, text)
        elif option == '2':
            dialogs = await client.get_dialogs()
            for i, dialog in enumerate(dialogs):
                print(f"{i}. {dialog.name}")
            choice = int(input("Выберите чат (цифра): "))
            chat = dialogs[choice]
            await show_chat(chat)
        elif option == '3':
            query = input("Что вы ищете?: ")
            # Добавить функцию поиска
        elif option == '4':
            # Реализация блокировки чатов
            pass
        elif option == '5':
            # Реализация блокировки пользователей
            pass
        else:
            print(Fore.RED + "Неверный выбор. Попробуйте еще раз." + Style.RESET_ALL)

async def show_chat(chat):
    clear_screen()
    
    print(Fore.RED + Style.BRIGHT + 'BTQGRAM' + Style.RESET_ALL)
    
    messages = await client.get_messages(chat, limit=50)
    
    for message in messages:
        print(Fore.WHITE + Style.BRIGHT + f"{message.sender_id}: {message.text}" + Style.RESET_ALL)
    
    print(Fore.WHITE + Style.BRIGHT + "ПОСМОТРЕТЬ ВСЕ СООБЩЕНИЯ [1]" + Style.RESET_ALL)
    print(Fore.WHITE + Style.BRIGHT + "СМОТРЕТЬ ДАЛЕЕ [2]" + Style.RESET_ALL)
    print(Fore.WHITE + Style.BRIGHT + "НАПИСАТЬ СООБЩЕНИЯ [3]" + Style.RESET_ALL)
    print(Fore.WHITE + Style.BRIGHT + "ВЫЙТИ ИЗ ЧАТА [4]" + Style.RESET_ALL)
    
    choice = input("Выберите опцию: ")

    if choice == '1':
        await view_all_messages(chat)
    elif choice == '2':
        # Добавить логику для просмотра следующей группы сообщений
        print("Функция еще не реализована.")
    elif choice == '3':
        text = input("Введите сообщение для отправки: ")
        await send_message(chat, text)
    elif choice == '4':
        return  # Вернуться в основное меню

async def view_all_messages(chat):
    clear_screen()
    print(Fore.RED + Style.BRIGHT + 'BTQGRAM' + Style.RESET_ALL)

    messages = await client.get_messages(chat)
    for message in messages:
        print(Fore.WHITE + Style.BRIGHT + f"{message.sender_id}: {message.text}" + Style.RESET_ALL)

    print(Fore.WHITE + "Нажмите любую клавишу, чтобы вернуться назад...")
    input()

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
