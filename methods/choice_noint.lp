% Method defined by Jacques, and modified to remove integers.
% Expected to scale more than the initial method.

rel(X,Y):- edge(X,Y).
rel(Y,X):- edge(X,Y).

% Choice of elements in set 1 and 2 of a concept
1 { obj(X): rel(X,_)}.
1 { att(Y): rel(_,Y)}.
% A node is impossible in a set if not linked to some node in the other set
impobj(X):- rel(X,_), att(Y), not rel(X,Y).
impatt(Y):- rel(_,Y), obj(X), not rel(X,Y).
% Consistency ; no impossible element can be added to the concept
:- impobj(X), obj(X).
:- impatt(X), att(X).
% Maximality  ; all possible elements have to be added to the concept
:- not impobj(X), not obj(X), rel(X,_).
:- not impatt(Y), not att(Y), rel(_,Y).

#show.
#show obj/1.
#show att/1.
