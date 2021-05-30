require('./constants');
global.config = require('./config');

var bodyParser=require('body-parser');
var express = require('express');
var session = require('express-session');
const createError = require('http-errors');
const path = require('path');


var app = express();

var authenticateController=require('./controllers/authenticate-controller');
var registerController=require('./controllers/register-controller');


app.use(express.static(path.join(__dirname, 'public')));
app.use(session({
	secret: 'secret',
	resave: true,
	saveUninitialized: true,
    cookie: { maxAge: 6000000 }
}));

app.use(bodyParser.urlencoded({extended:true}));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

// rutas
require('./routes')(app);

// modelos
global.models = require('./models');

// catch 404 and forward to error handler
app.use((req, res, next) => {
    next(createError(404));
  });


// error handler
// eslint-disable-next-line no-unused-vars
app.use((err, req, res, next) => {
    // set locals, only providing error in development
    res.locals.message = err.message;
    res.locals.error = req.app.get('env') === 'development' ? err : {};
  
    // render the error page
    res.status(err.status || 500);
    res.render('error');
  });

console.log(authenticateController);

//MIDDLEWARE
function isLoggedIn(req,res,next) {
if(req.isAuthenticated()){
    return next();
}
res.redirect("/iniciar-sesion");
}

//app.listen(8070);
module.exports = app;