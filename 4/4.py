import asyncio 
from aiogram import Bot, Dispatcher, F  
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton  
from aiogram.filters import Command  #

TOKEN = ""  

bot = Bot(token=TOKEN)  # создаём объект бота
dp = Dispatcher()  # создаём диспетчер 

user_tasks = {}  
WEEK_DAYS = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]  # список дней недели

# главное меню бота
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Задать дела")],
        [KeyboardButton(text="📋 Посмотреть дела")]
    ],
    resize_keyboard=True  # уменьшает клавиатуру под экран
)

# клавиатура выбора дня недели
days_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=day)] for day in WEEK_DAYS] + [[KeyboardButton(text="⬅ Назад")]],
    resize_keyboard=True
)

# функция создания клавиатуры задач для конкретного пользователя и дня
def tasks_kb(user_id: int, day: str):
    tasks = user_tasks.get(user_id, {}).get(day, [])  # получаем задачи пользователя на выбранный день
    kb = [[KeyboardButton(text=f"✔ {t}")] for t in tasks]  # каждая задача как кнопка "выполнить"
    kb.append([KeyboardButton(text="⬅ Назад")])  # кнопка возврата
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


# обработчик команды /start
@dp.message(Command("start"))
async def start(message: Message):
    name = message.from_user.first_name  # имя пользователя
    await message.answer(f"Привет, {name}! 👋\nЯ TODO-бот на неделю.", reply_markup=main_kb)


# обработчик команды /help
@dp.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer( # сообщение выводимое при команде help
        "📌 Как пользоваться:\n"
        "1. Нажми 'Задать дела' и выбери день.\n"
        "2. Просто напиши текст задачи.\n"
        "3. Нажми на кнопку с задачей (✔), чтобы её выполнить (удалить).\n"
        "4. 'Назад' вернет в главное меню."
    )


# обработка кнопки "назад"
@dp.message(F.text == "⬅ Назад")
async def back(message: Message):
    await message.answer("Главное меню", reply_markup=main_kb)


# обработка кнопок перехода в выбор дней
@dp.message(F.text.in_(["📝 Задать дела", "📋 Посмотреть дела"]))
async def show_days_menu(message: Message):
    await message.answer("Выбери день недели:", reply_markup=days_kb)


# выбор конкретного дня недели
@dp.message(F.text.in_(WEEK_DAYS))
async def choose_day(message: Message):
    user_id = message.from_user.id  # id пользователя
    day = message.text  # выбранный день

    user_tasks.setdefault(user_id, {})["_current_day"] = day  # сохраняем текущий день пользователя

    await message.answer(
        f"📅 День: {day}\nНапиши задачу или нажми на готовую:",
        reply_markup=tasks_kb(user_id, day)  # показываем задачи этого дня
    )


# обработка выполнения задачи (нажатие ✔)
@dp.message(F.text.startswith("✔ "))
async def complete_task(message: Message):
    user_id = message.from_user.id  # id пользователя
    task_text = message.text[2:]  # убираем "✔ " из текста
    data = user_tasks.get(user_id, {})  # получаем данные пользователя
    day = data.get("_current_day")  # текущий выбранный день

    # проверяем, что день выбран и задача существует
    if day and task_text in data.get(day, []):
        data[day].remove(task_text)  # удаляем задачу
        await message.answer(f"✅ Выполнено: {task_text}", reply_markup=tasks_kb(user_id, day))
    else:
        await message.answer("Задача не найдена или день не выбран.")


# добавление новой задачи (любой текст)
@dp.message(F.text)
async def add_task(message: Message):
    user_id = message.from_user.id  # id пользователя
    data = user_tasks.get(user_id, {})  # данные пользователя
    day = data.get("_current_day")  # текущий выбранный день

    # если день не выбран — просим выбрать
    if not day:
        await message.answer("Сначала выбери день недели!", reply_markup=main_kb)
        return

    data.setdefault(day, []).append(message.text)  # добавляем задачу в список
    await message.answer(f"➕ Добавлено в {day}", reply_markup=tasks_kb(user_id, day))


# точка входа в приложение
async def main():
    await dp.start_polling(bot)  # запуск бота (начинает слушать Telegram)


# запуск файла напрямую
if __name__ == "__main__":
    asyncio.run(main())  # старт асинхронного цикла и бота