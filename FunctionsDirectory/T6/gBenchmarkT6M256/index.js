'use strict';

exports.gFunctionT6M256 = (request, response) => {
 response.status(200).send('Hello World!');
};

exports.event = (event, callback) => {
  callback();
};

