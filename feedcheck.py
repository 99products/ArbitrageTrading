import datetime
from cryptofeed import FeedHandler
from cryptofeed.callback import  TickerCallback
from cryptofeed.defines import TICKER
from cryptofeed.exchange.binance import Binance
import requests
import threading
import json


TELEGRAM_API_TOKEN='1744663241:AAGQf-dSj8nwUD4SIUMQf4oIAjg9TsMgdGY'
TELEGRAM_CHANNEL='wazirx_updates'

BINANCE_SYMBOLS=['BTC-USDT', 'ETH-USDT', 'BNB-USDT', 'NEO-USDT', 'LTC-USDT', 'QTUM-USDT', 'ADA-USDT', 'XRP-USDT', 'EOS-USDT', 'TUSD-USDT', 'IOTA-USDT', 'XLM-USDT', 'ONT-USDT', 'TRX-USDT', 'ETC-USDT', 'ICX-USDT', 'NULS-USDT', 'VET-USDT', 'PAX-USDT', 'USDC-USDT', 'LINK-USDT', 'WAVES-USDT', 'BTT-USDT', 'ONG-USDT', 'HOT-USDT', 'ZIL-USDT', 'ZRX-USDT', 'FET-USDT', 'BAT-USDT', 'XMR-USDT', 'ZEC-USDT', 'IOST-USDT', 'CELR-USDT', 'DASH-USDT', 'NANO-USDT', 'OMG-USDT', 'THETA-USDT', 'ENJ-USDT', 'MITH-USDT', 'MATIC-USDT', 'ATOM-USDT', 'TFUEL-USDT', 'ONE-USDT', 'FTM-USDT', 'ALGO-USDT', 'GTO-USDT', 'DOGE-USDT', 'DUSK-USDT', 'ANKR-USDT', 'WIN-USDT', 'COS-USDT', 'COCOS-USDT', 'MTL-USDT', 'TOMO-USDT', 'PERL-USDT', 'DENT-USDT', 'MFT-USDT', 'KEY-USDT', 'DOCK-USDT', 'WAN-USDT', 'FUN-USDT', 'CVC-USDT', 'CHZ-USDT', 'BAND-USDT', 'BUSD-USDT', 'BEAM-USDT', 'XTZ-USDT', 'REN-USDT', 'RVN-USDT', 'HBAR-USDT', 'NKN-USDT', 'STX-USDT', 'KAVA-USDT', 'ARPA-USDT', 'IOTX-USDT', 'RLC-USDT', 'CTXC-USDT', 'BCH-USDT', 'TROY-USDT', 'VITE-USDT', 'FTT-USDT', 'EUR-USDT', 'OGN-USDT', 'DREP-USDT', 'TCT-USDT', 'WRX-USDT', 'BTS-USDT', 'LSK-USDT', 'BNT-USDT', 'LTO-USDT', 'AION-USDT', 'MBL-USDT', 'COTI-USDT', 'STPT-USDT', 'WTC-USDT', 'DATA-USDT', 'SOL-USDT', 'CTSI-USDT', 'HIVE-USDT', 'CHR-USDT', 'BTCUP-USDT', 'BTCDOWN-USDT', 'GXS-USDT', 'ARDR-USDT', 'MDT-USDT', 'STMX-USDT', 'KNC-USDT', 'REP-USDT', 'LRC-USDT', 'PNT-USDT', 'COMP-USDT', 'SC-USDT', 'ZEN-USDT', 'SNX-USDT', 'ETHUP-USDT', 'ETHDOWN-USDT', 'ADAUP-USDT', 'ADADOWN-USDT', 'LINKUP-USDT', 'LINKDOWN-USDT', 'VTHO-USDT', 'DGB-USDT', 'GBP-USDT', 'SXP-USDT', 'MKR-USDT', 'DCR-USDT', 'STORJ-USDT', 'BNBUP-USDT', 'BNBDOWN-USDT', 'XTZUP-USDT', 'XTZDOWN-USDT', 'MANA-USDT', 'AUD-USDT', 'YFI-USDT', 'BAL-USDT', 'BLZ-USDT', 'IRIS-USDT', 'KMD-USDT', 'JST-USDT', 'SRM-USDT', 'ANT-USDT', 'CRV-USDT', 'SAND-USDT', 'OCEAN-USDT', 'NMR-USDT', 'DOT-USDT', 'LUNA-USDT', 'RSR-USDT', 'PAXG-USDT', 'WNXM-USDT', 'TRB-USDT', 'BZRX-USDT', 'SUSHI-USDT', 'YFII-USDT', 'KSM-USDT', 'EGLD-USDT', 'DIA-USDT', 'RUNE-USDT', 'FIO-USDT', 'UMA-USDT', 'EOSUP-USDT', 'EOSDOWN-USDT', 'TRXUP-USDT', 'TRXDOWN-USDT', 'XRPUP-USDT', 'XRPDOWN-USDT', 'DOTUP-USDT', 'DOTDOWN-USDT', 'BEL-USDT', 'WING-USDT', 'LTCUP-USDT', 'LTCDOWN-USDT', 'UNI-USDT', 'NBS-USDT', 'OXT-USDT', 'SUN-USDT', 'AVAX-USDT', 'HNT-USDT', 'FLM-USDT', 'UNIUP-USDT', 'UNIDOWN-USDT', 'ORN-USDT', 'UTK-USDT', 'XVS-USDT', 'ALPHA-USDT', 'AAVE-USDT', 'NEAR-USDT', 'SXPUP-USDT', 'SXPDOWN-USDT', 'FIL-USDT', 'FILUP-USDT', 'FILDOWN-USDT', 'YFIUP-USDT', 'YFIDOWN-USDT', 'INJ-USDT', 'AUDIO-USDT', 'CTK-USDT', 'BCHUP-USDT', 'BCHDOWN-USDT', 'AKRO-USDT', 'AXS-USDT', 'HARD-USDT', 'DNT-USDT', 'STRAX-USDT', 'UNFI-USDT', 'ROSE-USDT', 'AVA-USDT', 'XEM-USDT', 'AAVEUP-USDT', 'AAVEDOWN-USDT', 'SKL-USDT', 'SUSD-USDT', 'SUSHIUP-USDT', 'SUSHIDOWN-USDT', 'XLMUP-USDT', 'XLMDOWN-USDT', 'GRT-USDT', 'JUV-USDT', 'PSG-USDT', '1INCH-USDT', 'REEF-USDT', 'OG-USDT', 'ATM-USDT', 'ASR-USDT', 'CELO-USDT', 'RIF-USDT', 'BTCST-USDT', 'TRU-USDT', 'CKB-USDT', 'TWT-USDT', 'FIRO-USDT', 'LIT-USDT', 'SFP-USDT', 'DODO-USDT', 'CAKE-USDT', 'ACM-USDT', 'BADGER-USDT', 'FIS-USDT', 'OM-USDT', 'POND-USDT', 'DEGO-USDT', 'ALICE-USDT', 'LINA-USDT', 'PERP-USDT', 'RAMP-USDT', 'SUPER-USDT', 'CFX-USDT', 'EPS-USDT', 'AUTO-USDT', 'TKO-USDT', 'PUNDIX-USDT', 'TLM-USDT', '1INCHUP-USDT', '1INCHDOWN-USDT', 'BTG-USDT', 'MIR-USDT', 'BAR-USDT', 'FORTH-USDT', 'BAKE-USDT', 'BURGER-USDT', 'SLP-USDT', 'SHIB-USDT', 'ICP-USDT', 'AR-USDT', 'POLS-USDT', 'MDX-USDT', 'MASK-USDT', 'LPT-USDT']

#Only these symbols can be transferred between wazirx and binance
SUPPORTED_SYMBOLS=['XEM-USDT', 'BZRX-USDT', 'GTO-USDT', 'VET-USDT', 'PAXG-USDT', 'SHIB-USDT', 'IOTX-USDT', 'BNT-USDT', 'DOGE-USDT', 'HBAR-USDT', 'HNT-USDT', 'COMP-USDT', 'WAVES-USDT', 'DOCK-USDT', 'CHZ-USDT', 'AION-USDT', 'DGB-USDT', 'ZRX-USDT', 'KAVA-USDT', 'KMD-USDT', 'IOST-USDT', 'CAKE-USDT', 'DOT-USDT', 'UMA-USDT', 'BAND-USDT', 'AVA-USDT', 'BTC-USDT', 'CVC-USDT', 'AVAX-USDT', 'TKO-USDT', 'EGLD-USDT', 'WIN-USDT', 'FTM-USDT', 'ENJ-USDT', 'INJ-USDT', 'CRV-USDT', 'FTT-USDT', 'ONE-USDT', 'GRT-USDT', 'ANKR-USDT', 'SUSHI-USDT', 'ALGO-USDT', 'ATOM-USDT', 'SC-USDT', 'AAVE-USDT', 'BLZ-USDT', 'UNI-USDT', 'LINK-USDT', 'CKB-USDT', 'WRX-USDT', 'SNX-USDT', 'YFI-USDT', 'LUNA-USDT', 'XTZ-USDT', 'ARDR-USDT', 'MANA-USDT', 'KSM-USDT', 'COS-USDT', 'FIL-USDT', 'EOS-USDT', 'BAL-USDT', 'FET-USDT', 'ETC-USDT', 'BNB-USDT', 'CELR-USDT', 'ETH-USDT', 'ZEC-USDT', 'REN-USDT', 'REP-USDT', 'ZIL-USDT', 'ADA-USDT']

CHANGE_THRESHOLD=1.0

TELEGRAM_WAIT_TIME=5

#The bid/ask can be for very low volume too, so check the volume threshold before triggering the change
VOLUME_THRESHOLD=100

def ticker(exchange, key, bid, ask, e, f):

    # print (str(e)+" "+str(f))
    wazirxbid=wazirxvalues[key]['buy']
    wazirxask = wazirxvalues[key]['sell']
    binanceask=float(ask)
    binancebid = float(bid)



    change = calculate_change(wazirxbid,binanceask)
    # print(change)
    if(change>CHANGE_THRESHOLD and change!=100.0):
        # Check and trigger for buy in binance and sell in wazirx
        message = construct_message(key, False, binanceask, wazirxbid, change)
        wait_post_telegram(message, key,binancebid,binanceask,False,change)

    change = calculate_change(binancebid,wazirxask)
    # print(change)
    if (change > CHANGE_THRESHOLD and change != 100.0):
        #Check and trigger for buy in wazirx and sell in binance
        message=construct_message(key,True,wazirxask,binancebid,change)
        wait_post_telegram(message,key,binancebid,binanceask,True,change)


#The bid in other exchange is greather than ask in given exchange,
#then we have a positive change and trigger
def calculate_change(bid:float, ask:float):
    if(ask==0):
        return 0
    return ((bid - ask) / ask) * 100


postedmessagetracking={}



#Not to spam the channel, wait for TELEGRAM_WAIT_TIME between subsequent posts
def wait_post_telegram(message:str,key:str,binancebuyvalue:float,binancesellvalue:float,buywazirx:bool,change:float):
    lasttimestamp = postedmessagetracking[key] if key in postedmessagetracking.keys() else None
    if(not lasttimestamp or (datetime.datetime.now()-lasttimestamp).seconds>=TELEGRAM_WAIT_TIME):
       postedmessagetracking[key] = datetime.datetime.now()
       #validate once again with the depth as we dont stream wazirx tickers
       if validate_wazirx_depth(key,buywazirx,binancebuyvalue,binancesellvalue,change):
            posttelegram(message)


def construct_message(key:str,buywazirx:bool,buyprice:float,sellprice:float,change:float):
    return key+"\n"+("Buy in wazirx " if buywazirx else"Buy in Binance ")+str(buyprice)+"\n"+("Sell in Binance " if buywazirx else"Sell in Wazirx ")+str(sellprice)+"\n"+str(change)

def validate_wazirx_depth(key:str, buywazirx:bool, binancebidvalue:float, binanceaskvalue:float, change:float):
    depth=wazirx_depth(key)
    if buywazirx:
        # check ask
        topask=depth['asks'][0][0]
        topask=float(topask)
        newchange=calculate_change(binancebidvalue, topask)
        # print(key+' Buy wazirx Initial change: ' + str(change) + " double checked: " + str(newchange))
        if newchange >CHANGE_THRESHOLD:
            volume=topask*float(depth['asks'][0][1])
            return volume>VOLUME_THRESHOLD


    else:
        #check bid
        topbid = depth['bids'][0][0]
        topbid = float(topbid)
        newchange = calculate_change(topbid, binanceaskvalue)
        # print(key+ ' Buy binance Initial change: ' + str(change) + " double checked: " + str(newchange))
        if newchange > CHANGE_THRESHOLD:
            volume=topbid*float(depth['bids'][0][1])
            return volume>VOLUME_THRESHOLD

    print('Rejected in double check '+key)
    return False



def wazirx_depth(key:str):
    key =key.lower().replace('-','')
    response=requests.get('https://api.wazirx.com/api/v2/depth?market='+key)
    return response.json()

def posttelegram(message:str):
    print('post.. \n'+ message)
    try:
        url = "https://api.telegram.org/bot"+TELEGRAM_API_TOKEN+"/sendMessage?chat_id=@"+TELEGRAM_CHANNEL+"&text=" + message
        response = requests.post(url)
        print(response)
    except:
        print('Error sending')

wazirxvalues={}

def wazirxusdt():
    keys=updatewazirx()
    subscribe(keys)

def updatewazirx():
    # print('Updating wazirx')
    response = requests.get("https://api.wazirx.com/api/v2/tickers")
    keys = []
    feed = response.json()
    for key in feed.keys():
        if (key.endswith('usdt')):
            newkey = key.replace('usdt', '-usdt').upper()
            if (newkey in SUPPORTED_SYMBOLS):
                keys.append(newkey)
                wazirxvalues[newkey] = {'buy': float(feed[key]['buy']), 'sell': float(feed[key]['sell']),
                                        'last': float(feed[key]['last'])}

    threading.Timer(5, updatewazirx).start()
    return keys

def subscribe(symbols):
    symbols=['ALGO-USDT']
    fh = FeedHandler()

    ticker_cb = {TICKER: TickerCallback(ticker)}
    fh.add_feed(Binance(symbols=symbols, channels=[TICKER], callbacks=ticker_cb))
    fh.run()


def formatassets():
    with open('supported.json') as f:
        data = json.load(f)
    supportedkeys=[]
    for entry in data:
        supportedkey=entry['assetCode']+'-USDT'
        if supportedkey in BINANCE_SYMBOLS:
            supportedkeys.append(supportedkey)

    print(supportedkeys)

# formatassets()
wazirxusdt()

# print(validate_wazirx_depth('ALGO-USDT',True,1.02,1.05))
# posttelegram('hello11')
