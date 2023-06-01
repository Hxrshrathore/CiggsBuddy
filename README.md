# Telegram Expense Tracker Bot

This is a Telegram bot that helps you track your daily expenses for cigarettes and provides features to calculate and analyze your expenses. It allows you to record the number of cigarettes smoked and the total cost, provides a summary of total expenses, compares expenses with the previous month, and exports data to an Excel file.

## Features

- Record daily expenses for cigarettes.
- Calculate the total number of cigarettes smoked.
- Calculate the total expenses.
- Compare expenses with the previous month.
- Export data to an Excel file.

## Setup

1. Clone the repository:

   ```shell
   git clone https://github.com/HxrshRathore/telegram-expense-tracker-bot.git
   ```

2. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

3. Obtain a Telegram bot token by creating a new bot using the BotFather bot on Telegram. Replace `'YOUR_API_TOKEN'` in the `main()` function of `expense_tracker_bot.py` with your bot token.

4. Run the bot:

   ```shell
   python expense_tracker_bot.py
   ```

5. Start a conversation with your bot on Telegram and use the available commands to track and analyze your expenses.

## Usage

- `/start`: Start the bot and display the menu with available options.
- `/record`: Start the conversation to record daily expenses. Follow the prompts to enter the number of cigarettes and the total cost.
- `/clear`: Clear all recorded data.
- `/totalcigs`: Display the total number of cigarettes.
- `/totalexpense`: Display the total expenses.
- `/compare`: Compare expenses with the previous month.
- `/excel`: Export data to an Excel file.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

Please note that this bot is provided for educational and personal use only. Use it responsibly and at your own risk. The developer is not responsible for any misuse or damages caused by this bot.

## Acknowledgements

This bot is built using the `python-telegram-bot` library. Special thanks to the library developers for their contribution.

## Contact

For any questions or inquiries, please contact [Hars@Webvortex.Studio](mailto:Harsh@WebVortex.Studio).

Enjoy tracking your expenses with the Telegram Expense Tracker Bot!
