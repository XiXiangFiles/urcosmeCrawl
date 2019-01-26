var mysql= require('mysql');
var db = mysql.createConnection({
		 host     : '127.0.0.1',
		 user     : 'pi',
		 password : 'nccutest',
		 database:"kekeproject"
	});
class backend{
	getProduct(req, res, next){
		let searchReq=JSON.parse(req.body.data);
		console.log(searchReq)
			
		let sqlFoundation=`SELECT * FROM products WHERE s_index in (SELECT s_index FROM serial WHERE c_index in (SELECT c_index FROM category WHERE c_id =${searchReq.foundation.id})) and price BETWEEN  ${searchReq.foundation.range[0]} and ${searchReq.foundation.range[1]} ORDER BY products.grade DESC`;
		let sqlEyebrow=`SELECT * FROM products WHERE s_index in (SELECT s_index FROM serial WHERE c_index in (SELECT c_index FROM category WHERE c_id =${searchReq.eyebrow.id})) and price BETWEEN  ${searchReq.eyebrow.range[0]} and ${searchReq.eyebrow.range[1]} ORDER BY products.grade DESC`;
		let sqlEyeliner=`SELECT * FROM products WHERE s_index in (SELECT s_index FROM serial WHERE c_index in (SELECT c_index FROM category WHERE c_id =${searchReq.eyeliner.id})) and price BETWEEN  ${searchReq.eyeliner.range[0]} and ${searchReq.eyeliner.range[1]} ORDER BY products.grade DESC`;
		let sqlLipGloss=`SELECT * FROM products WHERE s_index in (SELECT s_index FROM serial WHERE c_index in (SELECT c_index FROM category WHERE c_id =${searchReq.lipGloss.id})) and price BETWEEN  ${searchReq.lipGloss.range[0]} and ${searchReq.lipGloss.range[1]} ORDER BY products.grade DESC`;
		let sqlFullcolor=`SELECT * FROM products WHERE s_index in (SELECT s_index FROM serial WHERE c_index in (SELECT c_index FROM category WHERE c_id =${searchReq.fullcolor.id})) and price BETWEEN  ${searchReq.fullcolor.range[0]} and ${searchReq.fullcolor.range[1]} ORDER BY products.grade DESC`;

		console.log(sqlFullcolor);
		
		let promise=new Promise(function(resolve){	
			db.query(sqlFoundation,function (err, results, fields){	
				let obj={};
				if(err){
					obj.status="false";
					resolve(obj);
				}else{
					obj.status="true";
					let foundation=[];
					for (let i=0;i<20;i++)
						foundation.push(results[i]);
					obj.foundation=foundation;
					resolve(obj);
				}
			});
		});
		promise.then(function(full){
			let promise=new Promise(function(resolve){
				db.query(sqlEyebrow,function (err, results, fields){	
					let obj={};
					obj.foundation=full.foundation;
					if(err){
						obj.status="false";
						resolve(obj);
					}else{
						obj.status="true";
						let eyebrow=[];
						for (let i=0;i<20;i++)
							eyebrow.push(results[i]);
						obj.eyebrow=eyebrow;
						resolve(obj);
					}
				});
			});
			promise.then(function(full){
				let promise=new Promise(function(resolve){
					db.query(sqlEyeliner,function (err, results, fields){	
						let obj={};
						obj.foundation=full.foundation;
						obj.eyebrow=full.eyebrow;
						if(err){
							obj.status="false";
							resolve(obj);
						}else{
							obj.status="true";
							let eyeliner=[];
							for (let i=0;i<20;i++)
								eyeliner.push(results[i]);
							obj.eyeliner=eyeliner;
							resolve(obj);
						}
					});
				});
				promise.then(function(full){
					let promise=new Promise(function(resolve){
						db.query(sqlLipGloss,function (err, results, fields){	
							let obj={};
							obj.foundation=full.foundation;
							obj.eyebrow=full.eyebrow;
							obj.eyeliner=full.eyeliner;
							if(err){
								obj.status="false";
								resolve(obj);
							}else{
								obj.status="true";
								let lipGloss=[];
								for (let i=0;i<20;i++)
									lipGloss.push(results[i]);
								obj.lipGloss=lipGloss;
								resolve(obj);
							}
						});
					});
					promise.then(function(full){
						let promise=new Promise(function(resolve){
							db.query(sqlFullcolor,function (err, results, fields){	
								let obj={};
								obj.foundation=full.foundation;
								obj.eyebrow=full.eyebrow;
								obj.eyeliner=full.eyeliner;
								obj.lipGloss=full.lipGloss;
								if(err){
									obj.status="false";
									resolve(obj);
								}else{
									obj.status="true";
									let fullcolor=[];
									for (let i=0;i<20;i++)
										fullcolor.push(results[i]);
									obj.fullcolor=fullcolor;
									resolve(obj);
								}
							});
						});
						promise.then(function(full){	
							res.write(JSON.stringify(full));
							res.end();
						});
					});
				});
			});
		});
	}
}
module.exports = backend

