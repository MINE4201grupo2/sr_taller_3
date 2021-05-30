
 
module.exports.listTracks= function(req,res){
  if(req.session.loggedin){
    const connection = require('./../db');
 
    connection.query('SELECT * FROM tracks limit 50', function (error, results, fields) {
      if (error) {
	  		res.status(500).json({"status_code": 500,"status_message": "internal server error"});
	  	} else {
        res.render('pages/recomendations/preferences-tracks',{title: 'getTracks',
                            userProfile: { email: req.session.email },
                            artists: results}
                  );
      }

    });
  }else{res.redirect('/iniciar-sesion');}
}
