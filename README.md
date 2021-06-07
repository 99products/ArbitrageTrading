# ArbitrageTrading
Arbitrage is trading that exploits the tiny differences in price between identical assets in two or more markets. 

The arbitrage trader buys the asset in one market and sells it in the other market at the same time in order to pocket the difference between the two prices

Here we are trying to do it between binance and wazirx.

1. Generally the ask is always higher than the bid in given exchange
2. For arbitrage to work, For the given coinpair, the ask in one exchange should be less than the bid in other, so you can buy from that ask and sell to the other bid
3. Once the change % is greater than the threshold, we notify to our telegram channel
4. Configure CHANGE_THRESHOLD, TELEGRAM_API_TOKEN for your bot, and TELEGRAM_CHANNEL ( your bot should be admin for the channel, to be able to post message)


Note:  With more and more users, arbitrage becomes a rare event, and may not work always, and even if does it will last only for a short time window.

This project aims at leveraging binance and wazirx api to give a start to use and understand how crypto exchanges work ( ask, bid etc.)
