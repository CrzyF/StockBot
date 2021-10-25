import os
import telebot
import yfinance as yf

API_KEY = os.getenv('YOUR_APIKEY_HERE')
bot = telebot.TeleBot('YOUR_APIKEY_HERE')

@bot.message_handler(commands=['Greet'])
def greet(message):
  bot.reply_to(message, "Hey! Hows it going?")

@bot.message_handler(commands=['hello'])
def hello(message):
  bot.send_message(message.chat.id, "Hello!")

@bot.message_handler(commands=['wsb'])
def get_stocks(message):
  response = ""
  stocks = ['gme', 'amc', 'nok', 'aapl', 'nio', 'uber', 'wish', 'negg', 'pltr', 'f', 'ge', 'amd', 'itub', 'nokpf', 'bac', 'ccl', 'clov', 'spce', 'pbr', 'rig', 'aal', 't', 'bbd', 'plug', 'abev', 'xpev', 'fcel', 'xom', 'azn', 'tsla', 'vale', 'clf', 'mro', 'twtr', 'fcx', 'msft', 'baba', 'gsat', 'sofi', 'ko', 'siri', 'hban', 'nclh', 'tal', 'dvn', 'ual', 'x', 'auy', 'mu', 'tme', 'dkng', 'orcl', 'jpm', 'csco', 'vz', 'ggb', 'gold', 'ms', 'fb', 'cciv', 'intc', 'ba', 'pfe', 'snap', 'kgc', 'viac', 'qcom', 'teva', 'bp', 'chpt', 'et', 'gm', 'li', 'btg', 'hpe', 'rblx', 'pton','tsm', 'slb', 'cve', 'sklz', 'rycey', 'bb', 'apa', 'rf', 'agnc', 'mrna', 'jd', 'iq', 'nvda', 'znga', 'kmi', 'qs', 'tjx', 'csx', 'nokpf', 'ar', 'm', 'otly', 'swn', 'abnb', 'cmcsa', 'cvx', 'nlok', 'vips', 'pcg', 'rllcf', 'run', 'mpc', 'spwr', 'hmy', 'sdc', 'veon', 'nrz', 'hal', 'tigr', 'cop', 'key', 'work', 'gfi', 'lumn', 'nkla', 'luv', 'pins', 'mrk', 'v', 'bmy', 'pdd', 'dis', 'fhn', 'fsr', 'aa', 'pbr-a', 'open', 'afrm', 'nycb', 'fubo', 'schw', 'alxn', 'upwk', 'rkt', 'infy', 'kr', 'amx', 'lb', 'cog', 'umc', 'bpy', 'wba', 'usb', 'jblu', 'cvs', 'hst', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',]
  stock_data = []
  for stock in stocks:
    data = yf.download(tickers=stock, period='2d', interval='1d')
    data = data.reset_index()
    response += f"-----{stock}-----\n"
    stock_data.append([stock])
    columns = ['stock']
    for index, row in data.iterrows():
      stock_position = len(stock_data) - 1
      price = round(row['Close'], 2)
      format_date = row['Date'].strftime('%m/%d')
      response += f"{format_date}: {price}\n"
      stock_data[stock_position].append(price)
      columns.append(format_date)
    print()

  response = f"{columns[0] : <10}{columns[1] : ^10}{columns[2] : >10}\n"
  for row in stock_data:
    response += f"{row[0] : <10}{row[1] : ^10}{row[2] : >10}\n"
  response += "\nStock Data"
  print(response)
  bot.send_message(message.chat.id, response)

def stock_request(message):
  request = message.text.split()
  if len(request) < 2 or request[0].lower() not in "price":
    return False
  else:
    return True

@bot.message_handler(func=stock_request)
def send_price(message):
  request = message.text.split()[1]
  data = yf.download(tickers=request, period='5m', interval='1m')
  if data.size > 0:
    data = data.reset_index()
    data["format_date"] = data['Datetime'].dt.strftime('%m/%d %I:%M %p')
    data.set_index('format_date', inplace=True)
    print(data.to_string())
    bot.send_message(message.chat.id, data['Close'].to_string(header=False))
  else:
    bot.send_message(message.chat.id, "No data!?")

bot.polling()
