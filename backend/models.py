from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    submissions = relationship("Submission", back_populates="user")


class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(String(10), nullable=False)  # Easy, Medium, Hard
    constraints = Column(Text)
    input_format = Column(Text)
    output_format = Column(Text)
    sample_input = Column(Text)
    sample_output = Column(Text)
    hidden_testcases = Column(Text)  # JSON string of [{input, output}, ...]

    submissions = relationship("Submission", back_populates="problem")


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    language = Column(String(20), nullable=False)
    code = Column(Text, nullable=False)
    verdict = Column(String(30), nullable=False)
    execution_time = Column(Float, nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="submissions")
    problem = relationship("Problem", back_populates="submissions")


class PlaygroundRun(Base):
    __tablename__ = "playground_runs"

    id = Column(Integer, primary_key=True, index=True)
    language = Column(String(20), nullable=False)
    code = Column(Text, nullable=False)
    output = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
