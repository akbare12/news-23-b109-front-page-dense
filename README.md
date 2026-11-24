# THE WORLD TODAY — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b109-front-page-dense/rank.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b109-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image summing up 23 November 2026's world news: the AI rout hitting Asia (Kospi −3.3%),
the UN chief's call to regulate AI before it's too late, and the US lead over China at a record
low — plus 28 more stories, a world map with numbered pins, and a DATE CHECK box that keeps
other days' news out.

## Run

```sh
python3 draw.py        # regenerate entry.png (1024x1024)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copy entry.png to out/entry.png
```

`main.py` is stdlib-only and verifies the PNG (signature, IHDR 1024x1024, chunk CRCs,
IEND last, size ≤ 1 MiB) before copying it. It never writes next to itself.
