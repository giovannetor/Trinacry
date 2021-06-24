import os
import time
from enum import Enum
from io import StringIO
from pathlib import Path
from packaging import version

from sqlalchemy import __version__ as sqlav
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import desc

from models import Scores

if version.parse(sqlav) >= version.parse('1.4.0'):
    from sqlalchemy.engine import create
else:
    from sqlalchemy import engine as create

__all__ = ['AdminStats', 'Manager']


#Enum con tutte le statischiche che posso richiedere
class AdminStats(Enum):
    WIN = 1
    PLAYER = 2
    TIME = 3
    SCORE = 4
    TOT = 5


class Manager:
    engine: create

    def __init__(self, db_path):
        db_base_path = os.path.dirname(db_path)
        Path(db_base_path).mkdir(parents=True, exist_ok=True)
        sqlite_filepath = db_path
        self.engine = create_engine(f"sqlite:///{sqlite_filepath}")

    def cont_scores(self, team_members: [str], punteggio: int) -> [Scores]:
        session_maker = sessionmaker()
        session_maker.configure(bind=self.engine)
        session = session_maker()
        users: [Scores] = []

        for team_member in team_members:
            user = None
            try:
                user = (
                    session.query(Scores)
                        .filter(Scores.username == team_member)
                        .one_or_none()
                )
            except OperationalError:
                Scores.__table__.create(bind=self.engine, checkfirst=True)
                print("Tabella scores creata")

            if user is None:
                user = Scores(username=team_member, score=punteggio)
                session.add(user)
            else:
                user.score = user.score + punteggio

            users.append(user)
        session.commit()

        return users

    def cont_win(self, team_members: [str]) -> [Scores]:
        session_maker = sessionmaker()
        session_maker.configure(bind=self.engine)
        session = session_maker()
        users: [Scores] = []

        for team_member in team_members:
            user = None
            try:
                user = (
                    session.query(Scores)
                        .filter(Scores.username == team_member)
                        .one_or_none()
                )
            except OperationalError:
                Scores.__table__.create(bind=self.engine, checkfirst=True)
                print("Tabella scores creata")

            if user is None:
                user = Scores(username=team_member, win=1)
                session.add(user)
            else:
                user.win = user.win + 1

            users.append(user)
        session.commit()

        return users

    def cont_tot(self, team_members: [str]) -> [Scores]:
        session_maker = sessionmaker()
        session_maker.configure(bind=self.engine)
        session = session_maker()
        users: [Scores] = []

        for team_member in team_members:
            user = None
            try:
                user = (
                    session.query(Scores)
                        .filter(Scores.username == team_member)
                        .one_or_none()
                )
            except OperationalError:
                Scores.__table__.create(bind=self.engine, checkfirst=True)
                print("Tabella scores creata")

            if user is None:
                user = Scores(username=team_member, tot=1)
                session.add(user)
            else:
                user.tot = user.tot + 1

            users.append(user)
        session.commit()

        return users

    def cont_time(self, team_members: [str], hours: int = 0, minutes: int = 0, seconds: int = 0) -> [Scores]:
        session_maker = sessionmaker()
        session_maker.configure(bind=self.engine)
        session = session_maker()
        users: [Scores] = []
        time_played: int = (hours * 3600) + (minutes * 60) + seconds

        for team_member in team_members:
            user = None
            try:
                user = (
                    session.query(Scores)
                        .filter(Scores.username == team_member)
                        .one_or_none()
                )
            except OperationalError:
                Scores.__table__.create(bind=self.engine, checkfirst=True)
                print("Tabella scores creata")

            if user is None:
                user = Scores(username=team_member, time=time_played)
                session.add(user)
            else:
                user.time = user.time + time_played

            users.append(user)
        session.commit()

        return users

    def update_players(self, team_members: [str], win: bool = False, punteggio: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0) -> [Scores]:
        session_maker = sessionmaker()
        session_maker.configure(bind=self.engine)
        session = session_maker()
        users: [Scores] = []
        time_played: int = (hours * 3600) + (minutes * 60) + seconds
        win_value = 1 if win else 0

        for team_member in team_members:
            user = None
            try:
                user = (
                    session.query(Scores)
                        .filter(Scores.username == team_member)
                        .one_or_none()
                )
            except OperationalError:
                Scores.__table__.create(bind=self.engine, checkfirst=True)
                print("Tabella scores creata")

            if user is None:
                user = Scores(
                    username=team_member,
                    score=punteggio,
                    win=win_value,
                    tot=1,
                    time=time_played
                )
                session.add(user)
            else:
                user.score = user.score + punteggio
                user.win = user.win + win_value
                user.tot = user.tot + 1
                user.time = user.time + time_played

            users.append(user)
        session.commit()

        return users

    def delete_player(self, username: str) -> Scores:
        session_maker = sessionmaker()
        session_maker.configure(bind=self.engine)
        session = session_maker()
        user = (
            session.query(Scores)
                .filter(Scores.username == username)
                .one_or_none()
        )
        if user is not None:
            session.delete(user)
            session.commit()
        else:
            raise Exception("Giocatore non trovato")

        session.close()
        return user


    def get_user(self, username: str) -> Scores:
        session_maker = sessionmaker()
        session_maker.configure(bind=self.engine)
        session = session_maker()
        user = (
            session.query(Scores)
                .filter(Scores.username == username)
                .one_or_none()
        )
        session.close()
        return user

    @staticmethod
    def format_player_stat(score: Scores):
        result = StringIO()
        win_rate = 0 if score.tot == 0 else score.win / score.tot
        result.write(f"Dati del giocatore:\n")
        result.write(f"- Username: {score.username}\n")
        result.write(f"- Score: {score.score}\n")
        result.write(f"- Win: {score.win}\n")
        result.write(f"- Tot: {score.tot}\n")
        result.write(f"- Time: {score.time}\n")
        result.write(f"- Win Rate: {win_rate}\n")
        return result.getvalue()

    def show_stats(self, username: str) -> str:
        score = self.get_user(username)
        return self.format_player_stat(score)

    def show_stats_admin(self, stat: AdminStats, username: str = None, max_stats: int = 10) -> str:
        if stat == AdminStats.PLAYER and username is None:
            raise ValueError("Lo username deve essere specificato se vuoi conoscere le statistiche del player")

        result = StringIO()

        session_maker = sessionmaker()
        session_maker.configure(bind=self.engine)
        session = session_maker()

        i = 1
        if stat == AdminStats.WIN:
            stats = session.query(Scores.username, Scores.win).order_by(desc(Scores.win)).limit(max_stats).all()
            for stat in stats:
                result.write(f"{i}) {stat.username}- {stat.win}\n")
                i += 1
        elif stat == AdminStats.SCORE:
            stats = session.query(Scores.username, Scores.score).order_by(desc(Scores.score)).limit(max_stats).all()
            for stat in stats:
                result.write(f"{i}) {stat.username}- {stat.score}\n")
                i += 1
        elif stat == AdminStats.TIME:
            stats = session.query(Scores.username, Scores.time).order_by(desc(Scores.time)).limit(max_stats).all()
            for stat in stats:
                score_time = time.strftime('%H:%M:%S', time.gmtime(stat.time))
                result.write(f"{i}) {stat.username}- {score_time}\n")
                i += 1
        elif stat == AdminStats.TOT:
            stats = session.query(Scores.username, Scores.tot).order_by(desc(Scores.tot)).limit(max_stats).all()
            for stat in stats:
                result.write(f"{i}) {stat.username}- {stat.tot}\n")
                i += 1
        elif stat == AdminStats.PLAYER:
            score = self.get_user(username)
            if score is None:
                result.write(f"Non esiste nessun giocatore con il nome {username}")
            else:
                result.write(self.format_player_stat(score))
        else:
            raise ValueError(f"Statistica selezionata non corretta")
        session.close()
        return result.getvalue()
