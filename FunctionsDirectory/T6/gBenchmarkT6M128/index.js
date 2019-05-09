'use strict';

exports.gFunctionT6M128 = (request, response) => {
  response.status(200).send('Hello World!');
};

exports.event = (event, callback) => {
  callback();
};

