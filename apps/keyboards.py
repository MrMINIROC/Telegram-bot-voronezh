from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from info.locations import locations


main = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=loc["name"])] for loc in locations],
    resize_keyboard=True,
    input_field_placeholder="Выберите нужное место"
)

def get_location_keyboard(url: str, current_index: int) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text='Далее', callback_data=f"next_{current_index + 1}")]
        if current_index < len(locations) - 1 else None,  
        [InlineKeyboardButton(text='Маршрут', url=url)]  
    ]
    return InlineKeyboardMarkup(inline_keyboard=[b for b in buttons if b])  


location_data = {
    loc["name"]: {
        "description": loc["description"],
        "photo": loc["photo"],
        "keyboard": get_location_keyboard(loc["url"], index)
    } for index, loc in enumerate(locations)
}


__all__ = ["main", "location_data", "locations"]