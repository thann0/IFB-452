pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract EnergyToken is ERC20 {
    constructor(uint256 initialSupply) ERC20("EnergyToken", "ETK") {
        _mint(msg.sender, initialSupply);
    }
}