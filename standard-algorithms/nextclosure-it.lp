% Iterative implementation of Next Closure algorithm,
%  using the iterative mode of clingo.
%  INPUT: rel(X,Y): object X is in relation with attribute Y.
%  OUTPUT: ext(N,X): concept N has X in its extent.
%          int(N,Y): concept N has Y in its intent.

#include <incmode>.

object(G) :- rel(G,_).
attribute(M) :- rel(_,M).

% Initially, produce the concept whose intent is the whole set of attributes.
int(0,M) :- attribute(M).
ext(0,G) :- object(G) ; rel(G,M): int(0,M).

% Initialize next step.
maxobject(Max) :- Max=#max{O:object(O)}.
current(0,X) :- maxobject(X).
next(0,X) :- maxobject(X).


#program step(k).

% Produce the extent.
current(k,X) :- not empty(k-1) ; double_derived(k-1,X) ; next(k,T) ; T>=X.
current(k,X) :-     empty(k-1) ; current(k-1,X)        ; next(k,T) ; T>=X.
current(k,X) :- next(k,X).  % add the next object

% Change of state.
next(k,T) :- not empty(k-1) ; T=#max{O:object(O), not double_derived(k-1,O)}.
next(k,T) :-     empty(k-1) ; T=#max{O:object(O), not current(k-1,O), O<MaxCurrent} ; MaxCurrent=#max{P:current(k-1,P)}.

% Derivation groups.
derived(k,Y) :-  attribute(Y) ; rel(X,Y): current(k,X).
double_derived(k,X) :- object(X) ; rel(X,Y): derived(k,Y).

% Newly derived objects must be greater than the next object.
empty(k) :- next(k,T) ; X<T ; double_derived(k,X) ; not current(k,X).

% Yield the concept.
ext(k,O) :- not empty(k) ; double_derived(k,O).
int(k,A) :- not empty(k) ; derived(k,A).


#program check(k).
:- query(k) ; not ext(k,O) ; object(O).


% Outputs.
#show ext/2.
#show int/2.
