<?php
error_reporting(1);

/**
 * Mongodb helper class
 */
class mongoHelper{
    /**
     * __construct
     *
     * @params:
     *    $mdb        string : name of the database to connect to
     *    $collection string : name of collection to use
     */
    function __construct($mdb=null,$collection=null){

        $this->mdb = $mdb;
        $this->collection = $collection;
        $this->dbdotcoll = $this->mdb.'.'.$this->collection;
        $this->manager = new MongoDB\Driver\Manager("mongodb://localhost:27017");
        $this->writeConcern = new MongoDB\Driver\WriteConcern(MongoDB\Driver\WriteConcern::MAJORITY, 1000);
        
    }
    
    /**
     * setMdb - Sets the database to work with
     *
     * @params:
     *    $mdb        string : name of the database to connect to
     *
     * @returns:
     *     null
     */
    function setMdb($mdb){
        $this->mdb = $mdb;
        $this->dbdotcoll = $this->mdb.'.'.$this->collection;
    }
    
    /**
     * setDbcoll - Sets the collection to work with
     *
     * @params:
     *    $mdb        string : name of the database to connect to
     *
     * @returns:
     *     null
     */
    function setDbcoll($collection){
        $this->collection = $collection;
        $this->dbdotcoll = $this->mdb.'.'.$this->collection;
    }
    
    /**
     * insert - Inserts 1 or more documents into mongodb
     *
     * @params:
     *    $documents array : associative array, or array of associative arrays, of documents
     * @returns:
     *     ids array : array of document id's that got inserted
     */
    function insert($documents){
        if(!$this->db_coll_set()){
            return ["error"=>"db or collection not set."];
        }
        $_ids = [];
        $bulk = new MongoDB\Driver\BulkWrite;
        if(!is_array($documents)){
            return array("error"=>"document not an array.");
        }

        foreach($documents as $doc){
            if(!$this->isAssoc($doc)){
                return array("error"=>"document not associative array.");
            }
            $_ids[] = $bulk->insert($doc);
        }
        
        $result = $this->manager->executeBulkWrite($this->dbdotcoll, $bulk, $this->writeConcern);
        
        return $_ids;
        
    }
    
    /**
     * update - Updates 1 document in mongodb
     *
     * @params:
     *    $filter array : associative array giving values to identify the document
     *    $set array    : associative array with key value pairs to "change" in existing doc
     *    $params array : associative array with ['multi' => false, 'upsert' => false]
     * @returns:
     *     ids array : array of document id's that got inserted
     */
    function update($filter,$set,$params=null){
        if(!$this->db_coll_set()){
            return ["error"=>"db or collection not set."];
        }
        $_ids = [];
        $bulk = new MongoDB\Driver\BulkWrite;
        
        if(!$params){
            $params = ['multi' => false, 'upsert' => false];
        }
        
        $bulk->update(
            $filter,
            ['$set' => $set],
            $params
        );
        $result = $this->manager->executeBulkWrite($this->dbdotcoll, $bulk, $this->writeConcern);
        
        return $result;
        
    }
    
    /**
     * query - query's the database
     *
     * @params:
     *    $filter     array : associative array of key value pairs to match for selection
     *                        (filter disqualifies documents from the result)
     *    $projection array : associative array of keys to remove or add to result 
     *                        (projection removes portions of the result)
     * @returns:
     *     results array : array of document that got selected
     * 
     * @example:
     *      $docs = $mymongo->query(["category"=>"Laptop"],["_id"=>0,"price"=>1]);
     *      // this finds all docs where category == laptop and only returns the prices
     */
    function query($filter=[],$projection=[]){
        if(!$this->db_coll_set()){
            return ["error"=>"db or collection not set."];
        }
        $results = [];
        
        $options = [
           'projection' => $projection,
        ];
        
        if(array_key_exists('_id',$filter) && strlen($filter['_id']) >= 24){
            $filter['_id'] = new MongoDB\BSON\ObjectID($filter['_id']);
        }
        
        $query = new MongoDB\Driver\Query($filter, $options);
        $cursor = $this->manager->executeQuery($this->dbdotcoll, $query);
        
        foreach ($cursor as $document) { 
            $results[] = $document;
        }
        return $results;
    }
    
    /**
     * delete - delete's items from the database
     *
     * @params:
     *    $documents    array : associative array of key value pairs to match for deletion
     *
     * @returns:
     *     ids          int : count of deleted items
     *
     * @example:
     *      $docs = $mymongo->query([['_id'=>9]]);
     *      // this finds doc where id == 9 and removes it.
     */
    function delete($documents=null){
        if(!$this->db_coll_set()){
            return ["error"=>"db or collection not set."];
        }
        $bulk = new MongoDB\Driver\BulkWrite;
        if($documents){
            foreach($documents as $doc){
                if(!$this->isAssoc($doc)){
                    return array("error"=>"DELETE failed, document not associative array.");
                }
                //If the '_id' is in array and its long (like a mongo id) 
                //then convert into a mongoid object
                if(array_key_exists('_id',$doc) && strlen($doc['_id']) >= 24){
                    $doc['_id'] = new MongoDB\BSON\ObjectID($doc['_id']);
                }
                
                //run the delete
                $bulk->delete($doc);
            }
        }else{
            $bulk->delete([]);
        }
        
        $result = $this->manager->executeBulkWrite($this->dbdotcoll, $bulk, $this->writeConcern);
        return $result->getDeletedCount();

    }
    
    private function isAssoc(array $arr){
        if (array() === $arr) return false;
        return array_keys($arr) !== range(0, count($arr) - 1);
    }
    
    private function db_coll_set(){
        return $this->mdb != null && $this->collection != null;
    }
    
}

class thelog{
    function __construct($filename='log.txt'){
        $this->filename = $filename;
    }
    function clear_log(){
        file_put_contents($this->filename,'');
    }
    function do_log($data){
        file_put_contents($this->filename,print_r($data,true),FILE_APPEND);
        file_put_contents($this->filename,"\n",FILE_APPEND);
    }
}



if($argv[1] == 'run_tests'){
    $products = [
        ["_id"=>1, "product_name"=>"Apple IPhone 6", "price"=>"$630", "category"=>"Mobile Phone" ],
        [ "_id"=>3, "product_name"=>"Samsung T.V", "price"=>"$900", "category"=>"Electronics"],
        [ "_id"=>4, "product_name"=>"Apple IPAD", "price"=>"$400", "category"=>"Tablet" ],
        [ "_id"=>5, "product_name"=>"MacBook Pro", "price"=>"$800", "category"=>"Laptop"],
        [ "_id"=>6, "product_name"=>"Dell Laptop", "price"=>"$620", "category"=>"Laptop"],
        ["_id"=>7, "product_name"=>"Canon EOS 700D DSLR Camera", "price"=>"$400", "category"=>"Camera"], 
        ["_id"=>8, "product_name"=>"Nikon D7100 DSLR Camera ", "price"=>"$440", "category"=>"Camera"],
        ["_id"=>9, "product_name"=>"HTC Phone", "price"=>"$200", "category"=>"Mobile Phone"],
        ["_id"=>10, "product_name"=>"LG Monitor", "price"=>"$500", "category"=>"Electronics"],
        [ "_id"=>11, "product_name"=>"Samsung Printer", "price"=>"$320", "category"=>"Electronics"],
        [ "_id"=>12, "product_name"=>"Samsung Gear Live Black - Made for Android", "price"=>"$250", "category"=>"Watch"],
        [ "_id"=>13, "product_name"=>"Apple Watch", "price"=>"$380", "category"=>"Watch"],
        [ "_id"=>14, "product_name"=>"lenovo Laptop", "price"=>"$420", "category"=>"Laptop"],
        [ "_id"=>15, "product_name"=>"joes Laptop", "price"=>"$920", "category"=>"Laptop"] 
        ];

    $mymongo = new mongoHelper('onlinestore','products'); // connect to db and collection
    $mymongo->delete();                         // delete all products from the collection
    
    $ids = $mymongo->insert($products);         // insert array of products
    
    $mymongo->delete([['_id'=>9]]);             // delete product with id == 9
    $mymongo->delete([['price' => '$420']]);    // delete product with price == '420'
    
    //query(filter_array,projection_array);
    //filter = key value pairs to match items in the db
    //project = key value pairs of what to return in the result array
    //This query finds all items with category == laptop and only return the price.
    //The _id is always in the result unless you explicitly exclude it like below.
    $docs = $mymongo->query(["category"=>"Laptop"],["_id"=>0,"price"=>1]);
    print_r($docs);
    
    //update($filter,$new_values)
    //This update finds the product with id==15 and updates its product name
    //    from joes laptop to bobs laptop
    $res = $mymongo->update(["_id"=>15],["product_name"=>"bobs Laptop"]);
    
    //This returns all items from db.collection
    $docs = $mymongo->query();
    print_r($docs);
}




