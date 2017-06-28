                   %   f g h i j k
rel(a,(f;g)).      % a × ×
rel(b,(g;h;j;k)).  % b   × ×   × ×
rel(c,(i;j;k)).    % c       × × ×
rel(d,(g;i)).      % d   ×   ×
rel(e,(f;g;h;i)).  % e × × × ×


% Solutions
% a e × f g
% a b d e × g
% b × g h j k
% c × i j k
% b c × j k
% c d e × i
% d e × g i
% e × f g h i
% b e × g h
