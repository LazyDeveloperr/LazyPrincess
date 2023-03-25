# import openai
# from pyrogram import Client, filters
# from pyrogram.types import Message


# openai.api_key = "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"
# app = Client("my_bot_token_here")


# # Define message handler for incoming messages
# @app.on_message(filters.private)
# async def handle_message(client: Client, message: Message):
#     # Send a prompt to the GPT-3 API with the incoming message text
#     response = openai.Completion.create(
#         engine="davinci",
#         prompt=message.text,
#         max_tokens=1024,
#         n=1,
#         stop=None,
#         temperature=0.5
#     )
    
#     # Send the GPT-3 API response back to the user
#     await client.send_message(chat_id=message.chat.id, text=response.choices[0].text)


# # @Client.message_handler(filters.private | filters.incoming)
# # async def gpt(client, message):
# #     response = openai.Completion.create(
# #         model = "text-davinci-003",
# #         prompt = message.text,
# #         temperature=0.5,
# #         max_tokens=1024,
# #         top_p=1,
# #         frequency_penalty=0.2,
# #         presence_penalty=0.0,
# #     )
# #     await message.reply(response.choices[0].text)

# # if __name__ == "__main__":
# #     executor.start_polling(dp)
    

# app.run()

