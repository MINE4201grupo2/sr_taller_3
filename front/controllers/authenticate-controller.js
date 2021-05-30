// npm i cryptr
// npm install express-sessions

var Cryptr = require('cryptr');
cryptr = new Cryptr('myTotalySecretKey');

module.exports.authenticate=function(req,res){
    var email=req.body.email;
    var password=req.body.password;
    const connection = require('./../db');
 
   
    connection.query('SELECT * FROM users WHERE email = ?',[email], function (error, results, fields) {
      if (error) {
          res.json({
            status:false,
            message:'there are some error with query'
            })
      }else{
       
        if(results.length >0){
            decryptedString = cryptr.decrypt(results[0].password);
            if(password==decryptedString){
                req.session.loggedin = true;
                req.session.email = email;
                req.session.userid = results[0].id;
                res.redirect('/')
                
            }else{
                res.json({
                  status:false,
                  message:"Email and password does not match"
                 });
                 res.end();
            }
          
        }
        else{
          res.json({
              status:false,    
            message:"Email does not exits"
          });
          res.end();
        }
      }
    });
}
