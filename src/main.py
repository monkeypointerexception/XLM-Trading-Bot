import time

from algos import calculate_rsi, stop_loss
from orders import sell_order, buy_order
from authenticate import CoinbaseExchangeAuth
from constants import cbprokeys

def main():
    #instantiate the auth and stop loss objects 
    auth = CoinbaseExchangeAuth(cbprokeys.key, cbprokeys.secret, cbprokeys.passphrase)
    stp_val = stop_loss(0,auth)

    try:
        while True:
            stp_val()
            rsi = calculate_rsi(auth)
            if rsi >= 70:
                sell_order(auth,stp_val)
            elif rsi <= 30:
                buy_order(auth,stp_val)
            else:
                print(rsi)
            time.sleep(5)
        #control + c 
    except KeyboardInterrupt:
        print("trading halted :(")

if __name__ == "__main__":
    main()
