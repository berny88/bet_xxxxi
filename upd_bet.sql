select 'insert into bet (uuid, fk_game, fk_user, resultA, resultB, nbpoints) values ('|| ROW_NUMBER() OVER(ORDER BY key) ||','|| key||','|| uuid||','|| 0||','|| 0||','|| 0||');'
from betuser u, GAME g
where g.key like 'FIN8%';
