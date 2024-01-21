import boto3
import os
from telegram.ext import Updater, CommandHandler, MessageHandler,Filters

#your credintials

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
S3_BUCKET_NAME = ''
#your telegram bot ID
bid='' 

# Initialize the S3 client
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# Function to list music files in the S3 bucket
def list_music(update, context):
    try:
        response = s3.list_objects(Bucket=S3_BUCKET_NAME)
        music_list = [obj['Key'] for obj in response['Contents'] if obj['Key'].endswith('.mp3')]

        if music_list:
            music_names = "\n".join(music_list)
            update.message.reply_text(f"Available music:\n{music_names}")
        else:
            update.message.reply_text("No music files found.")
    except Exception as e:
        update.message.reply_text(f"An error occurred: {str(e)}")
        print(f"An error occurred: {str(e)}");
def first(update, context):
    try:
        response = s3.list_objects(Bucket=S3_BUCKET_NAME, MaxKeys=1)
        if "Contents" in response and len(response["Contents"]) > 0:
            first_object = response["Contents"][0]
            file_key = first_object["Key"]
            file_path = download_file(file_key)
            if file_path:
                update.message.reply_document(document=open(file_path, 'rb'))
                os.remove(file_path)
            else:
                update.message.reply_text("Failed to download the file.")
        else:
            update.message.reply_text("No files found in the S3 bucket.")
    except Exception as e:
        update.message.reply_text(f"An error occurred: {str(e)}")

# Function to download the file locally
def download_file(file_key: str) -> str:
    try:
        local_file_path = f'/tmp/{os.path.basename(file_key)}'
        s3.download_file(S3_BUCKET_NAME, file_key, local_file_path)
        return local_file_path
    except Exception as e:
        print(f"Failed to download file: {str(e)}")
        return None
# Function to handle playing music
def play_music(update, context):
    try:
        music_name = update.message.text
        if music_name.endswith('.mp3') and music_name in [obj['Key'] for obj in s3.list_objects_v2(Bucket=S3_BUCKET_NAME)['Contents']]:
            s3_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{music_name}"
            update.message.reply_text(f"Playing: {music_name}")
            # Implement your music playing logic here using the obtained S3 URL
            # For example, you can use a music player library to play the music
        else:
            update.message.reply_text("Invalid music name or music not found.")
    except Exception as e:
        update.message.reply_text(f"An error occurred: {str(e)}")

def start_message(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to Spotify Crack!")

def handle_audio(update, context):
    try:
        # Check if the received message contains an audio file
        if update.message.audio:
            file = update.message.audio.get_file()
            print(file);
            # Download the file locally
            file_path = f'D:\pyy\hand\songsS3\{file.file_id}.mp3'
            file.download(file_path);

            # Upload the file to S3
            update.message.reply_text(f"Playing: recivefbiwf");
            s3.upload_file(file_path, S3_BUCKET_NAME, f"kpo.mp3")
            os.remove(file_path);

            update.message.reply_text("File uploaded to S3 successfully!")
        else:
            update.message.reply_text("Please upload an audio file.")
    except Exception as e:
        update.message.reply_text(f"An error occurred: {str(e)}")

def main():
    updater = Updater(bid,use_context=True) #
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("list", list_music))
    dp.add_handler(CommandHandler("start", start_message))
    dp.add_handler(CommandHandler("first", first)) 
    dp.add_handler(MessageHandler(Filters.audio, handle_audio))


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
