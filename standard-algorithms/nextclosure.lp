% Iterative implementation of close-by-one algorithm.
%  INPUT: rel(X,Y): object X is in relation with attribute Y.
%  OUTPUT: ext(N,X): concept N has X in its extent.
%          int(N,Y): concept N has Y in its intent.

object(G) :- rel(G,_).
attribute(M) :- rel(_,M).


% Initial step.
int(1,A) :- attribute(A).
ext(1,O) :- object(O) ; rel(O,A): int(1,A).
step(2).
current(2,X) :- X=#max{O:object(O)}.
next(2,X) :- X=#max{O:object(O)}.

% While loop: there is a next step iif current state is not the last possible state.
step(N+1) :- step(N) ; not last_step(N) ; N<100.

% Derivation at step N.
derived(N,Y) :- step(N) ; current(N,_) ; attribute(Y) ; rel(X,Y): current(N,X).
double_derived(N,X) :- step(N) ; current(N,_) ; object(X) ; rel(X,Y): derived(N,Y).
newly_derived_object(N,X) :- step(N) ; double_derived(N,X) ; not current(N,X).

% It is a concept if all newly derived objects are greater than the next object.
is_concept(N) :- step(N) ; next(N,T) ; X>=T: newly_derived_object(N,X).
% Yield the concept.
ext(N,O) :- is_concept(N) ; double_derived(N,O).
int(N,A) :- is_concept(N) ; derived(N,A).
% Changes of state.
next_next(N,T) :-     is_concept(N) ; step(N) ; T=#max{O:object(O), not double_derived(N,O)}.
next_next(N,T) :- not is_concept(N) ; step(N) ; T=#max{O:object(O), not current(N,O), O<MaxCurrent} ; MaxCurrent=#max{P:current(N,P)}.

% Changes of state for current/2, needing an intermediary variable.
current_intermediate(N,X) :- is_concept(N) ; double_derived(N,X).
current_intermediate(N,X) :- is_concept(N) ; next_next(N,X).  % add the next object
current_intermediate(N,X) :- not is_concept(N) ; current(N,X).
current_intermediate(N,X) :- not is_concept(N) ; next_next(N,X).
next_current(N,X) :- current_intermediate(N,X) ; next_next(N,T) ; T>=X.

current(N+1,X) :- next_current(N,X).
next(N+1,X) :- next_next(N,X).

% If the next element is #inf, meaning #max has no value,
%  i.e. there is no object that is not in double_derived or current,
%  then the maximal subset of G (G itself) has been treated.
%  The enumeration is therefore done.
last_step(N) :- next_next(N,#inf).


#show.
#show is_concept/1.
#show current/2.
#show next/2.
#show derived/2.
#show double_derived/2.
#show ext/2.
#show int/2.
#show last_step/1.
% #show step/1.
% #show newly_derived_object/2.
% #show next_current/2.
% #show next_next/2.
% #show current_intermediate/2.

% DEBUG:
% 1 { one_step(X) : step(X) } 1.
% 1 { one_step(4..6) }.
% #show is_concept(N): one_step(N), is_concept(N).
% #show current(N,X): one_step(N), current(N,X).
% #show next_current(N,X): one_step(N), next_current(N,X).
% #show next(N,X): one_step(N), next(N,X).
% #show next_next(N,X): one_step(N), next_next(N,X).
% #show derived(N,X): one_step(N), derived(N,X).
% #show double_derived(N,X): one_step(N), double_derived(N,X).
% #show newly_derived_object(N,X): one_step(N), newly_derived_object(N,X).
% #show ext(N,X): one_step(N), ext(N,X).
% #show int(N,X): one_step(N), int(N,X).
% #show current_intermediate(N,X): one_step(N), current_intermediate(N,X).
