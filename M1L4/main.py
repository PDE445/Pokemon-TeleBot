import telebot
import random
from config import token
from logic import Pokemon, battle  # ✅ Добавлен импорт функции battle

bot = telebot.TeleBot(token)

# --- Команда /go ---
@bot.message_handler(commands=['go'])
def go(message):
    username = message.from_user.username or message.from_user.first_name
    if username not in Pokemon.pokemons:
        pokemon = Pokemon(username)
        bot.send_message(message.chat.id, f"🎉 Поздравляю, {username}! Твой покемон создан!")
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "⚠️ У тебя уже есть покемон! Используй /info, чтобы посмотреть информацию.")

# --- Команда /info ---
@bot.message_handler(commands=['info'])
def info(message):
    username = message.from_user.username or message.from_user.first_name
    if username in Pokemon.pokemons:
        bot.send_message(message.chat.id, Pokemon.pokemons[username].info())
    else:
        bot.reply_to(message, "❌ У тебя пока нет покемона. Создай его командой /go")

# --- Команда /stats ---
@bot.message_handler(commands=['stats'])
def stats(message):
    username = message.from_user.username or message.from_user.first_name
    if username in Pokemon.pokemons:
        bot.send_message(message.chat.id, Pokemon.pokemons[username].show_stats())
    else:
        bot.reply_to(message, "❌ У тебя пока нет покемона. Создай его командой /go")

# --- Команда /levelup ---
@bot.message_handler(commands=['levelup'])
def levelup(message):
    username = message.from_user.username or message.from_user.first_name
    if username in Pokemon.pokemons:
        bot.send_message(message.chat.id, Pokemon.pokemons[username].level_up())
    else:
        bot.reply_to(message, "❌ У тебя пока нет покемона. Создай его командой /go")

# --- Команда /rename <новое имя> ---
@bot.message_handler(commands=['rename'])
def rename(message):
    username = message.from_user.username or message.from_user.first_name
    if username in Pokemon.pokemons:
        try:
            new_name = message.text.split(" ", 1)[1]
            bot.send_message(message.chat.id, Pokemon.pokemons[username].rename(new_name))
        except IndexError:
            bot.reply_to(message, "⚠️ Используй формат: /rename <новое имя>")
    else:
        bot.reply_to(message, "❌ У тебя пока нет покемона. Создай его командой /go")

# --- Команда /add_ability <способность> ---
@bot.message_handler(commands=['add_ability'])
def add_ability(message):
    username = message.from_user.username or message.from_user.first_name
    if username in Pokemon.pokemons:
        try:
            ability = message.text.split(" ", 1)[1]
            bot.send_message(message.chat.id, Pokemon.pokemons[username].add_ability(ability))
        except IndexError:
            bot.reply_to(message, "⚠️ Используй формат: /add_ability <название способности>")
    else:
        bot.reply_to(message, "❌ У тебя пока нет покемона. Создай его командой /go")


# ✅ --- Новая команда /attack ---
@bot.message_handler(commands=['attack'])
def attack_handler(message):
    # Проверяем, что сообщение отправлено в ответ на другое
    if not message.reply_to_message:
        bot.reply_to(message, "⚠️ Чтобы атаковать, ответь командой /attack на сообщение другого игрока.")
        return

    attacker = message.from_user.username or message.from_user.first_name
    defender = message.reply_to_message.from_user.username or message.reply_to_message.from_user.first_name

    if not attacker or not defender:
        bot.reply_to(message, "❌ У одного из игроков отсутствует username.")
        return

    # Проверяем наличие покемонов
    if attacker not in Pokemon.pokemons:
        bot.reply_to(message, f"😢 У @{attacker} нет покемона! Используй /go чтобы создать.")
        return
    if defender not in Pokemon.pokemons:
        bot.reply_to(message, f"😢 У @{defender} нет покемона! Используй /go чтобы создать.")
        return

    # Получаем покемонов
    attacker_pokemon = Pokemon.pokemons[attacker]
    defender_pokemon = Pokemon.pokemons[defender]

    # Проводим бой
    result = battle(attacker_pokemon, defender_pokemon, attacker, defender)

    # Отправляем результат боя
    bot.send_message(message.chat.id, result, parse_mode="HTML")


# --- Подсказка по командам ---
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id,
    "🕹 Доступные команды:\n"
    "/go — создать покемона\n"
    "/info — информация о покемоне\n"
    "/stats — характеристики покемона\n"
    "/levelup — повысить уровень\n"
    "/rename <имя> — переименовать покемона\n"
    "/add_ability <способность> — добавить способность\n"
    "/attack — атаковать другого игрока (ответь на его сообщение)\n"
    "/help — показать список команд")

# --- Запуск бота ---
print("✅ Бот запускается... ждём команды от Telegram")
bot.infinity_polling(none_stop=True)
