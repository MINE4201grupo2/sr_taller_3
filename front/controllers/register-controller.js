var Cryptr = require('cryptr');
// cryptr = new Cryptr('myTotalySecretKey');
 
 
module.exports.register=function(req,res){
  var today = new Date();
  var encryptedString = cryptr.encrypt(req.body.password);

  let re = /^(.*?)\@/
  let userId= req.body.email
  userId = re.exec(userId)[1];
  var user={
      "user_id": userId,
      "email":req.body.email,
      "password":encryptedString,
      "created_at":today,
      "updated_at":today
  }
  const connection = require('./../db');
 
  connection.query('INSERT INTO users SET ?',user, function (error, results, fields) {
    if (error) {
      res.render('pages/users/signup_confirm',{
          status:false,
          message:'No se pudo insertar correctamente el usuario'
      })
    }else{
      res.render('pages/users/signup_confirm',{
          status:true,
          data:results,
          message:'Usuario registrado '
      })
    }
  });
}

