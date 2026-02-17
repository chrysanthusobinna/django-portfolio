"""
VertexAICVExtractor – calls Google Vertex AI API (Gemini)
to extract structured CV data from plain text.

Usage:
    from portfolio_app.vertex_ai_cv_extractor import VertexAICVExtractor

    extractor = VertexAICVExtractor()
    parsed_data = extractor.extract(cv_text)
"""

import json
import logging
import re
import time
import uuid
from typing import Dict, Any, Optional

try:
    from vertexai.preview.generative_models import GenerativeModel, Part
    from vertexai import init as vertexai_init
    HAS_VERTEXAI = True
except ImportError:
    try:
        # Fallback to older import path
        from vertexai.language_models import TextGenerationModel
        from vertexai import init as vertexai_init
        HAS_VERTEXAI = True
        USE_LEGACY_API = True
    except ImportError:
        HAS_VERTEXAI = False
        USE_LEGACY_API = False

from django.conf import settings

logger = logging.getLogger(__name__)

# ---------- Vertex AI system / user prompts ----------

SYSTEM_PROMPT = (
    "You are a CV-to-JSON extractor.\n\n"
    "RULES:\n"
    "- Output MUST be valid JSON only. No markdown. No extra text. No code fences.\n"
    "- Do NOT hallucinate. If information is missing, use null or [].\n"
    "- Keep descriptions concise.\n"
    "- Normalize dates to \"YYYY-MM-DD\" when possible. "
    "If only a year is present, use \"YYYY-01-01\". If unknown, null.\n"
    "- For phone numbers keep the original format from the CV.\n"
    "- For LinkedIn provide the full URL (https://linkedin.com/in/...).\n\n"
    "Return this EXACT JSON schema (no additional keys):\n"
    "{\n"
    '  "contact": {"email_address": null, "phone_number": null, "linkedin": null},\n'
    '  "country": null,\n'
    '  "address": null,\n'
    '  "about": null,\n'
    '  "employment": [\n'
    '    {"employer_name": null, "job_title": null, "description_of_duties": null, '
    '"start_date": null, "end_date": null}\n'
    "  ],\n"
    '  "education": [\n'
    '    {"qualification": null, "institution_name": null, '
    '"start_date": null, "end_date": null}\n'
    "  ],\n"
    '  "certifications": [\n'
    '    {"name": null, "issuer": null, "date_issued": null}\n'
    "  ],\n"
    '  "projects": [\n'
    '    {"title": null, "description": null, "link": null}\n'
    "  ]\n"
    "}\n"
)

USER_PROMPT_TEMPLATE = (
    "Extract structured data from the following CV text and return ONLY "
    "valid JSON matching the schema above.\n\n"
    "--- CV TEXT START ---\n{cv_text}\n--- CV TEXT END ---"
)

# Stricter retry prompt used when the first attempt returns invalid JSON.
RETRY_SYSTEM_PROMPT = (
    "You previously failed to return valid JSON. "
    "This time you MUST return ONLY raw JSON — "
    "absolutely no markdown, no backticks, no commentary. "
    "Use double quotes for all keys and string values. "
    "Follow the schema exactly.\n\n" + SYSTEM_PROMPT
)

# ---------- Validation helpers ----------

EMAIL_RE = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)
PHONE_RE = re.compile(
    r"^(\+?\d{1,4}[\s\-.]?)?\(?\d{1,5}\)?[\s\-.]?\d{1,5}[\s\-.]?\d{1,9}$"
)
LINKEDIN_RE = re.compile(
    r"https?://(www\.)?linkedin\.com/in/[\w\-]+/?$", re.IGNORECASE
)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _validate_field(value, regex):
    """Return value if it matches regex, else None."""
    if value and regex.match(str(value).strip()):
        return str(value).strip()
    return None


def _normalize_date(raw):
    """
    Best-effort normalise a date string to YYYY-MM-DD.
    Accepts YYYY-MM-DD, YYYY/MM/DD, YYYY, etc.
    Returns None if not parseable.
    """
    if not raw:
        return None
    raw = str(raw).strip()
    if DATE_RE.match(raw):
        return raw
    # Only year
    year_match = re.match(r"^(\d{4})$", raw)
    if year_match:
        return f"{year_match.group(1)}-01-01"
    # Slash variant
    slash = re.match(r"^(\d{4})/(\d{1,2})/(\d{1,2})$", raw)
    if slash:
        return f"{slash.group(1)}-{int(slash.group(2)):02d}-{int(slash.group(3)):02d}"
    # Try dateutil as last resort
    try:
        from dateutil import parser as date_parser
        dt = date_parser.parse(raw, fuzzy=True)
        return dt.strftime("%Y-%m-%d")
    except Exception:
        pass
    # Extract just year
    y = re.search(r"\b(19|20)\d{2}\b", raw)
    if y:
        return f"{y.group()}-01-01"
    return None


def _dedup_dicts(items, keys):
    """Remove duplicate dicts based on a subset of keys."""
    seen = set()
    unique = []
    for item in items:
        sig = tuple(str(item.get(k, "")).lower().strip() for k in keys)
        if sig not in seen:
            seen.add(sig)
            unique.append(item)
    return unique


# ---------- Main extractor class ----------

class VertexAICVExtractor:
    """
    Calls Google Vertex AI API with Gemini model to extract structured CV data.

    Settings required:
        VERTEXAI_PROJECT_ID  – set via env var or django settings.
        VERTEXAI_LOCATION    – set via env var or django settings (default: us-central1).
        GOOGLE_APPLICATION_CREDENTIALS – path to service account key file.

    Example:
        >>> extractor = VertexAICVExtractor()
        >>> data = extractor.extract("John Doe\\nSoftware Engineer...")
        >>> print(data["contact"]["email_address"])
    """

    MODEL = "gemini-1.5-flash"
    TIMEOUT = 60  # seconds

    def __init__(self, project_id=None, location=None):
        if not HAS_VERTEXAI:
            raise ImportError(
                "Vertex AI libraries not installed. "
                "Install with: pip install google-cloud-aiplatform"
            )

        self.project_id = project_id or getattr(settings, "VERTEXAI_PROJECT_ID", None)
        self.location = location or getattr(settings, "VERTEXAI_LOCATION", "us-central1")
        self.use_legacy_api = globals().get("USE_LEGACY_API", False)
        
        if not self.project_id:
            raise ValueError(
                "VERTEXAI_PROJECT_ID is not configured. "
                "Set it in env.py / environment variables."
            )

        # Initialize Vertex AI
        try:
            vertexai_init(project=self.project_id, location=self.location)
            if not self.use_legacy_api:
                # Use gemini-2.5-flash-lite as suggested
                self.model = GenerativeModel("gemini-2.5-flash-lite")
            else:
                self.model = TextGenerationModel.from_pretrained("text-bison@002")
        except Exception as exc:
            logger.error("Failed to initialize Vertex AI: %s", exc)
            raise ValueError(f"Vertex AI initialization failed: {exc}")

    # ---- public API ----

    def extract(self, cv_text: str) -> Optional[Dict[str, Any]]:
        """
        Send CV text to Vertex AI and return validated parsed_data dict.
        Returns None only if every attempt (including retry) fails.
        """
        request_id = uuid.uuid4().hex[:10]
        logger.info("[%s] Starting Vertex AI CV extraction (model=%s)", request_id, self.MODEL)

        # --- First attempt ---
        t0 = time.time()
        raw_json = self._call_vertex_ai(cv_text, SYSTEM_PROMPT, request_id)
        elapsed = time.time() - t0
        logger.info("[%s] Vertex AI responded in %.2fs", request_id, elapsed)

        parsed = self._parse_json(raw_json, request_id)

        # --- Retry once with stricter prompt ---
        if parsed is None:
            logger.warning("[%s] First attempt returned invalid JSON – retrying", request_id)
            t0 = time.time()
            raw_json = self._call_vertex_ai(cv_text, RETRY_SYSTEM_PROMPT, request_id)
            elapsed = time.time() - t0
            logger.info("[%s] Vertex AI retry responded in %.2fs", request_id, elapsed)
            parsed = self._parse_json(raw_json, request_id)

        if parsed is None:
            logger.error("[%s] Vertex AI failed after retry – falling back to regex parser", request_id)
            return None  # caller should fall back

        # --- Validate & normalise ---
        validated = self._validate_and_normalise(parsed, request_id)
        return validated

    # ---- internal helpers ----

    def _call_vertex_ai(self, cv_text: str, system_prompt: str, req_id: str) -> Optional[str]:
        """
        Call Vertex AI API and return the raw text from the response.
        """
        try:
            # Combine system prompt and user prompt
            full_prompt = f"{system_prompt}\n\n{USER_PROMPT_TEMPLATE.format(cv_text=cv_text)}"
            
            if not self.use_legacy_api:
                # New GenerativeModel API (using gemini)
                response = self.model.generate_content(
                    full_prompt,
                    generation_config={
                        "temperature": 0.1,
                        "max_output_tokens": 8192,
                    }
                )
                
                # Extract text from response
                if response and response.candidates and len(response.candidates) > 0:
                    candidate = response.candidates[0]
                    if candidate.content and candidate.content.parts:
                        return candidate.content.parts[0].text
            else:
                # Legacy Text Generation API
                response = self.model.predict(
                    full_prompt,
                    temperature=0.1,
                    max_output_tokens=8192,
                )
                
                if response and hasattr(response, 'text'):
                    return response.text
            
            logger.error("[%s] Vertex AI returned no response", req_id)
            return None

        except Exception as exc:
            logger.error("[%s] Vertex AI API error: %s", req_id, exc)
            return None

    def _parse_json(self, raw: Optional[str], req_id: str) -> Optional[Dict[str, Any]]:
        """Try to parse raw text as JSON. Strip markdown fences if present."""
        if not raw:
            return None
        # Strip markdown code fences just in case
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
            cleaned = re.sub(r"\s*```$", "", cleaned)
        try:
            data = json.loads(cleaned)
            if isinstance(data, dict):
                return data
            logger.warning("[%s] Vertex AI JSON is not a dict", req_id)
            return None
        except json.JSONDecodeError as exc:
            logger.warning("[%s] JSON parse error: %s", req_id, exc)
            return None

    def _validate_and_normalise(self, data: Dict[str, Any], req_id: str) -> Dict[str, Any]:
        """Validate fields, normalise dates, de-duplicate lists."""
        result = {
            "contact": {},
            "country": None,
            "address": None,
            "about": None,
            "employment": [],
            "education": [],
            "certifications": [],
            "projects": [],
        }

        # --- Contact ---
        contact_raw = data.get("contact") or {}
        result["contact"] = {
            "email_address": _validate_field(
                contact_raw.get("email_address"), EMAIL_RE
            ),
            "phone_number": (
                str(contact_raw["phone_number"]).strip()
                if contact_raw.get("phone_number")
                else None
            ),
            "linkedin": _validate_field(
                contact_raw.get("linkedin"), LINKEDIN_RE
            ),
        }

        # --- Country & Address ---
        country = data.get("country")
        if country and isinstance(country, str) and country.strip():
            result["country"] = country.strip()[:100]

        address = data.get("address")
        if address and isinstance(address, str) and address.strip():
            result["address"] = address.strip()[:255]

        # --- About ---
        about = data.get("about")
        if about and isinstance(about, str) and about.strip():
            result["about"] = about.strip()[:1500]

        # --- Employment ---
        for emp in data.get("employment") or []:
            if not emp.get("employer_name") and not emp.get("job_title"):
                continue
            result["employment"].append({
                "employer_name": (emp.get("employer_name") or "").strip(),
                "job_title": (emp.get("job_title") or "").strip(),
                "description_of_duties": (
                    (emp.get("description_of_duties") or "").strip()[:9500]
                ),
                "start_date": _normalize_date(emp.get("start_date")),
                "end_date": _normalize_date(emp.get("end_date")),
            })
        result["employment"] = _dedup_dicts(
            result["employment"], ["employer_name", "job_title", "start_date"]
        )

        # --- Education ---
        for edu in data.get("education") or []:
            if not edu.get("institution_name"):
                continue
            result["education"].append({
                "qualification": (edu.get("qualification") or "").strip(),
                "institution_name": (edu.get("institution_name") or "").strip(),
                "start_date": _normalize_date(edu.get("start_date")),
                "end_date": _normalize_date(edu.get("end_date")),
            })
        result["education"] = _dedup_dicts(
            result["education"], ["institution_name", "qualification", "start_date"]
        )

        # --- Certifications ---
        for cert in data.get("certifications") or []:
            if not cert.get("name"):
                continue
            result["certifications"].append({
                "name": (cert.get("name") or "").strip(),
                "issuer": (cert.get("issuer") or "").strip(),
                "date_issued": _normalize_date(cert.get("date_issued")),
            })
        result["certifications"] = _dedup_dicts(
            result["certifications"], ["name", "issuer"]
        )

        # --- Projects ---
        for proj in data.get("projects") or []:
            if not proj.get("title"):
                continue
            result["projects"].append({
                "title": (proj.get("title") or "").strip(),
                "description": (proj.get("description") or "").strip()[:500],
                "link": (proj.get("link") or "").strip() or None,
            })
        result["projects"] = _dedup_dicts(
            result["projects"], ["title"]
        )

        logger.info(
            "[%s] Validated: %d employment, %d education, %d certs, %d projects",
            req_id,
            len(result["employment"]),
            len(result["education"]),
            len(result["certifications"]),
            len(result["projects"]),
        )
        return result
