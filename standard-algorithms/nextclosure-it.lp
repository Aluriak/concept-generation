% Iterative implementation of close-by-one algorithm,
%  using the iterative mode of clingo.
%  INPUT: rel(X,Y): object X is in relation with attribute Y.
%  OUTPUT: ext(N,X): concept N has X in its extent.
%          int(N,Y): concept N has Y in its intent.

#include <incmode>.
#const istop="UNSAT".
% #const imin=1.
%#const imax=11.


#program base.
object(G) :- rel(G,_).
attribute(M) :- rel(_,M).

int(0,A) :- attribute(A).
ext(0,O) :- object(O) ; rel(O,A): int(0,A).
current(1,X) :- X=#max{O:object(O)}.
next(1,X) :- X=#max{O:object(O)}.



#show ext/2.
#show int/2.
% #show next_next/2.
% #show is_concept/1.


#program step(k).
step(k).

derived(k,Y) :- step(k) ; current(k,_) ; attribute(Y) ; rel(X,Y): current(k,X).
double_derived(k,X) :- step(k) ; current(k,_) ; object(X) ; rel(X,Y): derived(k,Y).
newly_derived_object(k,X) :- step(k) ; double_derived(k,X) ; not current(k,X).

% It is a concept if all newly derived objects are greater than the next object.
is_concept(k) :- step(k) ; next(k,T) ; X>=T: newly_derived_object(k,X).
% Yield the concept.
ext(k,O) :- is_concept(k) ; double_derived(k,O).
int(k,A) :- is_concept(k) ; derived(k,A).
% Changes of state.
next_next(k,T) :-     is_concept(k) ; step(k) ; T=#max{O:object(O), not double_derived(k,O)}.
next_next(k,T) :- not is_concept(k) ; step(k) ; T=#max{O:object(O), not current(k,O), O<MaxCurrent} ; MaxCurrent=#max{P:current(k,P)}.

% Changes of state for current/2, needing an intermediary variable.
current_intermediate(k,X) :- is_concept(k) ; double_derived(k,X).
current_intermediate(k,X) :- is_concept(k) ; next_next(k,X).  % add the next object
current_intermediate(k,X) :- not is_concept(k) ; current(k,X).
current_intermediate(k,X) :- not is_concept(k) ; next_next(k,X).
next_current(k,X) :- current_intermediate(k,X) ; next_next(k,T) ; T>=X.

current(k+1,X) :- next_current(k,X).
next(k+1,X) :- next_next(k,X).

% If the next element is #inf, meaning #max has no value,
%  i.e. there is no object that is not in double_derived or current,
%  then the maximal subset of G (G itself) has been treated.
%  The enumeration is therefore done.
last_step(k+1) :- next_next(k,#inf).




#program check(k).
% If it is the last step, finish by making the model unsatisfiable.
:- last_step(k), query(k).
