"""Interactive local web viewer server for Zecpath AI Day 4 Data Structuring.

Serves an interactive dashboard at http://localhost:8000 allowing candidates,
supervisors, and engineers to visually explore raw resumes vs structured AI JSON,
test real-time schema validation, and inspect entity design architecture.
"""

from __future__ import annotations

import http.server
import json
import socketserver
import sys
import webbrowser
from pathlib import Path

# Ensure repository root is on sys.path
repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from jsonschema import Draft202012Validator

from parsers.models import CandidateProfile, JobProfile

PORT = 8000
WEB_DIR = repo_root / "web_viewer"
BASE_DATA = repo_root / "data"


class ZecpathViewerHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler serving the static dashboard and Day 4 data APIs."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def do_GET(self) -> None:  # noqa: N802
        """Handle GET requests for static files and REST endpoints."""
        if self.path == "/api/data":
            self._serve_full_dataset()
        elif self.path == "/api/schemas":
            self._serve_schemas()
        elif self.path == "/api/extracted":
            self._serve_extracted_data()
        else:
            super().do_GET()

    def _serve_full_dataset(self) -> None:
        """Return all 10 resumes, 4 JDs, raw text, and structured data with validation status."""
        resume_schema_path = BASE_DATA / "schemas" / "resume_schema.json"
        jd_schema_path = BASE_DATA / "schemas" / "job_description_schema.json"

        resume_validator = None
        if resume_schema_path.exists():
            r_schema = json.loads(resume_schema_path.read_text(encoding="utf-8"))
            resume_validator = Draft202012Validator(r_schema)

        jd_validator = None
        if jd_schema_path.exists():
            j_schema = json.loads(jd_schema_path.read_text(encoding="utf-8"))
            jd_validator = Draft202012Validator(j_schema)

        resumes = []
        raw_resumes_dir = BASE_DATA / "raw" / "resumes"
        struct_resumes_dir = BASE_DATA / "structured" / "resumes"

        for json_path in sorted(struct_resumes_dir.glob("*.json")):
            raw_path = raw_resumes_dir / json_path.name.replace(".json", ".txt")
            raw_content = raw_path.read_text(encoding="utf-8") if raw_path.exists() else ""
            struct_content = json.loads(json_path.read_text(encoding="utf-8"))

            is_valid = True
            error_msg = None
            if resume_validator:
                errors = list(resume_validator.iter_errors(struct_content))
                if errors:
                    is_valid = False
                    error_msg = errors[0].message

            try:
                profile = CandidateProfile.model_validate(struct_content)
                candidate_name = profile.contact_info.full_name
                domain = profile.domain
                experience_years = profile.total_experience_years
                skills_count = len(profile.skills)
            except Exception as e:
                is_valid = False
                error_msg = str(e)
                candidate_name = "Unknown"
                domain = "General"
                experience_years = 0.0
                skills_count = 0

            resumes.append({
                "id": json_path.stem,
                "file_name": json_path.name,
                "candidate_name": candidate_name,
                "domain": domain,
                "experience_years": experience_years,
                "skills_count": skills_count,
                "is_valid": is_valid,
                "error": error_msg,
                "raw_text": raw_content,
                "structured_json": struct_content,
            })

        jobs = []
        raw_jds_dir = BASE_DATA / "raw" / "job_descriptions"
        struct_jds_dir = BASE_DATA / "structured" / "job_descriptions"

        for json_path in sorted(struct_jds_dir.glob("*.json")):
            raw_path = raw_jds_dir / json_path.name.replace(".json", ".txt")
            raw_content = raw_path.read_text(encoding="utf-8") if raw_path.exists() else ""
            struct_content = json.loads(json_path.read_text(encoding="utf-8"))

            is_valid = True
            error_msg = None
            if jd_validator:
                errors = list(jd_validator.iter_errors(struct_content))
                if errors:
                    is_valid = False
                    error_msg = errors[0].message

            try:
                job = JobProfile.model_validate(struct_content)
                title = job.title
                company = job.company_name
                role_type = job.role_type.value
                min_exp = job.requirements.minimum_experience_years
                req_skills_count = len(job.requirements.required_skills)
            except Exception as e:
                is_valid = False
                error_msg = str(e)
                title = "Unknown"
                company = "Unknown"
                role_type = "TECHNICAL"
                min_exp = 0.0
                req_skills_count = 0

            jobs.append({
                "id": json_path.stem,
                "file_name": json_path.name,
                "title": title,
                "company": company,
                "role_type": role_type,
                "min_exp": min_exp,
                "req_skills_count": req_skills_count,
                "is_valid": is_valid,
                "error": error_msg,
                "raw_text": raw_content,
                "structured_json": struct_content,
            })

        response_data = {
            "status": "success",
            "resumes_count": len(resumes),
            "jobs_count": len(jobs),
            "all_valid": all(r["is_valid"] for r in resumes) and all(j["is_valid"] for j in jobs),
            "resumes": resumes,
            "jobs": jobs,
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(response_data, indent=2).encode("utf-8"))

    def _serve_schemas(self) -> None:
        """Return raw JSON schemas."""
        resume_schema_path = BASE_DATA / "schemas" / "resume_schema.json"
        jd_schema_path = BASE_DATA / "schemas" / "job_description_schema.json"

        data = {
            "resume_schema": json.loads(resume_schema_path.read_text(encoding="utf-8")) if resume_schema_path.exists() else {},
            "job_schema": json.loads(jd_schema_path.read_text(encoding="utf-8")) if jd_schema_path.exists() else {},
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def _serve_extracted_data(self) -> None:
        """Return all cleaned text and extraction metadata from data/extracted/."""
        extracted_dir = BASE_DATA / "extracted"
        items = []

        for json_file in sorted(extracted_dir.glob("*_extracted.json")):
            try:
                meta = json.loads(json_file.read_text(encoding="utf-8"))
                items.append(meta)
            except Exception:
                pass

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "success", "count": len(items), "items": items}, indent=2).encode("utf-8"))


def start_server() -> None:
    """Launch the HTTP server and open default browser."""
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    server_address = ("", PORT)

    class ReusableTCPServer(socketserver.TCPServer):
        allow_reuse_address = True

    try:
        with ReusableTCPServer(server_address, ZecpathViewerHandler) as httpd:
            url = f"http://localhost:{PORT}"
            print("\n" + "=" * 70)
            print("  ZECPATH AI -- DAY 4 DATA STRUCTURING WEB VIEWER")
            print("=" * 70)
            print(f"  Live Dashboard Running at: {url}")
            print("  Serving 10 Multi-Domain Resumes & 4 Job Descriptions")
            print("  Press Ctrl+C to stop the server.")
            print("=" * 70 + "\n")

            try:
                webbrowser.open(url)
            except Exception:
                pass

            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Viewer server stopped.")
    except OSError as e:
        if "address already in use" in str(e).lower() or "10048" in str(e):
            print(f"\n[WARNING] Port {PORT} is currently in use. Trying port {PORT + 1}...")
            # Try alternate port
            with ReusableTCPServer(("", PORT + 1), ZecpathViewerHandler) as httpd:
                url = f"http://localhost:{PORT + 1}"
                print(f"  Live Dashboard Running at: {url}")
                webbrowser.open(url)
                httpd.serve_forever()
        else:
            raise e


if __name__ == "__main__":
    start_server()
