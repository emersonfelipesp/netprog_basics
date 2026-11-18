# Repository work instructions

Preserve the authored course examples, data, original requirements and tutorial
instructions. Automatic CI promises Python 3.8.20 and all seven original
producers. Keep the push and pull-request admission for master. Do not run the
original network examples against a live device or sandbox during source work.

The automatic profile is explicitly offline source-contract validation. It does
not establish live NETCONF, CLI, SNMP, RESTCONF or VPN behavior. Keep real library
imports, narrow network fixtures, the fail-closed socket guard and all SNMP
success/error assertions. Do not replace these checks with syntax-only coverage.

Use an owned environment and the hash-locked requirements-ci.txt. Run Ruff on
tests, execute the complete tests on actual Python 3.8.20, validate the workflow
definition, and compare original source/data digests before publication. Run a
per-function complexity audit for changed executable code, with threshold 10.
The .nms-git-workflow.json declares the actual staged syntax, lint and test gates.

Keep repository permissions read-only and publish only bounded test artifacts.
Do not add deployment, release, credential, host or runner operations. Do not
copy private provider identifiers into public documentation or commit messages.
