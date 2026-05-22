#!/usr/bin/env python3
"""Build urban governance / real estate / marriage tracker data."""

from __future__ import annotations

import importlib.util
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[0]
OUTPUT = ROOT / "data" / "urban_marriage_tracker.json"
BASE_SCRIPT = REPO_ROOT / "standalone-policy-journal-tracker" / "scripts" / "update_policy_tracker.py"

MAX_PAPERS_PER_JOURNAL = int(os.getenv("MAX_URBAN_MARRIAGE_PAPERS_PER_JOURNAL", "12"))

TRACKED_JOURNALS = [
    {"name": "American Economic Review", "field": "经济学", "issn": "0002-8282", "issue_url": "https://www.aeaweb.org/journals/aer"},
    {"name": "Quarterly Journal of Economics", "field": "经济学", "issn": "0033-5533", "issue_url": "https://academic.oup.com/qje"},
    {"name": "Journal of Political Economy", "field": "经济学", "issn": "0022-3808", "issue_url": "https://www.journals.uchicago.edu/journals/jpe"},
    {"name": "Econometrica", "field": "经济学", "issn": "0012-9682", "issue_url": "https://onlinelibrary.wiley.com/journal/14680262"},
    {"name": "Review of Economic Studies", "field": "经济学", "issn": "0034-6527", "issue_url": "https://academic.oup.com/restud"},
    {"name": "Journal of Urban Economics", "field": "经济学", "issn": "0094-1190", "issue_url": "https://www.sciencedirect.com/journal/journal-of-urban-economics"},
    {"name": "Regional Science and Urban Economics", "field": "经济学", "issn": "0166-0462", "issue_url": "https://www.sciencedirect.com/journal/regional-science-and-urban-economics"},
    {"name": "China Economic Review", "field": "经济学", "issn": "1043-951X", "issue_url": "https://www.sciencedirect.com/journal/china-economic-review"},
    {"name": "American Political Science Review", "field": "政治学", "issn": "0003-0554", "issue_url": "https://www.cambridge.org/core/journals/american-political-science-review"},
    {"name": "American Journal of Political Science", "field": "政治学", "issn": "0092-5853", "issue_url": "https://onlinelibrary.wiley.com/journal/15405907"},
    {"name": "Journal of Politics", "field": "政治学", "issn": "0022-3816", "issue_url": "https://www.journals.uchicago.edu/journals/jop"},
    {"name": "British Journal of Political Science", "field": "政治学", "issn": "0007-1234", "issue_url": "https://www.cambridge.org/core/journals/british-journal-of-political-science"},
    {"name": "Comparative Political Studies", "field": "政治学", "issn": "0010-4140", "issue_url": "https://journals.sagepub.com/home/cps"},
    {"name": "Journal of Public Administration Research and Theory", "field": "公共管理学", "issn": "1053-1858", "issue_url": "https://academic.oup.com/jpart"},
    {"name": "Public Administration Review", "field": "公共管理学", "issn": "0033-3352", "issue_url": "https://onlinelibrary.wiley.com/journal/15406210"},
    {"name": "Journal of Policy Analysis and Management", "field": "公共管理学", "issn": "0276-8739", "issue_url": "https://onlinelibrary.wiley.com/journal/15206688"},
    {"name": "Governance", "field": "公共管理学", "issn": "0952-1895", "issue_url": "https://onlinelibrary.wiley.com/journal/14680491"},
    {"name": "Policy Studies Journal", "field": "公共管理学", "issn": "0190-292X", "issue_url": "https://onlinelibrary.wiley.com/journal/15410072"},
    {"name": "American Sociological Review", "field": "社会学", "issn": "0003-1224", "issue_url": "https://journals.sagepub.com/home/asr"},
    {"name": "American Journal of Sociology", "field": "社会学", "issn": "0002-9602", "issue_url": "https://www.journals.uchicago.edu/journals/ajs"},
    {"name": "Annual Review of Sociology", "field": "社会学", "issn": "0360-0572", "issue_url": "https://www.annualreviews.org/journal/soc"},
    {"name": "Social Forces", "field": "社会学", "issn": "0037-7732", "issue_url": "https://academic.oup.com/sf"},
    {"name": "European Sociological Review", "field": "社会学", "issn": "0266-7215", "issue_url": "https://academic.oup.com/esr"},
    {"name": "Demography", "field": "社会学", "issn": "0070-3370", "issue_url": "https://read.dukeupress.edu/demography"},
    {"name": "Journal of Marriage and Family", "field": "社会学", "issn": "0022-2445", "issue_url": "https://onlinelibrary.wiley.com/journal/17413737"},
    {"name": "Urban Studies", "field": "城市研究", "issn": "0042-0980", "issue_url": "https://journals.sagepub.com/home/usj"},
    {"name": "International Journal of Urban and Regional Research", "field": "城市研究", "issn": "0309-1317", "issue_url": "https://onlinelibrary.wiley.com/journal/14682427"},
    {"name": "Housing Studies", "field": "房地产/住房", "issn": "0267-3037", "issue_url": "https://www.tandfonline.com/journals/chos20"},
    {"name": "Housing Policy Debate", "field": "房地产/住房", "issn": "1051-1482", "issue_url": "https://www.tandfonline.com/journals/rhpd20"},
    {"name": "经济研究", "field": "中文期刊", "issue_url": "http://www.erj.cn/"},
    {"name": "管理世界", "field": "中文期刊", "issue_url": "http://www.mwm.net.cn/"},
    {"name": "中国工业经济", "field": "中文期刊", "issue_url": "http://ciejournal.ajcass.com/"},
    {"name": "政治学研究", "field": "中文期刊", "issue_url": "http://zgzz.chinajournal.net.cn/"},
    {"name": "公共管理学报", "field": "中文期刊", "issue_url": "http://ggglxb.hust.edu.cn/"},
    {"name": "社会学研究", "field": "中文期刊", "issue_url": "http://shxyj.ajcass.com/"},
    {"name": "中国人口科学", "field": "中文期刊", "issue_url": "http://zgrkkx.ajcass.com/"},
]

TOPIC_KEYWORDS = {
    "城市治理": [
        "urban governance", "city governance", "municipal governance", "local governance",
        "local government", "city government", "municipal", "metropolitan", "urban policy",
        "urban planning", "zoning", "neighborhood", "neighbourhood", "community governance",
        "urban renewal", "urbanization", "smart city", "public service delivery",
        "城市治理", "地方治理", "市政", "城市更新", "社区治理", "基层治理", "城市规划", "城镇化",
    ],
    "房地产": [
        "real estate", "housing", "house price", "home price", "property market",
        "housing market", "mortgage", "rent", "rental", "land market", "land use",
        "land value", "affordable housing", "homeownership", "gentrification",
        "住房", "房地产", "房价", "房租", "租赁", "土地市场", "土地出让", "保障房", "住房保障",
    ],
    "婚姻": [
        "marriage", "marital", "divorce", "spouse", "partner", "cohabitation",
        "assortative mating", "family formation", "fertility", "bride", "groom",
        "dowry", "marriage market", "intermarriage", "same-sex marriage",
        "婚姻", "结婚", "离婚", "配偶", "婚配", "婚恋", "彩礼", "家庭形成", "生育", "同居",
    ],
}


def load_base_module() -> Any:
    spec = importlib.util.spec_from_file_location("policy_tracker_base", BASE_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load base tracker module: {BASE_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def detect_topics(base: Any, title: str, abstract: str) -> List[str]:
    haystack = base.normalize_text(f"{title} {abstract}").lower()
    if not haystack:
        return []
    return [topic for topic, terms in TOPIC_KEYWORDS.items() if any(term in haystack for term in terms)]


def build_journal_block(base: Any, journal: Dict[str, Any], translator: Any) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "name": journal.get("name"),
        "field": journal.get("field", ""),
        "query_name": journal.get("query_name") or journal.get("name"),
        "issn": base.normalize_text(journal.get("issn")),
        "resolved_name": journal.get("name"),
        "issue_title": "Latest issue (Crossref)",
        "issue_url": journal.get("issue_url", ""),
        "matched_count": 0,
        "total_in_issue": 0,
        "papers": [],
        "error": None,
    }

    resolved_issn, resolved_name, resolve_error = base.resolve_crossref_journal(journal)
    if resolved_name:
        result["resolved_name"] = resolved_name
    if resolved_issn:
        result["issn"] = resolved_issn

    if not resolved_issn:
        result["error"] = resolve_error or "Unable to resolve journal ISSN from Crossref."
        return result

    try:
        payload = base.fetch_json(
            f"https://api.crossref.org/journals/{resolved_issn}/works",
            params={
                "sort": "published",
                "order": "desc",
                "rows": 240,
                "select": "title,URL,volume,issue,type,abstract,published-print,published-online,published,issued",
            },
        )
        items = payload.get("message", {}).get("items", [])
        latest_volume, latest_issue, latest_date = base.determine_latest_issue(items)

        if latest_volume and latest_issue:
            result["issue_title"] = f"Volume {latest_volume}, Issue {latest_issue}"
        elif latest_date[0] > 0:
            result["issue_title"] = f"Published {latest_date[0]:04d}-{latest_date[1]:02d}"

        picked: List[Dict[str, Any]] = []
        total_in_issue = 0
        for item in items:
            if item.get("type") != "journal-article":
                continue

            title_en = base.safe_title(item)
            url = base.normalize_text(item.get("URL", ""))
            if not title_en or not url:
                continue
            if not base.in_latest_issue(item, latest_volume, latest_issue, latest_date):
                continue

            total_in_issue += 1
            abstract_en = base.strip_html_text(item.get("abstract", ""))
            if not abstract_en:
                abstract_en = base.openalex_abstract_from_doi_url(url)
            abstract_en = base.normalize_text(abstract_en)

            matched_topics = detect_topics(base, title_en, abstract_en)
            if not matched_topics:
                continue

            picked.append(
                {
                    "title_en": title_en,
                    "title_zh": translator.translate(title_en, kind="title"),
                    "url": url,
                    "abstract_en": abstract_en,
                    "abstract_zh": translator.translate(base.trim_for_translation(abstract_en), kind="abstract") if abstract_en else "",
                    "matched_topics": matched_topics,
                }
            )
            if len(picked) >= MAX_PAPERS_PER_JOURNAL:
                break

        result["papers"] = picked
        result["matched_count"] = len(picked)
        result["total_in_issue"] = total_in_issue
        if resolve_error:
            result["error"] = f"ISSN fallback used: {resolve_error}"
    except Exception as exc:
        result["error"] = str(exc)

    return result


def load_previous_data() -> Dict[str, Any]:
    if not OUTPUT.exists():
        return {}
    try:
        return json.loads(OUTPUT.read_text(encoding="utf-8"))
    except Exception:
        return {}


def main() -> None:
    base = load_base_module()
    previous = load_previous_data()
    translator = base.KimiTranslator(api_key=base.KIMI_API_KEY, model=base.KIMI_MODEL)

    old_policy_key = previous.get("urban_marriage_tracker", {})
    if old_policy_key:
        shim = {"policy_tracker": old_policy_key}
        translator.warmup_cache(shim)

    journals = [build_journal_block(base, journal, translator) for journal in TRACKED_JOURNALS]
    tracker = {
        "topics": list(TOPIC_KEYWORDS.keys()),
        "topic_keywords": TOPIC_KEYWORDS,
        "max_papers_per_journal": MAX_PAPERS_PER_JOURNAL,
        "journals": journals,
        "note": (
            "Tracks latest-issue papers in selected domestic and international journals across economics, "
            "political science, public administration, sociology, urban studies, and housing studies. "
            "Crossref is the default source; Chinese journals without Crossref metadata are listed for manual "
            "source expansion."
        ),
    }

    payload = {
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "translation": {
            "engine": "kimi",
            "model": base.KIMI_MODEL,
            "enabled": translator.enabled,
            "success_count": translator.success_count,
            "fail_count": translator.fail_count,
            "failed_examples": translator.fail_samples,
            "note": "Set KIMI_API_KEY to enable Chinese translation.",
        },
        "urban_marriage_tracker": tracker,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    total_matches = sum(len(j.get("papers", [])) for j in journals)
    print(f"Wrote: {OUTPUT}")
    print(
        "Translation stats: "
        f"enabled={translator.enabled}, success={translator.success_count}, fail={translator.fail_count}"
    )
    print(f"Journals tracked: {len(journals)}, total matched papers={total_matches}")


if __name__ == "__main__":
    main()
