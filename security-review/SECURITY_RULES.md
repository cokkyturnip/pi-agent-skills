# SECURITY_RULES.md

## 1️⃣ Injection & Unsafe Deserialization
- **BLOCKED**: `pickle.load` on any external data source. Use JSON or safe serializers.
- **BLOCKED**: `torch.load` with `weights_only=False`. Must set `weights_only=True`.
- **BLOCKED**: `yaml.load` without `Loader=yaml.SafeLoader`. Use `yaml.safe_load`.
- **BLOCKED**: Direct string interpolation into SQL queries. Use parameterized statements / ORM.
- **BLOCKED**: `eval()` or `exec()` with any user‑supplied input.
- **BLOCKED**: `subprocess.run` / `os.system` with arguments derived from user data without strict whitelist.

## 2️⃣ Cross‑Site Scripting (XSS)
- **BLOCKED**: Assigning `innerHTML` or `dangerouslySetInnerHTML` with raw user content. Sanitize with DOMPurify or encode.
- **WARN**: Rendering user‑generated HTML via templating engines – ensure auto‑escaping is enabled.
- **BLOCKED**: `document.write` with user data.

## 3️⃣ Secrets & Credentials
- **BLOCKED**: Hard‑coding API keys, tokens, passwords, or any secret in source files.
- **BLOCKED**: Committing `.env` files with real secrets. Use placeholders and environment injection.
- **BLOCKED**: Storing JWT signing keys in code. Load from secret manager.
- **BLOCKED**: Embedding cloud provider credentials (AWS, GCP, Azure) directly in code.

## 4️⃣ Authentication & Authorization
- **MUST**: Every public endpoint verifies authentication (session, JWT, API key).
- **MUST**: All state‑changing actions (POST/PUT/DELETE/PATCH) enforce fine‑grained authorization checks.
- **MUST**: IDOR protection – verify the requesting user owns or is allowed to access the resource ID.
- **MUST**: Admin‑only routes require explicit admin role verification.
- **MUST**: Rate‑limit login, password‑reset, and token‑issuance endpoints.
- **MUST**: Passwords must be stored hashed with bcrypt/argon2, never plaintext.

## 5️⃣ Server‑Side Request Forgery (SSRF)
- **WARN**: Any `requests.get/POST` (or equivalent HTTP client) that consumes a URL derived from user input. Enforce allow‑list of trusted domains.
- **WARN**: Automatic redirect following on user‑supplied URLs – disable or validate target.

## 6️⃣ Path Traversal & File Access
- **BLOCKED**: Directly opening or reading files using user‑supplied paths without normalization and whitelist validation.
- **BLOCKED**: Serving files from a directory based purely on a request parameter.
- **WARN**: Using `path.join` with user data – verify final path does not escape allowed base directory.

## 7️⃣ File Upload Handling
- **BLOCKED**: Accepting uploads without MIME type and extension validation.
- **BLOCKED**: Storing user uploads in a web‑accessible directory with executable extensions.
- **BLOCKED**: No size limits on uploads – enforce a maximum payload size.
- **BLOCKED**: Using the original filename from the client – generate a safe server‑side name.

## 8️⃣ Logging & Information Disclosure
- **BLOCKED**: Logging plaintext passwords, tokens, or any PII.
- **BLOCKED**: Exposing stack traces or internal error details to end users.
- **WARN**: Over‑verbose API responses that leak internal schema – use DTOs.
- **BLOCKED**: Debug endpoints (e.g., `/debug`, `/status`) in production builds.

## 9️⃣ API & Webhook Security
- **MUST**: Proper CORS configuration – restrict `Access‑Control‑Allow‑Origin` to trusted origins.
- **MUST**: CSRF protection on state‑changing endpoints when using cookie‑based auth.
- **MUST**: Validate all request bodies against schemas (type, length, format).
- **MUST**: Rate‑limit all public endpoints to mitigate abuse.

## 🔟 Dependency & Supply‑Chain Hardening
- **WARN**: Installing npm/pip/gem packages from unverified sources – review maintainers and recent activity.
- **WARN**: Direct `git clone` of remote repositories without verification – lock to specific commit hashes.
- **WARN**: Unpinned dependencies – pin versions in lockfiles (package‑lock.json, Gemfile.lock, requirements.txt).

---

### Org‑Specific Policies (optional)
You can create a `claude-security-guidance.md` (or `security-guidance.md` in this repo) with additional rules that are specific to your organization. The content of that file will be concatenated with the rules above during the LLM diff review.

*Do NOT put secrets in the policy file.*