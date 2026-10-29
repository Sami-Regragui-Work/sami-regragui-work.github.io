"""Capture screenshots of the portfolio and of live project demos.

Runs in GitHub Actions (see .github/workflows/screenshots.yml).
Outputs go to screenshots/ at the repo root.
"""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "screenshots"
OUT.mkdir(exist_ok=True)

PORTFOLIO = (ROOT / "index.html").as_uri() + "?lang=en"
WORKSPACE_LIVE = "https://sami-regragui-work.github.io/WorkSpace-Staff-Manager/"

# (output file, url, width, height, full_page)
SHOTS = [
    ("portfolio-desktop.png", PORTFOLIO, 1440, 900, True),
    ("portfolio-mobile.png", PORTFOLIO, 390, 844, True),
    ("workspace-staff-manager.png", WORKSPACE_LIVE, 1280, 800, False),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for name, url, w, h, full in SHOTS:
        page = browser.new_page(
            viewport={"width": w, "height": h},
            device_scale_factor=1,
            reduced_motion="reduce",
        )
        page.goto(url, wait_until="networkidle", timeout=60_000)
        page.wait_for_timeout(800)  # let fonts and layout settle
        page.screenshot(path=str(OUT / name), full_page=full)
        print("saved", name)
        page.close()
    browser.close()
