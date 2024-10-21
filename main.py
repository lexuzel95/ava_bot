import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from PIL import Image, ImageDraw, ImageFont
import io

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Токен вашего бота
TOKEN = '7874393042:AAGV5qF1x6WgClyqRXzM6us1q2jHQXEgAq8'

# Укажите путь к вашему шрифту
FONT_PATH = '/Library/Fonts/Arial.ttf'  # Убедитесь, что у вас есть этот шрифт
# Замените на путь к вашему шрифту
FONT_SIZE = 120  # Размер шрифта увеличен в два раза

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Напиши мне текст, и я создам для тебя изображение.')

def generate_image(text: str) -> io.BytesIO:
    # Создаем изображение с белым фоном размером 1920x1920
    img = Image.new('RGB', (1920, 1920), color='white')  
    draw = ImageDraw.Draw(img)

    # Загружаем шрифт
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    # Получаем размер текста
    text_bbox = draw.textbbox((0, 0), text, font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Располагаем текст в центре
    x = (img.width - text_width) / 2
    y = (img.height - text_height) / 2
    draw.text((x, y), text, fill='black', font=font)

    # Сохраняем изображение в памяти
    img_io = io.BytesIO()
    img.save(img_io, 'PNG', quality=95)  # Качество изображения
    img_io.seek(0)
    return img_io

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    img_io = generate_image(text)
    await update.message.reply_photo(photo=img_io)

def main() -> None:
    # Создаем приложение и передаем ему токен
    application = ApplicationBuilder().token(TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
