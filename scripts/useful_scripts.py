from brownie import accounts, network, MockV3Aggregator
from web3 import Web3

# Those are useful scripts to deploy a mock, in case we are working in a local environment, and to get a proper account for the network.
# Since it's everything on brownie, the account used for non-local networks is retrieved from already saved account in the brownie venv.

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_DEV_ENVIRONMENTS = ["development", "ganache-local"]

DECIMALS = 8
STARTING_PRICE = 200000000000


def getAccount():
    active_network = network.show_active()
    print(
        f"\nThe active network is {active_network}, Getting an account for this one..."
    )
    if (
        active_network in LOCAL_DEV_ENVIRONMENTS
        or active_network in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.load("Developing-account")


def mockDeployer(_account):
    print("\n-------------------- Deploying Mocks...\n")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": _account})
        print("\n-------------------- Mocks deployed!\n")
    else:
        print("-------------------- Mocks ALREADY deployed!\n")
    return MockV3Aggregator[-1].address
