# Full Incident Report - Lab Sample Only (Own System)
Date: Oct 13, 2026 | Analyst: Aziz (Tier-1) | Status: Closed in lab

## Summary
SIEM mini detected a 3-stage chain in own lab: web brute-force, sudo abuse, and long DNS. No real user harmed. All data are samples.

## Timeline
11:00 - 4x 401/404 to /admin from 198.51.100.23 (T1110)
11:03 - sudo cat /etc/shadow and unknown admin bash (T1548)
11:04 - DNS 44 chars to external (T1071)
11:10 - Host isolated in own lab, IP blocked on own firewall, hashes saved, escalated to Tier-2

## MITRE
T1110 Brute Force, T1548 Privilege Escalation, T1071 C2, T1136 checked none new

## Action
Isolate own host, block IoC on own controls, hunt same hash in mailbox, reset lab passwords, save timeline + SHA256.

## Lesson
Raise web rule to >=5 if noisy, enforce MFA and sudo allowlist. Tests only in own lab and legal demos. Ready to follow team SOP.
