var querystring = require('querystring');
var http = require('http');
exports.handler =  (event, context, callback) => {
    console.log(event)
    console.log(event.rawQueryString)
    var queryresult = querystring.parse(event.rawQueryString)
    var postdata = 'name='+queryresult['name']
    console.log(queryresult['name'])
    // An object of options to indicate where to post to
    var post_options = {
        host: '3.34.96.125', //netune query server address
        port: '80',
        path: '/gender',
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': Buffer.byteLength(postdata)
        }
    };


    // Set up the request
    var post_req = http.request(post_options, function(res) {
        res.setEncoding('utf8');
        res.on('data', function (chunk) {
            console.log('Response: ' + chunk);
            // message = chunk;
            callback(null, chunk)
            context.succeed();
        });
        res.on('error', function (e) {
          console.log("Got error: " + e.message);
          // message = e.message;
           context.done(null, 'FAILURE');
          callback(null, 'FAILURE')
        });
    });

    // post the data
    post_req.write(postdata);
    post_req.end();

}
