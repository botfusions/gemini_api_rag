# Security Policy

## API Key Management

This project uses sensitive API keys for Apify and Google Gemini services. To ensure security:

### ✅ Current Security Measures

1. **Environment Variables**: All API keys are stored in a `.env` file and loaded using `python-dotenv`
2. **Git Ignore**: The `.env` file is included in `.gitignore` to prevent accidental commits
3. **Example Template**: A `.env.example` file provides a template with placeholder values
4. **No Hardcoded Keys**: Code uses `os.getenv()` to read API keys from environment variables

### 🔒 Security Audit Results

**Date**: 2025-11-07
**Branch**: claude/remove-exposed-api-keys-011CUu82B7huw79RjnUG5Woc

**Findings**:
- ✅ No API keys found in source code
- ✅ No API keys found in git history
- ✅ `.env` file properly gitignored
- ✅ All Python modules use environment variables for API keys
- ✅ `.env.example` exists with safe placeholder values

**Reviewed Files**:
- `gemini_client.py`: Uses `os.getenv('GEMINI_API_KEY')`
- `youtube_scraper.py`: Uses `os.getenv('APIFY_API_KEY')`
- `translator.py`: No API keys required
- `chat.py`: Inherits security from `gemini_client.py`
- `main.py`: No direct API key usage

### 📝 Best Practices for Contributors

1. **Never commit the `.env` file**
2. **Never hardcode API keys in source code**
3. **Always use `os.getenv()` to read sensitive configuration**
4. **Update `.env.example` when adding new environment variables**
5. **Rotate API keys if accidentally exposed**

### 🔑 Setting Up API Keys

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your actual API keys:
   ```
   APIFY_API_KEY=your_apify_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. Verify the file is ignored:
   ```bash
   git check-ignore -v .env
   ```

### 🚨 If You Accidentally Expose an API Key

1. **Immediately revoke/regenerate the key** in the respective service dashboard
2. **Remove the key from git history** if committed:
   ```bash
   # Use git filter-branch or BFG Repo-Cleaner
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   ```
3. **Update the key** in your `.env` file
4. **Force push** (if working on your own branch)

### 📋 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `APIFY_API_KEY` | Yes | API key for Apify YouTube scraper |
| `GEMINI_API_KEY` | Yes | API key for Google Gemini API |

### 🔍 Security Scanning

Regular security audits are performed on this repository to ensure:
- No credentials in source code
- No credentials in git history
- Proper use of `.gitignore`
- All sensitive data in environment variables

### 📞 Reporting Security Issues

If you discover a security vulnerability, please report it by:
1. Creating a private issue in the repository
2. Contacting the maintainers directly
3. **Do not** post security vulnerabilities in public issues

---

**Last Updated**: 2025-11-07
**Status**: ✅ Secure
