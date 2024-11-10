
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup , InlineKeyboardButton
#import texts
from crud_functions import *



api = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


kb = ReplyKeyboardMarkup()
button_1 = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация')
button_3 = KeyboardButton(text='Купить')
# kb.add(button_1)
# kb.add(button_2)

kb.row(button_1, button_2, button_3)

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Рассчитать')],
        [KeyboardButton(text='Информация')],
        [KeyboardButton(text='Купить')]
    ], resize_keyboard=True
)


@dp.message_handler(commands=['start'])
async def start_message(message):

    await message.answer(f"Здравствуйте, {message['chat']['first_name']} {message['chat']['last_name']}!")
    await message.answer('Я бот помогающий Вашему здоровью.')
    await message.reply('Нажмите кнопку \"Рассчитать\"', reply_markup=kb)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight =  State()
    sex_ =  State()




@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(f"Здравствуйте, {message['chat']['first_name']} {message['chat']['last_name']}!")
    await message.reply('Нажмите кнопку \"Рассчитать\"', reply_markup=kb)


@dp.message_handler(text='Рассчитать', state=None)
async def main_menu(message):
    #""" Пока закоментарим
    #Создайте клавиатуру InlineKeyboardMarkup с 2 кнопками InlineKeyboardButton:
    #С текстом 'Рассчитать норму калорий' и callback_data='calories'
    #С текстом 'Формулы расчёта' и callback_data='formulas'
    kb2 = InlineKeyboardMarkup()
    button_i1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
    button_i2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
    kb2.row(button_i1, button_i2)

    await message.reply('Выберите опцию:', reply_markup=kb2)
    #"""



@dp.message_handler(text='Купить', state=None)
async def get_buying_list(message):
    # Создайте Inline меню из 4 кнопок с надписями "Product1", "Product2", "Product3", "Product4".
    # У всех кнопок назначьте callback_data="product_buying"
    kb3 = InlineKeyboardMarkup()
    kb4 = InlineKeyboardMarkup()

    #button_Products = list() # пустой список из кнопок

    rows = get_all_products () # вытаскиваем БД
    await message.answer('Выберите вариант:')

    #button_Product1 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
    #button_Product2 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
    #button_Product3 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
    #button_Product4 = InlineKeyboardButton(text='Product4', callback_data='product_buying')

    i = 0
    for row in rows:

        button_Product = InlineKeyboardButton(text=row[1]+row[2]  , callback_data='product_buying')
        kb3.insert(button_Product)
        #button_Products.append(button_Product)


        await message.answer(f"Название:  {row[1]}  ")
        with open ( f'elteks/{i}.jpg', "rb") as img_i:
            await message.answer_photo (img_i, f"Описание: {row[2]}   |  Цена: {row[3]}")
        i = i + 1

    #button_Products_t = tuple(button_Products)
    #kb3.row( button_Products_t )
    #kb4.row(button_Product1, button_Product2)

    await message.reply('Выберите опцию:', reply_markup=kb3)



@dp.callback_query_handler(text='product_buying', state=None)
async def confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")


@dp.callback_query_handler(text='formulas', state=None )
async def get_formulas(call):
    await call.message.answer('https://www.calc.ru/Formula-Mifflinasan-Zheora.html')


@dp.callback_query_handler(text='calories', state=None)
async def set_age(call):# message: types.Message):
    await call.message.answer('Рассчитать норму калорий')

    await call.message.reply('Введите Ваш возраст:')
    await UserState.age.set()

#lories', state=None)
#async def set_age(message: types.Message):
#    await message.answer(f"Здравствуйте, {message['chat']['first_name']} {message['chat']['last_name']}!")
#    await message.answer('Я бот помогающий Вашему здоровью.')
#    await message.reply('Нажмите кнопку \"Рассчитать\"', reply_markup=kb)


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    if not message.text.isdigit(): # Возраст не цифирь
        await message.answer('Пожалуйста, вводите Ваш возраст числом')
        await state.finish()
        return
    await state.update_data(age=message.text)
    await message.answer('Введите Ваш рост (см):')
    await UserState.growth.set()



@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):

    if not message.text.isdigit(): # рост не цифирь
        await message.answer('Пожалуйста, вводите Ваш рост числом')
        await state.finish()
        return

    await state.update_data(growth=message.text)
    await message.answer('Введите Ваш вес (кг):')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_sex_(message, state):
    if not message.text.isdigit(): # вес не цифирь
        await message.answer('Пожалуйста, вводите Ваш вес числом')
        await state.finish()
        return

    await state.update_data(weight=message.text)
    await message.answer('Сообщите Ваш пол (М\Ж): ')
    await UserState.sex_.set()



@dp.message_handler(state=UserState.sex_)
async def send_calories(message, state):
    await state.update_data(sex_=message.text)
    data = await state.get_data()

    try:
        age = float(data['age'])
        weight = float(data['weight'])
        growth = float(data['growth'])
    except:
        await message.answer(f'Пожалуйста, вводите рост, вес и возраст цифрами.')
        #await message.answer(data )
        await state.finish()
        return

    # Упрощенный вариант формулы Миффлина-Сан Жеора:
    # для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5
    calories_man = 10 * weight + 6.25 * growth - 5 * age + 5
    #для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161
    calories_wom = 10 * weight + 6.25 * growth - 5 * age - 161

    sex_ =  str(data['sex_'])
    if sex_.upper() in ('M', 'М'):
        await message.answer(f'Норма (муж.): {calories_man} ккал')
    elif sex_.upper() in ('Ж', 'W', 'F'):
        await message.answer(f'Норма (жен.): {calories_wom} ккал')
    else:
        await message.answer('Пожалуйста, вводите пол только М или Ж.')

    await message.answer('До новых встреч!')
    await message.reply('Нажмите кнопку \"Рассчитать\"', reply_markup=kb)
    await state.finish()




#обработка нетипичноего сообщения
@dp.message_handler()
async def all_message(message):

#Создайте клавиатуру ReplyKeyboardMarkup и 2 кнопки KeyboardButton на ней со следующим текстом:
# 'Рассчитать' и 'Информация'. Сделайте так, чтобы клавиатура подстраивалась под размеры интерфейса
# устройства при помощи параметра resize_keyboard.
#Используйте ранее созданную клавиатуру в ответе функции start, используя параметр reply_markup

    await message.answer(f"Здравствуйте, {message['chat']['first_name']} {message['chat']['last_name']}!")
    await message.reply('Нажмите кнопку \"Рассчитать\"', reply_markup=kb)


if __name__ == '__main__':
    #initiate_db()
    #print(get_all_products () )
    executor.start_polling(dp, skip_updates=True)