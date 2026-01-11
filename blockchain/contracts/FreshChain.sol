// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FreshChain {
    
    struct TrackingEvent {
        string status;          // "In Transit", "Delivered"
        string location;        // "NH45, Chennai" (or GPS Coords)
        uint256 timestamp;
    }

    struct SensorAlert {
        string alertType;       // "TEMP_HIGH", "TEMP_LOW", "BACK_NORMAL"
        bytes encryptedData;    // Temperature data (Encrypted)
        uint256 timestamp;
    }

    struct Batch {
        string batchId;         // UUID (e.g. "550e8400-e29b...")
        string productType;     // "Tomatoes"
        address currentOwner;
        TrackingEvent[] history;
        SensorAlert[] alerts;
    }

    mapping(string => Batch) public batches;
    
    // 1. Create Batch (Farmer)
    function createBatch(string memory _batchId, string memory _productType) public {
        require(bytes(batches[_batchId].batchId).length == 0, "Batch ID exists");

        Batch storage b = batches[_batchId];
        b.batchId = _batchId;
        b.productType = _productType;
        b.currentOwner = msg.sender;

        // Initial Log
        b.history.push(TrackingEvent("Harvested", "Origin Farm", block.timestamp));
    }

    // 2. Update Location (Truck/Scanner)
    function updateLocation(string memory _batchId, string memory _status, string memory _location) public {
        Batch storage b = batches[_batchId];
        require(bytes(b.batchId).length != 0, "Batch not found");
        
        b.history.push(TrackingEvent(_status, _location, block.timestamp));
        b.currentOwner = msg.sender;
    }

    // 3. Report Excursion (IoT Sensors)
    function reportExcursion(string memory _batchId, string memory _alertType, bytes memory _encryptedSensorData) public {
        Batch storage b = batches[_batchId];
        require(bytes(b.batchId).length != 0, "Batch not found");

        b.alerts.push(SensorAlert({
            alertType: _alertType,
            encryptedData: _encryptedSensorData,
            timestamp: block.timestamp
        }));
    }

    // 4. Fetch Data (Consumer/ML)
    function getBatchDetails(string memory _batchId) public view returns (
        string memory batchId, 
        string memory productType, 
        TrackingEvent[] memory history, 
        SensorAlert[] memory alerts
    ) {
        Batch storage b = batches[_batchId];
        return (b.batchId, b.productType, b.history, b.alerts);
    }
}