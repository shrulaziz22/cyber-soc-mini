# Incident Report (Lab Sample - Own System Only)
1. On Oct 13, SIEM detected web brute-force 4x from 198.51.100.23 (T1110).
2. Same host attempted sudo to /etc/shadow and unknown admin login (T1548).
3. Then long DNS 44 chars indicated possible C2 (T1071), chain confirmed as incident.
4. Action: isolated own host, blocked IP on own firewall, saved hashes and timeline, escalated to Tier-2.
5. Lesson: raise web threshold if noisy and enforce MFA, all tests in own lab legally.
