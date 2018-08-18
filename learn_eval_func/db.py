# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.types import Float, String, Boolean
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_engine('sqlite:///db.sqlite3', echo=False)
metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
session = Session()


class Board(Base):
    __tablename__ = 'board'
    vec = Column(String(29), primary_key=True)
    score = Column(Float, nullable=False)
    searched = Column(Boolean, nullable=False)


class Move(Base):
    __tablename__ = 'move'
    parent_vec = Column(String(29),
                        ForeignKey('board.vec', onupdate='CASCADE', ondelete='CASCADE'))
    child_vec = Column(String(29),
                       ForeignKey('board.vec', onupdate='CASCADE', ondelete='CASCADE'))
    PrimaryKeyConstraint(parent_vec, child_vec)


Base.metadata.create_all(bind=engine)


def add_board(boards):
    q = session.query(Board)
    q = q.filter(Board.vec.in_(boards))
    d = {b.vec: b for b in q}
    for vec, (score, searched) in boards.items():
        if vec not in d:
            n = Board()
            n.vec = vec
        elif not searched:
            continue
        else:
            n = d[vec]
        n.score = score
        n.searched = searched
        session.add(n)


def add_move(moves):
    q = session.query(Move)
    for v1, v2 in moves:
        if q.filter(Move.parent_vec == v1, Move.child_vec == v2).first():
            continue
        m = Move()
        m.parent_vec = v1
        m.child_vec = v2
        session.add(m)
