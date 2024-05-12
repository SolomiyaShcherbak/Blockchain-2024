// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

contract MessageStorage {
    mapping(address => mapping(address => string[])) private _messages;
    mapping(address => address[]) private _contacts;

    event MessageSent(address indexed sender, address indexed receiver, string message);

    function sendMessage(address receiver, string memory message) external {
        require(receiver != address(0), "Invalid receiver address");
        require(bytes(message).length > 0, "Message cannot be empty");

        _messages[msg.sender][receiver].push(message);
        
        if (!isContact(msg.sender, receiver)) {
            _contacts[msg.sender].push(receiver);
        }
        if (!isContact(receiver, msg.sender)) {
            _contacts[receiver].push(msg.sender);
        }

        emit MessageSent(msg.sender, receiver, message);
    }

    function getMessagesFrom(address sender) external view returns (string[] memory) {
        return _messages[sender][msg.sender];
    }

    function getAllMessages() external view returns(string[][] memory){
        address[] memory userContacts = _contacts[msg.sender];
        string[][] memory userMessages = new string[][](userContacts.length);

        for (uint128 i = 0; i < userContacts.length; i++) {
            userMessages[i] = _messages[userContacts[i]][msg.sender];
        }

        return userMessages;
    }

    function viewContacts() external view returns (address[] memory) {
        return _contacts[msg.sender];
    }

    function isContact(address user, address contact) private view returns (bool) {
        for (uint i = 0; i < _contacts[user].length; i++) {
            if (_contacts[user][i] == contact) {
                return true;
            }
        }
        return false;
    }
}