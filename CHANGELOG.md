# Changelog

All notable repository maintenance work is recorded here.

## 2026-09-30

### Security
- Moved Django secret, database configuration, allowed hosts, and production security flags to environment variables.
- Removed hardcoded admin credentials from the admin login flow.
- Removed hardcoded SMS provider credentials from voter flows.
- Moved the hash-chain genesis secret to `BLOCKCHAIN_GENESIS_KEY`.
- Added `.env.example` and strengthened secret/environment ignore rules.
- Added CodeQL scanning for Python.

### Reliability
- Fixed OTP verification assignments so verified status is actually persisted and the OTP is cleared.
- Made the hash-chain implementation deterministic and type-safe.
- Added CI checks for Django configuration and tests.

### Documentation
- Reworked the README to describe the implementation as a custom hash-chain prototype rather than an Ethereum blockchain.
- Documented local setup, configuration, security limitations, architecture, and development checks.

### Repository hygiene
- Removed the tracked macOS `.DS_Store` file.
- Added CI and security workflows under `.github/workflows/`.

## Notes

These changes intentionally prioritize safe configuration and accurate documentation without claiming that the prototype provides guarantees required by real election infrastructure.
