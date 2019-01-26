var express = require('express');
var router = express.Router();
const Backend = require('../model/backend')
let backend=new Backend();
/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('urcosme', { title: 'Express' });
});
router.post('/getProducts',backend.getProduct);

module.exports = router;
