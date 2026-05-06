from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Problem
import json

router = APIRouter()

SEED_PROBLEMS = [
    {
        "title": "Two Sum",
        "description": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.",
        "difficulty": "Easy",
        "constraints": "2 <= nums.length <= 10^4\n-10^9 <= nums[i] <= 10^9\n-10^9 <= target <= 10^9",
        "input_format": "First line: space-separated integers (the array)\nSecond line: the target integer",
        "output_format": "Two space-separated indices (0-based)",
        "sample_input": "2 7 11 15\n9",
        "sample_output": "0 1",
        "hidden_testcases": json.dumps([
            {"input": "2 7 11 15\n9", "output": "0 1"},
            {"input": "3 2 4\n6", "output": "1 2"},
            {"input": "3 3\n6", "output": "0 1"}
        ])
    },
    {
        "title": "Reverse a String",
        "description": "Given a string `s`, return the string reversed.\n\nDo not use built-in reverse functions.",
        "difficulty": "Easy",
        "constraints": "1 <= s.length <= 10^5\ns consists of printable ASCII characters",
        "input_format": "A single line containing the string",
        "output_format": "The reversed string on a single line",
        "sample_input": "hello",
        "sample_output": "olleh",
        "hidden_testcases": json.dumps([
            {"input": "hello", "output": "olleh"},
            {"input": "abcde", "output": "edcba"},
            {"input": "racecar", "output": "racecar"}
        ])
    },
    {
        "title": "Palindrome Check",
        "description": "Given a string, determine if it is a palindrome. A palindrome reads the same forwards and backwards. Ignore case and non-alphanumeric characters.",
        "difficulty": "Easy",
        "constraints": "1 <= s.length <= 2 * 10^5",
        "input_format": "A single line containing the string",
        "output_format": "Print 'true' if palindrome, 'false' otherwise",
        "sample_input": "A man a plan a canal Panama",
        "sample_output": "true",
        "hidden_testcases": json.dumps([
            {"input": "A man a plan a canal Panama", "output": "true"},
            {"input": "race a car", "output": "false"},
            {"input": "Was it a car or a cat I saw", "output": "true"}
        ])
    },
    {
        "title": "Fibonacci Sequence",
        "description": "Given a number `n`, print the first `n` Fibonacci numbers separated by spaces.\n\nThe Fibonacci sequence starts: 0, 1, 1, 2, 3, 5, 8, ...",
        "difficulty": "Easy",
        "constraints": "1 <= n <= 50",
        "input_format": "A single integer n",
        "output_format": "First n Fibonacci numbers separated by spaces",
        "sample_input": "7",
        "sample_output": "0 1 1 2 3 5 8",
        "hidden_testcases": json.dumps([
            {"input": "7", "output": "0 1 1 2 3 5 8"},
            {"input": "1", "output": "0"},
            {"input": "10", "output": "0 1 1 2 3 5 8 13 21 34"}
        ])
    },
    {
        "title": "Maximum Subarray",
        "description": "Given an integer array `nums`, find the subarray with the largest sum, and return its sum.\n\nThis is the classic Kadane's Algorithm problem.",
        "difficulty": "Medium",
        "constraints": "1 <= nums.length <= 10^5\n-10^4 <= nums[i] <= 10^4",
        "input_format": "Space-separated integers on one line",
        "output_format": "A single integer — the maximum subarray sum",
        "sample_input": "-2 1 -3 4 -1 2 1 -5 4",
        "sample_output": "6",
        "hidden_testcases": json.dumps([
            {"input": "-2 1 -3 4 -1 2 1 -5 4", "output": "6"},
            {"input": "1", "output": "1"},
            {"input": "5 4 -1 7 8", "output": "23"}
        ])
    },
    {
        "title": "Valid Parentheses",
        "description": "Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.\n\nAn input string is valid if:\n- Open brackets must be closed by the same type of brackets.\n- Open brackets must be closed in the correct order.",
        "difficulty": "Medium",
        "constraints": "1 <= s.length <= 10^4\ns consists of parentheses only '()[]{}'",
        "input_format": "A single string of bracket characters",
        "output_format": "Print 'true' if valid, 'false' otherwise",
        "sample_input": "()[]{}",
        "sample_output": "true",
        "hidden_testcases": json.dumps([
            {"input": "()[]{}","output": "true"},
            {"input": "(]", "output": "false"},
            {"input": "([)]", "output": "false"},
            {"input": "{[]}", "output": "true"}
        ])
    },
    {
        "title": "Binary Search",
        "description": "Given a sorted array of integers and a target value, return the index of the target. If the target is not in the array, return -1.\n\nYou must write an O(log n) solution.",
        "difficulty": "Medium",
        "constraints": "1 <= nums.length <= 10^4\n-10^4 <= nums[i], target <= 10^4\nAll values in nums are unique\nnums is sorted in ascending order",
        "input_format": "First line: space-separated sorted integers\nSecond line: the target integer",
        "output_format": "The 0-based index of target, or -1 if not found",
        "sample_input": "-1 0 3 5 9 12\n9",
        "sample_output": "4",
        "hidden_testcases": json.dumps([
            {"input": "-1 0 3 5 9 12\n9", "output": "4"},
            {"input": "-1 0 3 5 9 12\n2", "output": "-1"},
            {"input": "5\n5", "output": "0"}
        ])
    },
    {
        "title": "Longest Common Subsequence",
        "description": "Given two strings `text1` and `text2`, return the length of their longest common subsequence.\n\nA subsequence is a sequence that appears in the same relative order, but not necessarily contiguous.",
        "difficulty": "Hard",
        "constraints": "1 <= text1.length, text2.length <= 1000\ntext1 and text2 consist only of lowercase English characters",
        "input_format": "First line: text1\nSecond line: text2",
        "output_format": "A single integer — the length of the LCS",
        "sample_input": "abcde\nace",
        "sample_output": "3",
        "hidden_testcases": json.dumps([
            {"input": "abcde\nace", "output": "3"},
            {"input": "abc\nabc", "output": "3"},
            {"input": "abc\ndef", "output": "0"}
        ])
    },
    {
        "title": "Word Ladder",
        "description": "Given two words, `beginWord` and `endWord`, and a dictionary `wordList`, return the number of words in the shortest transformation sequence from beginWord to endWord.\n\nEvery adjacent pair of words must differ by exactly one letter. beginWord is not part of the sequence count.\n\nReturn 0 if no such sequence exists.",
        "difficulty": "Hard",
        "constraints": "1 <= beginWord.length <= 10\nendWord.length == beginWord.length\n1 <= wordList.length <= 5000",
        "input_format": "Line 1: beginWord\nLine 2: endWord\nLine 3: space-separated wordList",
        "output_format": "A single integer",
        "sample_input": "hit\ncog\nhot dot dog lot log cog",
        "sample_output": "5",
        "hidden_testcases": json.dumps([
            {"input": "hit\ncog\nhot dot dog lot log cog", "output": "5"},
            {"input": "hit\ncog\nhot dot dog lot log", "output": "0"}
        ])
    },
    {
        "title": "N-Queens",
        "description": "The n-queens puzzle is the problem of placing `n` queens on an `n x n` chessboard such that no two queens attack each other.\n\nGiven an integer `n`, return the number of distinct solutions to the n-queens puzzle.",
        "difficulty": "Hard",
        "constraints": "1 <= n <= 9",
        "input_format": "A single integer n",
        "output_format": "A single integer — the number of distinct solutions",
        "sample_input": "4",
        "sample_output": "2",
        "hidden_testcases": json.dumps([
            {"input": "1", "output": "1"},
            {"input": "4", "output": "2"},
            {"input": "8", "output": "92"}
        ])
    },
]


def seed_problems(db: Session):
    if db.query(Problem).count() == 0:
        for p in SEED_PROBLEMS:
            db.add(Problem(**p))
        db.commit()


@router.get("/problems")
def list_problems(db: Session = Depends(get_db)):
    seed_problems(db)
    problems = db.query(Problem).all()
    return [
        {
            "id": p.id,
            "title": p.title,
            "difficulty": p.difficulty,
        }
        for p in problems
    ]


@router.get("/problem/{problem_id}")
def get_problem(problem_id: int, db: Session = Depends(get_db)):
    seed_problems(db)
    p = db.query(Problem).filter(Problem.id == problem_id).first()
    if not p:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Problem not found")
    return {
        "id": p.id,
        "title": p.title,
        "description": p.description,
        "difficulty": p.difficulty,
        "constraints": p.constraints,
        "input_format": p.input_format,
        "output_format": p.output_format,
        "sample_input": p.sample_input,
        "sample_output": p.sample_output,
    }
