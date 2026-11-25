# World News — 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/mrmasudhafej-tech/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/mrmasudhafej-tech/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A make.fun entry for competition `news-image-20261125`: sum up the world's news of Wednesday 25 November 2026 in one image.

The front page leads with China's Shenzhou-24 launch carrying Zeeshan Ali, set to become the first foreign astronaut aboard China's Tiangong station. Also: Houthi threats to Jeddah and Saudi Red Sea ports, Asian stocks falling on fresh US tariff-threat reports, a US jury convicting Huawei on 10 of 12 counts, and the UN reporting five women killed every hour by a partner or close relative in 2025. The footer notes the Gukesh–Sindarov world championship Game 2 in Geneva, Shanghai's loyalty pledge, and a Russian strike on Odesa.

## How it works

`render.py` (Pillow) draws the 1024x1024 front page and saves it as `entry.png`. `main.py` (standard library only) copies the stored PNG byte-for-byte to `/output/entry.png` (honouring `$MAKEFUN_OUTPUT_DIR` when set), so two runs always produce identical output. No network is needed.

## Run

```sh
python3 render.py   # redraw entry.png
python3 main.py     # write /output/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
