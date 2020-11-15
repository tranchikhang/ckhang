---
title: "Composition over Inheritance - Example in game development"
date: 2020-11-14
summary: "What are the differences between composition and inheritance"
keywords: "Object-oriented programming, Composition, PHP, Inheritance"
tags: [Object-oriented programming, Composition, PHP, Inheritance]
---

### Object-oriented programming - polymorphism
"Polymorphism" means having many form. In OOP, polymorphism is one of the core concepts. It allows developer to perform a single action in different ways (explained in programming way: allow the object to decide which "form" of function/method to implement or run, by defining one interface and multiple implementations).

The purpose of polymorphism is to enforce simplicity, making codes easy to extend and thus easily maintaining applications.

You can achieve polymorphism using inheritance or composition

* Inheritance occurs when a child class inherits from a parent class, and the child acquires all behaviors from the parent.
* [Composition is a way to combine objects or data types into more complex ones](https://en.wikipedia.org/wiki/Object_composition), rather than inheriting from a base or parent class.

### The differences between Inheritance and Composition
The main difference between inheritance and composition is in the relationship between objects...

* Inheritance is an "is-a" relationship, used to design a class on what it is
* Composition is a "has-a" relationship, used to design a class on what it does

... and their effect:

* Classes and objects created through inheritance are **tightly** coupled, changing the parent (or superclass) in an inheritance relationship can cause unwanted side effects on the subclass.
* Classes and objects created through composition are **loosely** coupled, which means you can easily change the component parts, brings more flexibility for the program.

### An example using inheritance
\* In this article, I will use PHP because it's my go-to language.

\* Composition over inheritance is a principle, there is no "correct" way to do it because it depends on the language. You can use many techniques like Interface (C#, PHP), object merging (JS), strategy pattern etc to achieve composition design.

**Scenario:** you are making a game. An action RPG game (think Diablo, Grim Dawn).

At the beginning of the game, user can choose a class. This is the first version of the game, you only have 2 classes: Warrior and Wizard.
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
First you have `BaseClass`, which is an abstract class. Then Warrior and Wizard inherit BaseClass, and implement different action in `attack`. This looks sensible and follows a textbook intro to OOP.

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

**Problem #2:** your Wizard now can `block` (or Warrior can `heal`) but won't do anything. The reason is we haven't implemented it, but even if we do, it would be incorrect, cause only Warrior can block and only Wizard can heal.
```PHP
<?php
$warrior->heal();
$wizard->block()
```
We won't deal with this right now, I will go over all the problems with inheritance, then try to fix them with composition.

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

### Fixing the problem with composition
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