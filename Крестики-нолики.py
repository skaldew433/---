import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация игрового состояния
game_state = {
    "board": [" " for _ in range(9)],
    "current_player": "X",
    "game_over": False
}

def render_board(board):
    buttons = []
    for i in range(0, 9, 3):
        buttons.append([
            InlineKeyboardButton(board[i], callback_data=str(i)),
            InlineKeyboardButton(board[i+1], callback_data=str(i+1)),
            InlineKeyboardButton(board[i+2], callback_data=str(i+2))
        ])
    return buttons

def check_winner(board):
    win_positions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # горизонтальные линии
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # вертикальные линии
        [0, 4, 8], [2, 4, 6]              # диагональные линии
    ]
    for pos in win_positions:
        if board[pos[0]] == board[pos[1]] == board[pos[2]] != " ":
            return board[pos[0]]
    if " " not in board:
        return "Ничья"
    return None

# Функция старта
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global game_state
    game_state = {
        "board": [" " for _ in range(9)],
        "current_player": "X",
        "game_over": False
    }
    buttons = render_board(game_state["board"])
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text('Игра началась! Игрок X ходит первым.', reply_markup=reply_markup)

# Функция обработки хода
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global game_state
    query = update.callback_query
    if query is None:
        logger.error("Update.callback_query is None")
        return

    if game_state["game_over"]:
        await query.answer("Игра уже закончена. Начните новую игру командой /start.")
        return

    move = int(query.data)
    if game_state["board"][move] != " ":
        await query.answer("Эта клетка уже занята.")
        return

    game_state["board"][move] = game_state["current_player"]
    winner = check_winner(game_state["board"])
    if winner:
        game_state["game_over"] = True
        message = f"Игра закончена! Победитель: {winner}" if winner != "Ничья" else "Игра закончена! Ничья."
    else:
        game_state["current_player"] = "O" if game_state["current_player"] == "X" else "X"
        message = f"Ход игрока {game_state['current_player']}."

    buttons = render_board(game_state["board"])
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.edit_message_text(text=message, reply_markup=reply_markup)

def main() -> None:
    # Вставьте сюда ваш токен
    application = Application.builder().token("6897800176:AAEZ3iaMnuWfX_PWwyGk31xiQuaURp-UBwA").build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
