// load the things we need
var express = require('express');
var app = express();
const bodyParser  = require('body-parser');

// required module to make calls to a REST API
const axios = require('axios');

app.use(bodyParser.urlencoded());

// set the view engine to ejs
app.set('view engine', 'ejs');

// use res.render to load up an ejs view file

// index page 
app.get('/', function(req, res) {
     res.render("pages/index.ejs", {});

});

  app.post('/process_login', function(req, res){
    var user = req.body.username;
    var password = req.body.password;

    if(user === 'admin' && password === 'password') // '===': triple equal checks if the object type is the same between to objects; ex: 1 vs '1'
    {
        res.render('pages/welcome.ejs', {
            user: user,
            auth: true
        });
    }
    else
    {
        res.render('pages/welcome.ejs', {
            user: 'UNAUTHORIZED',
            auth: false
        });
    }
  })

  app.post('/')


app.listen(8085);
console.log('8085 is the magic port');
