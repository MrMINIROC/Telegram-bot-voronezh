from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from info.locations import locations

# Главное меню
start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Начать путь")],
        [KeyboardButton(text="Полный маршрут")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)

# Меню выбора локаций (для "Полного маршрута")
location_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=loc["name"])] for loc in locations
    ] + [[KeyboardButton(text="Назад")]],  # Добавляем кнопку "Назад"
    resize_keyboard=True,
    input_field_placeholder="Выберите локацию"
)

# Клавиатура для навигации по локациям
def get_location_keyboard(url: str, current_index: int) -> InlineKeyboardMarkup:
    buttons = []
    
    # Кнопка "Далее"
    if current_index < len(locations) - 1:
        buttons.append([InlineKeyboardButton(text='Далее', callback_data=f"next_{current_index + 1}")])
    
    # Кнопка "Маршрут"
    buttons.append([InlineKeyboardButton(text='Маршрут', url=url)])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Создаем словарь с данными о локациях
location_data = {
    loc["name"]: {
        "description": loc["description"],
        "photo": loc["photo"],  # Список фотографий
        "keyboard": get_location_keyboard(loc["url"], index)
    } for index, loc in enumerate(locations)
}

__all__ = ["start_keyboard", "location_menu", "location_data", "locations"]