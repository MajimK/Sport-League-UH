from fastapi import APIRouter, Depends, HTTPException, status
from app.database.db import get_session
from app.schemas.teams import TeamCreate
from app.schemas.utils import AddPlayersResponse, AddPlayersRequest
from app.schemas.players import PlayerCreate
from sqlmodel import Session
from app.utils.extract_data import (extract_players, fetch_players_from_nextcloud, FacultadEnum, SportEnum)
from app.core.players import save_player
from app.core.teams import save_team, get_teams_by_name
from app.core.teams import add_players_to_team


router = APIRouter(prefix="/form", tags=["Teams"])


@router.get("/charge-form", status_code=status.HTTP_201_CREATED)
def get_players_forms(session: Session=Depends(get_session)):
    try:
        players = extract_players()

        for fila in players:
            ci = fila[1664]
            nombre = fila[1665]
            faculty = fila[1666]

            player = PlayerCreate(
                CI=ci,
                name=nombre,
                faculty= FacultadEnum.obtener_nombre_formateado(faculty)
            )
            team_name = fila[1670]
            deporte = fila[1671]
            game_name= SportEnum.get_name_by_number(deporte)
            print(game_name)

            
            team = TeamCreate(
                name=team_name,
                description="descripicion",
                game_name= game_name
            )

            try:
                db_player = save_player(player, session)
                if not db_player:
                    continue
                db_team = save_team(team, session)
                if not db_team:
                    db_team = get_teams_by_name(team.name, session)
                    continue
                        
                add_player = AddPlayersRequest(players=[db_player.player_id or 0])
                
                if not db_team.team_id:
                    print(f"Error: Equipo no tiene ID válido: {db_team}")
                    continue
                add_players_to_team(db_team.team_id,add_player,session)


            except ValueError as e:
                print(f"{e}")
    except ValueError as e:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    
@router.get("/charge-data-nextcloud", status_code= status.HTTP_201_CREATED)
def get_players(session= Depends(get_session)):
    all_players = fetch_players_from_nextcloud()
    for player in all_players:
        try:
            save_player(player, session)
        except ValueError as e:
            print(e)
            continue





