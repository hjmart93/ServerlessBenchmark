'use strict';

exports.gFunctionT1 = (request, response) => {
  response.status(200).send('Hello World!');
};

exports.event = (event, callback) => {
  callback();
};
