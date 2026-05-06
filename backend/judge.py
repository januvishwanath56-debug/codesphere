import subprocess
import tempfile
import os
import time
import json

TIMEOUT = 10  # seconds
MEMORY_LIMIT = "128m"
CPU_QUOTA = "50000"  # 50% of one CPU

DOCKER_IMAGES = {
    "python": "codesphere-python",
    "cpp": "codesphere-cpp",
    "java": "codesphere-java",
}

FILE_NAMES = {
    "python": "solution.py",
    "cpp": "solution.cpp",
    "java": "Solution.java",
}

RUN_COMMANDS = {
    "python": "python3 solution.py",
    "cpp": "g++ -O2 -o solution solution.cpp && ./solution",
    "java": "javac Solution.java && java Solution",
}


def run_code(language: str, code: str, stdin_input: str = "") -> dict:
    """
    Execute code in a Docker container and return result.
    Falls back to direct execution if Docker is unavailable (dev mode).
    """
    try:
        return _run_in_docker(language, code, stdin_input)
    except Exception as e:
        # Fallback for development/testing without Docker
        return _run_direct(language, code, stdin_input)


def _run_in_docker(language: str, code: str, stdin_input: str) -> dict:
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = FILE_NAMES[language]
        filepath = os.path.join(tmpdir, filename)

        with open(filepath, "w") as f:
            f.write(code)

        cmd = [
    "docker", "run",
    "-i",
    "--rm",
    "--network", "none",
    "--memory", MEMORY_LIMIT,
    "--cpu-quota", CPU_QUOTA,
    "--cpu-period", "100000",
    "--pids-limit", "50",
    "--read-only",
    "--tmpfs", "/tmp:size=32m",
    # "-v", f"{tmpdir}:/code:ro",
    "-v", f"{tmpdir}:/code",
    "-w", "/code",
    DOCKER_IMAGES[language],
    "sh", "-c", RUN_COMMANDS[language]
]

        start_time = time.time()
        try:
            result = subprocess.run(
                cmd,
                input=stdin_input,
                capture_output=True,
                text=True,
                timeout=TIMEOUT
            )
            elapsed = round(time.time() - start_time, 3)

            if result.returncode != 0:
                stderr = result.stderr.strip()
                if "error" in stderr.lower() or "Error" in stderr:
                    return {"status": "Compilation Error", "output": stderr, "time": elapsed}
                return {"status": "Runtime Error", "output": stderr, "time": elapsed}

            return {"status": "OK", "output": result.stdout.strip(), "time": elapsed}

        except subprocess.TimeoutExpired:
            return {"status": "Time Limit Exceeded", "output": "", "time": TIMEOUT}


def _run_direct(language: str, code: str, stdin_input: str) -> dict:
    """Direct execution fallback for development mode (no Docker)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = FILE_NAMES[language]
        filepath = os.path.join(tmpdir, filename)

        with open(filepath, "w") as f:
            f.write(code)

        start_time = time.time()

        try:
            if language == "python":
                cmd = ["python3", filepath]
            elif language == "cpp":
                out_path = os.path.join(tmpdir, "solution")
                compile_result = subprocess.run(
                    ["g++", "-O2", "-o", out_path, filepath],
                    capture_output=True, text=True, timeout=30
                )
                if compile_result.returncode != 0:
                    return {"status": "Compilation Error", "output": compile_result.stderr.strip(), "time": 0}
                cmd = [out_path]
            elif language == "java":
                compile_result = subprocess.run(
                    ["javac", filepath],
                    capture_output=True, text=True, timeout=30, cwd=tmpdir
                )
                if compile_result.returncode != 0:
                    return {"status": "Compilation Error", "output": compile_result.stderr.strip(), "time": 0}
                cmd = ["java", "-cp", tmpdir, "Solution"]

            result = subprocess.run(
                cmd,
                input=stdin_input,
                capture_output=True,
                text=True,
                timeout=TIMEOUT
            )
            elapsed = round(time.time() - start_time, 3)

            if result.returncode != 0:
                return {"status": "Runtime Error", "output": result.stderr.strip(), "time": elapsed}

            return {"status": "OK", "output": result.stdout.strip(), "time": elapsed}

        except subprocess.TimeoutExpired:
            return {"status": "Time Limit Exceeded", "output": "", "time": TIMEOUT}
        except FileNotFoundError as e:
            return {"status": "Runtime Error", "output": f"Interpreter not found: {str(e)}", "time": 0}


def judge_submission(language: str, code: str, test_cases: list) -> dict:
    """
    Run code against all hidden test cases and return verdict.
    test_cases: [{"input": "...", "output": "..."}, ...]
    """
    for i, tc in enumerate(test_cases):
        result = run_code(language, code, tc["input"])

        if result["status"] != "OK":
            return {
                "verdict": result["status"],
                "passed": i,
                "total": len(test_cases),
                "execution_time": result["time"],
                "output": result["output"]
            }

        expected = tc["output"].strip()
        actual = result["output"].strip()

        if actual != expected:
            return {
                "verdict": "Wrong Answer",
                "passed": i,
                "total": len(test_cases),
                "execution_time": result["time"],
                "output": actual
            }

    return {
        "verdict": "Accepted",
        "passed": len(test_cases),
        "total": len(test_cases),
        "execution_time": result["time"],
        "output": ""
    }
