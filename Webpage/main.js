var express = require('express'); 
var app = express(); 
var assert = require('assert'); 
var mongodb = require('mongodb'); 
var bodyParser = require('body-parser'); 

app.use(bodyParser.json()); 
app.use(bodyParser.urlencoded({
	extended: true
})); 

var MongoClient = mongodb.MongoClient; 
var db_name = 'aqua'; 
var url = "mongodb://Sahil:Sahil_742995@ds139844.mlab.com:39844/aqua";  

app.get('/getData', function(req, res){
	MongoClient.connect(url, {useNewUrlParser: true },function(err, client) {

		var db = client.db("aqua");

		db.collection('posts').find().limit(1).sort({$natural:-1}).toArray(function(err, result){
			if(err){
				console.log(err);
			} else if (result.length){
				console.log('Found: ', result); 
				res.status(200).send(JSON.stringify(result)); 
			} else {
				console.log('No Document(s) found with defined "find" criteria!'); 
			}
			client.close(); 
		}); 
	}); 
}); 

var server = app.listen(process.env.PORT, function(){
	var port = server.address().port; 
	console.log("Node app listening at http://127.0.0.1:%s",port); 
}); 