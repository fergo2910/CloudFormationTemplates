// require the dependencies we installed
var app = require('express')();
var responseTime = require('response-time')
var bodyParser = require('body-parser')
var axios = require('axios');
var consul = require('consul');
const product = require('./controller/product');

app.set('port', (process.env.PORT || 7000));
app.use(responseTime());
app.use(bodyParser.json());       // to support JSON-encoded bodies
app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
  extended: true
}));

app.post('/api/product', product.create);
app.get('/api/product/:product', product.retrieve);
app.get('/api/all', product.list);
app.get('/ping', function(req, res) {
  res.send("pong");
});

app.listen(app.get('port'), function(){
  console.log('Server listening on port: ', app.get('port'));
});


// create a new consul client and connect to the consul instance
var consul = new consul({
  host: 'consul',
  port: 8500,
});

// register service to the consul agent
let options = {
  "Name": 'service_api',
  "ID": 'service_api',
  "Tags": [ "primary", "v1" ],
  "Address": "node_api",
  "Port": 7000,
	"Check": {
		"id": "ping",
		"HTTP": "http://node_api:7000/ping",
		"Interval": "10s",
		"timeout": "5s"
   }
};

consul.agent.service.register(options, function(err) {
  if (err) throw err;
});