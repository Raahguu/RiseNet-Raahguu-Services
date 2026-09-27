from flask import Flask, request, Response, render_template, make_response, redirect
import subprocess
import requests
from eth_account import Account
from  decimal import Decimal
import time

app = Flask(__name__)
ANVIL_URL = "http://127.0.0.1:8545"

from web3 import Web3
w3 = Web3(Web3.HTTPProvider(ANVIL_URL))
assert w3.is_connected()

# Gets the balance of an account
def get_balance(address):
    return w3.from_wei(w3.eth.get_balance(address), "ether")

# Gives the specified address the specified amount
def fund_account(address, amount):
    current_balance = get_balance(address)

    w3.provider.make_request(
        "anvil_setBalance",
        [
            address,
            hex(int(amount + w3.to_wei(current_balance, "ether")))
        ]
    )

# Creates account
def get_keys():
    account = Account.create()
    fund_account(account.address, w3.to_wei(10, "ether"))
    return account.address, account.key.hex()

# Eth Fountain
FOUNT_COOLDOWN=60
_last_click = {}

def check_cooldown(address) -> bool:
    now = time.time()

    if (now - int(_last_click.get(address, 0))) > 60:
        _last_click[address] = now
        return True
    else: 
        return False


@app.route('/', methods=["GET"])
def index():
    new_cookie = False

    # Check if the cookie already exists
    addresses = [request.cookies.get(name) for name in ["pub", "priv"]]
    # If not, create one
    if None in addresses:
        # 0 = Public
        # 1 = Private
        addresses[0], addresses[1] = get_keys()
        new_cookie = True

    balance = get_balance(addresses[0])

    # Build the response using the cookie value
    response = make_response(render_template(
        "index.html",
        pubk=addresses[0],
        privk=addresses[1],
        bal=balance,
    ))

    # Set the cookie only if it was missing
    if new_cookie:
        response.set_cookie("pub", addresses[0])
        response.set_cookie("priv", addresses[1])

    return response

@app.route('/', methods=["POST"])
def rpc():
    # Check to make sure anvil control commands aren't being used
    if request.json["method"].startswith("anvil_"):
        return {"error": "Method not allowed"}, 403

    r = requests.post(
        ANVIL_URL,
        data=request.data,
        headers={
            k: v
            for k, v in request.headers.items()
            if k.lower() != "host"
        },
    )

    return Response(
        r.content,
        status=r.status_code,
        content_type=r.headers.get("Content-Type"),
    )

# Add 10 eth to a users account
@app.route("/fount", methods=["POST"])
def gen_eth():
    public, private = [request.cookies.get(name) for name in ["pub", "priv"]]

    if check_cooldown(public):
        fund_account(public, w3.to_wei(1, "ether"))

    return 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
