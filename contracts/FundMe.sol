// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

import "@chainlink/contracts/src/v0.7/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.7/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256;

    mapping(address => uint256) public addressToAmountFunded;
    address[] private funders;
    address private owner;
    AggregatorV3Interface private dataFeed;

    constructor(address _priceFeed) {
        dataFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    // Function that returns owner of this contract
    function getOwner() public view returns (address) {
        return (owner);
    }

    // Function that returns ethereum price in USD expressed in wei precision
    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = dataFeed.latestRoundData();
        return (uint256(answer * (10 ** 10))); // Multiply by missing wei precision digits
    }

    // Convert ETH amount expressed in wei into USD, expressed in wei precision
    function convert(uint256 ethQty) private view returns (uint256) {
        uint256 ethPrice = getPrice();
        uint256 usdQty = (ethQty * ethPrice) / (10 ** 18); // Divide by wei precision
        return (usdQty);
    }

    // Returns the entrance Fee expressed in eth (wei precision)
    function getEntranceFee() public view returns (uint256) {
        uint256 minimum = 50 * 10 ** 18;
        uint256 ethPrice = getPrice();
        return ((minimum * (10 ** 18)) / ethPrice);
    }

    //--------------------------------------------------------------------------------------------------------

    // Function that checks if the funding is higher than 50 USD and accept/refuses it
    function fund() public payable {
        uint256 minimum = 50 * 10 ** 18; // Minimum funding expressed in wei precision
        require(convert(msg.value) > minimum, "Too low funding! Add more ETH!");

        addressToAmountFunded[msg.sender] += msg.value;

        if (funders.length == 0) {
            funders.push(msg.sender);
        } else {
            for (uint256 i = 0; i < funders.length; i++) {
                if (msg.sender == funders[i]) {
                    break;
                }
                if (i + 1 == funders.length) {
                    funders.push(msg.sender);
                }
            }
        }
    }

    // Recover all the funds without needing the explicit address
    function withdraw() public {
        payable(msg.sender).transfer(addressToAmountFunded[msg.sender]);
        addressToAmountFunded[msg.sender] = 0;
    }

    //-------------------------------------------------------------------------------------------------------

    // This modifier forces the function to execute this code
    modifier onlyOwner() {
        require(msg.sender == owner, "You're not the owner!");
        _;
    }

    // Function that put every address amount to 0 and withdraws to the owner
    function withdrawAll() private {
        for (uint256 index; index < funders.length; index++) {
            addressToAmountFunded[funders[index]] = 0;
        }
        payable(msg.sender).transfer(address(this).balance);
        funders = new address[](0);
    }

    // Function that makes you withdraw everything but only if you're the owner
    function ownerWithdrawAll() public onlyOwner {
        withdrawAll();
    }
}
