const redis = require('redis');
const async = require ('async');

// create a new redis client and connect to our local redis instance
const client = redis.createClient();

// if an error occurs, print it to the console
client.on('error', function (err) {
    console.log("Error " + err);
});

module.exports = {
    create: create,
    retrieve: retrieve,
    list: list
};

function create(req, res) {
    var key = req.body.key;
    var value = req.body.value;
    client.set(key, value, function (error, result) {
        if (result) {
            res.send({ "result": result });
        } else {
            res.send({ "result": "not OK" });
        }
    });
}

function retrieve(req, res) {
    var key = req.params.product;
    client.get(key, function (error, result) {
        if (result) {
            res.send(result);
        } else {
            res.send("not set");
        }
    });
}

function list(req, res) {
    var products = [];
    client.keys('*', function (err, keys) {
        if (err) return console.log(err);
        if (keys) {
            async.map(keys, function (key, cb) {
                client.get(key, function (error, value) {
                    if (error) return cb(error);
                    var products = {};
                    products['key'] = key;
                    products['value'] = value;
                    cb(null, products);
                });
            }, function (error, results) {
                if (error) return console.log(error);
                res.send(results);
            });
        }
    });
}