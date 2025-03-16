from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto  
from apps.keyboards import main, location_data, locations

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать!', reply_markup=main)

# Обработчик для всех локаций
@router.message(F.text.in_(location_data.keys()))
async def get_location_info(message: Message):
    location_name = message.text
    location_info = location_data[location_name]
    
    await message.answer_photo(
        photo=location_info["photo"],
        caption=f"{location_name}\n\n{location_info['description']}",
        reply_markup=location_info["keyboard"]
    )


@router.callback_query(F.data.startswith("next_"))
async def next_location(callback: CallbackQuery):
    next_index = int(callback.data.split("_")[1])
    
    if next_index < len(locations):
        next_location = locations[next_index]
        next_location_info = location_data[next_location["name"]]
        
        media = InputMediaPhoto(
            media=next_location_info["photo"],  
            caption=f"{next_location['name']}\n\n{next_location_info['description']}" 
        )
        
        await callback.message.edit_media(
            media=media,
            reply_markup=next_location_info["keyboard"]
        )
    
    await callback.answer()