% From "Querying Formal Contexts with Answer Set Programs".


obj(X):- rel(X,_), not outof_ext(X).
outof_ext(X):- rel(X,_) ; rel(_,Y) ; att(Y) ; not rel(X,Y).

att(Y):- rel(_,Y), not outof_int(Y).
outof_int(Y):- rel(_,Y) ; rel(X,_) ; obj(X) ; not rel(X,Y).

% Avoid ¬concepts containing all attributes and no objects
%  or all objects and no attributes.
:- not obj(X): obj(X).
:- not att(X): att(X).


#show.
#show obj/1.
#show att/1.
