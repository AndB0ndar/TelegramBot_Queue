from __future__ import annotations
from sqlalchemy import create_engine, DateTime, func, Boolean, Float, PickleType, desc
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, backref, Query, Mapped, mapped_column, \
    DeclarativeBase
from typing import List
from sqlalchemy import or_, and_
import psycopg2
Base = declarative_base()


class Queue(Base):
    __tablename__ = 'queue_table'
    id = mapped_column(Integer, primary_key=True)
    children = relationship("Place", back_populates="parent")
    name = Column(String)

    def __int__(self, name):
        self.name = name


class Place(Base):
    __tablename__ = 'place_table'
    id = mapped_column(Integer, primary_key=True)
    queue_id = mapped_column(ForeignKey("queue_table.id"))
    parent = relationship("Queue", back_populates="children")
    user_id = Column(Integer)
    place = Column(Integer)

    def __int__(self, queue_id, user_id, place):
        self.user_id = user_id
        self.queue_id = queue_id
        self.place = place


class QueueHandler(object):

    def __init__(self):
        self.meta = MetaData()
        self.engine = create_engine('postgresql+psycopg2://postgres:postgres@postgres:5432/queue')
        # self.engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5433/Queue')
        Base.metadata.create_all(self.engine)
    def create_queue(self, name):
        session = sessionmaker(bind=self.engine)()
        lst = session.query(Queue).filter(Queue.name == name).first()
        if lst is None:
            queue = Queue(name=name)
            session.add(queue)
            session.flush()
            queue_id = queue.id
            session.commit()
            session.close()
            return queue_id
        else:
            session.close()
            return False

    def get_last_place(self, session, q_id):
        lst = session.query(Place).filter(Place.queue_id == q_id).all()
        if lst:
            return max([x.place for x in lst]+1)
        else:
            return 0

    def connect_by_name(self, name, user_id):
        session = sessionmaker(bind=self.engine)()
        q = session.query(Queue).filter(Queue.name == name).first()
        if q is not None:
            check = session.query(Place).filter(Place.queue_id==q.id,Place.user_id==user_id).first()
            if check is None:
                place = Place(queue_id=q.id, user_id=user_id, place=self.get_last_place(session, q.id))
                session.add(place)
                session.commit()
                session.close()
                return True
            else:
                session.close()
                return False
        else:
            session.close()
            return False

    def connect_by_id(self, q_id, user_id):
        session = sessionmaker(bind=self.engine)()
        q = session.query(Queue).filter(Queue.id == q_id).first()
        if q is not None:
            place = Place(par_id=q.id, user_id=user_id, plase=self.get_last_place(session, q.id))
            session.add(place)
            session.commit()
            session.close()
            return True
        else:
            session.close()
            return False

    # def refresh_queue(self, q_id):

    def disconnect_by_id(self, q_id, user_id):
        session = sessionmaker(bind=self.engine)()
        q = session.query(Queue).filter(Queue.id == q_id).first()
        if q is not None:
            place = session.query(Place).filter(Place.queue_id == q_id, Place.user_id == user_id).first()
            if place is not None:
                session.delete(place)
                session.commit()
                session.close()
                return True
            else:
                session.close()
                return False
        else:
            session.close()
            return False

    def disconnect_by_name(self, name, user_id):
        session = sessionmaker(bind=self.engine)()
        q = session.query(Queue).filter(Queue.name == name).first()
        if q is not None:
            place = session.query(Place).filter(Place.queue_id == q.id, Place.user_id == user_id).first()
            if place is not None:
                session.delete(place)
                session.commit()
                session.close()
                # refresh()
                return True
            else:
                session.close()
                return False
        else:
            session.close()
            return False

    def info_by_id(self, q_id, user_id):
        session = sessionmaker(bind=self.engine)()
        q = session.query(Queue).filter(Queue.id == q_id).first()
        if q is not None:
            info_lst = session.query(Place).filter(Place.queue_id == q.id, Place.user_id==user_id).first()
            if info_lst is not None:
                session.close()
                return info_lst.place
            else:
                session.close()
                return False
        else:
            session.close()
            return False

    def info_by_name(self, q_name, user_id):
        session = sessionmaker(bind=self.engine)()
        q = session.query(Queue).filter(Queue.name == q_name).first()
        if q is not None:
            info_lst = session.query(Place).filter(Place.queue_id == q.id, Place.user_id == user_id).first()
            if info_lst is not None:
                session.close()
                return info_lst.place
            else:
                session.close()
                return False
        else:
            session.close()
            return False


if __name__ == "__main__":
    q = QueueHandler()
    print(q.create_queue("joan"))
