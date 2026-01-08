import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

const FreshChainModule = buildModule("FreshChainModule", (m) => {
  // Deploy the contract
  const freshChain = m.contract("FreshChain");

  return { freshChain };
});

export default FreshChainModule;