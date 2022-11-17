// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

/** 
 * @title Dummy Smart contract for IoTFeds Master Thesis
 * @dev Implements purchashing process along with voting process
 * @ Lydia Athanasiou
 */
contract smart_contract{

    // The address of the stored product
    address public productAddress;
    // The price of the product
    uint price;
    // The address of the stored comment
    address public commentAddress;
    // The available money of the consumer
    uint private balance;

    uint product_counter = 0; 

    // The mapping type that stores the mapping relationship between the address of product information and product ID 
    product_info_mapping[] public product;
    // The mapping type that stores the mapping relationship between product ID and address of seller’s account
    seller_mapping[] public sender;
    product_mapping[] public product;
    buyer_mapping[] public buyer;
    uint buyer_counter =0;

    //Prodduct entity, sellet entity and buyer entity
    struct Product 
    {
        uint product_id; 
        address productAddress;
        uint price;
    }

    struct Seller 
    {
        bytes32 name;   // short name (up to 32 bytes)
        uint balance;
    }

    struct Buyer 
    {
        bytes32 name;   // short name (up to 32 bytes)
        uint balance;
    }

    constructor()
    {
        sender = msg.sender;    
    }

    /** 
     * This method checks if a product is already uploaded to UI. If it is not it creates it.
     */
    function productUploading(address productAddress, uint256 price) public {
        
        product_counter = 0;
        //Verify whether the product information has been uploaded or not.
        if (product_info_mapping.contained(mapping(key=product_id, value=p))){
            return false;
        }
        
        //else Initialize the product instance and properties p = new p(address productAddress, uint256 price) and updates the status of smart contract
        p = new p();

        product_counter = product_counter + 1;
        product_info_mapping.append(mapping(key = productAddress, value = product_id));
        seller_mapping.append(mapping(key = product_id, value = msg.sender));
        product_mapping.append(mapping(key = product_id, value = p));

        //Publishes the event of success uploading of the product to UI
        // TODO
        
        return true;
    }


    /**
     * This function is desighed in order to excecute the procedure of purchage of a product.
     */
    function pruductPurchase(address product) public {

        //Verify whether the information of selected product has been uploaded on the system
        if ( !(product_info_mapping.contained(productAddress))){
              throw;
        }
        p = product_mapping[product_info_mapping[productAddress]];

        //Checks whether the buyer’s account has enough money
        if (msg.sender.balance < p.price) {
            throw;
        }
        
        p.buyer_counter = buyer_counter + 1;
        p.buyer_mapping.append(mapping(key = msg.sender, value = p.buyer_id));

        //Transfers the money from the buyer’s account to the seller’s account
        // msg.sender transfer p.price to p.seller

        //Publish the event of success transaction to UI --> trigger the event BuyProduct to UI
        // TODO

        return true;
        
    }

    /**
     * This function is designed in order to execute the procedure of product evaluation.
     */
    function productEvaluation(address product, address comment, uint score, 
                               bool isPositive, uint currentReputation) public {
       
        //Verify whether the product has been purchased
        if ( !(product_info_mapping.contained(productAddress))){
            throw;
        }
        
        p = product_mapping[product_info_mapping[productAddress]];
        // initialize temp variable comment_id is -1
        uint comment_id = -1;

        //Check whether the buyer has submitted the rating and comment
        if (seller_mapping[product_info_mapping[productAddress]] == msg.sender){
            p.seller_comment_id = p.seller_comment_id + 1;
            comment_id = p.seller_comment_id;
            p.buyer_counter = buyer_counter + 1;
            p.is_seller_comment[p.seller_id] = true;
            
            // update and append comment information in related mapping of product p
            // TODO
        }

        if ((p.seller_mapping)).contained(msg.sender){
            p.buyer_comment_id = p.buyer_comment_id + 1;
            comment_id = p.seller_comment_id;
            p.is_buyer_comment[p.buyer_id] = true;
            
            // update and append comment information in related mapping of product p
            // TODO
        }

        //Check whether the buyer and seller have submitted the ratings and comments
        if (is_buyer_comment[comment_id] == true and is_seller_comment[comment_id]== true){
            
            // update seller and buyer’s reputation including positive and negative rating
            return true;
            // trigger the event CommentEvent
            // TODO
        }else{
            return false;
        }
        
        // Broadcast the updated reputation scores to the blockchain
        return true;
    }
}
