% Object Intersections implementation in ASP.
%  INPUT:
%    rel(X,Y): object X has attribute Y.
%    object(O): current object to study is O.
%    concept_ext(X): current concept to study has X in its extent.
%    concept_int(Y): current concept to study has Y in its intent.
%    concepts_int(N,Y): intent number N contains attribute Y.
% If a concept is found, outputs ext/1 and int/1.


% Computer the intersection.
derived(A) :- rel(O,A) ; object(O).
inters(A) :- concept_int(A) ; derived(A).

% discard model if inters is found to be equivalent to any existing intent.
:- concepts_int(N,_) ; inters(A): concepts_int(N,A) ; concepts_int(N,A): inters(A).

% Create the concept.
ext(O) :- rel(O,_) ; rel(O,A): inters(A).
int(A) :- inters(A).
