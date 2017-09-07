% This method is expected to fail.
% This is performed in order to detect any problem in the automatic
%  method function generation, or in the automatic test generation.


% Here: missing rules and constraints. It's impossible that this code
%  yields correct answer sets.

% Even the empty context will fail:
obj(a).


% If the tests relatives to this method fails, it's either because:
%  - it is treated as any other concept generation method, without a special case for 'false' method.
%  - another method is named 'false', either because user wants it, or because the automatic generation of method function failed. One easy way to test this is to delete lines of a working generation method, and then run the unit tests until something broke. Chances are all tests will broke, since one method usurpated all the others.
