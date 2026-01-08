// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract FreshChain {
    
    struct Batch {
        uint256 id;
        string productName;
        uint256 price; // Price in Wei (1 ETH = 10^18 Wei)
        uint256 temperature;
        bool isDiscounted;
    }

    mapping(uint256 => Batch) public batches;
    uint256 public batchCount;

    // Event: This alerts your Frontend when the price changes
    event PriceUpdated(uint256 batchId, uint256 newPrice, uint256 temperature);

    // 1. Create a new batch of food (e.g. "Strawberries", 1000)
    function createBatch(string memory _name, uint256 _price) public {
        batchCount++;
        batches[batchCount] = Batch(batchCount, _name, _price, 0, false);
    }

    // 2. The Sensor calls this function to report temperature
    function updateTemperature(uint256 _batchId, uint256 _temp) public {
        Batch storage batch = batches[_batchId];
        batch.temperature = _temp;

        // FEFO LOGIC: If temp > 30 degrees, slash price by 50%
        if (_temp > 30 && !batch.isDiscounted) {
            batch.price = batch.price / 2;
            batch.isDiscounted = true;
        }

        emit PriceUpdated(_batchId, batch.price, _temp);
    }
}