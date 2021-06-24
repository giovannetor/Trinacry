from __future__ import annotations

from packaging import version
from sqlalchemy import Column, Integer, String
from sqlalchemy import __version__ as sqlav


__all__ = ['Scores']

if version.parse(sqlav) >= version.parse('1.4.0'):
    from dataclasses import dataclass
    from dataclasses import field

    from sqlalchemy.orm import registry
    mapper_registry = registry()


    @mapper_registry.mapped
    @dataclass
    class Scores:
        __tablename__ = "score"

        __sa_dataclass_metadata_key__ = "sa"

        username: str = field(
            init=True, metadata={"sa": Column(String(250), primary_key=True)}
        )
        score: int = field(default=0, metadata={"sa": Column(Integer)})
        win: int = field(default=0, metadata={"sa": Column(Integer)})
        tot: int = field(default=0, metadata={"sa": Column(Integer)})
        time: int = field(default=0, metadata={"sa": Column(Integer)})
else:
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class Scores(Base):
        __tablename__ = "score"
        username = Column(String(250), primary_key=True)
        score = Column(Integer, default=0)
        win = Column(Integer, default=0)
        tot = Column(Integer, default=0)
        time = Column(Integer, default=0)

        def __init__(self, username: str, score: int = 0, win: int = 0, tot: int = 0, time: int = 0):
            self.username = username
            self.score = score
            self.win = win
            self.tot = tot
            self.time = time

        def __repr__(self):
            return f"Scores(username= {self.username}, score= {self.score}, win= {self.win}, " \
                   f"tot= {self.tot}, time= {self.time})"
