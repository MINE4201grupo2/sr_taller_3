
 
module.exports.postPreferences=function(req,res){
    var sql_artists = "INSERT INTO `preferences` (`user_id`,`movie_id`,`created_at`) VALUES  ? "
    //if (error) throw error
    var data = req.body;
    var today = new Date();
    var userId= ''
    const connection = require('../db');
 
    connection.query('SELECT id FROM users WHERE email = ?',[req.session.email], function (error, results, fields) {
        if(error) throw error
        userId = results[0].id;
        //console.log(userId)
        var inserts = [];
        if(!Array.isArray(data.artists)){
            inserts.push([userId,data.artists,today]);
        }else{
            data.artists.forEach(function (item) {
                //console.log(item);   
                inserts.push([userId,item,today]);
            });
        }
        //console.log(inserts)
        connection.query(sql_artists,[inserts], function (error, results, fields) {
            if (error) throw error

           // res.redirect('/runController');
           res.redirect('/');
        });
    });

}