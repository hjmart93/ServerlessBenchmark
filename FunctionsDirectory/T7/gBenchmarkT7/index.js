'use strict';

exports.gFunctionT7 = (request, response) => {
	let n = request.query.n || 35;
	var stringv = 0;
   
    stringv = fib(n);

  response.status(200).send('' + stringv);
};

exports.event = (event, callback) => {
  callback();
};

function fib(n){
  if(n < 2) return n;
  
  return fib(n - 1) + fib(n - 2);
}
