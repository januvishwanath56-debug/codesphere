from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import Submission, Problem, PlaygroundRun
from routes.auth import get_current_user
from models import User
import judge as judge_engine
import json

router = APIRouter()


class RunRequest(BaseModel):
    language: str
    code: str
    stdin: Optional[str] = ""


class SubmitRequest(BaseModel):
    problem_id: int
    language: str
    code: str


@router.post("/run")
def run_code(req: RunRequest, db: Session = Depends(get_db)):
    if req.language not in ["python", "cpp", "java"]:
        raise HTTPException(status_code=400, detail="Unsupported language")

    result = judge_engine.run_code(req.language, req.code, req.stdin or "")

    # Save playground run
    run = PlaygroundRun(
        language=req.language,
        code=req.code,
        output=result.get("output", "")
    )
    db.add(run)
    db.commit()

    return {
        "status": result["status"],
        "output": result["output"],
        "execution_time": result.get("time", 0)
    }


@router.post("/submit")
def submit_code(
    req: SubmitRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    if req.language not in ["python", "cpp", "java"]:
        raise HTTPException(status_code=400, detail="Unsupported language")

    problem = db.query(Problem).filter(Problem.id == req.problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    test_cases = json.loads(problem.hidden_testcases)
    result = judge_engine.judge_submission(req.language, req.code, test_cases)

    submission = Submission(
        user_id=current_user.id if current_user else None,
        problem_id=req.problem_id,
        language=req.language,
        code=req.code,
        verdict=result["verdict"],
        execution_time=result.get("execution_time", 0)
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    return {
        "submission_id": submission.id,
        "verdict": result["verdict"],
        "passed": result["passed"],
        "total": result["total"],
        "execution_time": result.get("execution_time", 0)
    }


@router.get("/result/{submission_id}")
def get_result(submission_id: int, db: Session = Depends(get_db)):
    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")

    return {
        "id": sub.id,
        "problem_id": sub.problem_id,
        "language": sub.language,
        "verdict": sub.verdict,
        "execution_time": sub.execution_time,
        "submitted_at": sub.submitted_at
    }


@router.get("/submissions")
def get_my_submissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Login required")

    subs = (
        db.query(Submission)
        .filter(Submission.user_id == current_user.id)
        .order_by(Submission.submitted_at.desc())
        .limit(50)
        .all()
    )

    return [
        {
            "id": s.id,
            "problem_id": s.problem_id,
            "problem_title": s.problem.title if s.problem else "Unknown",
            "language": s.language,
            "verdict": s.verdict,
            "execution_time": s.execution_time,
            "submitted_at": s.submitted_at,
        }
        for s in subs
    ]
