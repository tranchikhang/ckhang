---
title: "JavaScript: Promise or async-await? Async without await, Await without async?"
date: 2021-01-17
summary: "Summary of JavaScript asynchronous programming"
keywords: "JavaScript, Software engineering, Promise, Await, Async, callback, Asynchronous programming"
tags: [JavaScript, Software engineering, Promise, Await, Async, callback, Asynchronous programming]
draft: true
---

The reason for this post is because I had some problems with wrapping my head around JavaScript asynchronous programming. I spent 4 hours scratching my head while fixing a bug in [my game](https://github.com/tranchikhang/MedievalWar). Even though I had some basic experience with asynchronous programming when I worked with .Net, but many concepts in JS still got me confused (I'm not blaming the language tho, considering that I didn't actually study JavaScript "the right way").

It would have been faster if I had a basic grasp of JS asynchronous, that's why I decided to summarize what I (may) have understood in this post.

### JavaScript Basis

First, JavaScript is synchronous, blocking, single-threaded.

Which means if you're executing a JS block of code on a page, then no other JavaScript on that page will be executed, only one operation can be processed at a time.

But what if we want to execute a function *after* another function has finished executing? That's where we have callback.

### Callback

A [callback](https://developer.mozilla.org/en-US/docs/Glossary/Callback_function) function is a function passed into another function as an argument, which is then invoked inside the outer function to complete some kind of routine or action.

*Callback can be synchronous or asynchronous*

#### Synchronous callback:
Example #1:
```JS
let arr = ['a', 'b', 'c'];

arr.forEach(function(item, index, array) {
    console.log(item, index)
});
```
```cmd
"a", 0
"b", 1
"c", 2
```
Here `foreach` function takes a callback and execute it synchronously, as [foreach](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach) does not wait for promises.

Example #2:
```JS
function functionOne(value, callback) {
    var y = value + 5;
    callback(y);
    console.log('After callback');
}

function functionTop() {
    var x = 5;
    console.log('x=' + x);
    functionOne(x, function(functionOneReturnedValue) {
        console.log('functionOne is executed, x=' + functionOneReturnedValue);

        // some useless job to cause waiting
        var a;
        for(var i = 0; i < 1000000000; i++){
            a += i;
        }

        console.log('Done with callback');
    });
    console.log('After functionTop');
}

functionTop();

```
```cmd
x=5
functionOne is executed, x=10
Done with callback
After callback
After functionTop
```
Notice the order: 'Done with callback' => 'After callback' => 'After functionTop', showing that the callback call is synchronous, all functions execute in the order they are called.

#### Asynchronous callback
Example #3:
```JS
var x = false;

function myFunction(callbackFn) {
    setTimeout( function() {
        console.log('inside setTimeout')
        callbackFn();
    }, 0 );
}

myFunction( function() {
    console.log('Start callback');
    x = true;
    console.log('End callback');
});
console.log('Final x=' + x)
```
```cmd
Final x=false
inside setTimeout
Start callback
End callback
```
I used `setTimeout` to make `myFunction` run asynchronously, then pass a callback function into it.
`x` still remains `false`, this is because any function given to the `setTimeout` function will be executed asynchronously, when the main thread is not busy.

Another example #4:
```JS
const array = [1, 2, 3, 4, 5];

array.forEach((el, i) => {
    setTimeout(() => {
        console.log('setTimeout:' + el);
    }, 2000);
    console.log(el);
});
```
```cmd
1
2
3
4
5
setTimeout:1
setTimeout:2
setTimeout:3
setTimeout:4
setTimeout:5
```
As I mentioned above, `foreach` function takes a callback and executes it synchronously. `setTimeout` returns a value immediately, then the next line begins to execute, but the asynchronous callback (`setTimeout`) will be executed later.

### Promise

Promise is a way to implement asynchronous programming in JavaScript. Promise was introduced in ES6 (ES2015).

MDN's definition: The [Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) object represents the eventual completion (or failure) of an asynchronous operation and its resulting value.

#### Differences between callback and promise
1. Callback is function, promise is object

Callback is a block of code which can be executed in response to events such as timer etc.

Promise is an object which stores information about whether the event has happened or not, if it has, what was the result.

2. Callback is passed as an argument, promise is returned

Callback is defined independently, is passed as an argument, and is stored in the function where it is called from.

Promise is created inside of asynchronous functions and then returned.

3. Callback can represent multiple events, promise represents one

Callback can be called multiple times by the function it is passed to.

Promise represents one event, a promise can only succeed or fail once.

![promises.png](https://media.prod.mdn.mozit.cloud/attachments/2018/04/18/15911/32e79f722e83940fdaea297acdb5df92/promises.png)

Example #1:
```JS
let p = new Promise((resolve, reject) => {
    // In this example, I will use setTimeout(...) to simulate asynchronous code
    setTimeout( function() {
        resolve('Success!')
    }, 250)
})

p.then((successMessage) => {
  // successMessage is whatever I passed in the resolve(...) function above
  console.log(successMessage)
});
```

Running `new Promise` will immediately call the function passed in as an argument (here it means `setTimeout` is called immediately).

Promise constructor takes one argument: a callback with two parameters, `resolve` and `reject`.

You can use the promise result when it becomes settled with 3 methods: `then`, `catch`, `finally`.

These methods also return a newly generated promise object, which can optionally be used for chaining.

Example #2:
```JS
let p = new Promise((resolve, reject) => {
  setTimeout( function() {
    reject('Error');
  }, 250)
})

p.then(function (msg) {
    console.log(msg);
}).catch(function (err) {
    console.warn(err);
});
```

### async - await

ES2017 (ES8) introduced the concept of `async` functions and `await` keywords, a higher level abstraction over promises.
They are just syntactic sugar on top of promises, making asynchronous code easier to write and to read.

First we have the `async` keyword:
* When you put `async` in front of a function declaration, it turns the function into an async function
* Async functions can contain zero or more await expressions
* Async functions always return a promise. If the return value of an async function is not explicitly a promise, it will be implicitly wrapped in a promise

Then, the `await` keyword:
* `await` only works inside async functions
* Causes async function execution to pause until a promise is settled
* If the Promise is rejected, the await expression throws the rejected value.
* To await a function, that function must return a promise

Example:
```JS
async function f() {
    let promise = new Promise((resolve, reject) => {
        setTimeout(() => resolve('done'), 1000)
    });

    let result = await promise; // wait until the promise resolves
    console.log(result);
}

f();
```
The function execution will “pause” at the line where we used `await`, and resume when the promise settled.

#### Await a function without async
Since `async` is still promise-based, we can `await` a function that returns a promise, even when that function is not an `async` function:
```JS
function f() {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve('done')
        }, 1000)
    });
}

async function f1() {
    let result = await f();
    console.log(result);
}
f1();
```
The below code has the same result:
```JS
async function f() {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve('done')
        }, 1000)
    });
}

async function f1() {
    let result = await f();
    console.log(result);
}
f1();
```

#### Async function without await inside
We can declare a function as `async` without using any `await`. In this case, the execution is not paused and your code will be executed in a non-blocking manner (asynchronous - no waiting). It is the same as not declaring that same function with `async`.

```JS
async function f() {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            console.log('Promise resolved')
            resolve('done')
        }, 1000)
    });
}

async function f1() {
    let result = f();
    console.log('f1 finished');
}
f1();
```
```cmd
f1 finished
Promise resolved
```
You can remove `async` keyword before `f1` and still get the same result.

With `await`:
```JS
async function f() {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            console.log('Promise resolved')
            resolve('done')
        }, 1000)
    });
}

async function f1() {
    let result = await f();
    console.log('f1 finished');
}
f1();
```
```cmd
Promise resolved
f1 finished
```

#### Calling async without await
Be careful when calling an `async` function without `await`:
```JS
let x =  0;
function resolveAfter2Seconds(x) {
    return new Promise(resolve => {
        setTimeout(() => {
            resolve(x);
        }, 2000);
    });
}

async function f1() {
    x = await resolveAfter2Seconds(10);
    console.log('x inside f1:' + x);
}

f1();
x = 3;
console.log('final x:' + x)
```
```cmd
final x:3
x inside f1:10
```
Since `f1` is asynchronous, when it is executed, the line `x = 3;` executes immediately without waiting.


References:

[MDN - Making asynchronous programming easier with async and await](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Async_await)

[MDN - async function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function)

[Introduction to ES6 Promises – The Four Functions You Need To Avoid Callback Hell](http://jamesknelson.com/grokking-es6-promises-the-four-functions-you-need-to-avoid-callback-hell/)

[Stack Overflow - Await doesn't wait](https://stackoverflow.com/questions/55960027/await-doesnt-wait)

[Stack Overflow - Async function without await in Javascript](https://stackoverflow.com/questions/45594596/async-function-without-await-in-javascript)

[Async functions - making promises friendly](https://developers.google.com/web/fundamentals/primers/async-functions)

[Stack Exchange - How does Javascript code become asynchronous when using callbacks?](https://softwareengineering.stackexchange.com/questions/194580/how-does-javascript-code-become-asynchronous-when-using-callbacks)