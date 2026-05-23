# ABA PayWay Python Demo

Simple Python demo for creating an ABA PayWay purchase request with values loaded from a `.env` file.

## Features

- Loads PayWay credentials from `.env`
- Generates the HMAC SHA-512 hash required by PayWay
- Sends a purchase request to the ABA PayWay sandbox API
- Saves the returned QR image when available

## Project Files

- `aba.py` - main payment request script
- `.env` - local configuration file for merchant credentials
- `requirements.txt` - Python dependencies

## Requirements

- Python 3.10+
- ABA PayWay sandbox or production credentials

## Installation

```bash
pip install -r requirements.txt
```

## Environment Setup

Create a `.env` file in the project root:

```env
PAYWAY_MERCHANT_ID=xxxxxxxx
PAYWAY_API_KEY=xxxxxxxx
PAYWAY_PURCHASE_URL=https://checkout-sandbox.payway.com.kh/api/payment-gateway/v1/payments/purchase
PAYWAY_CHECK_URL=PUT_CHECK_TRANSACTION_URL_HERE
BASE_URL=http://127.0.0.1:5000
CURRENCY=KHR
PAYWAY_URL=https://checkout-sandbox.payway.com.kh/api/payment-gateway/v1/payments/purchase
```

## Environment Variables

| Variable | Description |
| --- | --- |
| `PAYWAY_MERCHANT_ID` | Merchant ID provided by ABA PayWay |
| `PAYWAY_API_KEY` | Secret key used to generate the request hash |
| `PAYWAY_PURCHASE_URL` | Purchase API endpoint |
| `PAYWAY_CHECK_URL` | Check transaction endpoint |
| `BASE_URL` | Base URL used for success callback |
| `CURRENCY` | Payment currency such as `KHR` or `USD` |
| `PAYWAY_URL` | Fallback purchase URL if needed |

## Run

```bash
python3 aba.py
```

## Notes

- Keep `.env` private and do not commit it to Git.
- Sandbox purchase URL:
  `https://checkout-sandbox.payway.com.kh/api/payment-gateway/v1/payments/purchase`
- Production purchase URL:
  `https://checkout.payway.com.kh/api/payment-gateway/v1/payments/purchase`
