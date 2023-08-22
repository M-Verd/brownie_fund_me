from brownie import FundMe, accounts, network, config, MockV3Aggregator
from scripts.useful_scripts import *
from time import sleep


def deployFundMe(_account):
    price_feed_address = ""
    active_network = network.show_active()

    if active_network not in LOCAL_DEV_ENVIRONMENTS:
        price_feed_address = config["networks"][active_network]["ETH_USD_PRICE_FEED"]
    else:
        price_feed_address = mockDeployer(_account)

    ret_addr = FundMe.deploy(
        price_feed_address,
        {"from": _account},
        publish_source=config["networks"][active_network]["verify"],
    )

    return ret_addr


def main():
    deployFundMe(getAccount())

    sleep(4) if (
        network.show_active() in LOCAL_DEV_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ) else sleep(0)
