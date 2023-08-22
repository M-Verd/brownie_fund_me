from brownie import FundMe
from scripts.useful_scripts import getAccount


def print_info(fundme_addr):
    print(f"\nThe owner is: {fundme_addr.getOwner()}")
    print(f"Current ETH price is: {fundme_addr.getPrice()}")
    print(f"The entrance Fee is: {fundme_addr.getEntranceFee()}\n")


def fund(fundme_addr, account):
    fundme_addr.fund({"from": account, "value": 9000000000000000000})


def withdraw(fundme_addr, account):
    fundme_addr.withdraw({"from": account})


def main():
    fundme_addr = FundMe[-1]
    account = getAccount()

    print_info(fundme_addr)
    fund(fundme_addr, account)
    withdraw(fundme_addr, account)
