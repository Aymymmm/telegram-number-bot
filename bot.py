
import telebot
import requests
from bs4 import BeautifulSoup
import re

API_TOKEN = '7756130100:AAFHV-B64ri1Khar_ZxVrBONyG5ttj0WWMw'
bot = telebot.TeleBot(API_TOKEN)

مصادر متعددة للبحث

def search_emobiletracker(number):
try:
url = f"https://www.emobiletracker.com/track/?phone={number}&submit=Track"
headers = {"User-Agent": "Mozilla/5.0"}
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")
table = soup.find("table", class_="tracking-table")
if table:
rows = table.find_all("tr")
info = []
for row in rows:
cols = row.find_all("td")
if len(cols) == 2:
key = cols[0].get_text(strip=True)
val = cols[1].get_text(strip=True)
info.append(f"{key}: {val}")
return "\n".join(info)
else:
return "لا توجد بيانات واضحة من emobiletracker."
except:
return "حدث خطأ أثناء البحث في emobiletracker."

def search_freecarrierlookup(number):
try:
api_url = f"https://freecarrierlookup.com/getcarrier.php?phonenumber={number}"
res = requests.get(api_url)
if res.text:
data = res.json()
return f"مزود الخدمة: {data.get('carrier')}\nالنوع: {data.get('type')}"
else:
return "لا توجد نتائج من freecarrierlookup."
except:
return "حدث خطأ أثناء الاتصال بمصدر آخر."

@bot.message_handler(func=lambda m: True)
def handle_message(message):
if message.text.startswith("+") or message.text.isdigit():
bot.send_message(message.chat.id, "جاري البحث عن الرقم من عدة مصادر...")

    result_1 = search_emobiletracker(message.text.strip())
    result_2 = search_freecarrierlookup(message.text.strip())

    final_result = f"[emobiletracker]\n{result_1}\n\n[freecarrierlookup]\n{result_2}"
    bot.send_message(message.chat.id, final_result)
else:
    bot.send_message(message.chat.id, "أرسل رقمًا يبدأ بـ + أو بدون رموز.")


bot.infinity_polling()

