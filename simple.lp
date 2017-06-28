% Method consisting in the very exact definition of a concept.
% Expected to not scale at all.

% run: clingo -n 0 simple.lp


% Context described by:
%   e f g h
% a   x   x
% b   x
% c x x   x
% d x x
% (yields 4 concepts)
% rel(a,(f;h)).
% rel(b,f).
% rel(c,(e;f;h)).
% rel(d,(e;f)).


% Generating the concepts.
obj(X):- rel(X,_) ; rel(X,Y): att(Y).
att(Y):- rel(_,Y) ; rel(X,Y): obj(X).
% We found the 4 expected concepts.
% However, the following constraints unexpectedly remove some of them.


% With this one, remains only 3 concepts.
% :- not obj(_) ; not att(_).

% With the following two, remains only 1 concept.
% :- not obj(_).
% :- not att(_).


#show.
#show obj/1.
#show att/1.
