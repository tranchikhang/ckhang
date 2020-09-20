---
title: "Named parameters binding with pyodbc"
date: 2019-11-17
summary: "Binding parameter in pyodb with named placeholder without worrying about order"
draft: true
---

A few days ago, while working with python and Sql Server using pyodbc, I had some troubles with parameter binding. The library supports [binding](https://github.com/mkleehammer/pyodbc/wiki/Binding-Parameters) by marking the placeholder with "?" character and passing the value array into execute function.
```Python
c.execute('INSERT INTO user_info (first_name, last_name, home_address) VALUES (?, ?, ?)', [first_name, last_name, home_address])
```
First thing I noticed that it was hard to keep track all the parameters since I have to pass the value arrays with the correct order and all the placeholders are just "?". I want to use named placeholder like ":first_name", ":last_name" but it's not possible because pyodbc doesn't support it. After searching around, I found this similar question on SO: [Does pyodbc support any form of named parameters?](https://stackoverflow.com/questions/32748982/does-pyodbc-support-any-form-of-named-parameters), still no solution.


There are situations where named placeholder can be more convenient, for example, I have these values and a query:
```Python
# values is a dictionary of values you received from submitted form etc
values = {
    'first_name' = 'Khang'
    'last_name' = 'Tran'
    'home_address' = 'Tokyo'
    'office_address' = 'Chiyoda'
}
sql1 = 'INSERT INTO user_info (first_name, last_name, home_address) VALUES (?, ?, ?)'
```
If I want to execute sql1, I just need to pass a list as parameters:
```Python
[values['first_name'], values['last_name'], values['home_address']]
```
Then I want to execute another query, using the same values variable above, I have to specify the values again.
```Python
sql2 = 'INSERT INTO employee_info (first_name, last_name, office_address) VALUES (?, ?, ?)'
```
It would be great if I could just pass the whole array and the placeholder will map with the value automatically using the key name.
So I decided to make a function supporting named placeholder and auto mapping.
```Python
import re

def bindParams(sql, params):
    bindingParams = []
    matches = re.findall(r'[:]\w+', sql)
    if len(matches) == 0:
        return sql, bindingParams

    for match in matches:
        key = match[1:]
        if key in params:
            bindingParams.append(params[key])
        else:
            raise ValueError('No value with key: ' + key)

    sql = re.sub(r'[:]\w+', r'?', sql)

    return sql, bindingParams

params= {
    'first_name' : 'Khang',
    'last_name' : 'Tran',
    'home_address' : 'Itabashi',
    'office_address' : 'Chiyoda'
}

sql1 = 'INSERT INTO user_info (first_name, last_name, home_address) VALUES (:first_name, :last_name, :home_address)'
sql2 = 'INSERT INTO employee_info (first_name, last_name, office_address) VALUES (:first_name, :last_name, :office_address)'
sql, params1 = bindParams(sql1, params)
print(sql)
print(params1)
sql, params2 = bindParams(sql2, params)
print(sql)
print(params2)
```
Result:
```SQL
INSERT INTO user_info (first_name, last_name, home_address) VALUES (?, ?, ?)
['Khang', 'Tran', 'Itabashi']
INSERT INTO employee_info (first_name, last_name, office_address) VALUES (?, ?, ?)
['Khang', 'Tran', 'Chiyoda']
```
That's all, now I can use named placeholder and pass the value dictionary without worrying about the order.