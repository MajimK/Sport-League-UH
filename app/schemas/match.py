from pydantic import BaseModel

# class LeagueBase(BaseModel):
#     name: str
#     description: str
#     initial_date: int
#     final_date: int

# class LeagueCreate(LeagueBase):
#     pass

# class LeagueUpdate(LeagueBase):
#     league_id: int
#     pass

# class LeagueOut(LeagueBase):
#     league_id: int
#     pass

#     class Config:
#         from_attributes = True


class SearchLeagueMatches(BaseModel):
    season_id: int
    league_id: int

class TeamScore(BaseModel):
    team_id: int
    team_name: str
    score: int

class MatchScore(BaseModel):
    home: TeamScore
    away: TeamScore

class MatchOut(BaseModel):
    match_id: int
    month: int
    day: int
    score: MatchScore


