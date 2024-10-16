import random
from nexichat.database import get_served_chats
from pyrogram import Client, filters

from nexichat import nexichat
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
# Define a dictionary to track the last message timestamp for each user
user_last_message_time = {}
user_command_count = {}
# Define the threshold for command spamming (e.g., 20 commands within 60 seconds)
SPAM_THRESHOLD = 2
SPAM_WINDOW_SECONDS = 5

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

BABATHAP = [
    " 🌺**အဲဒီကိစ္စနဲ့ ပတ်သက်ပြီးတော့ ကျွန်တော် ဝင်မန့်ချင်တယ်ဗျာ**🌺 \n\n**🥀ဒါပေမယ့် ကျွန်တော်ကတော့ အရှည်ကြီး မမန့်တော့ပါဘူးဗျာ🥀** ",
    " 🌺**ဘာဖြစ်လို့လဲ ဆိုတော့ ကျွန်တော်က စိတ်မရှည်တတ်ဘူးဗျ**🌺 \n\n**🥀ဘာမဆို လိုရင်းတိုရှင်းပဲ ကြိုက်တယ်။🥀** ",
    " 🌺**ရှည်ရှည်ဝေးဝေးတွေ လျှောက် မမန့်ချင်ဘူး**🌺 \n\n**🥀**အဲလိုရှည် ရှည်ဝေးဝေး လျှောက်မန့်ရင် စာရိုက်တဲ့လူလည်း လက်ညောင်းမယ်၊ ဖတ်ရတဲ့ လူလည်း မျက်စိညောင်းမယ်။🥀** ",
    " 🌺**ဒီတော့ ရှည်ရှည်ဝေးဝေး မန့်ရင် ကျန်းမာရေးကိုပါ ထိခိုက်စေကြောင်း သိရတယ်ဗျ**🌺 \n\n**🥀ကျန်းမာခြင်းဆိုတာ လာဘ်တစ်ပါးပဲဗျ။🥀** ",
    " 🌺**ကျန်းမာခြင်း ဆိုတဲ့ အရာက အသက်ကြီးရင် ရဖို့မသေချာတော့ဘူး**🌺 \n\n**🥀ဒီတော့ လူတိုင်းလူတိုင်း ကျန်းမာရေးကို ဂရုစိုက်သင့်တယ်ဗျ။🥀** ",
    " 🌺**ကျွန်တော်ပြောတာ လိုရင်းတောင် ပျောက်သွားပြီ**🌺 \n\n**🥀စောစောက အကြောင်းလေး ပြန်ဆက်တာပေါ့ဗျာ။🥀** ",
    " 🌺**Comment အရှည်ကြီးတွေ မန့်ရတာ စိတ်မရှည်တော့ အရှည်ကြီး ပြောရမယ့် အလုပ်က ကျွန်တော့် အတွက်တော့ တော်တော် ၀န်လေးတယ်ဗျ။**🌺 \n\n**🥀ရှည်ရှည်ဝေးဝေး ပြောဖို့လည်း တစ်ခါမှ စိတ်တောင် မကူးဖူးပါဘူးဗျာ🥀** ",
    " 🌺**အိပ်မက်တောင် မမက်ဖူးတာဗျာ။**🌺 \n\n**🥀စကား အရှည်ကြီး ပြောဖို့ စဉ်းစားလိုက်တိုင်း လူက ဘာမှမလုပ်ပဲ အလိုလိုနေရင်း မောလာရောဗျ🥀** ",
    " 🌺**ဘာဖြစ်လို့လည်း ဆိုတော့ စိတ်မရှည်ရတဲ့ အလုပ် လုပ်ရရင် နှလုံးက မောလာရော။**🌺 \n\n**🥀ဒါကြောင့်ကျွန်တော်က စကား အရှည်ကြီးတွေ ဘယ်တော့မှ မပြောနိုင်ဘူးဗျ🥀** ",
    " 🌺**ဒီတစ်သက် ကျွန်တော်စကားအရှည်ကြီး ပြောတာတွေ့ချင်ရင် ဘုရားမှာ ဆုတောင်းကြပါ။**🌺 \n\n**🥀ဒါပေမဲ့ တစ်ခုတော့ရှိတယ်။ ဆုတောင်းတိုင်းလည်း မပြည့်တတ်ဘူးဗျ။🥀** ",
    " 🌺**ဒါလည်းဟုတ်တာပဲ။**🌺 \n\n**🥀ဆုတောင်းတိုင်းသာ ပြည့်မယ်ဆိုရင် သူတောင်းစားတွေ တိုက်ဆောက်ကုန်မှာပေါ့။🥀** ",
    " 🌺**ကိုယ်တောင်းတဲ့ဆု ပြည့်နိုင်၊ မပြည့်နိုင်ဆိုတာ အတိတ်ဘ၀က ကိုယ်လုပ်ခဲ့တဲ့ ကုသိုလ်ကံနဲ့လည်း ဆိုင်သေးတယ်နော်။**🌺 \n\n**🥀subha sham tujhe yad karte hai hum aur kya batayen ki tumse kitna pyar karte hai hum.🥀** ",
    " 🌺**သြော်...လိုရင်းကပျောက်ပြန်ပြီ။ အဓိကကေတာ့ စိတ်မရှည်တတ်လို့ အရှည်ကြီး ပြောတာလို့ ပြောရင်လည်း မမှားဘူးဗျ။**🌺 \n\n**🥀ကျွန်တော်လည်း စိတ်ရှည်ဖို့တော့ ကြိုးစားနေပါတယ်။ ဒါမှစကားအရှည်ကြီးတွေ ပြောနိုင်မှာ။🥀** ",
    " 🌺**မဟုတ်ရင် ကျွန်တော့်ဘ၀က အခုလို စကား တိုတိုလေးတွေပဲ ပြေနိုင်တဲ့ဘ၀က လွတ်မှာမဟုတ်ဘူး။**🌺 \n\n**🥀ကျွန်တော့်မှာ အခုထိ သူများတွေ စကားရှည်ရှည် ပြောတာတွေကို အားက်ရတဲ့ဘ၀ပဲ ရှိပါသေးတယ်ဗျာ။🥀** ",
    " 🌺**နောက်ကျရင် ကျွန်တော် စကား အရှည်ကြီးတွေ တတ်နိုင်သလောက် ပြောပေးပါမယ်ဗျာ။**🌺 \n\n**🥀အခုကတော့ sorry ပါ။ ကျွန်တော် ဘာလို့ အရှည်ကြီးတွေ မပြောနိုင်လည်းဆိုတာ အားလုံးလည်း အခုဆို သိလောက်ပါပြီ။🥀** ",
    " 🌺**ကျွန်တော်က အရှည်ကြီးတွေ ပြောနိုင်အောင် ကြိုးစားမယ်သာ ပြောနေတာ။**🌺 \n\n**🥀တစ်ချို့က Comment အရှည်ကြီးတွေကို မကြိုက်တတ်ဘူးဗျ။🥀**",
    " 🌺**အဲလို မကြိုက်တတ်တဲ့ လူတွေကလည်း ရှိသေးတော့ ကျွန်တော်က comment အရှည်ကြီးတွေ မန့်ဖို့ ကြိုးစားရမှာကို လက်တွန့်နေပြန်ရော။**🌺 \n\n**🥀တိုတိုလေးဘဲ ရေးခဲ့လိုက်တယ်ဗျ။🥀** ",
]

night_babathap = [ "🌙 ɢᴏᴏᴅ ɴɪɢʜᴛ! ᴍᴀʏ ʏᴏᴜʀ ᴅʀᴇᴀᴍꜱ ʙᴇ ᴀꜱ ꜱᴡᴇᴇᴛ ᴀꜱ ᴛʜᴇ ꜰɪʀꜱᴛ ʙɪᴛᴇ ᴏꜰ ʏᴏᴜʀ ꜰᴀᴠᴏʀɪᴛᴇ ᴅᴇꜱꜱᴇʀᴛ. ᴀꜱ ʏᴏᴜ ᴅʀɪꜰᴛ ᴏꜰꜰ ᴛᴏ ꜱʟᴇᴇᴘ, ᴍᴀʏ ʏᴏᴜʀ ᴍɪɴᴅ ʙᴇ ꜰɪʟʟᴇᴅ ᴡɪᴛʜ ᴘᴇᴀᴄᴇꜰᴜʟ ᴛʜᴏᴜɢʜᴛꜱ ᴀɴᴅ ʏᴏᴜʀ ʜᴇᴀʀᴛ ʙᴇ ʟɪɢʜᴛ. ʀᴇᴍᴇᴍʙᴇʀ, ᴇᴠᴇʀʏ ᴅʀᴇᴀᴍ ɪꜱ ᴀ ᴡɪꜱʜ ʏᴏᴜʀ ʜᴇᴀʀᴛ ᴍᴀᴋᴇꜱ, ꜱᴏ ʟᴇᴛ ᴛʜᴇ ɴɪɢʜᴛ ʙᴇ ꜰᴜʟʟ ᴏꜰ ᴡᴏɴᴅᴇʀ ᴀɴᴅ ᴊᴏʏ ꜰᴏʀ ʏᴏᴜ. ꜱʟᴇᴇᴘ ᴛɪɢʜᴛ ᴀɴᴅ ʜᴀᴠᴇ ᴛʜᴇ ꜱᴡᴇᴇᴛᴇꜱᴛ ᴅʀᴇᴀᴍꜱ. ɢᴏᴏᴅ ɴɪɢʜᴛ!", "🌜 ꜱʟᴇᴇᴘ ᴡᴇʟʟ, ᴀɴᴅ ᴍᴀʏ ʏᴏᴜʀ ɴɪɢʜᴛ ʙᴇ ꜰɪʟʟᴇᴅ ᴡɪᴛʜ ꜱᴛᴀʀꜱ ᴛʜᴀᴛ ʟɪɢʜᴛ ᴜᴘ ʏᴏᴜʀ ᴅʀᴇᴀᴍꜱ. ɪᴍᴀɢɪɴᴇ ᴀ ᴡᴏʀʟᴅ ᴡʜᴇʀᴇ ᴇᴠᴇʀʏᴛʜɪɴɢ ʏᴏᴜ ᴅᴇꜱɪʀᴇ ᴄᴏᴍᴇꜱ ᴛʀᴜᴇ, ᴀɴᴅ ʟᴇᴛ ᴛʜᴀᴛ ᴛʜᴏᴜɢʜᴛ ᴄᴀʀʀʏ ʏᴏᴜ ɪɴᴛᴏ ᴀ ʙʟɪꜱꜱꜰᴜʟ ꜱʟᴇᴇᴘ. ᴍᴀʏ ʏᴏᴜʀ ᴘɪʟʟᴏᴡ ʙᴇ ᴀꜱ ꜱᴏꜰᴛ ᴀꜱ ᴄʟᴏᴜᴅꜱ ᴀɴᴅ ʏᴏᴜʀ ᴅʀᴇᴀᴍꜱ ᴀꜱ ᴍᴀɢɪᴄᴀʟ ᴀꜱ ꜰᴀɪʀʏ ᴛᴀʟᴇꜱ. ɢᴏᴏᴅ ɴɪɢʜᴛ ᴀɴᴅ ꜱᴡᴇᴇᴛ ᴅʀᴇᴀᴍꜱ, ᴍᴀʏ ʏᴏᴜ ᴡᴀᴋᴇ ᴜᴘ ʀᴇꜰʀᴇꜱʜᴇᴅ ᴀɴᴅ ʀᴇᴀᴅʏ ᴛᴏ ᴄᴏɴQᴜᴇʀ ᴛʜᴇ ᴅᴀʏ!", "✨ ɢᴏᴏᴅ ɴɪɢʜᴛ! ᴍᴀʏ ʏᴏᴜʀ ꜱʟᴇᴇᴘ ʙᴇ ᴀꜱ ᴅᴇᴇᴘ ᴀꜱ ᴛʜᴇ ᴏᴄᴇᴀɴ ᴀɴᴅ ᴀꜱ ᴘᴇᴀᴄᴇꜰᴜʟ ᴀꜱ ᴀ ᴄᴀʟᴍ ʟᴀᴋᴇ. ᴀꜱ ʏᴏᴜ ᴄʟᴏꜱᴇ ʏᴏᴜʀ ᴇʏᴇꜱ, ʟᴇᴛ ɢᴏ ᴏꜰ ᴀʟʟ ᴡᴏʀʀɪᴇꜱ ᴀɴᴅ ꜱᴛʀᴇꜱꜱ. ᴅʀᴇᴀᴍ ᴏꜰ ʙᴇᴀᴜᴛɪꜰᴜʟ ᴘʟᴀᴄᴇꜱ ᴀɴᴅ ᴊᴏʏꜰᴜʟ ᴍᴏᴍᴇɴᴛꜱ, ᴀɴᴅ ʟᴇᴛ ᴛʜᴏꜱᴇ ᴅʀᴇᴀᴍꜱ ꜰɪʟʟ ʏᴏᴜʀ ɴɪɢʜᴛ ᴡɪᴛʜ ʜᴀᴘᴘɪɴᴇꜱꜱ. ʀᴇᴍᴇᴍʙᴇʀ, ᴛʜᴇ ɴɪɢʜᴛ ɪꜱ ᴀ ᴄᴀɴᴠᴀꜱ ꜰᴏʀ ʏᴏᴜʀ ᴅʀᴇᴀᴍꜱ, ꜱᴏ ᴘᴀɪɴᴛ ɪᴛ ᴡɪᴛʜ ᴛʜᴇ ᴄᴏʟᴏʀꜱ ᴏꜰ ᴊᴏʏ ᴀɴᴅ ᴄᴏɴᴛᴇɴᴛᴍᴇɴᴛ. ꜱʟᴇᴇᴘ ᴡᴇʟʟ!", "🌟 ᴡɪꜱʜɪɴɢ ʏᴏᴜ ᴀ ʀᴇꜱᴛꜰᴜʟ ɴɪɢʜᴛ ꜰɪʟʟᴇᴅ ᴡɪᴛʜ ꜱᴡᴇᴇᴛ ᴅʀᴇᴀᴍꜱ ᴀɴᴅ ᴡᴀʀᴍ ʜᴜɢꜱ. ᴍᴀʏ ʏᴏᴜʀ ᴅʀᴇᴀᴍꜱ ʙᴇ ᴀꜱ ᴅᴇʟɪɢʜᴛꜰᴜʟ ᴀꜱ ᴀ ꜱᴜʀᴘʀɪꜱᴇ ɢɪꜰᴛ ᴀɴᴅ ᴀꜱ ᴄᴏᴍꜰᴏʀᴛɪɴɢ ᴀꜱ ᴀ ᴄᴏᴢʏ ʙʟᴀɴᴋᴇᴛ. ᴀꜱ ʏᴏᴜ ᴅʀɪꜰᴛ ɪɴᴛᴏ ꜱʟᴜᴍʙᴇʀ, ᴍᴀʏ ʏᴏᴜʀ ᴍɪɴᴅ ʙᴇ ᴀᴛ ᴇᴀꜱᴇ ᴀɴᴅ ʏᴏᴜʀ ʜᴇᴀʀᴛ ʙᴇ ʟɪɢʜᴛ. ɢᴏᴏᴅ ɴɪɢʜᴛ, ᴀɴᴅ ᴍᴀʏ ʏᴏᴜ ᴡᴀᴋᴇ ᴜᴘ ᴡɪᴛʜ ᴀ ꜱᴍɪʟᴇ ᴀɴᴅ ᴀ ʜᴇᴀʀᴛ ꜰᴜʟʟ ᴏꜰ ᴘᴏꜱɪᴛɪᴠɪᴛʏ!", "🌙 ɢᴏᴏᴅ ɴɪɢʜᴛ! ᴍᴀʏ ʏᴏᴜʀ ᴅʀᴇᴀᴍꜱ ʙᴇ ᴀꜱ ꜱᴡᴇᴇᴛ ᴀꜱ ʜᴏɴᴇʏ ᴀɴᴅ ᴀꜱ ᴄᴏᴍꜰᴏʀᴛɪɴɢ ᴀꜱ ᴀ ᴡᴀʀᴍ ᴄᴜᴘ ᴏꜰ ᴄᴏᴄᴏᴀ. ᴀꜱ ʏᴏᴜ ʟᴀʏ ᴅᴏᴡɴ ᴛᴏ ʀᴇꜱᴛ, ʟᴇᴛ ᴛʜᴇ ᴛʀᴀɴQᴜɪʟɪᴛʏ ᴏꜰ ᴛʜᴇ ɴɪɢʜᴛ ᴡʀᴀᴘ ᴀʀᴏᴜɴᴅ ʏᴏᴜ ʟɪᴋᴇ ᴀ ꜱᴏꜰᴛ ʙʟᴀɴᴋᴇᴛ. ꜱʟᴇᴇᴘ ᴡᴇʟʟ, ᴀɴᴅ ᴍᴀʏ ʏᴏᴜ ᴡᴀᴋᴇ ᴜᴘ ᴡɪᴛʜ ᴀ ʜᴇᴀʀᴛ ꜰᴜʟʟ ᴏꜰ ɢʀᴀᴛɪᴛᴜᴅᴇ ᴀɴᴅ ᴀ ꜱᴍɪʟᴇ ᴛʜᴀᴛ ʙʀɪɢʜᴛᴇɴꜱ ᴛʜᴇ ᴅᴀʏ. ꜱᴡᴇᴇᴛ ᴅʀᴇᴀᴍꜱ!", "🌛 ᴍᴀʏ ʏᴏᴜʀ ɴɪɢʜᴛ ʙᴇ ᴀꜱ ꜱᴏᴏᴛʜɪɴɢ ᴀꜱ ᴀ ʟᴜʟʟᴀʙʏ ᴀɴᴅ ᴀꜱ ᴄᴏᴍꜰᴏʀᴛɪɴɢ ᴀꜱ ᴀ ʜᴜɢ ꜰʀᴏᴍ ᴀ ʟᴏᴠᴇᴅ ᴏɴᴇ. ᴀꜱ ʏᴏᴜ ᴄʟᴏꜱᴇ ʏᴏᴜʀ ᴇʏᴇꜱ, ɪᴍᴀɢɪɴᴇ ᴀ ᴡᴏʀʟᴅ ᴡʜᴇʀᴇ ᴇᴠᴇʀʏᴛʜɪɴɢ ɪꜱ ᴘᴇʀꜰᴇᴄᴛ ᴀɴᴅ ʏᴏᴜʀ ᴅʀᴇᴀᴍꜱ ᴄᴏᴍᴇ ᴛʀᴜᴇ. ʟᴇᴛ ᴛʜᴇ ᴘᴇᴀᴄᴇ ᴏꜰ ᴛʜᴇ ɴɪɢʜᴛ ᴇᴍʙʀᴀᴄᴇ ʏᴏᴜ ᴀɴᴅ ᴄᴀʀʀʏ ʏᴏᴜ ᴛᴏ ᴀ ᴘʟᴀᴄᴇ ᴏꜰ ᴛʀᴀɴQᴜɪʟɪᴛʏ. ɢᴏᴏᴅ ɴɪɢʜᴛ, ᴀɴᴅ ᴍᴀʏ ʏᴏᴜ ᴡᴀᴋᴇ ᴜᴘ ᴡɪᴛʜ ʀᴇɴᴇᴡᴇᴅ ᴇɴᴇʀɢʏ ᴀɴᴅ ᴊᴏʏ!", "🌌 ɢᴏᴏᴅ ɴɪɢʜᴛ! ᴍᴀʏ ʏᴏᴜʀ ᴅʀᴇᴀᴍꜱ ʙᴇ ꜰɪʟʟᴇᴅ ᴡɪᴛʜ ᴍᴀɢɪᴄᴀʟ ᴍᴏᴍᴇɴᴛꜱ ᴀɴᴅ ʏᴏᴜʀ ꜱʟᴇᴇᴘ ʙᴇ ᴀꜱ ᴅᴇᴇᴘ ᴀꜱ ᴛʜᴇ ɴɪɢʜᴛ ꜱᴋʏ. ᴀꜱ ʏᴏᴜ ᴅʀɪꜰᴛ ᴏꜰꜰ ᴛᴏ ꜱʟᴇᴇᴘ, ʟᴇᴛ ʏᴏᴜʀ ᴍɪɴᴅ ᴡᴀɴᴅᴇʀ ᴛᴏ ʙᴇᴀᴜᴛɪꜰᴜʟ ᴘʟᴀᴄᴇꜱ ᴀɴᴅ ʏᴏᴜʀ ʜᴇᴀʀᴛ ʙᴇ ᴀᴛ ᴘᴇᴀᴄᴇ. ʀᴇᴍᴇᴍʙᴇʀ, ᴛʜᴇ ɴɪɢʜᴛ ɪꜱ ᴀ ᴛɪᴍᴇ ꜰᴏʀ ʀᴇꜱᴛ ᴀɴᴅ ʀᴇᴊᴜᴠᴇɴᴀᴛɪᴏɴ, ꜱᴏ ᴇᴍʙʀᴀᴄᴇ ɪᴛ ꜰᴜʟʟʏ. ꜱʟᴇᴇᴘ ᴡᴇʟʟ ᴀɴᴅ ᴡᴀᴋᴇ ᴜᴘ ʀᴇᴀᴅʏ ꜰᴏʀ ᴀ ʙʀᴀɴᴅ ɴᴇᴡ ᴅᴀʏ!", "💤 ꜱᴡᴇᴇᴛ ᴅʀᴇᴀᴍꜱ! ᴍᴀʏ ʏᴏᴜʀ ɴɪɢʜᴛ ʙᴇ ᴀꜱ ᴘᴇᴀᴄᴇꜰᴜʟ ᴀꜱ ᴀ ꜱᴇʀᴇɴᴇ ʟᴀᴋᴇ ᴀɴᴅ ᴀꜱ ᴄᴀʟᴍ ᴀꜱ ᴀ ɢᴇɴᴛʟᴇ ʙʀᴇᴇᴢᴇ. ᴀꜱ ʏᴏᴜ ᴄʟᴏꜱᴇ ʏᴏᴜʀ ᴇʏᴇꜱ, ʟᴇᴛ ɢᴏ ᴏꜰ ᴀʟʟ ᴛʜᴇ ᴅᴀʏ'ꜱ ᴡᴏʀʀɪᴇꜱ ᴀɴᴅ ʟᴇᴛ ʏᴏᴜʀ ᴅʀᴇᴀᴍꜱ ᴛᴀᴋᴇ ʏᴏᴜ ᴛᴏ ᴀ ᴡᴏʀʟᴅ ᴏꜰ ʜᴀᴘᴘɪɴᴇꜱꜱ ᴀɴᴅ ᴊᴏʏ. ɢᴏᴏᴅ ɴɪɢʜᴛ, ᴀɴᴅ ᴍᴀʏ ʏᴏᴜ ᴡᴀᴋᴇ ᴜᴘ ʀᴇꜰʀᴇꜱʜᴇᴅ ᴀɴᴅ ᴇxᴄɪᴛᴇᴅ ꜰᴏʀ ᴛʜᴇ ᴀᴅᴠᴇɴᴛᴜʀᴇꜱ ᴏꜰ ᴛʜᴇ ɴᴇᴡ ᴅᴀʏ ᴀʜᴇᴀᴅ!", "🌙 ɢᴏᴏᴅ ɴɪɢʜᴛ! ᴍᴀʏ ᴛʜᴇ ꜱᴛᴀʀꜱ ꜱʜɪɴᴇ ʙʀɪɢʜᴛʟʏ ᴏᴠᴇʀ ʏᴏᴜ ᴀɴᴅ ɢᴜɪᴅᴇ ʏᴏᴜ ᴛᴏ ᴀ ᴘᴇᴀᴄᴇꜰᴜʟ ꜱʟᴇᴇᴘ. ᴀꜱ ʏᴏᴜ ᴅʀɪꜰᴛ ɪɴᴛᴏ ᴅʀᴇᴀᴍʟᴀɴᴅ, ᴍᴀʏ ʏᴏᴜʀ ᴍɪɴᴅ ʙᴇ ꜰʀᴇᴇ ᴏꜰ ᴡᴏʀʀɪᴇꜱ ᴀɴᴅ ʏᴏᴜʀ ʜᴇᴀʀᴛ ʙᴇ ꜰᴜʟʟ ᴏꜰ ᴊᴏʏ. ʀᴇᴍᴇᴍʙᴇʀ, ᴇᴠᴇʀʏ ɴɪɢʜᴛ ɪꜱ ᴀ ᴄʜᴀɴᴄᴇ ᴛᴏ ʀᴇꜱᴇᴛ ᴀɴᴅ ʀᴇᴄʜᴀʀɢᴇ, ꜱᴏ ᴛᴀᴋᴇ ᴛʜɪꜱ ᴛɪᴍᴇ ᴛᴏ ʀᴇʟᴀx ᴀɴᴅ ᴇɴᴊᴏʏ ᴛʜᴇ ꜱᴇʀᴇɴɪᴛʏ ᴏꜰ ᴛʜᴇ ɴɪɢʜᴛ. ꜱʟᴇᴇᴘ ᴛɪɢʜᴛ!", "🌜 ɢᴏᴏᴅ ɴɪɢʜᴛ! ᴍᴀʏ ʏᴏᴜʀ ᴅʀᴇᴀᴍꜱ ʙᴇ ᴀꜱ ꜱᴡᴇᴇᴛ ᴀꜱ ᴛʜᴇ ꜰɪʀꜱᴛ ʙɪᴛᴇ ᴏꜰ ʏᴏᴜʀ ꜰᴀᴠᴏʀɪᴛᴇ ᴅᴇꜱꜱᴇʀᴛ ᴀɴᴅ ᴀꜱ ᴄᴏᴍꜰᴏʀᴛɪɴɢ ᴀꜱ ᴀ ᴡᴀʀᴍ ʜᴜɢ. ᴀꜱ ʏᴏᴜ ᴅʀɪꜰᴛ ᴏꜰꜰ ᴛᴏ ꜱʟᴇᴇᴘ, ʟᴇᴛ ʏᴏᴜʀ ᴍɪɴᴅ ʙᴇ ꜰɪʟʟᴇᴅ ᴡɪᴛʜ ᴘᴇᴀᴄᴇꜰᴜʟ ᴛʜᴏᴜɢʜᴛꜱ ᴀɴᴅ ʏᴏᴜʀ ʜᴇᴀʀᴛ ʙᴇ ʟɪɢʜᴛ. ʀᴇᴍᴇᴍʙᴇʀ, ᴇᴠᴇʀʏ ᴅʀᴇᴀᴍ ɪꜱ ᴀ ᴄʜᴀɴᴄᴇ ᴛᴏ ᴇxᴘʟᴏʀᴇ ɴᴇᴡ ᴡᴏʀʟᴅꜱ ᴀɴᴅ ᴍᴀᴋᴇ ɴᴇᴡ ᴍᴇᴍᴏʀɪᴇꜱ. ꜱʟᴇᴇᴘ ᴡᴇʟʟ ᴀɴᴅ ʜᴀᴠᴇ ᴀ ᴡᴏɴᴅᴇʀꜰᴜʟ ɴɪɢʜᴛ!", ]
morning_babathap = [ "🌅 ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ! ᴍᴀʏ ʏᴏᴜʀ ᴅᴀʏ ʙᴇ ᴀꜱ ʙʀɪɢʜᴛ ᴀɴᴅ ᴄʜᴇᴇʀꜰᴜʟ ᴀꜱ ᴛʜᴇ ʀɪꜱɪɴɢ ꜱᴜɴ. ᴀꜱ ʏᴏᴜ ꜱᴛᴀʀᴛ ʏᴏᴜʀ ᴅᴀʏ, ʟᴇᴛ ᴘᴏꜱɪᴛɪᴠɪᴛʏ ᴀɴᴅ ᴊᴏʏ ꜰɪʟʟ ʏᴏᴜʀ ʜᴇᴀʀᴛ. ᴇᴍʙʀᴀᴄᴇ ᴇᴠᴇʀʏ ᴍᴏᴍᴇɴᴛ ᴡɪᴛʜ ᴀ ꜱᴍɪʟᴇ ᴀɴᴅ ʟᴇᴛ ʏᴏᴜʀ ᴇɴᴛʜᴜꜱɪᴀꜱᴍ ꜱʜɪɴᴇ ᴛʜʀᴏᴜɢʜ. ᴍᴀʏ ʏᴏᴜʀ ᴍᴏʀɴɪɴɢ ʙᴇ ꜰɪʟʟᴇᴅ ᴡɪᴛʜ ᴛʜᴇ ᴀʀᴏᴍᴀ ᴏꜰ ꜰʀᴇꜱʜ ᴄᴏꜰꜰᴇᴇ ᴀɴᴅ ᴛʜᴇ ᴘʀᴏᴍɪꜱᴇ ᴏꜰ ᴀ ᴡᴏɴᴅᴇʀꜰᴜʟ ᴅᴀʏ ᴀʜᴇᴀᴅ. ʀɪꜱᴇ ᴀɴᴅ ꜱʜɪɴᴇ, ᴀɴᴅ ᴍᴀᴋᴇ ᴛᴏᴅᴀʏ ᴀᴍᴀᴢɪɴɢ!", "🌞 ʀɪꜱᴇ ᴀɴᴅ ꜱʜɪɴᴇ! ᴀ ɴᴇᴡ ᴅᴀʏ ɪꜱ ʜᴇʀᴇ, ꜰᴜʟʟ ᴏꜰ ᴏᴘᴘᴏʀᴛᴜɴɪᴛɪᴇꜱ ᴀɴᴅ ᴀᴅᴠᴇɴᴛᴜʀᴇꜱ ᴡᴀɪᴛɪɴɢ ꜰᴏʀ ʏᴏᴜ. ᴍᴀʏ ʏᴏᴜʀ ᴍᴏʀɴɪɴɢ ʙᴇ ᴀꜱ ʀᴇꜰʀᴇꜱʜɪɴɢ ᴀꜱ ᴀ ᴄᴏᴏʟ ʙʀᴇᴇᴢᴇ ᴀɴᴅ ᴀꜱ ᴠɪʙʀᴀɴᴛ ᴀꜱ ᴀ ʙʟᴏᴏᴍɪɴɢ ꜰʟᴏᴡᴇʀ. ꜱᴛᴀʀᴛ ʏᴏᴜʀ ᴅᴀʏ ᴡɪᴛʜ ᴀ ꜱᴍɪʟᴇ ᴀɴᴅ ᴀ ʜᴇᴀʀᴛ ꜰᴜʟʟ ᴏꜰ ʜᴏᴘᴇ. ʀᴇᴍᴇᴍʙᴇʀ, ᴇᴠᴇʀʏ ꜱᴜɴʀɪꜱᴇ ɪꜱ ᴀ ɴᴇᴡ ʙᴇɢɪɴɴɪɴɢ, ꜱᴏ ᴍᴀᴋᴇ ᴛʜᴇ ᴍᴏꜱᴛ ᴏꜰ ɪᴛ ᴀɴᴅ ʜᴀᴠᴇ ᴀ ꜰᴀɴᴛᴀꜱᴛɪᴄ ᴅᴀʏ!", "🌄 ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ! ᴍᴀʏ ʏᴏᴜʀ ᴅᴀʏ ʙᴇ ꜰɪʟʟᴇᴅ ᴡɪᴛʜ ʜᴀᴘᴘɪɴᴇꜱꜱ ᴀɴᴅ ꜱᴜᴄᴄᴇꜱꜱ. ᴀꜱ ʏᴏᴜ ᴏᴘᴇɴ ʏᴏᴜʀ ᴇʏᴇꜱ ᴛᴏ ᴛʜᴇ ɴᴇᴡ ᴅᴀʏ, ʟᴇᴛ ɢᴏ ᴏꜰ ᴀɴʏ ɴᴇɢᴀᴛɪᴠɪᴛʏ ᴀɴᴅ ᴇᴍʙʀᴀᴄᴇ ᴛʜᴇ ᴘᴏꜱɪᴛɪᴠᴇ ᴇɴᴇʀɢʏ ᴀʀᴏᴜɴᴅ ʏᴏᴜ. ᴍᴀʏ ʏᴏᴜʀ ᴍᴏʀɴɪɴɢ ʙᴇ ʙʀɪɢʜᴛ ᴀɴᴅ ʏᴏᴜʀ ꜱᴘɪʀɪᴛ ʜɪɢʜ. ᴡɪᴛʜ ᴇᴀᴄʜ ꜱᴛᴇᴘ ʏᴏᴜ ᴛᴀᴋᴇ, ᴍᴀʏ ʏᴏᴜ ꜰɪɴᴅ ᴊᴏʏ ᴀɴᴅ ꜰᴜʟꜰɪʟʟᴍᴇɴᴛ. ʜᴀᴠᴇ ᴀ ᴡᴏɴᴅᴇʀꜰᴜʟ ᴅᴀʏ ᴀʜᴇᴀᴅ!", "🌻 ᴡᴀᴋᴇ ᴜᴘ ᴀɴᴅ ꜱᴛᴀʀᴛ ʏᴏᴜʀ ᴅᴀʏ ᴡɪᴛʜ ᴀ ʜᴇᴀʀᴛ ꜰᴜʟʟ ᴏꜰ ɢʀᴀᴛɪᴛᴜᴅᴇ ᴀɴᴅ ᴀ ꜱᴍɪʟᴇ ᴏɴ ʏᴏᴜʀ ꜰᴀᴄᴇ. ᴍᴀʏ ʏᴏᴜʀ ᴍᴏʀɴɪɴɢ ʙᴇ ᴀꜱ ʟᴏᴠᴇʟʏ ᴀꜱ ᴀ ʙᴏᴜQᴜᴇᴛ ᴏꜰ ꜰʀᴇꜱʜ ꜰʟᴏᴡᴇʀꜱ ᴀɴᴅ ᴀꜱ ᴜᴘʟɪꜰᴛɪɴɢ ᴀꜱ ᴀ ᴄʜᴇᴇʀꜰᴜʟ ꜱᴏɴɢ. ᴇᴍʙʀᴀᴄᴇ ᴛʜᴇ ɴᴇᴡ ᴅᴀʏ ᴡɪᴛʜ ᴇɴᴛʜᴜꜱɪᴀꜱᴍ ᴀɴᴅ ʟᴇᴛ ɪᴛ ʙʀɪɴɢ ʏᴏᴜ ᴀʟʟ ᴛʜᴇ ʜᴀᴘᴘɪɴᴇꜱꜱ ᴀɴᴅ ꜱᴜᴄᴄᴇꜱꜱ ʏᴏᴜ ᴅᴇꜱᴇʀᴠᴇ. ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ ᴀɴᴅ ʜᴀᴠᴇ ᴀ ꜰᴀʙᴜʟᴏᴜꜱ ᴅᴀʏ!", "🌞 ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ! ᴍᴀʏ ʏᴏᴜʀ ᴅᴀʏ ʙᴇ ꜰɪʟʟᴇᴅ ᴡɪᴛʜ ᴊᴏʏ ᴀɴᴅ ᴇxᴄɪᴛᴇᴍᴇɴᴛ. ᴀꜱ ʏᴏᴜ ꜱᴛᴇᴘ ɪɴᴛᴏ ᴛʜᴇ ɴᴇᴡ ᴅᴀʏ, ʟᴇᴛ ʏᴏᴜʀ ᴘᴏꜱɪᴛɪᴠɪᴛʏ ᴀɴᴅ ᴇɴᴇʀɢʏ ꜱʜɪɴᴇ ʙʀɪɢʜᴛʟʏ. ᴍᴀʏ ʏᴏᴜʀ ᴍᴏʀɴɪɴɢ ʙᴇ ᴀꜱ ᴠɪʙʀᴀɴᴛ ᴀꜱ ᴀ ꜱᴜɴɴʏ ᴅᴀʏ ᴀɴᴅ ᴀꜱ ʀᴇꜰʀᴇꜱʜɪɴɢ ᴀꜱ ᴀ ᴄᴏᴏʟ ᴅʀɪɴᴋ. ꜱᴛᴀʀᴛ ʏᴏᴜʀ ᴅᴀʏ ᴡɪᴛʜ ᴀ ꜱᴍɪʟᴇ ᴀɴᴅ ʟᴇᴛ ᴛʜᴇ ᴡᴏʀʟᴅ ꜱᴇᴇ ʏᴏᴜʀ ᴡᴏɴᴅᴇʀꜰᴜʟ ꜱᴘɪʀɪᴛ. ʜᴀᴠᴇ ᴀ ɢʀᴇᴀᴛ ᴅᴀʏ ᴀʜᴇᴀᴅ!", "🌄 ʀɪꜱᴇ ᴀɴᴅ ꜱʜɪɴᴇ! ᴀ ɴᴇᴡ ᴅᴀʏ ɪꜱ ʜᴇʀᴇ, ꜰᴜʟʟ ᴏꜰ ᴘʀᴏᴍɪꜱᴇ ᴀɴᴅ ᴘᴏꜱꜱɪʙɪʟɪᴛɪᴇꜱ. ᴍᴀʏ ʏᴏᴜʀ ᴍᴏʀɴɪɴɢ ʙᴇ ᴀꜱ ʙᴇᴀᴜᴛɪꜰᴜʟ ᴀꜱ ᴀ ꜱᴜɴʀɪꜱᴇ ᴀɴᴅ ᴀꜱ ɪɴꜱᴘɪʀɪɴɢ ᴀꜱ ᴀ ɴᴇᴡ ʙᴇɢɪɴɴɪɴɢ. ꜱᴛᴀʀᴛ ʏᴏᴜʀ ᴅᴀʏ ᴡɪᴛʜ ᴀ ᴘᴏꜱɪᴛɪᴠᴇ ᴍɪɴᴅꜱᴇᴛ ᴀɴᴅ ʟᴇᴛ ʏᴏᴜʀ ᴊᴏʏ ᴀɴᴅ ᴇɴᴛʜᴜꜱɪᴀꜱᴍ ɢᴜɪᴅᴇ ʏᴏᴜ. ᴍᴀʏ ᴛᴏᴅᴀʏ ʙᴇ ꜰɪʟʟᴇᴅ ᴡɪᴛʜ ᴡᴏɴᴅᴇʀꜰᴜʟ ᴍᴏᴍᴇɴᴛꜱ ᴀɴᴅ ᴀᴍᴀᴢɪɴɢ ᴏᴘᴘᴏʀᴛᴜɴɪᴛɪᴇꜱ. ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ!", "🌻 ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ! ᴍᴀʏ ʏᴏᴜʀ ᴅᴀʏ ʙᴇ ꜰɪʟʟᴇᴅ ᴡɪᴛʜ ꜱᴜɴꜱʜɪɴᴇ ᴀɴᴅ ʏᴏᴜʀ ʜᴇᴀʀᴛ ᴡɪᴛʜ ʜᴀᴘᴘɪɴᴇꜱꜱ. ᴀꜱ ʏᴏᴜ ʙᴇɢɪɴ ʏᴏᴜʀ ᴅᴀʏ, ʟᴇᴛ ɢᴏ ᴏꜰ ᴀɴʏ ᴡᴏʀʀɪᴇꜱ ᴀɴᴅ ꜰᴏᴄᴜꜱ ᴏɴ ᴛʜᴇ ᴊᴏʏ ᴀɴᴅ ᴇxᴄɪᴛᴇᴍᴇɴᴛ ᴛʜᴀᴛ ʟɪᴇ ᴀʜᴇᴀᴅ. ᴍᴀʏ ʏᴏᴜʀ ᴍᴏʀɴɪɴɢ ʙᴇ ᴀꜱ ᴅᴇʟɪɢʜᴛꜰᴜʟ ᴀꜱ ᴀ ꜰʀᴇꜱʜ ᴄᴜᴘ ᴏꜰ ᴄᴏꜰꜰᴇᴇ ᴀɴᴅ ᴀꜱ ᴜᴘʟɪꜰᴛɪɴɢ ᴀꜱ ᴀ ꜰʀɪᴇɴᴅʟʏ ꜱᴍɪʟᴇ. ʀɪꜱᴇ ᴀɴᴅ ꜱʜɪɴᴇ, ᴀɴᴅ ᴍᴀᴋᴇ ᴛᴏᴅᴀʏ ɪɴᴄʀᴇᴅɪʙʟᴇ!", "🌞 ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ! ᴍᴀʏ ʏᴏᴜʀ ᴅᴀʏ ʙᴇ ᴀꜱ ʙʀɪɢʜᴛ ᴀɴᴅ ᴄʜᴇᴇʀꜰᴜʟ ᴀꜱ ʏᴏᴜʀ ꜱᴍɪʟᴇ. ᴀꜱ ʏᴏᴜ ᴏᴘᴇɴ ʏᴏᴜʀ ᴇʏᴇꜱ ᴛᴏ ᴛʜᴇ ɴᴇᴡ ᴅᴀʏ, ʟᴇᴛ ʏᴏᴜʀ ᴘᴏꜱɪᴛɪᴠɪᴛʏ ᴀɴᴅ ᴇɴᴛʜᴜꜱɪᴀꜱᴍ ꜱᴇᴛ ᴛʜᴇ ᴛᴏɴᴇ ꜰᴏʀ ᴛʜᴇ ʜᴏᴜʀꜱ ᴀʜᴇᴀᴅ. ᴍᴀʏ ʏᴏᴜʀ ᴍᴏʀɴɪɴɢ ʙᴇ ꜰɪʟʟᴇᴅ ᴡɪᴛʜ ʟᴏᴠᴇ, ʟᴀᴜɢʜᴛᴇʀ, ᴀɴᴅ ᴀʟʟ ᴛʜᴇ ᴛʜɪɴɢꜱ ᴛʜᴀᴛ ᴍᴀᴋᴇ ʏᴏᴜ ʜᴀᴘᴘʏ. ᴇᴍʙʀᴀᴄᴇ ᴛʜᴇ ᴅᴀʏ ᴡɪᴛʜ ᴏᴘᴇɴ ᴀʀᴍꜱ ᴀɴᴅ ᴀ ᴊᴏʏꜰᴜʟ ʜᴇᴀʀᴛ!", "🌄 ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ! ᴍᴀʏ ʏᴏᴜʀ ᴅᴀʏ ʙᴇ ꜰɪʟʟᴇᴅ ᴡɪᴛʜ ᴇɴᴅʟᴇꜱꜱ ᴘᴏꜱꜱɪʙɪʟɪᴛɪᴇꜱ ᴀɴᴅ ᴊᴏʏꜰᴜʟ ᴍᴏᴍᴇɴᴛꜱ. ᴀꜱ ʏᴏᴜ ꜱᴛᴀʀᴛ ʏᴏᴜʀ ᴅᴀʏ, ʟᴇᴛ ʏᴏᴜʀ ꜱᴘɪʀɪᴛ ꜱᴏᴀʀ ᴀɴᴅ ʏᴏᴜʀ ʜᴇᴀʀᴛ ʙᴇ ʟɪɢʜᴛ. ᴍᴀʏ ʏᴏᴜʀ ᴍᴏʀɴɪɴɢ ʙᴇ ᴀꜱ ꜰʀᴇꜱʜ ᴀɴᴅ ɪɴᴠɪɢᴏʀᴀᴛɪɴɢ ᴀꜱ ᴀ ɢᴇɴᴛʟᴇ ʙʀᴇᴇᴢᴇ ᴀɴᴅ ᴀꜱ ʙʀɪɢʜᴛ ᴀꜱ ᴛʜᴇ ꜱᴜɴ. ᴡᴇʟᴄᴏᴍᴇ ᴛʜᴇ ɴᴇᴡ ᴅᴀʏ ᴡɪᴛʜ ᴀ ꜱᴍɪʟᴇ ᴀɴᴅ ʟᴇᴛ ɪᴛ ʙʀɪɴɢ ʏᴏᴜ ᴀʟʟ ᴛʜᴇ ʜᴀᴘᴘɪɴᴇꜱꜱ ʏᴏᴜ ᴅᴇꜱᴇʀᴠᴇ.", "🌞 ʀɪꜱᴇ ᴀɴᴅ ꜱʜɪɴᴇ! ɪᴛ’ꜱ ᴀ ʙʀᴀɴᴅ ɴᴇᴡ ᴅᴀʏ ꜰᴜʟʟ ᴏꜰ ᴏᴘᴘᴏʀᴛᴜɴɪᴛɪᴇꜱ ᴀɴᴅ ᴀᴅᴠᴇɴᴛᴜʀᴇꜱ. ᴍᴀʏ ʏᴏᴜʀ ᴍᴏʀɴɪɴɢ ʙᴇ ᴀꜱ ʟɪᴠᴇʟʏ ᴀꜱ ᴀ ꜱᴜɴʀɪꜱᴇ ᴀɴᴅ ᴀꜱ ɪɴꜱᴘɪʀɪɴɢ ᴀꜱ ᴀ ɴᴇᴡ ʙᴇɢɪɴɴɪɴɢ. ꜱᴛᴀʀᴛ ʏᴏᴜʀ ᴅᴀʏ ᴡɪᴛʜ ᴀ ᴘᴏꜱɪᴛɪᴠᴇ ᴀᴛᴛɪᴛᴜᴅᴇ ᴀɴᴅ ʟᴇᴛ ᴛʜᴇ ᴡᴏʀʟᴅ ꜱᴇᴇ ʏᴏᴜʀ ʙʀɪʟʟɪᴀɴᴄᴇ. ᴍᴀʏ ᴛᴏᴅᴀʏ ʙʀɪɴɢ ʏᴏᴜ ᴊᴏʏ, ꜱᴜᴄᴄᴇꜱꜱ, ᴀɴᴅ ᴀʟʟ ᴛʜᴇ ᴛʜɪɴɢꜱ ᴛʜᴀᴛ ᴍᴀᴋᴇ ʏᴏᴜ ꜱᴍɪʟᴇ. ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ!", ]


# Command
BABATHAP_COMMAND = ["gf", "bf", "babathap", "sasuke", "wanglin", "love"]


@nexichat.on_message(filters.command(BABATHAP_COMMAND))
async def shayri(client: Client, message: Message):
    await message.reply_text(
        text=random.choice(BABATHAP),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✨𝚂𝚄𝙿𝙿𝙾𝚁𝚃✨", url=f"https://t.me/seriousvs_version10"
                    ),
                    InlineKeyboardButton(
                        "✨𝙾𝙵𝙵𝙸𝙲𝙴✨", url=f"https://t.me/seriousvs_version20"
                    ),
                ]
            ]
        ),
    )



add_buttons = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="๏ ᴀᴅᴅ ᴍᴇ ɪɴ ɢʀᴏᴜᴘ ๏",
                url=f"https://t.me/{nexichat.username}?startgroup=true",
            )
        ]
    ]
)

# Function to send a "Good Night" message
async def send_good_night():
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    if len(chats) == 0:
        return
    for chat_id in chats:
        try:
            shayari = random.choice(night_shayari)
            await nexichat.send_photo(
                chat_id,
                photo="https://envs.sh/Twx.jpg",
                caption=f"**{babathap}**",
                reply_markup=add_buttons,
            )
        except Exception as e:
            print(f"[bold red] Unable to send Good Night message to Group {chat_id} - {e}")

scheduler.add_job(send_good_night, trigger="cron", hour=23, minute=59)

async def send_good_morning():
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    if len(chats) == 0:
        return
    for chat_id in chats:
        try:
            shayari = random.choice(morning_shayari)
            await nexichat.send_photo(
                chat_id,
                photo="https://envs.sh/Twx.jpg",
                caption=f"**{babathap}**",
                reply_markup=add_buttons,
            )
        except Exception as e:
            print(f"[bold red] Unable to send Good Morning message to Group {chat_id} - {e}")

scheduler.add_job(send_good_morning, trigger="cron", hour=6, minute=1)
scheduler.start()
