import telebot, base64, os, marshal, zlib, gzip, codecs, time 
from telebot import types 
token = "7389397379:AAHsQN69TRvMw8KoqbiNhUW5v47gyXeaFNQ"
bot = telebot.TeleBot(token)
def enco_filee(file_path, enco_Facsion):
    with open(file_path, "r", encoding="utf-8") as file:
        code = file.read()
    for encode_function in enco_Facsion:
        code = encode_function(code)
        time.sleep(2) 
    enc_pathis = "enc-" + os.path.basename(file_path)
    with open(enc_pathis, "w", encoding="utf-8") as enc_file:
        enc_file.write("#Encrypted by @IIYYYU \n")
        enc_file.write(code)   
    return enc_pathis
def base64_enc(code):
    enc_base64 = base64.b64encode(code.encode()).decode()
    return "import base64\nexec(base64.b64decode('" + enc_base64 + "'))"
def base32_enco(code):
    encoded_32 = base64.b32encode(code.encode()).decode()
    return "import base64\nexec(base64.b32decode('" + encoded_32 + "'))"
def lambda_encode(code):
    compressed_data = zlib.compress(code.encode('utf-8'))
    return "import zlib\nexec(zlib.decompress(" + repr(compressed_data) + ").decode())"
def zlib_encode(code):
    compressed_zlib = zlib.compress(code.encode('utf-8'))
    encoded_zlib = base64.b64encode(compressed_zlib).decode()
    return "import zlib\nimport base64\nexec(zlib.decompress(base64.b64decode('" + encoded_zlib + "')).decode())"
def gzip_encode(code):
    compressed_gzip = gzip.compress(code.encode())
    encoded_gzip = base64.b64encode(compressed_gzip).decode()
    return "import gzip\nimport base64\nexec(gzip.decompress(base64.b64decode('" + encoded_gzip + "')).decode())"
def marshal_encode(code):
    compiled_code = compile(code, '<string>', 'exec')
    encrypted_code = base64.b64encode(marshal.dumps(compiled_code, 10))
    return "import marshal\nimport base64\nexec(marshal.loads(base64.b64decode('" + encrypted_code.decode() + "')))"
def hex_encode(code):
    encoded_hex = code.encode().hex()
    return "exec(bytes.fromhex('" + encoded_hex + "'))"
def marshal_zlib_encode(code):
    compiled_code = compile(code, "<string>", 'exec')
    marshaled_code = marshal.dumps(compiled_code)
    compressed_code = zlib.compress(marshaled_code)
    encoded_code = "import zlib\nimport base64\nimport marshal\nexec(marshal.loads(zlib.decompress(" + repr(compressed_code) + ")))"
    return encoded_code
def encoded_rot13(code):
    encoded_rot13 = codecs.encode(code, 'rot_13')
    return "import codecs\nexec(codecs.decode(" + repr(encoded_rot13) + ", 'rot_13'))\n"
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """
👋 | مرحبا بك عزيزي في البوت
🚀 | يمكنك من خلال البوت تشفير الملفات البايثون
✅ | ارسل الملف لاقوم بتشفيرة :
""")
@bot.message_handler(content_types=['document'])
def handle_document(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_path = os.path.join(".", message.document.file_name)
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "✅ | جار التشفير...... ")
        enc_pathis = enco_filee(file_path, [base64_enc, base32_enco, lambda_encode, zlib_encode, gzip_encode, marshal_encode, marshal_zlib_encode, hex_encode, encoded_rot13])
        with open(enc_pathis, 'rb') as enc_file:
            bot.send_document(message.chat.id, enc_file)
        os.remove(file_path)
        os.remove(enc_pathis)
    except Exception as errors:
        bot.reply_to(message, f"⛔ | خطأ :- {errors}")
print("Running... /start ")
bot.infinity_polling()
