---
title: "Composition over Inheritance - Example in game development"
date: 2020-11-14
summary: "What are the differences between composition and inheritance"
keywords: "Object-oriented programming, Composition, PHP, Inheritance"
tags: [Object-oriented programming, Composition, PHP, Inheritance]
---

\* In this post, I won't go over the basic concept of Object-oriented programming (OOP), assuming that you already have the basic understanding of OOP.
### Object-oriented programming - polymorphism
"Polymorphism" means having many form. In OOP, polymorphism is one of the core concepts, allows developer to perform a single action in different ways. Explained in programming way: polymorphism allows the object to decide which "form" of function/method to implement or run, by defining one interface and multiple implementations.

The purpose of polymorphism is to enforce simplicity, making codes easy to extend and thus easily maintaining applications.

You can achieve polymorphism using inheritance or composition:

* Inheritance occurs when a child class inherits from a parent class, and the child acquires all behaviors from the parent.
* [Composition is a way to combine objects or data types into more complex ones](https://en.wikipedia.org/wiki/Object_composition), rather than inheriting from a base or parent class.

### Why composition over inheritance?
The main difference between inheritance and composition is in the relationship between objects:

* Inheritance is an "is-a" relationship, used to design a class on **what it is**
* Composition is a "has-a" relationship, used to design a class on **what it does**

And their effects:

* Classes and objects created through inheritance are **tightly** coupled, changing the parent (or superclass) in an inheritance relationship can cause unwanted side effects on the subclass.
* Classes and objects created through composition are **loosely** coupled, which means you can easily change the component parts, bringing more flexibility for the program.

The primary intention of composition is to make the design more flexible. Your component can be easily added into object without repercussion. Composition also allows you to design your class where components can be replaced/modified if needed.

If we compare between composition and inheritance in a larger context, it would be between OOP and component oriented design. Both of them are **not mutually exclusive concepts**, so the most of the principles of the former still hold if you take the latter approach.

For example, if your super class and subclass share the exact same implementation, then you should use inheritance to provide the implementation. If there are many classes that have a behavior which is shared between different hierarchies, then you should consider using interface and implement composition design.

### How to implement component oriented design?

Composition over inheritance is a principle, **not a design pattern**, there is no "correct" way to do it because it depends on the language. You can use many techniques like Interface (C#, PHP etc), object merging (JS), design pattern (Bridge, Strategy...) etc to achieve composition design.

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

After a few months, you want to update your game (new DLC!). The Warrior now can block (but cannot heal) and the Wizard can heal (but cannot block).

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

**Problem #2:** your Wizard now can call `block`, and Warrior can call `heal`, but nothing will happen.
```PHP
<?php
$warrior->heal();
$wizard->block()
```
We can implement some logic to throw an exception when the above cases happen, even though it's not really an optimal solution.

This is the first sign indicating for composition, where your subclass only needs some/part of the behavior exposed by super class.

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

We will try to apply composition design using Interface, convert the above actions into component then "inject" them into our classes.
First we define a `Role` interface:
```PHP
<?php
interface Role {
    public function attack();
    public function block();
    public function heal();
}
````

Then we define all roles:

```PHP
<?php
interface IPhysicalAttacker {
    public function attack();
}

class PhysicalAttacker implements IPhysicalAttacker {
    public function attack() {
        echo "Melee attack\n";
    }
}

interface IDefender {
    public function block();
}

class Defender implements IDefender {
    public function block() {
        echo "Block\n";
    }
}

interface IMagicAttacker {
    public function attack();
}

class MagicAttacker implements IMagicAttacker {
    public function attack() {
        echo "Magic attack\n";
    }
}

interface IHealer {
    public function heal();
}

class Healer implements IHealer {
    public function heal() {
        echo "Heal\n";
    }
}
````

Then the class:

```PHP
<?php
class Warrior
{
    private $attackRole;
    private $defendRole;

    public function __construct() {
        $this->attackRole = new PhysicalAttacker();
        $this->defendRole = new Defender();
    }

    public function attack()
    {
        $this->attackRole->attack();
    }

    public function block()
    {
        $this->defendRole->block();
    }
}

class Wizard
{
    private $attackRole;
    private $healRole;

    public function __construct() {
        $this->attackRole = new MagicAttacker();
        $this->healRole = new Healer();
    }

    public function attack()
    {
        $this->attackRole->attack();
    }

    public function heal()
    {
        $this->healRole->heal();
    }
}

class BattleMage
{
    private $attackRole;
    private $healRole;

    public function __construct() {
        $this->attackRole = new PhysicalAttacker();
        $this->healRole = new Healer();
    }

    public function attack()
    {
        $this->attackRole->attack();
    }

    public function heal()
    {
        $this->healRole->heal();
    }
}

class Paladin
{
    private $attackRole;
    private $defendRole;
    private $healRole;

    public function __construct() {
        $this->attackRole = new PhysicalAttacker();
        $this->defendRole = new Defender();
        $this->healRole = new Healer();
    }

    public function attack()
    {
        $this->attackRole->attack();
    }

    public function block()
    {
        $this->defendRole->block();
    }

    public function heal()
    {
        $this->healRole->heal();
    }
}
```
Let's test it:
```PHP
<?php
echo "\nWarrior\n";
$warrior = new Warrior();
$warrior->attack();
$warrior->block();

echo "\nWizard\n";
$wizard = new Wizard();
$wizard->attack();
$wizard->heal();

echo "\nBattle Mage\n";
$battleMage = new BattleMage();
$battleMage->attack();
$battleMage->heal();

echo "\nPaladin\n";
$paladin = new Paladin();
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

That's less code duplication now.

The code is flexible enough in case you want to add some new classes with new actions (a necromancer who can `summon` but cannot heal`heal`, an assassin who can `evade` but cannot `block`). And in case you want to modify the behavior of those actions, you just need to update one function in the corresponding role.

You can even change the behavior at runtime:

```PHP
<?php
class BattleMage
{
    private $attackRole;
    private $healRole;

    public function __construct() {
        $this->attackRole = new PhysicalAttacker();
        $this->healRole = new Healer();
    }

    public function setAttackType($attackType) {
        $this->attackRole = $attackType;
    }

    public function attack()
    {
        $this->attackRole->attack();
    }

    public function heal()
    {
        $this->healRole->heal();
    }
}

$battleMage = new BattleMage();
$battleMage->attack();
$battleMage->heal();
$battleMage->setAttackType(new MagicAttacker());
$battleMage->attack();
```
Result:
```cmd
Melee attack
Heal
Magic attack
```

### Conclusion

Composition over inheritance does not mean that you should always use composition over inheritance. Both of them have pros and cons, depend on how you want your system to work, what makes sense architecturally, and how easy it will be for maintain and testing.


References:

[Game Programming Patterns - Decoupling Patterns - Component](https://gameprogrammingpatterns.com/component.html)

[Unity - Managing different weapons in scripting](https://answers.unity.com/questions/513863/managing-different-weapons-in-scripting.html)

[Unity - Component-based weapon system](https://forum.unity.com/threads/component-based-weapon-system.204999/)

[Composition over inheritance](https://en.wikipedia.org/wiki/Composition_over_inheritance)

[Strategy Pattern - Composition over Inheritance](https://onewheelstudio.com/blog/2020/8/16/strategy-pattern-composition-over-inheritance)

[How object-oriented are videogames?](https://gamedev.stackexchange.com/questions/14158/how-object-oriented-are-videogames)

[Should I still prefer composition over inheritance if the child classes need BOTH the parent interface AND its class properties?](https://softwareengineering.stackexchange.com/questions/372498/should-i-still-prefer-composition-over-inheritance-if-the-child-classes-need-bot)