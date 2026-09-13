import telebot
import requests
import traceback
import time

TOKEN = "8722399403:AAFiToRXglUc2DQ26FlQt1zzh6nU8BW-I8U"

print("جاري تشغيل البوت...")

try:
    bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")
    print("✅ البوت اتعمل بنجاح")
except Exception as e:
    print("❌ فشل إنشاء البوت:")
    print(e)
    traceback.print_exc()
    exit()

WATERMARK = "\n\n———————\nmade by ConSss"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        bot.reply_to(message, 
            "👋 أهلاً بك في بوت جلب معلومات تيك توك!\n\n"
            "أرسل اسم المستخدم فقط بدون @ وسأجيبك بكل التفاصيل (الدولة + الإحصائيات + البايو...)"
            + WATERMARK)
    except Exception as e:
        print("خطأ في /start:", e)

@bot.message_handler(func=lambda message: True)
def get_tiktok_info(message):
    try:
        username = message.text.strip().replace('@', '').lower()
        if not username:
            bot.reply_to(message, "ابعت يوزر صحيح يا باشا" + WATERMARK)
            return

        msg = bot.reply_to(message, "⏳ جاري جلب البيانات..." + WATERMARK)

        url = f"https://user.tikmatrix.com/api/user?username={username}"
        
        response = requests.get(url, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            
            profile = data.get('profile', {})
            stats = data.get('stats', {})

            nickname = profile.get('Nickname', 'غير محدد')
            username_full = profile.get('Username', f'@{username}')
            country = profile.get('Country', 'غير متوفر')
            language = profile.get('Language', 'غير متوفر')
            about = profile.get('About', 'لا يوجد بايو')
            bio_link = profile.get('Bio Link', 'لا يوجد')
            user_id = profile.get('User ID', 'غير متوفر')
            sec_uid = profile.get('SecUID', 'غير متوفر')
            created = profile.get('Account Created', 'غير متوفر')
            avatar = profile.get('Avatar URL', '')

            followers = stats.get('Followers', '0')
            following = stats.get('Following', '0')
            hearts = stats.get('Hearts', '0')
            videos = stats.get('Videos', '0')

            caption = (
                f"👤 **بيانات حساب تيك توك**\n\n"
                f"🔹 **الاسم:** {nickname}\n"
                f"🔹 **اليوزر:** {username_full}\n"
                f"🌍 **الدولة:** {country}\n"
                f"🗣 **اللغة:** {language}\n"
                f"📅 **تاريخ الإنشاء:** {created}\n\n"
                f"📊 **الإحصائيات:**\n"
                f"👥 المتابعين: `{followers}`\n"
                f"➡️ المتابَعون: `{following}`\n"
                f"❤️ الإعجابات: `{hearts}`\n"
                f"🎬 الفيديوهات: `{videos}`\n\n"
                f"🆔 **User ID:** `{user_id}`\n"
                f"🔐 **SecUID:** `{sec_uid}`\n\n"
                f"📝 **البايو:**\n{about}\n\n"
                f"🔗 **رابط البايو:** {bio_link}\n"
                f"🔗 **رابط الحساب:** https://www.tiktok.com/{username_full}"
                + WATERMARK
            )

            try:
                if avatar and avatar.startswith("http"):
                    bot.send_photo(message.chat.id, avatar, caption=caption)
                    bot.delete_message(message.chat.id, msg.message_id)
                else:
                    bot.edit_message_text(caption, message.chat.id, msg.message_id)
            except:
                bot.edit_message_text(caption, message.chat.id, msg.message_id)

        else:
            bot.edit_message_text("❌ الحساب مش موجود أو اليوزر غلط." + WATERMARK, message.chat.id, msg.message_id)

    except Exception as e:
        try:
            bot.reply_to(message, f"⚠️ حصل خطأ:\n`{str(e)}`" + WATERMARK)
        except:
            pass
        print("خطأ في جلب البيانات:")
        traceback.print_exc()

print("🚀 البوت شغال دلوقتي... ابعتله رسالة في التليجرام")

while True:
    try:
        bot.infinity_polling(timeout=30, long_polling_timeout=15, skip_pending=True)
    except Exception as e:
        print("البوت وقع، بيعيد التشغيل بعد 5 ثواني...")
        print(e)
        traceback.print_exc()
        time.sleep(5)