% Method consisting in the very exact definition of a concept.
% Expected to not scale at all.


% Generating the concepts.
obj(X):- rel(X,_) ; rel(X,Y): att(Y).
att(Y):- rel(_,Y) ; rel(X,Y): obj(X).

% Avoid non-concept (no object or no attribute)
:- not obj(X):obj(X).
:- not att(Y):att(Y).
% :- not obj(_).
% :- not att(_).


#show.
#show obj/1.
#show att/1.
