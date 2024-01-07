# with Love @LazyDeveloperr 💘
# Subscribe YT @LazyDeveloperr - to learn more about this for free...

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
import asyncio
import aiohttp
import os
import json
import shutil
import requests
import math
import time
from urllib.parse import urlparse
from info import *
from datetime import datetime
from Script import script
from plugins.rlazy_thumbnail import *
from pyrogram import enums
from database.users_chats_db import db
logging.getLogger("pyrogram").setLevel(logging.WARNING)
from database.lazy_utils import progress_for_pyrogram, humanbytes, TimeFormatter
from lazybot.ran_text import random_char

LAZYS_FILE_ID = "CAACAgUAAxkBAAEQ2YpljSvD5sq-Flkm9TV8afTGo7Kr4gACgwMAAjO28FeYSaGKzSOuUTME CAACAgIAAxkBAAEQ2ppljXqrYNVEN_hsFrm72H_tJvwZEQACdgUAAj-VzApFV7w2VozN3TME CAACAgIAAxkBAAEQ2pxljXr88eSrY-fNSv8tWqTsKQXSTwACWgUAAj-VzAobFrmFvSDDnTME CAACAgUAAxkBAAEQ2p5ljXsOArpCEAIuyF_X-cjbcq8y9wACUQMAAn4--FdPtUqUKQy6njME CAACAgUAAxkBAAEQ2qJljXtSW5xxVc0xk6J4dx1TIcReXQACOggAAibGUFalOk-a8Gmc2TME CAACAgIAAxkBAAEQ2qZljXt7emeVhLmGav1fiCUbTVKK6AACyRIAAmA0gEtb-P-xaa3sxjME CAACAgIAAxkBAAEQ2qhljXuRfi61G-Th8T9R7AIO_E-GFQACgBgAAsC2UEmimzNNrlDPPDME CAACAgIAAxkBAAEQ2qpljXuwpjQsCWqkR190gR6vSLrjpgAC7hQAAuNVUEk4S4qtAhNhvDME CAACAgIAAxkBAAEQ2qxljXvF9LzAOBwWqqGxYghZBptPFwACXgUAAj-VzAqq1ncTLO-MOTME CAACAgUAAxkBAAEQ2q5ljXvfjuP7GSEGy5LOIubDdZD24wACdAQAAg0N-VchhV4I8_I1XjME CAACAgUAAxkBAAEQ2rBljXvzM7MpUVZcpRkiYGPiG89UJgACeAMAAqZh-FfxCTpwVzCOEzME CAACAgUAAxkBAAEQ2rJljXwNvgcYFau24iQ57pNx72IbyAACdQQAAmh1-Ffusjt1plc9YzME CAACAgUAAxkBAAEQ2rRljXwhXX-JMs8GFzz2QZRxdUk9lAADBAACXtDwV04PGDy02iQAATME CAACAgUAAxkBAAEQ2rZljXwsAAEr4nU50WP3Hz_0HCxmYSwAAuwDAAISQflXYznjU3iGTvkzBA CAACAgIAAxkBAAEQ2rhljXxPS3Qd-BV9RnA_0OwPiKsSCQACdwUAAj-VzApljNMsSkHZTjME CAACAgIAAxkBAAEQ2rxljXxsaNqc3gMhzW7FovMiXOvYnQAC-hMAAtSF8Etb7jRObi-mqzME CAACAgUAAxkBAAEQ2sBljXzQxfyPIRI4ch3cHPk-rsCzpQACowkAAonICFTwfKVoynUZvzME CAACAgUAAxkBAAEQ2sJljXzqbHl83Fv7n3m0HfNHBrho4QACCwoAAi7EUVfwywxU4Qq7_jME CAACAgUAAxkBAAEQ2sRljXz-3uxQIFRstS3R5W-y0dC5qgAC5QUAAruXSFaWNURJP7tfwjME CAACAgQAAxkBAAEQ2sZljX0jh3vLtJpWZcxxj5bay9t-ZAACKxAAAk1zwFPGlaV1QZjTkTME CAACAgUAAxkBAAEQ23pljX7l5QqJeF5D5N3HZzH11wKW-AAC_QMAAhOM-FfHw6MTc_AX9TME CAACAgUAAxkBAAEQ23hljX7ivAeA9bzizIEtO1zLWdR3cgACQQQAAu-M8FelaJ5dHSa2IjME CAACAgUAAxkBAAEQ23ZljX7g-mO-JJ_zXANWQP_Iu0XSdwADBAACXtDwV04PGDy02iQAATME CAACAgUAAxkBAAEQ23RljX7d5-rssmw93XU3X7DFQ2eQnAACAQQAAjcM8Vc5TYjCrZcv9jME CAACAgIAAxkBAAEQ23BljX7TxvX88ZWgmaCtC69e8oRFtwACyxQAAt2wUUlMYGw0MqQdYTME CAACAgIAAxkBAAEQ225ljX7SHE230w8XkqVhWGnCZCaEywACmxgAApd_GUmWaHhj5QhlhDME CAACAgIAAxkBAAEQ22xljX7NXu_n0gWTgdJbO2WV6LqwCQACFBUAAuCUyEl75qEC_trvQjME CAACAgIAAxkBAAEQ22pljX7LVSnENXQzGww9r62wOqSj8QACYRQAArT6gEs6giPSo52pzjME CAACAgIAAxkBAAEQ22hljX7FZhbAOn2M_Jv_b4_Ekfu4fQACMBMAAuMikUvBPXzxtKbSdTME CAACAgUAAxkBAAEQ22ZljX7BfFC_nYdWmtu05FPnFPnwsAACoQYAAqReUFYvH5-81YCd2TME CAACAgIAAxkBAAEQ22RljX6qPHWpw3uMFsRZThYk7ed1VAACNAADpsrIDFFqS0RzOZ6RMwQ CAACAgIAAxkBAAEQ22JljX6oYwU5DK4iqQOhHKPIJmdItAACNwADpsrIDAe-9Dzoj1lFMwQ CAACAgIAAxkBAAEQ22BljX6mqfCiiq4lkzCy5arscT9chQACMAADpsrIDN5j5wS_ajpFMwQ CAACAgIAAxkBAAEQ215ljX6lCDcQW-CdfWoP82uwvJ-d5gACPQADpsrIDG9X2CRSFUdMMwQ CAACAgIAAxkBAAEQ21xljX6hzov-plccFYwdhZLjCtERtwACYgMAArrAlQUGVK1U7t1DvjME CAACAgIAAxkBAAEQ21pljX6g7JtkVQgJPRZvUuHEeESzFAACYQMAArrAlQWtCQpcpHMj6zME CAACAgIAAxkBAAEQ21hljX6e4T2BXINz9aHC6bbOhN98-AACXwMAArrAlQV3VCzBKTQhzTME CAACAgIAAxkBAAEQ21ZljX6dOiFyPo25z-k3TemJM-AW0AACZAMAArrAlQUCMw3LNvhMBzME CAACAgIAAxkBAAEQ21RljX6aUwXFnLOUckJO6pPsJY7eJQACYwMAArrAlQXFRT6GJ_YYjDME CAACAgIAAxkBAAEQ21JljX6WcSoazCBpf-lSi_JWkRTJcQACXgMAArrAlQVceSrBWv5H7DME CAACAgIAAxkBAAEQ21BljX6TIJxdnk3g2pW4w92UCdGffgACaAMAArrAlQX1qKrummjK4jME CAACAgIAAxkBAAEQ205ljX6Q0uBqgIDVDsUvCNotXNVUxgACVwMAArrAlQVMHrV9flRvYDME CAACAgIAAxkBAAEQ20xljX6PRN-zZQoa_qKWSRtIr-faagACUQMAArrAlQV7yJzLJQ11NTME CAACAgIAAxkBAAEQ20pljX6LO0vO5MGfXTr5raW8awoMCgACZwMAArrAlQUYRInTOvVi5zME CAACAgUAAxkBAAEQ20hljX6CtrJGoRQbkhgunIrnnxmPtgACWAUAAj_q8FQzC8bJrK17oTME CAACAgUAAxkBAAEQ20ZljX56xaIj4yAYphK71XnLiv5piQACMgUAAiH_OFZUebKV2aRk4jME CAACAgUAAxkBAAEQ20JljX5ulp4Hs5GCtcwOoc5tQE5q7AACDgsAAqTleVRk8KSVmKztdTME CAACAgUAAxkBAAEQ20BljX5suhUDAvXCbRW66o_RVL-eLQAC0AUAAmKRSVbH3lZrdPrmzDME CAACAgUAAxkBAAEQ2z5ljX5rZp6rb2npKqJJUZjihq6nfgACEgYAAlHRSVZQOGffLaUQPDME CAACAgUAAxkBAAEQ2zxljX5pCWHmOGS5Kz7xWQFqQHiwIwACfQYAAihQOVXHMR0c722MljME CAACAgUAAxkBAAEQ2zpljX5nMXdpa64FlfpCt55M13RkTQACAgcAAqnwQVUZPTpNSHHYyzME CAACAgUAAxkBAAEQ2zhljX5lvTqj_GdHD0mjE8Gm_yoNuQACkwYAAnSE4FR1rf6moEtC3jME CAACAgQAAxkBAAEQ2zZljX5e9FXfOHq-pfQ--JC1E6f9NAACwgwAApu9YFOto4bf2PBvjjME CAACAgQAAxkBAAEQ2zRljX5c0OUYHcAWTjQsOVviMVVwqAACOxAAArb8IFC1KxiPG8NRXTME CAACAgQAAxkBAAEQ2zJljX5Yvtmjilx1LyeaH_9aFvRabQAClg4AAgpU4FPdiPEnNU-eAzME CAACAgQAAxkBAAEQ2zBljX5VlUhlERMNYflfQ_TFofjlcAAC5gsAAk8cWVNQLKJXQdhgTjME CAACAgUAAxkBAAEQ2y5ljX5HRQ7tY6cNxh1UDp1bek0uSAACRgUAAsVy2VfQ727ilW4Q0TME CAACAgIAAxkBAAEQ2yxljX5BdWIW00GJ7VfNNH84yKol_AACuAwAAu4J0Uju07GbH7xLtjME CAACAgIAAxkBAAEQ2ypljX4_ef4Gvip3zLn9S46-fThs8QACjw8AAnUuOUhbsCYf9OCDLzME CAACAgIAAxkBAAEQ2yhljX4-F93VJ9SI5Nqrw7hkgAuBYAACrA4AApttOUg2JQmaMDgs5DME CAACAgIAAxkBAAEQ2yZljX49k54WbfWZrWrz-XsOn-RLaQACmgsAArKo0EgS53Dn4tBGxjME CAACAgIAAxkBAAEQ2yRljX47vGql9dU1anPD8Gtr21GdDQACxAsAAotw0UgnQqg-jzV7MDME CAACAgIAAxkBAAEQ2yJljX45vhWNHZaM9cz_3A2hTdUcqgACYgwAAoRLUUneeFbkxCAnAzME CAACAgIAAxkBAAEQ2yBljX43ddBRisbLWhf3XCbfq-I6tQACHQ0AAh770Egx8DhQz29keTME CAACAgUAAxkBAAEQ2x5ljX4GJLG--Tdif5GXum4ySAPSUgACPAcAAvRbsVY-RudjcCNnRzME CAACAgUAAxkBAAEQ2xxljX4EJ1zBF-RDDI8Bw9C8TgU-dgACagcAAtOjsVaqe68IYcN1YjME CAACAgUAAxkBAAEQ2xpljX3_JsNCovrCShBKl-XwTMB1WQAC1ggAAtbKwVaoIpJ458lrbzME CAACAgUAAxkBAAEQ2xhljX3-rpUSr-Zysb5jM-UHdtflzwAC8wcAApZv8VZ2tD2uxVCppjME CAACAgUAAxkBAAEQ2xZljX38lCLPiGavo7umPSqqMY37VAACHAgAAsjxwFbq9aiknIndhjME CAACAgUAAxkBAAEQ2xRljX36Xdiuk8Pj_V1alIcWxpstPQAC9gcAAoOYwFbpOHyXHUEwojME CAACAgIAAxkBAAEQ2xJljX3uGw7RTdNeT1kcKleZdN9iWwACAQADwDZPExguczCrPy1RMwQ CAACAgIAAxkBAAEQ2xBljX3teYnVU4XRYcJbFUm29hgmxQACCQADwDZPE-_NG6JK_3GVMwQ CAACAgIAAxkBAAEQ2w5ljX3pISsLZHZG9AGeNJLzMkpgewACBQADwDZPE_lqX5qCa011MwQ CAACAgIAAxkBAAEQ2wxljX3f39-jvHcMId63H9DYQ9mmfwACHgADwDZPE6FgWy2rAAHeBDME CAACAgIAAxkBAAEQ2wpljX3YMNw4lagYeQyyrsm512RZ6gACCgADwDZPE_8Nrj7oDv0IMwQ CAACAgIAAxkBAAEQ2wABZY190jAxdLz3PpozCPddAyED4l4AAhMAA8A2TxOqs4f3fzjKpTME CAACAgIAAxkBAAEQ2v5ljX3RtHBG3Y5NgWNzhP8lCteK1QACAgADwDZPEwj1bkX6hKdZMwQ CAACAgUAAxkBAAEQ2vxljX3G0gxj5pR5rvF17IqbYOce0gACGBsAAhg7sVYEbqcxgVB0BzME CAACAgUAAxkBAAEQ2vpljX3FWN6o0BPvs6t1CsHPSlRY1AACdAoAAj1wsVagMcQaa7DpwDME CAACAgIAAxkBAAEQ2vhljX24IOhI5O_okxvJQLpEQu58DgACchIAAkblqUjyTBtFPtcDUTME CAACAgIAAxkBAAEQ2vZljX2zxFnUYPHtcIoHXkT3ARcV9gACXhIAAuyZKUl879mlR_dkOzME CAACAgIAAxkBAAEQ2vRljX2yJAv_Cu1ILriYIwllOTWzSgACchIAAkblqUjyTBtFPtcDUTME CAACAgIAAxkBAAEQ2vJljX2xNWg1gnxa6xYW4ceNAk7C0AACQhAAAjPFKUmQDtQRpypKgjME CAACAgIAAxkBAAEQ2vBljX2wDLfaSn8v0z5hRi5ygCFQ3gACdhEAAsMAASlJLbkjGWa6DogzBA CAACAgIAAxkBAAEQ2u5ljX2vwTtkxdzk9vx_7sLNQQysxAACvAwAAocoMEntN5GZWCFoBDME CAACAgIAAxkBAAEQ2uxljX2uWkQ0WZuEYqv-ERLKCAgZHgACoxAAAvF3qEh-OxgSw5fVQTME CAACAgIAAxkBAAEQ2upljX2s4GgknJbdiydP1onraOVl0AACaBEAAoWPKEnJ3C01n5I86TME CAACAgIAAxkBAAEQ2uhljX2rpDsEjlPjyvqtgI9HUka2zQACtA4AAnrnsEhInMQI4qVJTzME CAACAgIAAxkBAAEQ2uZljX2qUv5ReJO76qrQs6uuI_w8YAACkBAAAmteqEgcGk7MnoBFmDME CAACAgIAAxkBAAEQ2uRljX2kr05pfviYamDRHv1sV1QBhAACYgwAAoRLUUneeFbkxCAnAzME CAACAgIAAxkBAAEQ2uJljX2hc3ay1OVdOqbAOZSATyPewQACTwsAAiIPqEiffAABWBhYw3gzBA CAACAgIAAxkBAAEQ2uBljX2fD73IIJCnHUhV3C0j3snJ1QACVgwAAtIc2EgGpDcOv3z8XjME CAACAgUAAxkBAAEQ2t5ljX2WDFSnD_cwS5X294G-UrGqUgACxQUAAtKzoFTAWloi3EjAeTME CAACAgUAAxkBAAEQ2txljX2VCFKoA1IkjeNvj3Nq6onA-QACYAQAAioMGFT31AZIdDgfzDME CAACAgUAAxkBAAEQ2tpljX2SoNNnbgE8TH85w2e9wY_aRgACHAsAAjTXKVWSm3iPcbpSVjME CAACAgUAAxkBAAEQ2thljX2RYxSAq_Cayr9ljiDKv6HWZQACHwUAAwYhVsBmt0GBA78hMwQ CAACAgUAAxkBAAEQ2tZljX2OEKazpqSC2yGcvCG9pm882QACzQoAAiDn2VUKLZEKuLBP0DME CAACAgUAAxkBAAEQ2tRljX2L9UzJcL5Ou7F153lNhLaKpgACLwUAAnQ78VeOB3PdfvLh9jME CAACAgUAAxkBAAEQ2tJljX2HCqUHsmfhIrLfI9dc8JwIPQACxQQAAmtnGFRD00nwm6LHDjME CAACAgIAAxkBAAEQ2tBljX1oTRpo7Mu2N_qQSSDUYdHgBwACTwsAAiIPqEiffAABWBhYw3gzBA CAACAgIAAxkBAAEQ2s5ljX1lpq2nIeSMh2ABs7GMWArFvAACagsAArVLqEgy_6fKZOLx5jME CAACAgIAAxkBAAEQ2sxljX1kbYfwmVO0OegtwdAjEN6CGgACrQwAAvGUQUihcDy_-h_T6TME CAACAgIAAxkBAAEQ2spljX1hLlkVpoHdI4SJT7h1_LFTVAACJAwAAviQOEiWAywHzwABlxgzBA CAACAgQAAxkBAAEQ2sZljX0jh3vLtJpWZcxxj5bay9t-ZAACKxAAAk1zwFPGlaV1QZjTkTME CAACAgUAAxkBAAEQ2sRljXz-3uxQIFRstS3R5W-y0dC5qgAC5QUAAruXSFaWNURJP7tfwjME CAACAgUAAxkBAAEQ2sJljXzqbHl83Fv7n3m0HfNHBrho4QACCwoAAi7EUVfwywxU4Qq7_jME CAACAgUAAxkBAAEQ2sBljXzQxfyPIRI4ch3cHPk-rsCzpQACowkAAonICFTwfKVoynUZvzME CAACAgIAAxkBAAEQ2rxljXxsaNqc3gMhzW7FovMiXOvYnQAC-hMAAtSF8Etb7jRObi-mqzME CAACAgUAAxkBAAEQ2sJljXzqbHl83Fv7n3m0HfNHBrho4QACCwoAAi7EUVfwywxU4Qq7_jME CAACAgUAAxkBAAEQ2sBljXzQxfyPIRI4ch3cHPk-rsCzpQACowkAAonICFTwfKVoynUZvzME CAACAgIAAxkBAAEQ2rxljXxsaNqc3gMhzW7FovMiXOvYnQAC-hMAAtSF8Etb7jRObi-mqzME CAACAgIAAxkBAAEQ2rpljXxg0p_h1RoD1tBlVOvwFc-SzwAC_RMAAqrbgEuv3ujuB8gacDME CAACAgIAAxkBAAEQ2rhljXxPS3Qd-BV9RnA_0OwPiKsSCQACdwUAAj-VzApljNMsSkHZTjME CAACAgUAAxkBAAEQ2rZljXwsAAEr4nU50WP3Hz_0HCxmYSwAAuwDAAISQflXYznjU3iGTvkzBA CAACAgUAAxkBAAEQ2rRljXwhXX-JMs8GFzz2QZRxdUk9lAADBAACXtDwV04PGDy02iQAATME CAACAgUAAxkBAAEQ2rJljXwNvgcYFau24iQ57pNx72IbyAACdQQAAmh1-Ffusjt1plc9YzME CAACAgUAAxkBAAEQ2q5ljXvfjuP7GSEGy5LOIubDdZD24wACdAQAAg0N-VchhV4I8_I1XjME CAACAgIAAxkBAAEQ2qxljXvF9LzAOBwWqqGxYghZBptPFwACXgUAAj-VzAqq1ncTLO-MOTME CAACAgIAAxkBAAEQ2qpljXuwpjQsCWqkR190gR6vSLrjpgAC7hQAAuNVUEk4S4qtAhNhvDME CAACAgIAAxkBAAEQ2qhljXuRfi61G-Th8T9R7AIO_E-GFQACgBgAAsC2UEmimzNNrlDPPDME CAACAgIAAxkBAAEQ2qZljXt7emeVhLmGav1fiCUbTVKK6AACyRIAAmA0gEtb-P-xaa3sxjME CAACAgUAAxkBAAEQ2qRljXtnTHB4pmFFoKUQHw7JupE7-wACpwUAAuW4WFaFOaIX4LMhuDME CAACAgUAAxkBAAEQ2p5ljXsOArpCEAIuyF_X-cjbcq8y9wACUQMAAn4--FdPtUqUKQy6njME CAACAgIAAxkBAAEQ2pxljXr88eSrY-fNSv8tWqTsKQXSTwACWgUAAj-VzAobFrmFvSDDnTME CAACAgIAAxkBAAEQ2ppljXqrYNVEN_hsFrm72H_tJvwZEQACdgUAAj-VzApFV7w2VozN3TME CAACAgUAAxkBAAEQ2YpljSvD5sq-Flkm9TV8afTGo7Kr4gACgwMAAjO28FeYSaGKzSOuUTME"
lazystickerset = LAZYS_FILE_ID.split()

async def ddl_call_back(client, query):
    # logger.info(client)
    cb_data = query.data
    lzmsg = query.message.reply_to_message  # msg will be callback query
    message_idx = lzmsg.id #getting id
    # youtube_dl extractors
    tg_send_type, youtube_dl_format, youtube_dl_ext, ranom = cb_data.split("|")
    print(cb_data)
    random1 = random_char(5)
    save_ytdl_json_path = DOWNLOAD_LOCATION + \
        "/" + str(query.from_user.id) + f'{ranom}' + ".json"
    try:
        with open(save_ytdl_json_path, "r", encoding="utf8") as f:
            response_json = json.load(f)
    except (FileNotFoundError) as e:
        await client.delete_messages(
            chat_id=query.message.chat.id,
            message_ids=message_idx,
            revoke=True
        )
        return False
    youtube_dl_url = query.message.reply_to_message.text
    custom_file_name = str(response_json.get("title")) + \
        "_" + youtube_dl_format + "." + youtube_dl_ext
    youtube_dl_username = None
    youtube_dl_password = None
    if "|" in youtube_dl_url:
        url_parts = youtube_dl_url.split("|")
        if len(url_parts) == 2:
            youtube_dl_url = url_parts[0]
            custom_file_name = url_parts[1]
        elif len(url_parts) == 4:
            youtube_dl_url = url_parts[0]
            custom_file_name = url_parts[1]
            youtube_dl_username = url_parts[2]
            youtube_dl_password = url_parts[3]
        else:
            for entity in query.message.reply_to_message.entities:
                if entity.type == "text_link":
                    youtube_dl_url = entity.url
                elif entity.type == "url":
                    o = entity.offset
                    l = entity.length
                    youtube_dl_url = youtube_dl_url[o:o + l]
        if youtube_dl_url is not None:
            youtube_dl_url = youtube_dl_url.strip()
        if custom_file_name is not None:
            custom_file_name = custom_file_name.strip()
        # https://stackoverflow.com/a/761825/4723940
        if youtube_dl_username is not None:
            youtube_dl_username = youtube_dl_username.strip()
        if youtube_dl_password is not None:
            youtube_dl_password = youtube_dl_password.strip()
        logger.info(youtube_dl_url)
        logger.info(custom_file_name)
    else:
        for entity in query.message.reply_to_message.entities:
            if entity.type == "text_link":
                youtube_dl_url = entity.url
            elif entity.type == "url":
                o = entity.offset
                l = entity.length
                youtube_dl_url = youtube_dl_url[o:o + l]
    ######################## 
    try:
        if "youtu" in youtube_dl_url or "youtube" in youtube_dl_url:
            logger.info('cant define file size for youtube videos')
        else:
            xLAZY_BAAPUx_d_size = requests.head(youtube_dl_url)    
            xLAZY_BAAPUx_t_length = int(xLAZY_BAAPUx_d_size.headers.get("Content-Length", 0))
            xLAZY_BAAPUx_path = urlparse(youtube_dl_url).path
            xLAZY_BAAPUx_u_name = os.path.basename(xLAZY_BAAPUx_path)
            total_length = humanbytes(xLAZY_BAAPUx_t_length)
        logger.info(total_length)
        sizee = "undefined" if "youtu" in youtube_dl_url or "youtube" in youtube_dl_url else total_length
        namee = "undefined" if "youtu" in youtube_dl_url or "youtube" in youtube_dl_url else xLAZY_BAAPUx_u_name
    except Exception as e:
        logger.error(f"Something went wrong in the code =>::: {e}")
    ######################## 
    try:
        lazy_sticker = await query.message.reply_sticker(sticker=random.choice(lazystickerset))
    except Exception as e:
        await print(e)
        pass

    description = script.CUSTOM_CAPTION_UL_FILE
    start = datetime.now()
    
    description = script.CUSTOM_CAPTION_UL_FILE
    if "fulltitle" in response_json:
        description = response_json["fulltitle"][0:1021]
    tmp_directory_for_each_user = DOWNLOAD_LOCATION + "/" + str(query.from_user.id) + f'{random1}'
    if not os.path.isdir(tmp_directory_for_each_user):
        os.makedirs(tmp_directory_for_each_user)
    download_directory = tmp_directory_for_each_user + "/" + custom_file_name
    command_to_exec = []
    async with aiohttp.ClientSession() as session:
        c_time = time.time()
        try:
            await download_coroutine(
                client,
                session,
                custom_file_name,
                youtube_dl_url,
                download_directory,
                query.message.chat.id,
                query.message.id,
                c_time,
            )
        except TimeoutError:
            await query.edit_message_text(
                text=script.SLOW_URL_DECED,
            )
            return False
    if os.path.exists(download_directory):
        end_one = datetime.now()
        await query.edit_message_text(
            text=script.UPLOAD_START,
        )
        file_size = TG_MAX_FILE_SIZE + 1
        try:
            file_size = os.stat(download_directory).st_size
        except FileNotFoundError as exc:
            download_directory = os.path.splitext(download_directory)[0] + "." + "mkv"
            # https://stackoverflow.com/a/678242/4723940
            file_size = os.stat(download_directory).st_size
        if file_size > TG_MAX_FILE_SIZE:
            await query.edit_message_text(
                text=script.RCHD_TG_API_LIMIT,
            )
        else:
            start_time = time.time()
            if (await db.get_upload_as_doc(query.from_user.id)) is False:
                thumbnail = await Gthumb01(client, query)
                await lazy_sticker.delete()
                try:
                    lazy_sticker01 = await query.message.reply_sticker(sticker=random.choice(lazystickerset))
                except Exception as e:
                    await client.send_message(chat_id = query.message.chat.id, text=f"🥳")
                    pass
                await client.send_document(
                    chat_id=query.message.chat.id,
                    document=download_directory,
                    thumb=thumbnail,
                    caption=f"**{custom_file_name}**\n\n🧬Data costs: `{sizee}`",
                    reply_to_message_id=message_idx,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        script.LAZY_UPLOAD_START.format(custom_file_name),
                        query.message,
                        start_time
                    )
                )
                await lazy_sticker01.delete()
            else:
                 width, height, duration = await Mdata01(download_directory)
                 thumb_image_path = await Gthumb02(client, query, duration, download_directory)
                 await lazy_sticker.delete()
                 try:
                     lazy_sticker02 = await query.message.reply_sticker(sticker=random.choice(lazystickerset))
                 except Exception as e:
                     await client.send_message(chat_id = query.message.chat.id, text=f"🥳")
                     pass
                 await client.send_video(
                    chat_id=query.message.chat.id,
                    video=download_directory,
                    caption=f"**{custom_file_name}**\n\n🧬Data costs: `{sizee}`",
                    duration=duration,
                    width=width,
                    height=height,
                    supports_streaming=True,
                    thumb=thumb_image_path,
                    reply_to_message_id=message_idx,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        script.LAZY_UPLOAD_START.format(custom_file_name),
                        query.message,
                        start_time
                    )
                )
                 await lazy_sticker02.delete()
            if tg_send_type == "audio":
                duration = await Mdata03(download_directory)
                thumbnail = await Gthumb01(client, query)
                await lazy_sticker.delete()
                try:
                    lazy_sticker03 = await query.message.reply_sticker(sticker=random.choice(lazystickerset))
                except Exception as e:
                    await client.send_message(chat_id = query.message.chat.id, text=f"🥳")
                    pass
                await client.send_audio(
                    chat_id=query.message.chat.id,
                    audio=download_directory,
                    caption=f"**{custom_file_name}**\n\n🧬Data costs: `{sizee}`",
                    parse_mode=enums.ParseMode.HTML,
                    duration=duration,
                    thumb=thumbnail,
                    reply_to_message_id=message_idx,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        script.LAZY_UPLOAD_START.format(custom_file_name),
                        query.message,
                        start_time
                    )
                )
                await lazy_sticker03.delete()
            elif tg_send_type == "vm":
                width, duration = await Mdata02(download_directory)
                thumbnail = await Gthumb02(client, query, duration, download_directory)
                await lazy_sticker.delete()
                try:
                    lazy_sticker04 = await query.message.reply_sticker(sticker=random.choice(lazystickerset))
                except Exception as e:
                    await client.send_message(chat_id = query.message.chat.id, text=f"🥳")
                    pass
                await client.send_video_note(
                    chat_id=query.message.chat.id,
                    video_note=download_directory,
                    duration=duration,
                    length=width,
                    thuly_to_message_id=message_idx,
                    promb=thumbnail,
                    repgress=progress_for_pyrogram,
                    progress_args=(
                        script.LAZY_UPLOAD_START.format(custom_file_name),
                        query.message,
                        start_time
                    )
                )
                await lazy_sticker04.delete()
            else:
                logger.info("Did this happen? :\\")
            end_two = datetime.now()
            try:
                os.remove(download_directory)
                os.remove(thumb_image_path)
            except:
                pass
            time_taken_for_download = (end_one - start).seconds
            time_taken_for_upload = (end_two - end_one).seconds
            await query.edit_message_text(
                text=script.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS.format(time_taken_for_download, time_taken_for_upload, youtube_dl_url, namee, custom_file_name, sizee ),
                disable_web_page_preview=True
            )
    else:
        await query.edit_message_text(
            text=script.NO_VOID_FORMAT_FOUND.format("Incorrect Link"),
            disable_web_page_preview=True
        )

async def download_coroutine(bot, session, custom_file_name, url, file_name, chat_id, message_id, start):
    downloaded = 0
    display_message = ""
    async with session.get(url, timeout=PROCESS_MAX_TIMEOUT) as response:
        total_length = int(response.headers["Content-Length"])
        content_type = response.headers["Content-Type"]
        xLAZY_BAAPUx_path = urlparse(url).path
        xLAZY_BAAPUx_u_name = os.path.basename(xLAZY_BAAPUx_path)
        if "text" in content_type and total_length < 500:
            return await response.release()
        await bot.edit_message_text(
            chat_id,
            message_id,
            text=""""**ღ♡ ɪɴɪᴛɪᴀᴛɪɴɢ ʟᴀᴢʏ ᴄᴏɴꜱᴛʀᴜᴄᴛɪᴏɴ ♡♪** \n⬇️⏬ `{}`\n🧬**ѕιzє:**`{}`
            """.format(xLAZY_BAAPUx_u_name, humanbytes(total_length))
        )
        with open(file_name, "wb") as f_handle:
            while True:
                chunk = await response.content.read(CHUNK_SIZE)
                if not chunk:
                    break
                f_handle.write(chunk)
                downloaded += CHUNK_SIZE
                now = time.time()
                diff = now - start
                xLAZY_BAAPUx_path = urlparse(url).path
                xLAZY_BAAPUx_u_name = os.path.basename(xLAZY_BAAPUx_path)
                if round(diff % 5.00) == 0 or downloaded == total_length:
                    percentage = downloaded * 100 / total_length
                    speed = downloaded / diff
                    elapsed_time = round(diff) * 1000
                    time_to_completion = round(
                        (total_length - downloaded) / speed) * 1000
                    estimated_total_time = elapsed_time + time_to_completion
                    xxLAZY_BAPUXX_total_size = humanbytes(total_length)
                    tp = round(percentage, 2)
                    xxLAZY_BAPUXX_estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)
                    template_name = custom_file_name if custom_file_name else "**⚠ You haven't given any custom name...**"

                    xLDx = f"**ღ♡ ʀᴜɴɴɪɴɢ ʟᴀᴢʏ ᴄᴏɴꜱᴛʀᴜᴄᴛɪᴏɴ ♡♪**\n**ᵉⁿʲᵒʸ ˢᵘᵖᵉʳᶠᵃˢᵗ ᵈᵒʷⁿˡᵒᵈ ᵇʸ [ᴸᵃᶻʸᴰᵉᵛᵉˡᵒᵖᵉʳʳ](https://t.me/LazyDeveloperr)◔_◔** \n\n**░░✩ 📂𝐎𝐑𝐆 𝐅𝐈𝐋𝐄𝐍𝐀𝐌𝐄 ✩ **\n<code>{xLAZY_BAAPUx_u_name}</code>\n\n**░░✩ 📝𝐍𝐄𝐖 𝐍𝐀𝐌𝐄 ✩ **\n<code>{template_name}</code>\n\n ☼﹍︿﹍ⲯ﹍︿﹍﹍︿﹍ⲯ﹍︿﹍☼\n⚡️**Done:{tp}**%| 🧬ѕιzє: {xxLAZY_BAPUXX_total_size}"
                    progress = "{0}{1}".format(
                        ''.join(["█" for i in range(math.floor(percentage / 5))]),
                        ''.join(["░" for i in range(20 - math.floor(percentage / 5))]))
                    tmp = xLDx + "\n" + progress + script.PROGRESS_BAR.format( 
                        round(percentage, 2),
                        humanbytes(downloaded),
                        humanbytes(total_length),
                        humanbytes(speed),
                        xxLAZY_BAPUXX_estimated_total_time if xxLAZY_BAPUXX_estimated_total_time != '' else "0 s"
                    )
                    try:
                        current_message = tmp
                        if current_message != display_message:
                            await bot.edit_message_text(
                                chat_id,
                                message_id,
                                text=current_message,
                                disable_web_page_preview=True
                            )
                            display_message = current_message
                    except Exception as e:
                        logger.info(str(e))
                        pass
        return await response.release()
