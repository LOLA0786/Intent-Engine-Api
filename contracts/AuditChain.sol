// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AuditChain {
    mapping(bytes32 => string) private audits;

    event AuditAppended(bytes32 indexed id, string payload);

    function appendAudit(bytes memory payload) public returns (bytes32) {
        bytes32 id = keccak256(payload);
        audits[id] = string(payload);
        emit AuditAppended(id, string(payload));
        return id;
    }

    function getAudit(bytes32 id) public view returns (string memory) {
        return audits[id];
    }
}
