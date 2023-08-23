from brownie import FundMe, network
from scripts.useful_scripts import (
    getAccount,
    LOCAL_DEV_ENVIRONMENTS,
    FORKED_LOCAL_ENVIRONMENTS,
)
from scripts.deploy import deployFundMe
from time import sleep

# This script will interact with an already deployed contract.
# If it wasn't already deployed it will deploy one to run the interactions.


def print_info(fundme_addr):
    print(f"\nThe owner is: {fundme_addr.getOwner()}")
    print(f"Current ETH price is: {fundme_addr.getPrice()}")
    print(f"The entrance Fee is: {fundme_addr.getEntranceFee()}\n")


def fund(fundme_addr, account):
    tx = fundme_addr.fund({"from": account, "value": 9000000000000000000})
    tx.wait(1)


def withdraw(fundme_addr, account):
    tx = fundme_addr.withdraw({"from": account})
    tx.wait(1)


def main():
    fundme_addr = ""
    account = getAccount()

    try:
        fundme_addr = FundMe[-1]
    except:
        print("No already deployed contract found, deploying one...\n")
        fundme_addr = deployFundMe(account)

    print_info(fundme_addr)
    fund(fundme_addr, account)
    withdraw(fundme_addr, account)

    sleep(2) if (
        network.show_active() in LOCAL_DEV_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ) else sleep(0)
