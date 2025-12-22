from sqlmodel import Session, select, and_
from app.database.models.Match import Match
from app.database.models.MatchTeam import MatchTeam
from app.database.models.history import Season_league_team_player
from app.database.models.players import Players
from app.database.models.teams import Team
from app.schemas.match import SearchLeagueMatches, TeamScore, MatchScore


def get_match_by_id(match_id: int, session: Session):
    query = select(Match).where(Match.match_id == match_id)
    match = session.exec(query).first()
    return match

# def get_matches_by_league(search: SearchLeagueMatches, session: Session):
#     query = (select(Match)
#             .where(
#                 and_(Match.season_id == search.season_id,
#                      Match.league_id == search.league_id))
#             .limit(100))
#     rows = session.exec(query).all()

#     for match in rows:
        
        
#     return matches

def get_teams_in_match(match_id: int, session: Session):
    query = (select(Team)
            .join(MatchTeam)
            .where(MatchTeam.match_id == match_id))
    teams = session.exec(query).all()
    return teams

def get_players_in_match(match_id: int, session: Session):
    query = (select(Players)
            .join(Season_league_team_player)
            .join(MatchTeam)
            .where(MatchTeam.match_id == match_id))
    
    players = session.exec(query).all()
    return players

def get_score_in_match(match_id: int, session: Session):
    rows = session.exec(
        select(MatchTeam).where(MatchTeam.match_id == match_id)
    ).all()

    result = {}

    for row in rows:
        team = session.get(Team, row.team_id)
        if team is not None:
            team_score = TeamScore(
                team_id=row.team_id,
                team_name=team.name,
                score=row.score
            )
            result[row.role] = team_score   

    return MatchScore(home=result["home"], away=result["away"])

# def save_league(league: LeagueCreate, session: Session):
#     existing_league = get_league_by_name(league.name, session)

#     if existing_league:
#         raise ValueError("El equipo ya esta creado")
    
#     db_league = Leagues.from_orm(league)
#     session.add(db_league)
#     session.commit()
#     session.refresh(db_league)
#     return db_league


# def get_players_by_league(league_id: int, session: Session):
#     league = session.get(Leagues, league_id)
#     if not league:
#         return None
    
#     query = ( select(Players)
#             .join(Season_league_team_player)
#             .where(Season_league_team_player.league_id == league_id)
#             .distinct()
#             )
#     players_league = session.exec(query).all()
#     return players_league


# def get_teams_by_league(league_id: int, session: Session):
#     league = session.get(Leagues, league_id)
#     if not league:
#         return None
    
#     query = ( select(Team)
#             .join(Season_league_team_player)
#             .where(Season_league_team_player.league_id == league_id)
#             .distinct()
#             )
#     teams_league = session.exec(query).all()
#     return teams_league

# def get_seasons_by_league(league_id: int, session: Session):
#     league = session.get(Leagues, league_id)
#     if not league:
#         return None
    
#     query = ( select(Season)
#             .join(Season_league_team_player)
#             .where(Season_league_team_player.league_id == league_id)
#             .distinct()
#             )
#     seasons_league = session.exec(query).all()
#     return seasons_league
