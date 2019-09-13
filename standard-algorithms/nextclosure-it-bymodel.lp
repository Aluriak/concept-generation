% Copy of nextclosure-it.lp, but using incmode differently,
%  yielding one model per concept instead of all in one single model.
% This is kept because it is way easier to debug it than
%   the more impressive single-shot model.

#include <incmode>.
#const istop="UNSAT".

#program base.
object(G) :- rel(G,_).
attribute(M) :- rel(_,M).

% Initially, produce the concept whose intent is the whole set of attributes.
int(0,M) :- attribute(M).
ext(0,G) :- object(G); rel(G,M): int(0,M).

% Initialize next step.
maxobject(Max):- Max=#max{O:object(O)}.
current(0,X) :- maxobject(X).
next(0,X) :- maxobject(X).


#program step(k).

% Change of state.
next(k,T) :- not empty(k-1) ; T=#max{O:object(O), not double_derived(k-1,O)}.
next(k,T) :-     empty(k-1) ; T=#max{O:object(O), not current(k-1,O), O<MaxCurrent} ; MaxCurrent=#max{P:current(k-1,P)}.

% Produce the extent.
current(k,X) :- not empty(k-1) ; double_derived(k-1,X) ; next(k,T) ; T>=X.
current(k,X) :-     empty(k-1) ; current(k-1,X)        ; next(k,T) ; T>=X.
current(k,X) :- next(k,X).  % add the next object

% Derivation groups.
derived(k,Y) :-  attribute(Y) ; rel(X,Y): current(k,X).
double_derived(k,X) :- object(X) ; rel(X,Y): derived(k,Y).

% Newly derived objects must be greater than the next object.
empty(k) :- next(k,T) ; X<T ; double_derived(k,X) ; not current(k,X).

% Yield the concept.
ext(k,O) :- not empty(k) ; double_derived(k,O).
int(k,A) :- not empty(k) ; derived(k,A).


#program check(k).
% :- query(k) ; next(k,#inf).
:- query(k) ;  ext(k-1,O): object(O).


% Outputs.
#show.
#show ext(k,N): ext(k,N), query(k).
#show int(k,N): int(k,N), query(k).
% #show next(k,N): next(k,N), query(k).
% #show double_derived(k,N): double_derived(k,N), query(k).
