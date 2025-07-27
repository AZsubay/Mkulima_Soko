from flask import Response
from database import add_price, get_prices_by_crop_and_region
import africastalking
import os
from dotenv import load_dotenv

# Load credentials
load_dotenv()
africastalking.initialize(os.getenv("AT_USERNAME"), os.getenv("AT_API_KEY"))
sms = africastalking.SMS
def send_sms(to, message):
    try:
        sms.send(message, [to])
    except Exception as e:
        print("SMS failed:", e)
MESSAGES = {
    "sw": {
        "language_choice": "CON Chagua lugha:\n1. Kiswahili\n2. English",
        "welcome": "CON Karibu Mkulima Soko 🧑🏾‍🌾\n1. Angalia bei ya mazao\n2. Tuma bei ya mazao",
        "select_category": "CON Chagua aina ya zao:\n1. Mazao ya Chakula\n2. Mazao ya Biashara",
        "enter_crop_name": "CON Andika jina la zao:",
        "enter_region": "CON Ingiza jina la mkoa (mf. Mbeya):",
        "price_result": "END Bei ya {crop} katika {region} ni wastani wa TZS {avg}/kg",
        "no_prices": "END Hakuna bei za {crop} katika {region} kwa sasa.",
        "input_crop_price": "CON Ingiza jina la zao, bei, na mkoa (mf. Mpunga 1300 Morogoro):",
        "confirm_submission": "END {crop} kwa TZS {price}/kg ({region}) imepokelewa. Asante!",
        "invalid_format": "END Samahani, format si sahihi. Tumia (mf. Maharage 2100 Arusha).",
        "invalid_choice": "END Chaguo si sahihi. Jaribu tena.",
        "sms_confirmation": "{crop} kwa TZS {price}/kg ({region}) imepokelewa kwenye Mkulima Soko.",
    },
    "en": {
        "language_choice": "CON Choose language:\n1. Kiswahili\n2. English",
        "welcome": "CON Welcome to Mkulima Soko 🧑🏾‍🌾\n1. Check crop prices\n2. Submit crop price",
        "select_category": "CON Choose crop type:\n1. Food crops\n2. Cash crops",
        "enter_crop_name": "CON Enter crop name:",
        "enter_region": "CON Enter region name (e.g. Mbeya):",
        "price_result": "END Average price of {crop} in {region} is TZS {avg}/kg",
        "no_prices": "END No prices found for {crop} in {region}.",
        "input_crop_price": "CON Enter crop name, price, and region (e.g. Rice 1500 Mbeya):",
        "confirm_submission": "END {crop} at TZS {price}/kg in {region} has been received. Thank you!",
        "invalid_format": "END Invalid format. Try (e.g. Rice 1500 Mbeya).",
        "invalid_choice": "END Invalid choice. Please try again.",
        "sms_confirmation": "{crop} at TZS {price}/kg in {region} has been received in Mkulima Soko.",
    }
}


def send_sms(to, message):
    try:
        sms.send(message, [to])
    except Exception as e:
        print("SMS failed:", e)

def handle_ussd(session_id, service_code, phone_number, text):
    parts = text.strip().split("*")
    level = len(parts)

    if text == "":
        return Response(MESSAGES["sw"]["language_choice"], mimetype="text/plain")

    # Language selection
    if parts[0] == "1":
        lang = "sw"
    elif parts[0] == "2":
        lang = "en"
    else:
        return Response("END Invalid language selection.", mimetype="text/plain")

    # Main menu
    if level == 1:
        return Response(MESSAGES[lang]["welcome"], mimetype="text/plain")

    # Check Prices Flow
    elif parts[1] == "1":
        if level == 2:
            return Response(MESSAGES[lang]["select_category"], mimetype="text/plain")
        elif level == 3:
            return Response(MESSAGES[lang]["enter_crop_name"], mimetype="text/plain")
        elif level == 4:
            return Response(MESSAGES[lang]["enter_region"], mimetype="text/plain")
        elif level == 5:
            crop = parts[3].capitalize()
            region = parts[4].capitalize()
            prices = get_prices_by_crop_and_region(crop, region)
            if prices:
                avg = sum(prices) // len(prices)
                msg = MESSAGES[lang]["price_result"].format(crop=crop, region=region, avg=avg)
            else:
                msg = MESSAGES[lang]["no_prices"].format(crop=crop, region=region)
            return Response(msg, mimetype="text/plain")

    # Submit Price Flow
    elif parts[1] == "2":
        if level == 2:
            return Response(MESSAGES[lang]["select_category"], mimetype="text/plain")
        elif level == 3:
            return Response(MESSAGES[lang]["input_crop_price"], mimetype="text/plain")
        elif level == 4:
            try:
                category = "Chakula" if parts[2] == "1" else "Biashara" if parts[2] == "2" else None
                if not category:
                    return Response(MESSAGES[lang]["invalid_choice"], mimetype="text/plain")

                data = parts[3].split(" ")
                crop = data[0].capitalize()
                price = int(data[1])
                region = " ".join(data[2:]).capitalize()

                add_price(crop, region, price, category)  # Updated to include category

                confirmation = MESSAGES[lang]["confirm_submission"].format(crop=crop, price=price, region=region)
                sms_text = MESSAGES[lang]["sms_confirmation"].format(crop=crop, price=price, region=region)
                send_sms(phone_number, sms_text)

                return Response(confirmation, mimetype="text/plain")
            except:
                return Response(MESSAGES[lang]["invalid_format"], mimetype="text/plain")

    return Response(MESSAGES[lang]["invalid_choice"], mimetype="text/plain")
