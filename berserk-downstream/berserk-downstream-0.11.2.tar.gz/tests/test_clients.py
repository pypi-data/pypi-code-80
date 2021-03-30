import berserk
import config

session = berserk.TokenSession(config.API_KEYS['ADMIN_LICHESS_TOKEN'])
lichess = berserk.Client(session=session)

x = lichess.tournaments.create_arena(5, 2, 60, teamId='niner-chess-club', minRating=1000, maxRating=2200, nbRatedGame=20)
print(x)
