const http = require('http');
const fs = require('fs');
const ratelimit = require('express-rate-limit')
const PORT = process.env.PORT || 5000;
const FILENAME = 'location.txt';

http.createServer(function (req, res) {
  if (req.url === '/') {
    // Handle GET request for home page
    fs.readFile(FILENAME, function (err, data) {
      if (err) {
        console.error(err);
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('Internal Server Error');
      } else {
        // Render HTML template with file contents in scroll box
        const content = data.toString().replace(/\n/g, '<br>');
        const html = `<html>
          <head>
            <title>Locations</title>
            <style>
              .container {
                margin: 0 auto;
                max-width: 600px;
              }
              .scroll-box {
                height: 300px;
                overflow-y: scroll;
              }
              h1 {
                color: #337ab7;
                text-align: center;
              }
              .logo {
                display: block;
                margin: 0 auto;
                width: 200px;
              }
            </style>
          </head>
          <body>
            <div class="container">
              <h1>Locations</h1>
              <img src="logo.png" alt="Logo" class="logo">
              <div class="scroll-box">${content}</div>
            </div>
          </body>
        </html>`;
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(html);
      }
    });
  } else if (req.method === 'POST' && req.url === '/add-message') {
    // Handle POST request to add message to file
    let body = '';
    req.on('data', function (chunk) {
      body += chunk;
    });
    req.on('end', function () {
      fs.writeFile(FILENAME, body + '\n', function (err) {
        if (err) {
          console.error(err);
          res.writeHead(500, { 'Content-Type': 'text/plain' });
          res.end('Internal Server Error');
        } else {
          res.writeHead(302, { 'Location': '/' });
          res.end();
        }
      });
    });
  } else {
    // Handle unknown request
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('Not Found');
  }
}).listen(PORT);

console.log(`Server running on port ${PORT}`);
