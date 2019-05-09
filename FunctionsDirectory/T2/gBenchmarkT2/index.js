'use strict';

exports.gFunctionT2 = (request, response) => {
  response.status(200).send('Hello World!');
};

exports.event = (event, callback) => {
  callback();
};
