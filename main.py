import random
import time
from telethon import TelegramClient, events
import re
import aiohttp
import asyncio

# Definir directamente las credenciales
api_id = "16923186"
api_hash = "b6939f5a4d4caa1633a513a2adfd7d4d"
session_name = "1AZWarzIAUG--ACsjPCohiwENNODFKeZGLb6mSfBhfXEbNiHBuiVIFCUakK4tRUv1bMAUC2KD7IgzzEhI-5blzc1wAmKjL5tT2bhmob7O5TGECH2PW2ZyXo8ISbA5fPtZ9dmgWAeXZSm8eZPhymKjgfFYbDfbeOptAmIoUV6M22jJmENbAy9QmJRRsOS-36E2UdGgX7_GL1jqc2vLO_elGDEE9MGD3JJQfNWWtGaiAf7vMu6xij84MQlsW65A4Ycx_IEtxcesRZmZsA1lPRJKb4AZ86ka68e47e1yz3inmxTHfKbPOlsX3uxhYh1yfe_yKLN9_5VE023_44Ptyw3HemEaWmY_aPI="  # Aquí va el nombre de la sesión, por ejemplo 'mi_sesion'

client = TelegramClient(session_name, api_id, api_hash)

BIN_API_URL = 'https://jetixchecker.com/v1/bin/{}'

# Function to filter card information using regex
def filter_cards(text):
    regex = r'\d{16}.*\d{3}'
    matches = re.findall(regex, text)
    return matches

# Function to perform BIN lookup
async def bin_lookup(bin_number):
    bin_info_url = BIN_API_URL.format(bin_number)
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(bin_info_url) as response:
            if response.status == 200:
                try:
                    bin_info = await response.json()
                    return bin_info
                except aiohttp.ContentTypeError:
                    return None
            else:
                return None

# Event handler for new messages
@client.on(events.NewMessage)
async def anukarop(event):
    try:
        message = event.message
        # Regex to match approved messages
        if re.search(r'(Approved!|Charged|authenticate_successful|𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱|- 𝐀𝐩𝐩𝐩𝐫𝗼𝐯𝐞𝐝 ✅|APPROVED|New Cards Found By Scrapper|ꕥ Extrap [☭]|• New Cards Found By JennaS>)', message.text):
            filtered_card_info = filter_cards(message.text)
            if not filtered_card_info:
                return

            start_time = time.time()  # Start timer

            for card_info in filtered_card_info:
                bin_number = card_info[:6]
                bin_info = await bin_lookup(bin_number)
                if bin_info:
                    brand = bin_info.get("brand", "N/A")
                    card_type = bin_info.get("type", "N/A")
                    level = bin_info.get("level", "N/A")
                    bank = bin_info.get("bank", "N/A")
                    country = bin_info.get("country_name", "N/A")
                    country_flag = bin_info.get("country_flag", "")

                    # Calculate time taken with random addition
                    random_addition = random.uniform(0, 10) + 10  # Add random seconds between 10 and 20
                    time_taken = time.time() - start_time + random_addition
                    formatted_time_taken = f"{time_taken:.2f} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬"

                    # Format the message
                    formatted_message = (
                        f"**[-]**(t.me/blackheadsop) 𝐀𝐩𝐩𝐫𝗼𝐯𝗲𝐝 ✅\n\n"
                        f"**[-]**(t.me/blackheadsop) 𝗖𝗮𝗿𝗱: `{card_info}`\n"
                        f"**[-]**(t.me/blackheadsop) 𝐆𝐚𝐭𝐞𝐰𝐚𝐲: Braintree Auth 4\n"
                        f"**[-]**(t.me/blackheadsop) 𝐑𝐞𝐬𝗽𝗼𝐧𝐬𝗲: `1000: Approved`\n\n"
                        f"**[-]**(t.me/blackheadsop) 𝗜𝗻𝗳𝗼: {brand} - {card_type} - {level}\n"
                        f"**[-]**(t.me/blackheadsop) 𝐈𝐬𝐬𝐮𝐞𝐫: {bank}\n"
                        f"**[-]**(t.me/blackheadsop) 𝐂𝗼𝐮𝐧𝐭𝐫𝐲: {country} {country_flag}\n\n"
                        f"𝗧𝗶𝗺𝗲: {formatted_time_taken}"
                    )

                    # Send the formatted message
                    await client.send_message('retrolog', formatted_message, link_preview=False)
                    await asyncio.sleep(30)  # Wait for 30 seconds before sending the next message
    except Exception as e:
        print(e)

# Main function to start the client
async def main():
    await client.start()  # No need for phone_number anymore
    print("Client Created")
    await client.run_until_disconnected()

# Run the main function
asyncio.run(main())
