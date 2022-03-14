//SPDX : MIT

pragma solidity ^0.6.0;

import "./SimpleStorage.sol";

contract StorageFactory{

    SimpleStorage[] public simpleStorageArray;

    function createSimpleStorageContract()public{
        SimpleStorage simpleStorage = new SimpleStorage();
        simpleStorageArray.push(simpleStorage);//address 
        // create the contract and add to the array
    }

    function sfStore(uint256 _simpleStorageIndex, uint256 _simpleStorageNo) public{
        //we need address and ABI
        SimpleStorage simpleStorage=SimpleStorage(address(simpleStorageArray[_simpleStorageIndex]));//address is given to get the corresponding contract
        simpleStorage.store(_simpleStorageNo);//add the favourite no the nth contract
    }

    function sfGet(uint256 _simpleStorageIndex) public view returns(uint256){//view- state is viewing not changing
         SimpleStorage simpleStorage=SimpleStorage(address(simpleStorageArray[_simpleStorageIndex]));
         return simpleStorage.retrieve();

         // OR return SimpleStorage(address(simpleStorageArray[_simpleStorageIndex])).retrieve(); - FOR above to 2 lines
    }
}
