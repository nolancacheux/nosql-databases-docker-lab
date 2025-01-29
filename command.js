// collection is a group of documents , the equivalent of a table in a relational database
// document is a set of key-value pairs, the equivalent of a row in a relational database
// field is a key-value pair in a document, the equivalent of a column in a relational database

// to return all the documents in a collection, we use the find() method


/// séance 1
db.restaurant.find({"borough":"Brooklyn"}).count()

db.restaurant.find({"borough":'Brooklyn',"cuisine":'Italian'})

db.restaurant.find({"borough":"Brooklyn","cuisine":"Italian","address.street": "5 Avenue" })

db.restaurant.find({"borough":"Brooklyn","cuisine" : "Italian","address.street": "5 Avenue",name :/p/i })

db.restaurant.find({"borough":"Brooklyn","cuisine" : "Italian","address.street": "5 Avenue",name :/e^/i })

db.restaurant.find({"borough":"Brooklyn","cuisine" : "Italian","address.street": "5 Avenue",name :/pizza/i },{_id:0,name:1,"grades.score" : 1})

db.restaurant.find({"borough":"Manhattan","grades.score" : {$lt: 10}},{_id:0,name:1,"grades.score" : 1})-

db.restaurant.find({"grades":{$elemMatch : {"grade": "C" , "score" : {$lt:40}}}},{"grades.grade" :1,"grades.score":1}) 

db.restaurant.find({"grades.0.grade": "C"},{"grades.grade" :1})

db.restaurant.distinct("grades.grade")

db.restaurant.distinct("borough")

//// séance 2 

db.restaurant.aggregate([{$match:{"grades.0.grade":"C"}},{$project:{"name":1,"borough":1,"_id":0}}])

//we use aggregate to use multiple operations in one query

const varMatch = {$match :{"grades.0.grade":"C"}};
const Varproject = {$project:{"name":1,"borough":1,"_id":0}};
const VarSort = {$sort:{"name":1}};

db.restaurant.aggregate([varMatch,Varproject,VarSort])

const varGroup = { $group : {"_id" : null, "total" : {$sum : 1} } }; 
db.restaurant.aggregate( [ varMatch, varGroup ] );
// equivalent à : 
db.restaurant.count({"grades.0.grade":"C"}) 
db.restaurant.find({"grades.0.grade":"C"}).count()



const varGroup2 = { $group : {"_id" : "borough", "total" : {$sum : 1} } }; 
db.restaurant.aggregate( [ varMatch, varGroup2 ] );

const varGroup3 = { $group : {"_id" : "$borough", "total" : {$sum : 1} } }; 
db.restaurant.aggregate( [ varMatch, varGroup3 ] );


varUnwind = {$unwind : "$grades"} // on décompose le tableau grades
varGroup4 = { $group : {"_id" : "$borough", "moyenne" : {$avg : "$grades.score"} } }; 
varSort2 = { $sort : { "moyenne" : -1 } } // -1 pour trier par ordre décroissant 
db.restaurant.aggregate( [ varUnwind, varGroup4, varSort2 ] );

db.restaurant.updateOne({"_id": ObjectId("6790bd8c88e23996bb1415b1")}, {$set: {"comment": "My new comment"}});
db.restaurant.find({"_id": ObjectId("6790bd8c88e23996bb1415b1")});

db.restaurant.update(
    {"grades.grade" : {$not : {$eq : "C"}}}, 
    {$set : {"comment" : "acceptable"}},
    {multi: true}
);
    
db.restaurant.find({"grades.grade" : {$not : {$eq : "C"}}});

db.restaurant.find( {"grades.grade" : {$not : {$eq : "C"}}} ).forEach( 
    function(restaurant){
        total = 0;
        for(i=0 ; i<restaurant.grades.length ; i++){
            if(restaurant.grades[i].grade == "A")         total += 3;
            else if(restaurant.grades[i].grade == "B")    total += 1;
            else                                          total -= 1;
        }
        restaurant.note = total;
        db.restaurant.updateOne({_id: restaurant._id}, {$set: restaurant});
    }
);

db.restaurants.remove( 
    {"note":0}, 
    {"multi" : true} 
    );
    7

db.restaurant.find({ "grades.grade": { $not: { $eq: "C" } } }).forEach(function (restaurant) {
    let total = 0;

    for (let i = 0; i < restaurant.grades.length; i++) {
        if (restaurant.grades[i].grade == "A") {
            total += 3;
        } else if (restaurant.grades[i].grade == "B") {
            total += 1;
        } else {
            total -= 1;
        }
    }
    db.restaurant.updateMany({ _id: restaurant._id }, { $set: { mark: total } });
});