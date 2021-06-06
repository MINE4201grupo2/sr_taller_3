module.exports = (app) => {

  var authenticateController=require('./../../controllers/authenticate-controller');
  var registerController=require('./../../controllers/register-controller');
  var moviesController=require('../../controllers/movies-controller');
  var preferencesController=require('../../controllers/preferences-controller');
  var recomendationsController=require('../../controllers/recomendation_controller');
  var runController=require('../../controllers/run');

  app.post('/controllers/register-controller/', registerController.register);
  app.post('/controllers/authenticate-controller/', authenticateController.authenticate);
  app.post('/controllers/preferences-controller/', preferencesController.postPreferences);

  /* GET pages/users listing. */
  app.get('/', (req, res) => {
    if(req.session.loggedin){
      res.render('pages/index', { title: 'RecomendationcesParaTi',userProfile: {loggedIn:true,  email: req.session.email } });
    }else{
        res.render('index');
    }    
  });
  app.get('/404', (req, res) => {
    res.render('pages/404', { title: 'Página no encontrada' });
  });
  app.get('/iniciar-sesion', (req, res) => {
    if(req.session.loggedin){
      res.redirect('/');
    }else{
      res.render('pages/users/login', { title: 'Iniciar Sesión', description: '' });
    }   
  });
  app.get('/registro', (req, res) => {
    res.render('pages/users/signup', { title: 'Registrarse', description: '' });
  });
  app.get('/registro-confirmacion', (req, res) => {
    res.render('pages/users/signup_confirm', { title: 'Registrarse' });
  });
  // User
  app.get('/cerrar-sesion', (req, res) => {
    req.session.loggedIn=false;
    req.session.destroy();
    res.render('pages/users/logout', { title: 'Cerrar Sesión' });
  });

  // publico
  app.get('/successful', (req, res) => {
    res.render('pages/successful', { title: 'Diseño enviado' });
  });
  app.get('/error', (req, res) => {
    res.render('pages/error', { title: 'Error al recibir el archivo' });
  });

  app.get("/user", (req, res) => {
    if(req.session.loggedin){
      res.render("pages/users/user", { title: "Profile", userProfile: { email: req.session.email } });
    }else{
        res.redirect('/iniciar-sesion');
    }   

  });

  app.get("/preference", moviesController.listMovies);
  
  app.post('/recomendation-movies', recomendationsController.listRecomendations);

  app.get("/runController", runController.runController);

  app.get("/model-select", (req, res) => {
    if(req.session.loggedin){
      res.render('pages/recomendations/model-select', {userProfile: { email: req.session.email }, 
                                                      models:['coseno'],
                                                      } );
    }else{
        res.redirect('/iniciar-sesion');
    }   
  });
  
};
