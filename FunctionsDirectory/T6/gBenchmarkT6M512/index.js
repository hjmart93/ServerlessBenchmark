'use strict';

exports.gFunctionT6M512 = (request, response) => {
	response.status(200).send('Hello World!');
};

exports.event = (event, callback) => {
  callback();
};
