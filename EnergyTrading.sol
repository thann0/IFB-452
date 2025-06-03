pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract EnergyTrading {
    IERC20 public token;

    struct Offer {
        address prosumer;
        uint energyAmount;  // in kWh
        uint pricePerUnit;  // in tokens per kWh
        bool active;
    }

    Offer[] public offers;

    constructor(address _token) {
        token = IERC20(_token);
    }

    // Prosumer creates an energy offer
    function createOffer(uint energyAmount, uint pricePerUnit) public {
        require(energyAmount > 0, "Energy amount must be greater than 0");
        require(pricePerUnit > 0, "Price must be greater than 0");
        offers.push(Offer(msg.sender, energyAmount, pricePerUnit, true));
    }

    // Consumer buys energy from an offer
    function buyEnergy(uint offerId, uint energyAmount) public {
        Offer storage offer = offers[offerId];
        require(offer.active, "Offer not active");
        require(offer.energyAmount >= energyAmount, "Not enough energy available");

        uint totalPrice = energyAmount * offer.pricePerUnit;
        require(token.transferFrom(msg.sender, offer.prosumer, totalPrice), "Token transfer failed");

        offer.energyAmount -= energyAmount;
        if (offer.energyAmount == 0) {
            offer.active = false;
        }
    }

    // Get number of offers (for UI)
    function getOfferCount() public view returns (uint) {
        return offers.length;
    }
}