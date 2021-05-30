// Defines de connection to de DB
var mysql      = require('mysql');
var connection = mysql.createPool({
  host     : 'localhost',
  user     : 'user_taller1',
  password : 'taller1.',
  database : 'taller1'
});

module.exports = connection; 