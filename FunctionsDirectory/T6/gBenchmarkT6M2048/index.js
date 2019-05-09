'use strict';

exports.gFunctionT6M2048 = (request, response) => {
  	response.status(200).send('Hello World!');
};

exports.event = (event, callback) => {
  callback();
};
