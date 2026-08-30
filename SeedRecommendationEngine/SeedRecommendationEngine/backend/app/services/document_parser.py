import io
import re
from typing import Any, Dict, Optional, Tuple

from ..utils.logger import get_logger

logger = get_logger("document_parser")


class DocumentParser:
    """
    Parses agricultural laboratory reports, soil test sheets, CSVs, and plain text
    to extract agronomic parameters (N, P, K, pH, District, Moisture, Rainfall).
    """

    @staticmethod
    def parse_pdf(file_bytes: bytes) -> str:
        text = ""
        try:
            from pypdf import PdfReader

            reader = PdfReader(io.BytesIO(file_bytes))
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as exc:
            logger.warning(f"pypdf extraction failed or not available: {exc}")
            # Fallback raw ASCII decoding
            text = file_bytes.decode("utf-8", errors="ignore")
        return text

    @staticmethod
    def parse_csv(file_bytes: bytes) -> Tuple[str, Dict[str, Any]]:
        extracted: Dict[str, Any] = {}
        text_summary = ""
        try:
            import pandas as pd

            df = pd.read_csv(io.BytesIO(file_bytes))
            text_summary = df.head(10).to_string()

            # Inspect columns (case-insensitive)
            cols = {str(c).strip().lower(): c for c in df.columns}
            
            # Map standard features
            key_maps = {
                "n": ["n", "nitrogen", "available_n"],
                "p": ["p", "phosphorus", "available_p", "phosphate"],
                "k": ["k", "potassium", "available_k", "potash"],
                "ph": ["ph", "soil_ph", "ph_level"],
                "temperature": ["temperature", "temp"],
                "humidity": ["humidity", "relative_humidity"],
                "rainfall": ["rainfall", "rain", "precipitation"],
                "district": ["district", "location", "region"],
            }

            for std_key, aliases in key_maps.items():
                for alias in aliases:
                    if alias in cols:
                        col_name = cols[alias]
                        val = df[col_name].dropna().iloc[0] if not df[col_name].dropna().empty else None
                        if val is not None:
                            try:
                                if std_key in ["n", "p", "k", "temperature", "humidity", "rainfall"]:
                                    extracted[std_key] = float(val)
                                elif std_key == "ph":
                                    extracted[std_key] = round(float(val), 2)
                                else:
                                    extracted[std_key] = str(val)
                            except (ValueError, TypeError):
                                pass
                        break
        except Exception as exc:
            logger.warning(f"CSV extraction failed: {exc}")
            text_summary = file_bytes.decode("utf-8", errors="ignore")
        return text_summary, extracted

    @classmethod
    def extract_features_from_text(cls, text: str) -> Dict[str, Any]:
        extracted: Dict[str, Any] = {}
        lower = text.lower()

        # Regular expressions for N, P, K, pH
        # E.g. "N: 90", "Nitrogen = 85.5", "N - 90 ppm", "N=90"
        n_match = re.search(r"(?:nitrogen|available\s*n|\bn\b)\s*[:=\-]?\s*([0-9]+(?:\.[0-9]+)?)", lower)
        if n_match:
            try:
                extracted["N"] = float(n_match.group(1))
            except ValueError:
                pass

        p_match = re.search(r"(?:phosphorus|available\s*p|phosphate|\bp\b)\s*[:=\-]?\s*([0-9]+(?:\.[0-9]+)?)", lower)
        if p_match:
            try:
                extracted["P"] = float(p_match.group(1))
            except ValueError:
                pass

        k_match = re.search(r"(?:potassium|available\s*k|potash|\bk\b)\s*[:=\-]?\s*([0-9]+(?:\.[0-9]+)?)", lower)
        if k_match:
            try:
                extracted["K"] = float(k_match.group(1))
            except ValueError:
                pass

        # pH match: "pH: 6.5", "pH = 6.2", "pH 5.8", "පීඑච් 6.5"
        ph_match = re.search(r"(?:soil\s*ph|\bph\b|පීඑච්)\s*[:=\-]?\s*([0-9]+(?:\.[0-9]+)?)", lower)
        if ph_match:
            try:
                val = float(ph_match.group(1))
                if 2.0 <= val <= 11.0:
                    extracted["ph"] = round(val, 2)
            except ValueError:
                pass

        # Rainfall: "rainfall: 200mm", "rain 150"
        rf_match = re.search(r"(?:rainfall|precipitation|rain|වර්ෂාපතන|මழை)\s*[:=\-]?\s*([0-9]+(?:\.[0-9]+)?)", lower)
        if rf_match:
            try:
                extracted["rainfall"] = float(rf_match.group(1))
            except ValueError:
                pass

        # Temperature: "temp 28C", "temperature: 25"
        temp_match = re.search(r"(?:temperature|temp|උෂ්ණත්ව|வெப்பநிலை)\s*[:=\-]?\s*([0-9]+(?:\.[0-9]+)?)", lower)
        if temp_match:
            try:
                extracted["temperature"] = float(temp_match.group(1))
            except ValueError:
                pass

        # Humidity: "humidity: 80%"
        hum_match = re.search(r"(?:humidity|තෙතමන|ஈரப்பதம்)\s*[:=\-]?\s*([0-9]+(?:\.[0-9]+)?)", lower)
        if hum_match:
            try:
                extracted["humidity"] = float(hum_match.group(1))
            except ValueError:
                pass

        # Check for District name mention
        from .chat_knowledge import DISTRICT_KNOWLEDGE
        for d in DISTRICT_KNOWLEDGE.keys():
            if d.lower() in lower:
                extracted["district"] = d
                break

        return extracted

    @classmethod
    def parse_file(cls, arg1: Any, arg2: Any) -> Dict[str, Any]:
        if isinstance(arg1, (bytes, bytearray)):
            file_bytes = bytes(arg1)
            filename = str(arg2)
        else:
            filename = str(arg1)
            file_bytes = bytes(arg2)

        ext = filename.lower().split(".")[-1] if "." in filename else ""
        extracted: Dict[str, Any] = {}
        raw_text = ""

        if ext == "pdf":
            raw_text = cls.parse_pdf(file_bytes)
            extracted = cls.extract_features_from_text(raw_text)
        elif ext == "csv":
            raw_text, csv_extracted = cls.parse_csv(file_bytes)
            extracted = cls.extract_features_from_text(raw_text)
            extracted.update(csv_extracted)
        else:
            raw_text = file_bytes.decode("utf-8", errors="ignore")
            extracted = cls.extract_features_from_text(raw_text)

        district = extracted.pop("district", None)
        return {
            "text": raw_text,
            "features": extracted,
            "district": district
        }
