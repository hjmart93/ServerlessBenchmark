'use strict';

function owFunctionT7(params) {
   let n = params.n || 35;
   var stringv = "";
   
    stringv = fib(n);

  return { payload: '' + stringv};
}

exports.owFunctionT7 = owFunctionT7;

function fib(n){
  if(n < 2) return n;
  
  return fib(n - 1) + fib(n - 2);
}