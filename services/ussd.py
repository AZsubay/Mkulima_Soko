from flask import request, make_response
from db import get_prices  # your DB function to get prices


def handle_ussd():
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "")

    # Split the user input by * to simulate multi-level menu navigation
    user_response = text.split("*") if text else []

    if text == "":
        # First menu
        response = "CON Karibu Mkulima Soko!\n"
        response += "1. Tazama bei ya mazao\n"
        response += "2. Ongeza mazao yako"
    
    elif user_response[0] == "1":
        if len(user_response) == 1:
            # Show crops options (example crops)
            response = "CON Chagua zao:\n"
            response += "1. Mahindi\n2. Maharage\n3. Mpunga"
        elif len(user_response) == 2:
            crop_map = {"1": "mahindi", "2": "maharage", "3": "mpunga"}
            crop_choice = user_response[1]
            crop = crop_map.get(crop_choice, None)
            if not crop:
                response = "END Chaguo batili."
            else:
                # Fetch prices from DB for this crop
                prices = get_prices()
                # Filter prices for this crop
                crop_prices = [p for c, r, p in prices if c == crop]
                if crop_prices:
                    avg_price = sum(crop_prices) // len(crop_prices)
                    response = f"END Bei ya wastani ya {crop.title()} ni TZS {avg_price}/kg"
                else:
                    response = f"END Hakuna taarifa za bei ya {crop.title()}."
        else:
            response = "END Chaguo batili."

    elif user_response[0] == "2":
        # For adding crops (simple placeholder)
        response = "END Huduma ya kuongeza mazao bado haijakamilika."

    else:
        response = "END Chaguo batili. Tafadhali jaribu tena."

    return make_response(response, 200, {"Content-Type": "text/plain"})
