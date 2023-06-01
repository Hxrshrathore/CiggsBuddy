import logging
import datetime
import pandas as pd
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables to store expense data
monthly_expenses = []
daily_expenses = []

# Conversation states
NUM_CIGS, TOTAL_COST = range(2)

# Handler for the /start command
def start(update: Update, context):
    menu_keyboard = [['/record', '/totalcigs'],
                     ['/totalexpense', '/compare'],
                     ['/clear', '/excel']]
    reply_markup = ReplyKeyboardMarkup(menu_keyboard)
    
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Welcome! This bot will help you calculate daily cigarette expenses and provide monthly reports. "
                                  "Please select an option from the menu.",
                             reply_markup=reply_markup)

# Handler for recording daily expenses
def record_expense_start(update: Update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please enter the number of cigarettes smoked today:")
    return NUM_CIGS

def record_num_cigarettes(update: Update, context):
    num_cigarettes = int(update.message.text)
    context.user_data['num_cigarettes'] = num_cigarettes

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please enter the total cost of the cigarettes (in INR):")
    return TOTAL_COST

def record_total_cost(update: Update, context):
    total_cost = float(update.message.text)

    today = datetime.date.today()
    daily_expenses.append(total_cost)
    monthly_expenses.append(total_cost)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Daily expense recorded: {total_cost} INR")

    # Compare with previous day's expense
    if len(daily_expenses) > 1:
        prev_expense = daily_expenses[-2]
        difference = total_cost - prev_expense
        percentage_diff = (difference / prev_expense) * 100

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Difference from previous day: {difference} INR ({percentage_diff}%)")

    return ConversationHandler.END

# Handler for clearing all records
def clear_records(update: Update, context):
    context.user_data.clear()
    daily_expenses.clear()
    monthly_expenses.clear()
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="All records have been cleared.")

# Handler for displaying the total number of cigarettes
def total_cigarettes(update: Update, context):
    total_cigs = sum(context.user_data.get('num_cigarettes', []) + [])
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Total number of cigarettes: {total_cigs}")

# Handler for displaying the total expenses
def total_expenses(update: Update, context):
    total_expenses = sum(monthly_expenses)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Total expenses: {total_expenses} INR")

# Handler for comparing with the previous month
def compare_previous_month(update: Update, context):
    if len(monthly_expenses) < 2:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Not enough data to compare with the previous month.")
        return

    this_month_expenses = sum(monthly_expenses[-2:])
    prev_month_expenses = sum(monthly_expenses[:-2])

    difference = this_month_expenses - prev_month_expenses
    percentage_diff = (difference / prev_month_expenses) * 100

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Difference from previous month: {difference} INR ({percentage_diff}%)")

# Handler for exporting data to Excel
def export_to_excel(update: Update, context):
    # Create a DataFrame from the data
    data = {'Date': [datetime.date.today() - datetime.timedelta(days=i) for i in range(len(daily_expenses))],
            'Cigarettes': context.user_data.get('num_cigarettes', []),
            'Expense': daily_expenses}
    df = pd.DataFrame(data)

    # Export the DataFrame to Excel
    filename = 'expense_report.xlsx'
    df.to_excel(filename, index=False)

    # Send the Excel file to the user
    context.bot.send_document(chat_id=update.effective_chat.id, document=open(filename, 'rb'))

# Create the bot
def main():
    updater = Updater(token='YOUR_API_TOKEN', use_context=True)
    dispatcher = updater.dispatcher

    # Define command handlers
    start_handler = CommandHandler('start', start)
    record_expense_handler = ConversationHandler(
        entry_points=[CommandHandler('record', record_expense_start)],
        states={
            NUM_CIGS: [MessageHandler(Filters.text & ~Filters.command, record_num_cigarettes)],
            TOTAL_COST: [MessageHandler(Filters.text & ~Filters.command, record_total_cost)],
        },
        fallbacks=[CommandHandler('cancel', start)]
    )
    clear_records_handler = CommandHandler('clear', clear_records)
    total_cigarettes_handler = CommandHandler('totalcigs', total_cigarettes)
    total_expenses_handler = CommandHandler('totalexpense', total_expenses)
    compare_previous_month_handler = CommandHandler('compare', compare_previous_month)
    export_to_excel_handler = CommandHandler('excel', export_to_excel)
    unknown_handler = MessageHandler(Filters.command, start)

    # Add command handlers to the dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(record_expense_handler)
    dispatcher.add_handler(clear_records_handler)
    dispatcher.add_handler(total_cigarettes_handler)
    dispatcher.add_handler(total_expenses_handler)
    dispatcher.add_handler(compare_previous_month_handler)
    dispatcher.add_handler(export_to_excel_handler)
    dispatcher.add_handler(unknown_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

