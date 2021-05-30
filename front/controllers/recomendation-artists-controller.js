
module.exports.listRecomendations=function(req,res){
    if(req.session.loggedin){
        const connection = require('./../db');
 
        var data = req.body;
        // Query song name an popular songs
        connection.query('SELECT id FROM users WHERE email = ?',[req.session.email], function (error, results, fields) {
            if(error) throw error
            var userId = results[0].id;

            var sql_artists = `CALL getRecomendationArtists (?,?,?,?)`
            //console.log(inserts)
            connection.query(sql_artists,[userId,data.model,data.type_model,20], function (error, results, fields) {
                if (error) throw error
                //console.log(results[0])
                res.render('pages/recomendations/recomendation-artists',{title: 'getArtists',
                                                                userProfile: { email: req.session.email },
                                                                artists: results[0]})
            });
        });
    }else{res.redirect('/iniciar-sesion');}

}