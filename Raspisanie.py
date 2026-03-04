# from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# from util import *
# import json
import asyncio
import requests
from aiogram.filters import Command
from aiogram import Bot, Dispatcher, types
from pygame.midi import frequency_to_midi

TELEGRAMM_TOKEN = '8387589572:AAElhVRAF1oDoER0xU_Zm0VJUyVghy36p4Q'
YANDEX_API_KEY = '78e31b76-59ca-424b-b5bb-b048465dac76'

bot = Bot(token=TELEGRAMM_TOKEN)
dp =Dispatcher()


#API Yandex запрос
def get_scheldule(from_code, to_code, date = None):
    from_code: 's9744205'
    to_code: 's9737109'
    url = "https://api.rasp.yandex-net.ru/v3.0/search/"
    params = {
        "apikey": YANDEX_API_KEY,
        "from": from_code,
        "to": to_code,

    }
    if date:
        params['date'] = date

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        date = response.json()
        return date.get("segments", [])
    except Exception as e:
        print(f"Error API: {e}")
        return None

@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот расписания.\n"
        "Используй команду /rasp <код_откуда> <код_куда> [дата]\n"
        "Например: /rasp s9600213 s9601723 2024-12-20")

@dp.message(Command('rasp'))
async def cmd_rasp(message: types.Message):
    args = message.text.split()
    if len(args) < 3:
        await message.answer("Ошибка: Укажите код отправления и прибытия. \nПример: rasp s9600213 s9601723")
        return
    from_code = args[1]
    to_code = args[2]
    date = args[3] if len(args) > 3 else None

    await message.answer("Ищу расписание...")

    segments = get_scheldule(from_code, to_code, date)

    if segments is None:
        await message.answer("Ошибка при запросе к API.")
        return

    if not segments:
        await message.answer("Расписание не найдено.")
        return

    reply = "🗓 *Найденные рейсы:*\n\n"
    for seg in segments[:5]:  # Покажем первые 5
        title = seg.get("thread", {}).get("title", "Неизвестный")
        dep_time = seg.get("departure", "").replace("T", " ")[:16]  # обрезаем время
        arr_time = seg.get("arrival", "").replace("T", " ")[:16]
        duration = seg.get("duration", 0) // 60  # переводим в минуты

        reply += (
            f"🚆 *{title}*\n"
            f"🕒 Отправление: {dep_time}\n"
            f"🏁 Прибытие: {arr_time}\n"
            f"⏱ В пути: {duration} мин.\n"
            f"---\n"
        )

    await message.answer(reply, parse_mode="Markdown")
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

# # ============== ИНИЦИАЛИЗАЦИЯ ==============
# dialog = Dialog()
# dialog.mode = None
# dialog.list = []
# dialog.user = {}
#
# # ============== ID ГЕРОЕВ ==============
# BUS_IDS = {
#     'abadon': 2,
#     'axe': 7,
#     'invoker': 39,
#     'puck': 54,
#     'shadow_shaman': 67,
#     'legion_commander': 41,
#     'juggernaut': 8,
# }
#
# BUS_NAMES_RU = {
#     'abadon': 'Абадон',
#     'axe': 'Акс',
#     'invoker': 'Инвокер',
#     'puck': 'Пак',
#     'shadow_shaman': 'Тень Шамана',
#     'legion_commander': 'Легионка',
#     'juggernaut': 'Джаггернаут'
# }
#
#
#
#
# # ============== ГЛАВНОЕ МЕНЮ ==============
# async def start(update, context):
#     dialog.mode = "start"
#
#     keyboard = [
#         [InlineKeyboardButton("🛡️ Узнай во сколько прийдёт твой автобус", callback_data='menu_hero')],
#         [InlineKeyboardButton("📊 Узнай вин-рейт героя", callback_data='menu_winrate')],
#         [InlineKeyboardButton("🏆 Узнай лучшего героя", callback_data='menu_top')],
#         [InlineKeyboardButton("📰 Новости про Pro команду", callback_data='menu_pro')],
#         [InlineKeyboardButton("📋 Выбери патч", callback_data='menu_patch')]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#
#     if update.callback_query:
#         await update.callback_query.edit_message_text("⚔️ Dota 2 Bot - Главное меню:", reply_markup=reply_markup)
#     else:
#         await update.message.reply_text("⚔️ Dota 2 Bot - Главное меню:", reply_markup=reply_markup)
#
#
# # ============== МЕНЮ ГЕРОЕВ ==============
# async def hero_menu(update, context):
#     dialog.mode = "hero"
#
#     keyboard = [
#         [InlineKeyboardButton("🔙 Вернуться в меню", callback_data='back_to_menu')],
#         [
#             InlineKeyboardButton("🛡️ Abadon", callback_data='hero_abadon'),
#             InlineKeyboardButton("🪓 Axe", callback_data='hero_axe')
#         ],
#         [
#             InlineKeyboardButton("🧙 Invoker", callback_data='hero_invoker'),
#             InlineKeyboardButton("🧚 Puck", callback_data='hero_puck')
#         ],
#         [
#             InlineKeyboardButton("🐍 Shadow Shaman", callback_data='hero_shadow_shaman'),
#             InlineKeyboardButton("⚔️ Legion Commander", callback_data='hero_legion_commander')
#         ],
#         [
#             InlineKeyboardButton("⚔️ Juggernaut", callback_data='hero_juggernaut'),
#         ]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#
#     if update.callback_query:
#         await update.callback_query.edit_message_text("🎮 Выбери героя:", reply_markup=reply_markup)
#
#
# # ============== ОБРАБОТЧИК КНОПОК ==============
#
#
# async def button_callback(update, context):
#     query = update.callback_query
#     await query.answer()
#
#     print(f"✅ Нажата кнопка: {query.data}")
#
#     if query.data == 'menu_hero':
#         await hero_menu(update, context)
#
#     elif query.data == 'back_to_menu':
#         await start(update, context)
#
#     elif query.data.startswith('hero_'):
#         hero_key = query.data.replace('hero_', '')
#         hero_name = HERO_NAMES_RU.get(hero_key, hero_key)
#
#         # Показываем загрузку
#         await query.edit_message_text(f"⏳ Загружаем сборку для {hero_name}...")
#
#         # Получаем данные (мгновенно!)
#         build_text = await fetch_hero_build(hero_key)
#
#         # Показываем результат
#         await query.edit_message_text(build_text, parse_mode='Markdown')
#
#         # Кнопки после сборки
#         keyboard = [
#             [InlineKeyboardButton("🔙 К героям", callback_data='menu_hero')],
#             [InlineKeyboardButton("🏠 Главное меню", callback_data='back_to_menu')]
#         ]
#         reply_markup = InlineKeyboardMarkup(keyboard)
#         await context.bot.send_message(
#             chat_id=update.effective_chat.id,
#             text="Что делаем дальше?",
#             reply_markup=reply_markup
#         )
#
#
# # ============== ЗАПУСК ==============
# app = ApplicationBuilder().token("8387589572:AAElhVRAF1oDoER0xU_Zm0VJUyVghy36p4Q").build()
# app.add_handler(CommandHandler("start", start))
# app.add_handler(CallbackQueryHandler(button_callback))
# app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,
#                                lambda u, c: send_text(u, c, "Используй кнопки меню! 👆")))
#
#
# app.run_polling()