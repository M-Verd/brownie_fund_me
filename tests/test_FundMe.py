from brownie import FundMe, accounts, network, exceptions
from scripts.deploy import deployFundMe
from scripts.useful_scripts import getAccount, LOCAL_DEV_ENVIRONMENTS
import pytest

# This testing script will test fund, withdraw and withdraw_only_owner functions


def test_fund():
    # ARRANGE
    account = getAccount()
    testing_address = deployFundMe(account)

    # ACT
    tx = testing_address.fund({"from": account, "value": 1 * (10**18)})
    tx.wait(1)

    # ASSERT
    assert testing_address.addressToAmountFunded(account) != 0


def test_withdraw():
    # ARRANGE
    account = getAccount()
    testing_address = deployFundMe(account)
    testing_address.fund({"from": account, "value": 1 * (10**18)})

    # ACT
    tx = testing_address.withdraw({"from": account})
    tx.wait(1)

    # ASSERT
    assert testing_address.addressToAmountFunded(account) == 0
    assert testing_address.balance() == 0


def test_withdraw_only_owner():
    if network.show_active() not in LOCAL_DEV_ENVIRONMENTS:
        pytest.skip("Only for Local Networks!")
    else:
        # ARRANGE
        account = getAccount()
        bad_actor = accounts.add()
        testing_address = deployFundMe(account)
        testing_address.fund({"from": account, "value": 1 * (10**18)})

        # ACT
        with pytest.raises(exceptions.VirtualMachineError):
            testing_address.ownerWithdrawAll({"from": bad_actor})

        tx = testing_address.ownerWithdrawAll({"from": account})
        tx.wait(1)

        # ASSERT
        assert testing_address.getOwner() == account
        assert testing_address.addressToAmountFunded(account) == 0
        assert testing_address.balance() == 0
