#const mino=1.
#const mina=1.


object(O):- rel(O,A).
attribute(A):- rel(O,A).

% Choice of the minimum of the concept.
1{minobj(X):object(X)}1.

% Choice of elements in the object part of the concept (at least mino objects).
concept(obj,X):- minobj(X).
mino-1{concept(obj,X): object(X), Min<X}:- minobj(Min).

% Choice of elements in the attribute part of the concept (at least mina attributes).
mina{concept(att,Y): rel(Min,Y)} :- minobj(Min).

% Object that is not in relation with some attribute in the concept.
impossible(obj,X):- object(X), concept(att,A), not rel(X,A).

% Attribute that is not in relation with some object in the concept.
impossible(att,Y):- attribute(Y), concept(obj,O), not rel(O,Y).

admissible(obj,X):- not impossible(obj,X); object(X).
admissible(att,Y):- not impossible(att,Y); attribute(Y).

% Consistency: no impossible object belonging to the concept.
:- impossible(obj,X); concept(obj,X).
:- impossible(att,Y); concept(att,Y).

% Maximality: all possible object or attribute have to be added to the acomp.
:- admissible(obj,X); not concept(obj,X).
:- admissible(att,Y); not concept(att,Y).

#show.
#show obj(X): concept(obj,X).
#show att(Y): concept(att,Y).
