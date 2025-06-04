
// SPDX-License-Identifier: MIT


pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract TokenMarketplace {
    IERC20 public token;
    uint public tokenPrice; // in wei per token, e.g., 1 ether = 10^18 wei

    constructor(address _token, uint _tokenPrice) payable {
        token = IERC20(_token);
        tokenPrice = _tokenPrice; // e.g., 1 ether
    }

    // Buy tokens with ether
    function buyTokens() public payable {
        uint tokensToBuy = msg.value / tokenPrice;
        require(tokensToBuy > 0, "Insufficient ether sent");
        require(token.balanceOf(address(this)) >= tokensToBuy, "Not enough tokens in reserve");
        token.transfer(msg.sender, tokensToBuy);
    }

    // Sell tokens for ether
    function sellTokens(uint amount) public {
        require(amount > 0, "Amount must be greater than 0");
        uint etherToSend = amount * tokenPrice;
        require(address(this).balance >= etherToSend, "Not enough ether in reserve");
        require(token.transferFrom(msg.sender, address(this), amount), "Token transfer failed");
        payable(msg.sender).transfer(etherToSend);
    }

    // Allow contract to receive ether during deployment or top-ups
    receive() external payable {}
}