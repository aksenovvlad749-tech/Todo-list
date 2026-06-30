import asyncio
import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Твой токен от BotFather
API_TOKEN = '8609174054:AAGWk4LHSPhHs5svR_hDcMbAEzb5hmevFGA'
# Имя файла, где будут храниться задачи
FILE_NAME = 'tasks.json'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Функция для загрузки задач из файла (если файла нет, вернет пустой словарь)
def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# Функция для сохранения задач в файл
def save_tasks(tasks):
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот-записная книжка.\n\n"
        "Вот что я умею:\n"
        "📝 `/add [текст задачи]` — добавить задачу\n"
        "📋 `/list` — показать мои задачи\n"
        "🧹 `/clear` — очистить список"
    )

# Команда /add (Добавление задачи)
@dp.message(Command("add"))
async def cmd_add(message: types.Message):
    # message.text содержит всю строку, например: "/add Купить молоко"
    # Нам нужно убрать саму команду "/add ", чтобы оставить только задачу
    task_text = message.text.replace("/add", "").strip()
    
    if not task_text:
        await message.answer("⚠️ Вы забыли написать саму задачу! Пример: `/add Купить молоко`")
        return

    user_id = str(message.from_user.id) # Получаем ID пользователя
    all_tasks = load_tasks() # Загружаем текущие задачи

    # Если у пользователя еще нет списка, создаем пустой список
    if user_id not in all_tasks:
        all_tasks[user_id] = []
    
    # Добавляем новую задачу в список пользователя
    all_tasks[user_id].append(task_text)
    save_tasks(all_tasks) # Сохраняем обратно в файл

    await message.answer(f"✅ Задача \"{task_text}\" успешно добавлена!")

# Команда /list (Вывод списка задач с помощью ЦИКЛА)
@dp.message(Command("list"))
async def cmd_list(message: types.Message):
    user_id = str(message.from_user.id)
    all_tasks = load_tasks()

    # Проверяем, есть ли задачи у этого пользователя
    if user_id not in all_tasks or not all_tasks[user_id]:
        await message.answer("📭 Ваш список задач пуст!")
        return

    # А вот и наш ЦИКЛ FOR для сборки красивого сообщения
    response = "📋 Ваши задачи на сегодня:\n\n"
    for index, task in enumerate(all_tasks[user_id], 1):
        response += f"{index}. {task}\n"

    await message.answer(response)

# Команда /clear (Очистка)
@dp.message(Command("clear"))
async def cmd_clear(message: types.Message):
    user_id = str(message.from_user.id)
    all_tasks = load_tasks()

    if user_id in all_tasks:
        all_tasks[user_id] = [] # Обнуляем список задач пользователя
        save_tasks(all_tasks)
    
    await message.answer("🧹 Ваш список задач полностью очищен!")

# Запуск бота
async def main():
    print("Бот-планировщик успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())