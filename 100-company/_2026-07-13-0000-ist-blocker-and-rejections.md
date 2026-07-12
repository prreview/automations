# 2026-07-13 00:00 IST batch result

Accepted reports: 0

## checks run

- Read and normalized 261 existing company reports, 266 domains, and 1,007 recorded URLs before sourcing.
- Retrieved Raj’s CV from https://yagyaraj.com/cv and used its actual WaveMaker, Rava.ai, and Trevyn evidence for the fit screen.
- Queried YC’s public company directory through its browser-exposed Algolia index with `isHiring=true` and team size 5–30. It returned 744 profiles; 607 remained after company/domain dedupe.
- Loaded the current YC profile pages: 579 of those companies had 1,582 active role links.
- The latest stored YC batch already covers every role that passed the frontend/frontend-leaning full-stack, max-5-years, India-or-explicit-remote, and CV-fit screen. The rest failed at least one of those tests.

## blockers

- The scheduled time is 00:00 IST on 13 July, but this run executed at 23:08 IST on 12 July. The public YC data had not changed since the earlier 12 July run.
- Web search and page-extraction tools are unavailable because Firecrawl is unconfigured. Direct DuckDuckGo HTML returned an anti-bot page.
- No new job passed every required check. No company file or outreach was added to fill the target count.

## source links

- YC directory: https://www.ycombinator.com/companies
- Raj CV: https://yagyaraj.com/cv
