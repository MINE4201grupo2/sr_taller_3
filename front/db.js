// Defines de connection to de DB
var mysql      = require('mysql');
var connection = mysql.createPool({
  host     : 'localhost',
  user     : 'user_taller3',
  password : 'taller3.',
  database : 'taller3'
});

module.exports = connection; 