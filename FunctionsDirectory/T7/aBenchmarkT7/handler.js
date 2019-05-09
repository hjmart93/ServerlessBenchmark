'use strict';

/* eslint-disable no-param-reassign */

module.exports.aFunctionT7 = function (context) {
   let n = context.req.query.n || 35;
   var stringv = 0;
   
    stringv = fib(n);

  context.res = {
    // status: 200, /* Defaults to 200 */
    body: stringv,
  };

  context.done();
};

function fib(n){
  if(n < 2) return n;
  
  return fib(n - 1) + fib(n - 2);
}