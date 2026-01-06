from sqlmodel import Session, select, and_
from app.database.models.Match import Match
from app.database.models.MatchTeam import MatchTeam
from app.database.models.history import Season_league_team_player
from app.database.models.players import Players
from app.database.models.teams import Team
from app.schemas.match import SearchLeagueMatches, TeamScore, MatchScore, MatchOut,CreateMatches
from app.database.models.MatchTeam import TeamRole


def get_match_by_id(match_id: int, session: Session):
    query = select(Match).where(Match.match_id == match_id)
    match = session.exec(query).first()
    return match

def get_matches_by_league(search: SearchLeagueMatches, session: Session):
    query = (select(Match)
            .where(
                and_(Match.season_id == search.season_id,
                     Match.league_id == search.league_id))
            .limit(100))
    matches = session.exec(query).all()
    matches_out = []

    for match in matches:
        query_matchTeam = select(MatchTeam).where(MatchTeam.match_id == match.match_id)
        matchTeam = session.exec(query_matchTeam).all()

        if len(matchTeam) != 2:
            continue

        home = next(mt for mt in matchTeam if mt.role == "home")
        away = next(mt for mt in matchTeam if mt.role == "away")

        if not home or not away:
            continue

        home_team = session.get(Team, home.team_id)
        away_team = session.get(Team, away.team_id)

        if not home_team or not away_team:
            continue

        matches_out.append(
            MatchOut(
                match_id=match.match_id,
                month=match.month,
                day= match.day,
                team_home=home_team.name,
                team_home_id=home_team.team_id,
                team_away=away_team.name,
                team_away_id=away_team.team_id,
                score=MatchScore(home=TeamScore(team_id=home.team_id, team_name=home_team.name,score=home.score), away= TeamScore(team_id=away.team_id, team_name=away_team.name, score=away.score))
            )
        )
        
    return matches_out

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

def create_matches(create: CreateMatches, session: Session):

    # 1️⃣ Buscar equipos por nombre
    home_team = session.exec(
        select(Team).where(Team.name == create.home_name)
    ).first()

    away_team = session.exec(
        select(Team).where(Team.name == create.away_name)
    ).first()

    if not home_team or not away_team:
        raise ValueError("Uno o ambos equipos no existen")

    # 2️⃣ No puede jugar contra sí mismo
    if home_team.team_id == away_team.team_id:
        raise ValueError("Un equipo no puede jugar contra sí mismo")

    # 3️⃣ Evitar duplicado exacto accidental
    existing_match = session.exec(
        select(Match)
        .join(MatchTeam)
        .where(
            and_(
                Match.season_id == create.season_id,
                Match.league_id == create.league_id,
                Match.month == create.month,
                Match.day == create.day,
                MatchTeam.team_id == home_team.team_id,
                MatchTeam.team_id == away_team.team_id
                )
            )
    ).first()

    if existing_match:
        raise ValueError("Este partido ya existe")

    # 4️⃣ Crear Match
    match = Match(
        season_id=create.season_id,
        league_id=create.league_id,
        month=create.month,
        day=create.day,
        location=create.location
    )

    session.add(match)
    session.commit()
    session.refresh(match)

    if not match or not home_team or away_team:
        print(home_team)
        print(match)
        print(away_team)

    # 5️⃣ Crear MatchTeam (home)
    match_home = MatchTeam(
        match_id=match.match_id or 0,
        team_id=home_team.team_id or 0,
        role=TeamRole.home,
        score=0
    )

    # 6️⃣ Crear MatchTeam (away)
    match_away = MatchTeam(
        match_id=match.match_id or 0,
        team_id=away_team.team_id or 0,
        role=TeamRole.away,
        score=0
    )

    session.add(match_home)
    session.add(match_away)
    session.commit()

    return match


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
