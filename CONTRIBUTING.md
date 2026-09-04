# Contributing

Contributions should preserve the separation between skill-development data and
fixed evaluation data.

1. Do not add secrets, provider credentials, local absolute paths, or private
   benchmark outputs.
2. Do not reveal GPQA examples or other content carrying a no-online-disclosure
   condition.
3. Preserve source repository, source question ID, license metadata, and content
   hashes when changing dataset records.
4. Do not use acceptance questions to edit or select skills and then report the
   result as a sealed evaluation.
5. Run `python scripts/validate_release.py` before opening a pull request.
6. Explain scientific and provenance changes in the pull-request description.

