from brownie import FundMe, accounts, network, exceptions
from scripts.deploy import deployFundMe
from scripts.useful_scripts import getAccount, LOCAL_DEV_ENVIRONMENTS
import pytest


def test_fund():
    # ARRANGE
    account = getAccount()
    working_address = deployFundMe(account)

    # ACT
    tx = working_address.fund({"from": account, "value": 1 * (10**18)})
    tx.wait(1)

    # ASSERT
    assert working_address.getOwner() == account
    assert working_address.addressToAmountFunded(account) != 0


def test_withdraw():
    # ARRANGE
    account = getAccount()
    working_address = deployFundMe(account)
    working_address.fund({"from": account, "value": 1 * (10**18)})

    # ACT
    tx = working_address.withdraw({"from": account})
    tx.wait(1)

    # ASSERT
    assert working_address.addressToAmountFunded(account) == 0
    assert working_address.balance() == 0


def test_withdraw_only_owner():
    if network.show_active() not in LOCAL_DEV_ENVIRONMENTS:
        pytest.skip("Only for Local Networks!")
    else:
        # ARRANGE
        account = getAccount()
        bad_actor = accounts.add()
        working_address = deployFundMe(account)
        working_address.fund({"from": account, "value": 1 * (10**18)})

        # ACT
        with pytest.raises(exceptions.VirtualMachineError):
            working_address.ownerWithdrawAll({"from": bad_actor})

        tx = working_address.ownerWithdrawAll({"from": account})
        tx.wait(1)

        # ASSERT
        assert working_address.addressToAmountFunded(account) == 0
        assert working_address.balance() == 0
