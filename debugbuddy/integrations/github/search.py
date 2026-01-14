from typing import List, Dict, Optional, Tuple
from .client import GitHubClient

class GitHubSearcher:

    def __init__(self, client: GitHubClient):
        self.client = client

    def find_solutions(
        self,
        error_text: str,
        language: str,
        limit: int = 5,
        repo: Optional[str] = None,
        exact: bool = True,
        include_closed: bool = False,
    ) -> List[Dict]:
        query, error_type, message = self._build_query(
            error_text, language, repo=repo, exact=exact, open_only=True
        )
        issues = self.client.search_issues(query)

        if include_closed and not issues:
            query, error_type, message = self._build_query(
                error_text, language, repo=repo, exact=exact, open_only=False
            )
            issues = self.client.search_issues(query)

        if error_type:
            issues = self._rank_issues(issues, error_type, message)

        solutions = []
        for issue in issues[:limit]:
            solutions.append({
                'title': issue['title'],
                'url': issue['html_url'],
                'state': issue['state'],
                'reactions': issue.get('reactions', {}).get('total_count', 0),
                'comments': issue.get('comments', 0)
            })

        return solutions

    def _build_query(
        self,
        error_text: str,
        language: str,
        repo: Optional[str] = None,
        exact: bool = True,
        open_only: bool = True,
    ) -> Tuple[str, Optional[str], Optional[str]]:
        text = (error_text or "").strip()
        first_line = text.splitlines()[0] if text else ""
        error_type = None
        message = None

        if ":" in first_line:
            parts = first_line.split(":", 1)
            candidate = parts[0].strip()
            if "error" in candidate.lower() or "exception" in candidate.lower():
                error_type = candidate
                message = parts[1].strip()
        else:
            error_type = first_line if first_line else None

        terms = ["is:issue"]
        if open_only:
            terms.append("is:open")
        if language:
            terms.append(f"language:{language}")
        if repo:
            terms.append(f"repo:{repo}")

        if error_type:
            if exact:
                terms.append(f"\"{error_type}\"")
                terms.append("in:title")
            else:
                terms.append(error_type)
                terms.append("in:title,body")
        if message:
            short_message = message[:120].strip()
            if short_message:
                if exact:
                    terms.append(f"\"{short_message}\"")
                    terms.append("in:body")
                else:
                    terms.append(short_message)
                    terms.append("in:title,body")

        if not error_type and first_line:
            if exact:
                terms.append(f"\"{first_line[:120]}\"")
                terms.append("in:title,body")
            else:
                terms.append(first_line[:120])
                terms.append("in:title,body")

        return " ".join(terms), error_type, message

    def _rank_issues(self, issues: List[Dict], error_type: str, message: Optional[str]) -> List[Dict]:
        def score(issue: Dict) -> int:
            title = (issue.get("title") or "").lower()
            body = (issue.get("body") or "").lower()
            score_val = 0
            error_l = error_type.lower()
            if error_l in title:
                score_val += 4
            if error_l in body:
                score_val += 2
            if message:
                msg = message.lower()
                if msg and msg in title:
                    score_val += 2
                if msg and msg in body:
                    score_val += 1
            score_val += min(issue.get("comments", 0), 5)
            score_val += min(issue.get("reactions", {}).get("total_count", 0), 5)
            return score_val

        return sorted(issues, key=score, reverse=True)
