from sqlalchemy import Text, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import event
from .base import Base


class Info_user(Base):
    __tablename__ = "info_user"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_name: Mapped[str] = mapped_column(Text, nullable=True)
    payments: Mapped[bool] = mapped_column(Boolean, default=False)


class Quiz_user(Base):
    __tablename__ = "quiz_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    user_name: Mapped[str] = mapped_column(Text, nullable=True)
    answer_opros: Mapped[str] = mapped_column(Text, nullable=True)




class Passed_user(Base):
    __tablename__ = "Passed_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    friend_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    user_name: Mapped[str] = mapped_column(Text, nullable=True)
    result_user: Mapped[int] = mapped_column(BigInteger, nullable=True)





# @event.listens_for(Quiz_user, "after_insert")
# def create_passed_user(mapper, connection, target: Quiz_user):
#     stmt = Passed_user.__table__.insert().values(friend_id=target.user_id,
#                                                  user_id=0,
#                                                  user_name="Null",
#                                                  result_user=0)
#     connection.execute(stmt)

@event.listens_for(Quiz_user, "after_delete")
def delete_passed_user(mapper, connection, target: Quiz_user):
    stmt = Passed_user.__table__.delete().where(Passed_user.friend_id == target.user_id)
    connection.execute(stmt)
