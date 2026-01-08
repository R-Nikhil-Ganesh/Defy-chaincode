@echo off
echo Starting FreshChain Environment...

:: 1. Start Hardhat Node in a new window
start "Blockchain Node" cmd /k "cd blockchain && npx hardhat node"

:: 2. Wait 5 seconds for the node to wake up
timeout /t 5

:: 3. Deploy the Contract
echo Deploying Contract...
cd blockchain
call npx hardhat ignition deploy ./ignition/modules/FreshChain.ts --network localhost

:: 4. Pause to let you copy the address
echo.
echo ---------------------------------------------------
echo CHECK THE ADDRESS ABOVE!
echo If it changed, update it in backend/sensor_sim.py
echo ---------------------------------------------------
pause

:: 5. Switch to Backend and activate Python
cd ..\backend
call ..\venv\Scripts\activate
echo.
echo Ready to run sensor! Type: python sensor_sim.py
cmd /k