from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from apps.keyboards import start_keyboard, location_menu, location_data, locations

router = Router()

# Обработчик команды /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Добро пожаловать! Выберите действие:",
        reply_markup=start_keyboard
    )

# Обработчик кнопки "Начать путь"
@router.message(F.text == "Начать путь")
async def start_route(message: Message):
    # Показываем первую локацию
    first_location = locations[0]
    first_location_info = location_data[first_location["name"]]
    
    # Отправляем фотографии
    media_group = [
        InputMediaPhoto(media=photo) for photo in first_location_info["photo"]
    ]
    await message.answer_media_group(media=media_group)
    
    # Отправляем описание и клавиатуру
    await message.answer(
        text=f"📍название📍 {first_location['name']}\n\n📝описание📝 {first_location_info['description']}",
        reply_markup=first_location_info["keyboard"]
    )

# Обработчик кнопки "Полный маршрут"
@router.message(F.text == "Полный маршрут")
async def full_route(message: Message):
    # Показываем меню выбора локаций
    await message.answer(
        "Выберите локацию:",
        reply_markup=location_menu
    )

# Обработчик кнопки "Назад"
@router.message(F.text == "Назад")
async def back_to_main_menu(message: Message):
    # Возвращаем пользователя в главное меню
    await message.answer(
        "Выберите действие:",
        reply_markup=start_keyboard
    )

# Обработчик выбора локации из меню
@router.message(F.text.in_(location_data.keys()))
async def get_location_info(message: Message):
    location_name = message.text
    location_info = location_data[location_name]
    
    # Отправляем фотографии
    media_group = [
        InputMediaPhoto(media=photo) for photo in location_info["photo"]
    ]
    await message.answer_media_group(media=media_group)
    
    # Отправляем описание и клавиатуру
    await message.answer(
        text=f"📍название📍 {location_name}\n\n📝описание📝 {location_info['description']}",
        reply_markup=location_info["keyboard"]
    )

# Обработчик кнопки "Далее"
@router.callback_query(F.data.startswith("next_"))
async def next_location(callback: CallbackQuery):
    next_index = int(callback.data.split("_")[1])
    
    if next_index < len(locations):
        next_location = locations[next_index]
        next_location_info = location_data[next_location["name"]]
        
        # Отправляем фотографии
        media_group = [
            InputMediaPhoto(media=photo) for photo in next_location_info["photo"]
        ]
        await callback.message.answer_media_group(media=media_group)
        
        # Отправляем описание и клавиатуру
        await callback.message.answer(
            text=f"{next_location['name']}\n\n{next_location_info['description']}",
            reply_markup=next_location_info["keyboard"]
        )
    
    await callback.answer()