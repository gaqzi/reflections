# Template pattern and other dilemmas


While subclassing from a concrete or an abstract base class, we start to implement an architecture that is known as the template pattern. In the template pattern:

* Subclasses inherits implementation methods from the base class.
* Then those subclasses have to implement a few abstract methods that are required by the abstract base class.
* Eventually the base class calls the implementation of the abstract method.

In this case, both the subclass and the base class use each other's implementation methods to do some task and this two-way dance is usually hard to follow.


Coming soon...
