# NOSQL Databases : Docker and MongoDB Setup Guide

This file contains a series of Docker and MongoDB commands to set up and interact with a MongoDB database.

## 1st COURSE
## Steps:

1. **Start Docker Compose:**
    - `docker compose up`
    - This command starts the Docker containers defined in the Docker Compose file.

## Docker Compose Configuration

```yaml
services:
    mongo:
        image: mongo
        ports:
            - 27017:27017
        volumes:
            - ./data:/data/db

    mongo-express:
        image: mongo-express
        ports:
            - 8081:8081
        environment:
            ME_CONFIG_MONGODB_URL: mongodb://mongo:27017/
            ME_CONFIG_BASICAUTH: false
```

2. **Connect to MongoDB using `mongosh`:**
    - `mongosh`
    - This command connects to the MongoDB instance using the MongoDB Shell.

3. **Import data into MongoDB:**
    - `mongoimport --db Exercice --collection restaurant --file "C:\Users\nolan\Desktop\non_relationnal_database_docker_mongodb\restaurants.json"`
    - This command imports data from the specified JSON file into the 'restaurant' collection of the 'Exercice' database.

4. **Show all databases:**
    - `show dbs`
    - This command lists all databases in the MongoDB instance.

5. **Switch to the 'Exercice' database:**
    - `use Exercice`
    - This command switches the context to the 'Exercice' database.

6. **Find one document in the 'restaurant' collection:**
    - `db.restaurant.findOne()`
    - This command retrieves one document from the 'restaurant' collection.

7. **Find documents in the 'restaurant' collection where the 'borough' is 'Brooklyn':**
    - `db.restaurant.find({"borough":"Brooklyn"})`
    - This command retrieves all documents from the 'restaurant' collection where the 'borough' field is 'Brooklyn'.

8. **Count documents in the 'restaurant' collection where the 'borough' is 'Brooklyn':**
    - `db.restaurant.find({"borough":"Brooklyn"}).count()`
    - This command counts the number of documents in the 'restaurant' collection where the 'borough' field is 'Brooklyn'.

9. **Find documents in the 'restaurant' collection where the 'borough' is 'Brooklyn' and the 'cuisine' is 'Italian':**
    - `db.restaurant.find({"borough":"Brooklyn","cuisine":"Italian"})`
    - This command retrieves all documents from the 'restaurant' collection where the 'borough' field is 'Brooklyn' and the 'cuisine' field is 'Italian'.

10. **Find documents in the 'restaurant' collection where the 'borough' is 'Brooklyn', the 'cuisine' is 'Italian', and the 'address.street' is '5 Avenue':**
    - `db.restaurant.find({"borough":"Brooklyn","cuisine":"Italian","address.street":"5 Avenue"})`
    - This command retrieves all documents from the 'restaurant' collection where the 'borough' field is 'Brooklyn', the 'cuisine' field is 'Italian', and the 'address.street' field is '5 Avenue'.

11. **Find documents in the 'restaurant' collection where the 'borough' is 'Brooklyn', the 'cuisine' is 'Italian', the 'address.street' is '5 Avenue', and the 'name' contains the letter 'p':**
    - `db.restaurant.find({"borough":"Brooklyn","cuisine":"Italian","address.street":"5 Avenue",name:/p/i})`
    - This command retrieves all documents from the 'restaurant' collection where the 'borough' field is 'Brooklyn', the 'cuisine' field is 'Italian', the 'address.street' field is '5 Avenue', and the 'name' field contains the letter 'p'.

12. **Find documents in the 'restaurant' collection where the 'borough' is 'Brooklyn', the 'cuisine' is 'Italian', the 'address.street' is '5 Avenue', and the 'name' starts with the letter 'e':**
    - `db.restaurant.find({"borough":"Brooklyn","cuisine":"Italian","address.street":"5 Avenue",name:/e^/i})`
    - This command retrieves all documents from the 'restaurant' collection where the 'borough' field is 'Brooklyn', the 'cuisine' field is 'Italian', the 'address.street' field is '5 Avenue', and the 'name' field starts with the letter 'e'.

13. **Find documents in the 'restaurant' collection where the 'borough' is 'Brooklyn', the 'cuisine' is 'Italian', the 'address.street' is '5 Avenue', and the 'name' contains the word 'pizza', excluding the '_id' field and including only the 'name' and 'grades.score' fields:**
    - `db.restaurant.find({"borough":"Brooklyn","cuisine":"Italian","address.street":"5 Avenue",name:/pizza/i},{_id:0,name:1,"grades.score":1})`
    - This command retrieves all documents from the 'restaurant' collection where the 'borough' field is 'Brooklyn', the 'cuisine' field is 'Italian', the 'address.street' field is '5 Avenue', and the 'name' field contains the word 'pizza', excluding the '_id' field and including only the 'name' and 'grades.score' fields.

14. **Find documents in the 'restaurant' collection where the 'borough' is 'Manhattan' and the 'grades.score' is less than 10, excluding the '_id' field and including only the 'name' and 'grades.score' fields:**
    - `db.restaurant.find({"borough":"Manhattan","grades.score":{$lt:10}},{_id:0,name:1,"grades.score":1})`
    - This command retrieves all documents from the 'restaurant' collection where the 'borough' field is 'Manhattan' and the 'grades.score' field is less than 10, excluding the '_id' field and including only the 'name' and 'grades.score' fields.

15. **Find documents in the 'restaurant' collection where the 'borough' is 'Manhattan' and the 'grades.score' is less than 10 and not greater than or equal to 10, excluding the '_id' field and including only the 'name' and 'grades.score' fields:**
    - `db.restaurant.find({"borough":"Manhattan","grades.score":{$lt:10,$not:{$gte:10}}},{_id:0,name:1,"grades.score":1})`
    - This command retrieves all documents from the 'restaurant' collection where the 'borough' field is 'Manhattan' and the 'grades.score' field is less than 10 and not greater than or equal to 10, excluding the '_id' field and including only the 'name' and 'grades.score' fields.

16. **Find documents in the 'restaurant' collection where any grade is 'C' and the score is less than 40:**
    - `db.restaurant.find({"grades":{$elemMatch : {"grade": "C" , "score" : {$lt:40}}}},{"grades.grade" :1,"grades.score":1})`
    - This command retrieves all documents from the 'restaurant' collection where any grade is 'C' and the score is less than 40, including only the 'grades.grade' and 'grades.score' fields.

17. **Find documents in the 'restaurant' collection where the first grade is 'C':**
    - `db.restaurant.find({"grades.0.grade": "C"},{"grades.grade" :1})`
    - This command retrieves all documents from the 'restaurant' collection where the first grade is 'C', including only the 'grades.grade' field.

18. **Get distinct grades from the 'restaurant' collection:**
    - `db.restaurant.distinct("grades.grade")`
    - This command retrieves all distinct grades from the 'restaurant' collection.

19. **Get distinct boroughs from the 'restaurant' collection:**
    - `db.restaurant.distinct("borough")`
    - This command retrieves all distinct boroughs from the 'restaurant' collection.

## 2nd COURSE

20. **Aggregate documents where the first grade is 'C' and project specific fields:**
    - `db.restaurant.aggregate([{$match:{"grades.0.grade":"C"}},{$project:{"name":1,"borough":1,"_id":0}}])`
    - This command uses aggregation to match documents where the first grade is 'C' and projects the 'name' and 'borough' fields.

21. **Aggregate with multiple operations:**
    - ```javascript
      const varMatch = {$match :{"grades.0.grade":"C"}};
      const varProject = {$project:{"name":1,"borough":1,"_id":0}};
      const varGroup = { $group : {"_id" : null, "total" : {$sum : 1} } }; 
      db.restaurant.aggregate( [ varMatch, varGroup ] );
      // equivalent to: 
      db.restaurant.count({"grades.0.grade":"C"}) 
      db.restaurant.find({"grades.0.grade":"C"}).count()

      const varGroup2 = { $group : {"_id" : "borough", "total" : {$sum : 1} } }; 
      db.restaurant.aggregate( [ varMatch, varGroup2 ] );

      const varGroup3 = { $group : {"_id" : "$borough", "total" : {$sum : 1} } }; 
      db.restaurant.aggregate( [ varMatch, varGroup3 ] );

      const varUnwind = {$unwind : "$grades"}; // decompose the grades array
      const varGroup4 = { $group : {"_id" : "$borough", "average" : {$avg : "$grades.score"} } }; 
      const varSort2 = { $sort : { "average" : -1 } }; // -1 for descending order
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
              let total = 0;
              for(let i = 0; i < restaurant.grades.length; i++){
                  if(restaurant.grades[i].grade == "A") total += 3;
                  else if(restaurant.grades[i].grade == "B") total += 1;
                  else total -= 1;
              }
              restaurant.note = total;
              db.restaurant.updateOne({_id: restaurant._id}, {$set: restaurant});
          }
      );

      db.restaurant.remove( 
          {"note":0}, 
          {"multi" : true} 
      );

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
      ```
