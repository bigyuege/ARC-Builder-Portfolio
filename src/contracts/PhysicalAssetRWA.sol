// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

/**
 * @title PhysicalAssetRWA
 * @dev Real World Asset Tokenization with integrated Quality Assurance (QA) auditing.
 * Built for the ARC Ecosystem Hackathon.
 */
contract PhysicalAssetRWA is ERC721URIStorage, AccessControl {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIdCounter;

    bytes32 public constant MANUFACTURER_ROLE = keccak256("MANUFACTURER_ROLE");
    bytes32 public constant AUDITOR_ROLE = keccak256("AUDITOR_ROLE");

    enum QAStatus { Pending, Approved, Rejected }

    struct AssetDetails {
        string physicalSerialNumber;
        uint256 manufacturingDate;
        QAStatus status;
        address auditor;
    }

    // Mapping from token ID to its physical asset details
    mapping(uint256 => AssetDetails) public assetRegistry;

    // Events for off-chain indexing (e.g., The Graph)
    event AssetMinted(uint256 indexed tokenId, string serialNumber, address indexed manufacturer);
    event QAStatusUpdated(uint256 indexed tokenId, QAStatus status, address indexed auditor);

    constructor() ERC721("ARC Physical RWA", "ARCRWA") {
        // Grant the contract deployer the default admin role
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
    }

    /**
     * @dev Mints a new RWA token representing a physical asset. Only Manufacturers can mint.
     * @param to The address receiving the RWA token.
     * @param serialNumber The unique hardware serial number.
     * @param tokenURI IPFS link to the asset's metadata and legal documentation.
     */
    function mintAsset(address to, string memory serialNumber, string memory tokenURI) 
        public 
        onlyRole(MANUFACTURER_ROLE) 
        returns (uint256) 
    {
        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();

        _mint(to, tokenId);
        _setTokenURI(tokenId, tokenURI);

        assetRegistry[tokenId] = AssetDetails({
            physicalSerialNumber: serialNumber,
            manufacturingDate: block.timestamp,
            status: QAStatus.Pending,
            auditor: address(0)
        });

        emit AssetMinted(tokenId, serialNumber, msg.sender);
        return tokenId;
    }

    /**
     * @dev Updates the QA status of the physical asset. Only certified Auditors can call this.
     * @param tokenId The ID of the RWA token.
     * @param newStatus The new Quality Assurance status.
     */
    function auditAsset(uint256 tokenId, QAStatus newStatus) 
        public 
        onlyRole(AUDITOR_ROLE) 
    {
        require(_ownerOf(tokenId) != address(0), "Asset does not exist");
        require(newStatus != QAStatus.Pending, "Cannot revert to pending");

        assetRegistry[tokenId].status = newStatus;
        assetRegistry[tokenId].auditor = msg.sender;

        emit QAStatusUpdated(tokenId, newStatus, msg.sender);
    }

    // Override required by Solidity for multiple inheritance
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721URIStorage, AccessControl)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}