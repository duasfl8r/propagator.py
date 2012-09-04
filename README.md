propagator.py
=============

**propatagor.py** is a *propagator network* built with Python.

It is based on (or, should I say, translated from) the [Art of the Propagator][art],
a paper written by Alexey Radul and Gerald Sussman. There's a presentation
by Sussman called [We Really Don't Know How To Compute!][we-really-dont-know]
in which he explains the concepts and some applications wonderfully.

They wrote a complete propagator network and examples in MIT Scheme. I will
try to build a library that encompasses all the original features, together
with the examples.

My intentions translating it to Python are:

- Understanding how these propagators work -- I can make sense of Scheme
  functions (the trees), but it's more difficult to grasp the program as a
  whole (the forest).

- Making propagators available to a wider audience.

[art]: http://dspace.mit.edu/handle/1721.1/4421
[we-really-dont-know]: http://www.infoq.com/presentations/We-Really-Dont-Know-How-To-Compute
