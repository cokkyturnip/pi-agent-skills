---
name: security-review
description: Security review for generated code. Three layers — pattern warnings, LLM diff review, and cross-file data flow. Use when implementing features involving authentication, authorization, user input handling, database operations, file uploads, API endpoints, or sensitive data processing.
---

# Security Review

Security review for all generated code. The process consists of three layers:

1. **Pattern warnings** — Instant inline checks during coding for dangerous patterns (unsafe deserialization, hardcoded secrets, XSS, etc.).
2. **LLM diff review** — Comprehensive diff review with a security lens after coding is complete, prior to delivery.
3. **Cross-file data flow** — Data flow analysis of user input across files to detect multi-file vulnerabilities (IDOR, auth bypass, SSRF).

<HARD-GATE>
DO NOT deliver code touching authentication, authorization, user input, file uploads, API endpoints, or databases without running the three layers of security review above. This is MANDATORY.
</HARD-GATE>

## Layer 1 — Pattern Warnings (During Development)

Inspect every code block for the following dangerous patterns. If found, halt and rectify before continuing:

| Pattern | Action |
|---|---|
| `pickle.load` without source control | BLOCKED |
| `torch.load(weights_only=False)` | BLOCKED — use `weights_only=True` |
| `yaml.load` without `SafeLoader` | BLOCKED — use `yaml.safe_load` |
| `eval()` / `exec()` with user input | BLOCKED |
| `innerHTML` / `dangerouslySetInnerHTML` with user content | BLOCKED — use `textContent` or DOMPurify |
| API keys, tokens, hardcoded passwords | BLOCKED — use environment variables |
| SQL concatenation with user input (`f"SELECT {x}"`) | BLOCKED — use parameterized queries |
| `subprocess` / `os.system` with user arguments | BLOCKED — strict validation required |

## Layer 2 — LLM Diff Review (Post-Development)

Perform a comprehensive review after completing a feature:

1. Consult `SECURITY_RULES.md` for complete rules.
2. Review every modified file — scan for injection, XSS, hardcoded secrets, and path traversal.
3. Verify authentication — does every endpoint have a guard?
4. Verify authorization — does the user only access their own resources? (Prevent IDOR).
5. Check input validation — is every user input validated at the API boundary?
6. Check secrets — ensure no credentials in code, comments, or logs.
7. Report findings — fix all BLOCKED items; document rationale for all WARN items.
8. Deliver to user only after the code is verified clean.

## Layer 3 — Cross-File Data Flow

For complex features (multi-file, involving auth/user input):

1. Identify entry points (API endpoints, handlers, webhooks).
2. Trace the data flow from entry point to database/file system/response.
3. At each point, verify:
   - Authentication verified?
   - Authorization verified (does the user have access to this resource)?
   - Input validated (type, length, format)?
   - Output escaped for context (HTML, JSON, SQL)?
4. Document and remediate all weaknesses discovered.

## Mandatory Checklist

```markdown
- [ ] Layer 1: Pattern scan complete, no BLOCKED items
- [ ] Layer 2: Diff review complete, all findings addressed
- [ ] Layer 3: Data flow trace complete (if complex)
- [ ] SECURITY_RULES.md consulted
- [ ] All BLOCKED items rectified, all WARN items documented
- [ ] Code ready for delivery
```

## Red Flags — Halt and Rectify

If any of the following are found, STOP and remediate immediately before proceeding:

- Hardcoded credentials
- Raw SQL concatenation with user input
- API endpoint without authentication
- IDOR (User A can access User B's data)
- `innerHTML` with user content without sanitization
- `pickle` / `yaml.load` from untrusted sources
- File paths from user input without normalization
- Stack traces or debug information leaked to responses
