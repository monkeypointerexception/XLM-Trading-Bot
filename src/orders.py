import json, requests, math
import smtplib

from constants import api_url, coin, ids, email

def buy_order(auth, stop_loss):
    selling = get_balance(auth,ids.usd)
    balance = float(selling)
    
    if balance < 1:
        print("insufficient balance to buy")
        return
    
    x = float(get_price(auth))
    balance /= x
    # rounded b/c the smallest amount of xlm we can buy is 1
    balance = math.floor(balance)
    #create market order
    order = {
        'size': balance,
        'type': 'market',
        'side': 'buy',
        'product_id': coin,
    }
    the_order = json.dumps(order)
    
    r = requests.post(api_url + 'orders', the_order, auth=auth).json()
    send_email(r)
    
    #print buy order
    print(r)
    # update stop loss function
    q = requests.get(api_url + 'accounts/'+ids.xlm,auth=auth).json()
    total = ( float(q['balance']) * float(get_price(auth)) )
    stop_loss.update(total)

def sell_order(auth, stop_loss):
    selling = get_balance(auth,ids.xlm)
    balance = round(float(selling))
    if balance < 1:
        print("insufficient balance to sell")
        return
    #create market order
    order = {
        'size': balance,
        'type': 'market',
        'side': 'sell',
        'product_id': coin,
    }
    the_order = json.dumps(order)
    r = requests.post(api_url + 'orders', the_order, auth=auth).json()
    #no need to worry about stop loss now
    stop_loss.update(0)
    send_email(r)
    print(r)

def get_balance(auth, id):
    r = requests.get(api_url + 'accounts/'+ id,auth=auth).json()
    return r['available']

def get_price(auth):
    r = requests.get(api_url + 'products/'+coin+'/ticker',auth=auth).json()
    return r['price']

def send_email(the_order):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(email.user, email.email_pass)
        subject = 'TRADE PLACED'
        body = the_order

        msg = f'Subject: {subject}\n\n{body}'
        smtp.sendmail(email.user, email.recipient, msg)
