var mysql      = require('mysql');
var db = mysql.createConnection({
		  host     : '127.0.0.1',
		  user     : 'pi',
		  password : 'nccutest',
		  database:"kekeproject"
});
/*
db.query('SELECT * FROM `products` WHERE `grade` ="-.-"', function (error, res, fields){
	for(let i=0;i<res.length;i++){
		let adjust=new Promise(function(resolve){	
			let obj={};	
			obj.p_id=res[i].p_id;
			obj.price=res[i].grade;
			if(obj.price=="-.-"){
				obj.price="";
			}
			resolve(obj);
		});
		adjust.then(function(full){
			
			let update=`UPDATE products SET grade = '${full.price}' WHERE p_id =${full.p_id}`;
			console.log(update);
			db.query(update, function (error, res, fields){
				console.log(update);
			});
			
		});
	}
});
*/

db.query('SELECT p_id,s_index,name,grade,articalLink,marketDate,price,is_limit,is_discount,is_withdraw,info FROM products WHERE price LIKE "%/%" ORDER BY products.p_id ASC',function(err,res,field){
	for(let i=0;i<res.length;i++){
		let price=res[i].price.split('/');
		price[0]=price[0].trim();
		price[1]=price[1].trim();
		if(price[1].length==3){
			price[1]+="0";
		}
		let insert=`INSERT INTO products(s_index, name, grade, articalLink, marketDate, price, is_limit, is_discount, is_withdraw, info) VALUES ( '${res[i].s_index}', '${res[i].name}', '${res[i].grade}', '${res[i].articalLink}', '${res[i].marketDate}', '${price[0]}', ${res[i].is_limit}, ${res[i].is_discount}, ${res[i].is_withdraw}, '${res[i].info}')`;
		let insert2=`INSERT INTO products(s_index, name, grade, articalLink, marketDate, price, is_limit, is_discount, is_withdraw, info) VALUES ( '${res[i].s_index}', '${res[i].name}', '${res[i].grade}', '${res[i].articalLink}', '${res[i].marketDate}', '${price[1]}', ${res[i].is_limit}, ${res[i].is_discount}, ${res[i].is_withdraw}, '${res[i].info}')`;
		let del=`DELETE FROM products WHERE p_id  = ${res[i].p_id}`
		db.query(`${insert}`,function(err){
		//	if(!err){
			
				console.log(insert)
		//	}
		})
		db.query(`${insert2}`,function(err){
		//	if(!err){
			
				console.log(insert2)
		//	}
		})
		db.query(`${del}`,function(err){
		//	if(!err){
			
				console.log(del)
		//	}
		})	
	}
})
/*
db.query('SELECT * FROM `products` WHERE `price` =""', function (error, res, fields){
	for(let i=0;i<res.length;i++){
		let adjust=new Promise(function(resolve){	
			let obj={};	
			obj.p_id=res[i].p_id;
			obj.price=res[i].grade;
			if(obj.price=="-.-"){
				obj.price="";
			}
			resolve(obj);
		});
		adjust.then(function(full){
			
			let update=`UPDATE products SET price = '0' WHERE p_id =${full.p_id}`;
			console.log(update);
			db.query(update, function (error, res, fields){
				console.log(update);
			});
			
		});
	}
});
*/
/*
db.query('SELECT * FROM category WHERE 1', function (error, res, fields){
	for(let i=0;i<res.length;i++){
		let adjust=new Promise(function(resolve){	
			let obj={};	
			let className=res[i].className;
			obj.c_index=res[i].c_index;
			obj.className=className.replace(/[—,・,》,《]/gi,"");
			obj.className=obj.className.trim();
			resolve(obj);
		});
		adjust.then(function(full){
			let update=`UPDATE category SET className='${full.className}' WHERE c_index=${full.c_index}`;
			db.query(update, function (error, res, fields){
				console.log(update);
			});
			
		});
	}
});
*/
/*
db.query('SELECT b_id FROM brand WHERE 1', function (error, res, fields) {
		  if (error) throw error;
		  for (let i=0;i<res.length;i++){
			  	 	 let categorySql=`SELECT * FROM category ,brand WHERE category.b_id=brand.b_id and brand.b_id=${res[i].b_id} and category.c_id != 1 GROUP by category.className`;
			  		  console.log(categorySql);
			  	  }
});
*/
