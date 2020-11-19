---
title: "Composition over Inheritance - Example in game development"
date: 2020-11-14
summary: "What are the differences between composition and inheritance"
keywords: "Object-oriented programming, Composition, PHP, Inheritance"
tags: [Object-oriented programming, Composition, PHP, Inheritance]
---

### Object-oriented programming - polymorphism
"Polymorphism" means having many form. In OOP, polymorphism is one of the core concepts. allows developer to perform a single action in different ways. Explained in programming way: polymorphism allows the object to decide which "form" of function/method to implement or run, by defining one interface and multiple implementations.

The purpose of polymorphism is to enforce simplicity, making codes easy to extend and thus easily maintaining applications.

You can achieve polymorphism using inheritance or composition

* Inheritance occurs when a child class inherits from a parent class, and the child acquires all behaviors from the parent.
* [Composition is a way to combine objects or data types into more complex ones](https://en.wikipedia.org/wiki/Object_composition), rather than inheriting from a base or parent class.

### Why composition over inheritance?
The main difference between inheritance and composition is in the relationship between objects:

* Inheritance is an "is-a" relationship, used to design a class on **what it is**
* Composition is a "has-a" relationship, used to design a class on **what it does**

And their effects:

* Classes and objects created through inheritance are **tightly** coupled, changing the parent (or superclass) in an inheritance relationship can cause unwanted side effects on the subclass.
* Classes and objects created through composition are **loosely** coupled, which means you can easily change the component parts, brings more flexibility for the program.

The primary intention of composition is to make the design more flexible. Your component can be easily added into object without repercussion. Composition also allows you to design your class where components can be replaced/modified if needed.

More importantly, if we compare between composition and inheritance in a larger context, it would be between OOP and component oriented design. Both of them are not mutually exclusive concepts, so the most of the principles of the former still hold if you take the latter approach.

For example, if your super class and subclass share the exact same implementation, then you should use inheritance in the super class to provide the implementation. If there are many classes that have a behavior which is shared between different hierarchies, then you should consider using interface and implement composition design.

### How to implement component oriented design?

Composition over inheritance is a principle, **not a design pattern**, there is no "correct" way to do it because it depends on the language. You can use many techniques like Interface (C#, PHP), object merging (JS) etc to achieve composition design.

### Drawbacks

A common drawback of composition is that method provided by component may have to be re-implemented, even if they only [delegate](https://en.wikipedia.org/wiki/Delegation_(object-oriented_programming)) or [forward](https://en.wikipedia.org/wiki/Forwarding_(object-oriented_programming)) to another function.

Inheritance, on the other hand, does not require re-implementation of method, only when the subclass has a different behavior comparing to super class (override).

### An example using inheritance

**Scenario:** you are making a game. An action RPG game (think Diablo, Grim Dawn).

At the beginning of the game, user can choose a class. This is the first version of the game, you only have 2 classes: Warrior and Wizard.

So we have the basic implementation like this:
```PHP
<?php
abstract class BaseClass
{
    abstract public function attack() ;
}

class Warrior extends BaseClass
{
    public function attack()
    {
        echo "Melee attack\n";
    }
}

class Wizard extends BaseClass
{
    public function attack()
    {
        echo "Magic attack\n";
    }
}

$warrior = new Warrior();
$warrior->attack();

$wizard = new Wizard();
$wizard->attack();
```
Result:
```cmd
Melee attack
Magic attack
```
First you have `BaseClass`, which is an abstract class. Then Warrior and Wizard inherit BaseClass, and implement different actions in `attack`. This looks sensible and follows a textbook intro to OOP.

OK, you want to update your game (new DLC!). The Warrior now can block (but cannot heal) and the Wizard can heal (but cannot block).

```PHP
<?php
abstract class BaseClass
{
    abstract public function attack() ;
    abstract public function block() ;
    abstract public function heal() ;
}
```
**Problem #1:** you have to implement all there function *attack*, *block* and *heal* in subclasses.

**First attempt:** remove abstract class

```PHP
<?php
class BaseClass
{
    public function attack() {}
    public function block() {}
    public function heal() {}
}

class Warrior extends BaseClass
{
    public function attack()
    {
        echo "Melee attack\n";
    }

    public function block()
    {
        echo "Block\n";
    }
}


class Wizard extends BaseClass
{
    public function attack()
    {
        echo "Magic attack\n";
    }

    public function heal()
    {
        echo "Heal\n";
    }
}

$warrior = new Warrior();
$warrior->attack();
$warrior->block();

$wizard = new Wizard();
$wizard->attack();
$wizard->heal();
```
Result:
```cmd
Melee attack
Block
Magic attack
Heal
```

That's great, but...

**(Small) Problem #2:** your Wizard now can call `block` (or Warrior can call `heal`) but won't do anything.
```PHP
<?php
$warrior->heal();
$wizard->block()
```
This is not a big deal, since inside subclass, we can implement some logic to throw an exception when the above cases happen, but it's not really an optimal solution.

Now you have a new DLC, a new class called BattleMage is added, they can `attack` like Warrior, they can also `heal` like Wizard.

```PHP
<?php
class BattleMage extends BaseClass
{
    public function attack()
    {
        echo "Melee attack\n";
    }

    public function heal()
    {
        echo "Heal\n";
    }
}

$battleMage = new BattleMage();
$battleMage->attack();
$battleMage->heal();
```
Result:
```cmd
Melee attack
Heal
```
Your code is still running fine, but you are getting duplication of attack and heal action. They are basically the same action but defined in 2 different places.

Let's say you want to add a new class called Paladin, they can `attack`, `block` and even `heal`!

```PHP
<?php
class Paladin extends BaseClass
{
    public function attack()
    {
        echo "Melee attack\n";
    }

    public function block()
    {
        echo "Block\n";
    }

    public function heal()
    {
        echo "Heal\n";
    }
}

$paladin = new Paladin();
$paladin->attack();
$paladin->block();
$paladin->heal();
```
Result:
```cmd
Melee attack
Block
Heal
```

Your code does run, but more code duplication...

### Fixing the problem
Now take a look again at the game, you have:
* Warrior = attack + block
* Wizard = attack + heal
* BattleMage = attack + heal
* Paladin = attack + block + heal

**Attempt #1:**

We will try to apply composition using Interface. From the information above, we can define a `Role` interface:
```PHP
<?php
interface Role {
    public function canHeal();
    public function canBlock();
}
````

then we define all roles:

```PHP
<?php
class PhysicalAttacker implements Role {
    public function canHeal() {
        return false;
    }

    public function canBlock() {
        return true;
    }
}

class MagicUser implements Role {
    public function canHeal() {
        return true;
    }

    public function canBlock() {
        return false;
    }
}

class Paladin implements Role {
    public function canHeal() {
        return true;
    }

    public function canBlock() {
        return true;
    }
}
````

The BaseClass now will implement all the action: `attack`, `block`, `heal`.

```PHP
<?php
class BaseClass
{
    private $role;
    private $attack;

    public function __construct(string $attack, Role $role) {
        $this->attack = $attack;
        $this->role = $role;
    }

    public function attack() {
        echo $this->attack . "\n";
    }

    public function block() {
        if ($this->role->canBlock()) {
            echo "Block\n";
        }
    }

    public function heal() {
        if ($this->role->canHeal()) {
            echo "Heal\n";
        }
    }
}
```
Let's test it:
```PHP
<?php
echo "\nWarrior\n";
$warrior = new BaseClass("Melee attack", new PhysicalAttacker());
$warrior->attack();
$warrior->block();

echo "\nWizard\n";
$wizard = new BaseClass("Magic attack", new MagicUser());
$wizard->attack();
$wizard->heal();

echo "\nBattle Mage\n";
$battleMage = new BaseClass("Melee attack", new MagicUser());
$battleMage->attack();
$battleMage->heal();

echo "\nPaladin\n";
$paladin = new BaseClass("Melee attack", new Paladin());
$paladin->attack();
$paladin->block();
$paladin->heal();
```
Result:
```cmd
Warrior
Melee attack
Block

Wizard
Magic attack
Heal

Battle Mage
Melee attack
Heal

Paladin
Melee attack
Block
Heal
```

That's less code duplication now. The code is flexible enough in case you want to add some new classes with new actions (a necromancer who can `summon` but cannot heal`heal`, an assassin who can `hide` but cannot `block`). And in case you want to modify the behavior of those actions, you just need to update one function in `BaseClass`.

But there are still problems:
1. `attack` is still duplicated, we need to separate it into a different place.
2. Wizard still be able to call `block`, and Warrior still be able to call `heal` (even tho they won't do anything).
3. All roles have to implement all function of `Role` interface

(To be continue)

[Game Programming Patterns - Decoupling Patterns - Component](https://gameprogrammingpatterns.com/component.html)