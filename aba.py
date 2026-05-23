import hashlib
import hmac
import base64
import requests
import json
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()


def get_env(name, fallback=None, required=False):
    value = os.getenv(name, fallback)
    if required and not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def build_hash_string(fields):
    ordered_keys = [
        "req_time",
        "merchant_id",
        "tran_id",
        "amount",
        "items",
        "shipping",
        "ctid",
        "pwt",
        "firstname",
        "lastname",
        "email",
        "phone",
        "type",
        "payment_option",
        "return_url",
        "cancel_url",
        "continue_success_url",
        "return_deeplink",
        "currency",
        "custom_fields",
        "return_params",
    ]
    return "".join(str(fields[key]) for key in ordered_keys if key in fields)


API_URL = get_env("PAYWAY_PURCHASE_URL", fallback=get_env("PAYWAY_URL"), required=True)
MERCHANT_ID = get_env("PAYWAY_MERCHANT_ID", required=True)
API_KEY = get_env("PAYWAY_API_KEY", fallback=get_env("PAYWAY_PUBLIC_KEY"), required=True)
BASE_URL = get_env("BASE_URL", fallback="http://127.0.0.1:5000")
CURRENCY = get_env("CURRENCY", fallback="USD")

def generate_aba_hash(data_string):
    hash_obj = hmac.new(
        API_KEY.encode('utf-8'), 
        data_string.encode('utf-8'), 
        hashlib.sha512
    )
    return base64.b64encode(hash_obj.digest()).decode('utf-8')

def start_payment():
    now = datetime.now(timezone.utc)
    req_time = now.strftime("%Y%m%d%H%M%S") 
    tran_id = f"ORD{now.strftime('%Y%m%d%H%M%S')}"  
    amount = "4000.00" 
    items_list = [{"name":"Service","quantity":"1","price":"4000.00"}]
    items_json = json.dumps(items_list, separators=(',', ':'))
    items_base64 = base64.b64encode(items_json.encode('utf-8')).decode('utf-8')
    
    firstname = "Yorm"
    lastname = "Ratana"
    email = "test@example.com"
    phone = "012345678"
    transaction_type = "purchase"
    payload = {
        'req_time': req_time,
        'merchant_id': MERCHANT_ID,
        'tran_id': tran_id,
        'amount': amount,
        'items': items_base64,
        'firstname': firstname,
        'lastname': lastname,
        'email': email,
        'phone': phone,
        'type': transaction_type,
        'currency': CURRENCY,
        'continue_success_url': f"{BASE_URL.rstrip('/')}/success",
    }
    hash_value = generate_aba_hash(build_hash_string(payload))
    payload['hash'] = hash_value

    print(f"--- Sending: {tran_id} ---")
    try:
        response = requests.post(API_URL, data=payload)
        result = response.json()
        status_data = result.get('status', {})
        code = str(status_data.get('code'))

        if code in ['0', '00']:
            print("SUCCESS!")
            print(f"Checkout Link: {result.get('url')}")
            
            if 'qrImage' in result:
                qr_raw = result['qrImage'].split(",")[-1]
                with open("aba_qr.png", "wb") as f:
                    f.write(base64.b64decode(qr_raw))
                print("QR code saved to 'aba_qr.png'")
        else:
            print(f"Error: {status_data.get('message')}")
            print(f"Server Response: {result}")

    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    start_payment()
