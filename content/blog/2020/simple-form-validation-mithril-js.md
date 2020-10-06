---
title: "Simple Form Validation in MithrilJs"
date: 2020-08-08
summary: "How to validate form input in MithrilJS"
draft: true
---
Last time, I covered the basics of Mithril by creating a simple login page. In this post I will continue with form validation in a simple way.
I couldn't find any good tutorial covering form validation, except a snippet from [how-to-mithril](https://how-to-mithril.js.org/). This is my only reference for now, and I don't have much experience with Mithril, so this tutorial maybe not the best practice.
This time we only need to modify `Login.js` file. If you want to improve reusability, you may want to create separated file for each component.

### Input components
I will create separated component for each input, first is user name.
```JavaScript
let UserNameInput = {
    error: '',
    value: '',
    validate: () => {
        UserNameInput.error = !UserNameInput.value ? 'Please enter user name' : '';
    },
    isValid: () => {
        return UserNameInput.error ? false : true;
    },
    view: () => {
        return [
            m('input', {
                className: UserNameInput.error ? 'error' : '',
                placeholder: 'User Name',
                value: UserNameInput.value,
                type: 'text',
                oninput: e => {
                    UserNameInput.value = e.target.value;
                    UserNameInput.error && UserNameInput.validate()
                }
            }),
            UserNameInput.error && m('div.error-message', UserNameInput.error)
        ];
    }
};
```
I create `UserNameInput` component by defining a `view` method. I also added `error` property to store validation result, `value` property to store input value, which I will bind to input value later.
The next two functions are pretty self-explanatory, `validate` function checks input value, while `isValid` returns validation result.
Here I implement **one-way data binding** from component state to view, so I can set the value of input field using `UserNameInput.value` (ie: clear input data).
```JavaScript
value: UserNameInput.value
```
For data binding on the other direction, from view to state, I used `oninput` event, so when user types something, it will trigger the validation.
```JavaScript
oninput: e => {
    UserNameInput.value = e.target.value;
    UserNameInput.error && UserNameInput.validate()
}
```
That's how two-way data binding works in Mithril. This is something I really like about Mithril, just need to do a simple value assignment and we got data binding done.

And this line:
```JavaScript
UserNameInput.error && m('div.error-message', UserNameInput.error)
```
will show the error if validation failed.

Password input is pretty much the same.
```JavaScript
let PasswordInput = {
    error: '',
    value: '',
    validate: () => {
        PasswordInput.error = !PasswordInput.value ? 'Please enter password' : '';
    },
    isValid: () => {
        return PasswordInput.error ? false : true;
    },
    view: () => {
        return [
            m('input', {
                className: PasswordInput.error ? 'error' : '',
                placeholder: 'Password',
                value: PasswordInput.value,
                type: 'password',
                oninput: e => {
                    PasswordInput.value = e.target.value;
                    PasswordInput.error && PasswordInput.validate()
                }
            }),
            PasswordInput.error && m('div.error-message', PasswordInput.error)
        ];
    }
};
```
### Form component
I've created all input, now I need a form to put them in.
```JavaScript

let LoginForm = {
    isValid() {
        UserNameInput.validate();
        PasswordInput.validate();
        if (UserNameInput.isValid() && PasswordInput.isValid()) {
            return true;
        }
        return false;
    },
    view() {
        return m('form', [
            m('h1',
                'Login'
            ),
            // Passing component
            m(UserNameInput),
            m(PasswordInput),
            m('button', {
                    class: 'pure-button pure-button-primary',
                    id: 'loginBtn',
                    type: 'button',
                    onclick() {
                        if (LoginForm.isValid()) {
                            m.route.set('/dashboard')
                        }
                    }
                },
                'Login'
            )
        ])
    }
}
```
`LoginForm` has `isValid` function, which runs when user clicks login button.
```JavaScript
m(UserNameInput),
m(PasswordInput),
```
Here I pass 2 input components above to `LoginForm`, and call `isValid` function to validate our form in `onclick` event.

Finally, add css for validation message.
```CSS
.login div.error-message {
    margin: 0px 25px;
    font-size: 90%;
    color: red;
    min-height: 8px;
}
```
### Final
![simple-form-validation-mithril-js.gif](simple-form-validation-mithril-js.gif)
The validation above is pretty simple. It works but there are room for improvement:
* Create component for each type of validation to maximize reusability (required, length, etc)
* Format error message with parameter

And many other things. You can use this tutorial as a base for further development. Have fun with Mithril!
