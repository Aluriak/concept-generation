% Method defined by Jacques.
% Expected to scale more than the simple method.


% Choice of elements in set 1 and 2 of a concept
1 { concept(1,X): rel(X,_)}.
1 { concept(2,Y): rel(_,Y)}.
% A node is impossible in a set if not linked to some node in the other set
imp(1,X):- rel(X,_), concept(2,Y), not rel(X,Y), X!=Y.
imp(2,Y):- rel(_,Y), concept(1,X), not rel(X,Y), X!=Y.
% Consistency ; no impossible element can be added to the concept
:- imp(T,X), concept(T,X).
% Maximality  ; all possible elements have to be added to the concept
:- not imp(1,X), not concept(1,X), rel(X,_).
:- not imp(2,Y), not concept(2,Y), rel(_,Y).

#show.
#show obj(X): concept(1,X).
#show att(Y): concept(2,Y).
