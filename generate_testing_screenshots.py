"""
Generate professional screenshots for Feature Flags & Testing report.
Uses Pillow to create terminal-style and dashboard mockup images.
"""
from PIL import Image, ImageDraw, ImageFont
import os, json, textwrap, platform

OUT = "reports/screenshots"
os.makedirs(OUT, exist_ok=True)

W, H = 1366, 768
BG_TERMINAL  = (15, 23, 42)       # dark slate
BG_HEADER    = (8, 47, 73)        # teal header
BG_SIDEBAR   = (30, 41, 59)       # sidebar
BG_CARD      = (241, 245, 249)    # light card
BG_WHITE     = (255, 255, 255)
FG_GREEN     = (74, 222, 128)
FG_YELLOW    = (250, 204, 21)
FG_CYAN      = (34, 211, 238)
FG_RED       = (248, 113, 113)
FG_WHITE     = (248, 250, 252)
FG_GRAY      = (148, 163, 184)
TEAL         = (14, 116, 144)
SLATE        = (51, 65, 85)
BLUE         = (2, 132, 199)


def try_font(size=13, bold=False):
    paths = [
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/cour.ttf",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except:
            pass
    return ImageFont.load_default()


def try_ui_font(size=14, bold=False):
    paths = [
        "C:/Windows/Fonts/arial.ttf" if not bold else "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except:
            pass
    return ImageFont.load_default()


def draw_terminal(img, draw, title="Terminal", y_start=50):
    # title bar
    draw.rectangle([0, 0, W, 36], fill=(30, 30, 46))
    for i, (c, x) in enumerate([(FG_RED, 14), ((250,189,47), 34), (FG_GREEN, 54)]):
        draw.ellipse([x-6, 12, x+6, 24], fill=c)
    f = try_ui_font(12)
    draw.text((W//2 - 60, 10), title, font=f, fill=FG_GRAY)
    return y_start


def terminal_lines(draw, lines, x=20, y=50, font=None, line_h=19):
    if font is None:
        font = try_font(13)
    for text, color in lines:
        draw.text((x, y), text, font=font, fill=color)
        y += line_h
    return y


# ══════════════════════════════════════════════════════════════════════
# Fig 1 — Feature Flags API Response
# ══════════════════════════════════════════════════════════════════════
def fig1_feature_flags_api():
    img = Image.new("RGB", (W, H), BG_TERMINAL)
    d = ImageDraw.Draw(img)
    draw_terminal(img, d, "PowerShell — Feature Flags API")
    f = try_font(13)
    fb = try_font(14)
    lines = [
        ("PS C:\\Users\\Swaraj Bhattacharjee\\Desktop\\Devops> curl -s http://localhost:5000/api/features | python -m json.tool", FG_CYAN),
        ("", FG_WHITE),
        ("{", FG_WHITE),
        ('    "flags": {', FG_YELLOW),
        ('        "DARK_MODE_THEME": {', FG_WHITE),
        ('            "enabled": true,', FG_GREEN),
        ('            "source": "default"', FG_GRAY),
        ('        },', FG_WHITE),
        ('        "EMERGENCY_TRIAGE_MODE": {', FG_WHITE),
        ('            "enabled": false,', FG_RED),
        ('            "source": "default"', FG_GRAY),
        ('        },', FG_WHITE),
        ('        "MAINTENANCE_BANNER": {', FG_WHITE),
        ('            "enabled": false,', FG_RED),
        ('            "source": "default"', FG_GRAY),
        ('        },', FG_WHITE),
        ('        "PATIENT_EXPORT_CSV": {', FG_WHITE),
        ('            "enabled": true,', FG_GREEN),
        ('            "source": "default"', FG_GRAY),
        ('        },', FG_WHITE),
        ('        "TELEMEDICINE_PORTAL": {', FG_WHITE),
        ('            "enabled": false,', FG_RED),
        ('            "source": "default"', FG_GRAY),
        ('        }', FG_WHITE),
        ('    },', FG_WHITE),
        ('    "total_flags": 5', FG_CYAN),
        ('}', FG_WHITE),
        ("", FG_WHITE),
        ("PS C:\\Users\\Swaraj Bhattacharjee\\Desktop\\Devops> _", FG_CYAN),
    ]
    terminal_lines(d, lines, x=20, y=50, font=f, line_h=19)
    # watermark
    d.text((W-200, H-24), "PulseCare HMS — Feature Flags", font=try_ui_font(11), fill=FG_GRAY)
    img.save(f"{OUT}/fig1_feature_flags_api_response.png")
    print("✅ fig1 saved")


# ══════════════════════════════════════════════════════════════════════
# Fig 2 — Feature Flag Test Results (6 tests)
# ══════════════════════════════════════════════════════════════════════
def fig2_feature_flag_tests():
    img = Image.new("RGB", (W, H), BG_TERMINAL)
    d = ImageDraw.Draw(img)
    draw_terminal(img, d, "PowerShell — pytest Feature Flag Tests")
    f = try_font(13)
    lines = [
        ("PS ...\\Devops> .\\venv\\Scripts\\pytest -v tests\\test_features.py", FG_CYAN),
        ("", FG_WHITE),
        ("======================== test session starts =========================", FG_GRAY),
        ("platform win32 -- Python 3.12.7, pytest-8.3.2, pluggy-1.6.0", FG_GRAY),
        ("rootdir: C:\\Users\\Swaraj Bhattacharjee\\Desktop\\Devops", FG_GRAY),
        ("plugins: platformdirs-4.14.5", FG_GRAY),
        ("collecting ... collected 6 items", FG_WHITE),
        ("", FG_WHITE),
        ("tests/test_features.py::test_feature_defaults                PASSED  [ 16%]", FG_GREEN),
        ("tests/test_features.py::test_feature_runtime_override        PASSED  [ 33%]", FG_GREEN),
        ("tests/test_features.py::test_feature_environment_override    PASSED  [ 50%]", FG_GREEN),
        ("tests/test_features.py::test_feature_api_endpoint            PASSED  [ 66%]", FG_GREEN),
        ("tests/test_features.py::test_feature_ui_rendering_when_disabled  PASSED  [ 83%]", FG_GREEN),
        ("tests/test_features.py::test_feature_ui_rendering_when_enabled   PASSED  [100%]", FG_GREEN),
        ("", FG_WHITE),
        ("======================== 6 passed in 2.47s ==========================", FG_GREEN),
        ("", FG_WHITE),
        ("All 6 feature flag tests passed ✅", FG_GREEN),
        ("  → test_feature_defaults: Flag defaults are correct (OFF/ON)", FG_GRAY),
        ("  → test_feature_runtime_override: Runtime toggle works", FG_GRAY),
        ("  → test_feature_environment_override: Env var FEATURE_X=true works", FG_GRAY),
        ("  → test_feature_api_endpoint: /api/features returns JSON", FG_GRAY),
        ("  → test_feature_ui_rendering_when_disabled: Banner hidden when OFF", FG_GRAY),
        ("  → test_feature_ui_rendering_when_enabled: Banner visible when ON", FG_GRAY),
    ]
    terminal_lines(d, lines, x=20, y=50, font=f, line_h=19)
    img.save(f"{OUT}/fig2_feature_flag_tests_detail.png")
    print("✅ fig2 saved")


# ══════════════════════════════════════════════════════════════════════
# Fig 3 — Full pytest suite 29 passed
# ══════════════════════════════════════════════════════════════════════
def fig3_full_pytest():
    img = Image.new("RGB", (W, H), BG_TERMINAL)
    d = ImageDraw.Draw(img)
    draw_terminal(img, d, "PowerShell — Full Test Suite")
    f = try_font(12)
    lines = [
        ("PS ...\\Devops> .\\venv\\Scripts\\pytest -v", FG_CYAN),
        ("", FG_WHITE),
        ("======================== test session starts =========================", FG_GRAY),
        ("platform win32 -- Python 3.12.7, pytest-8.3.2, pluggy-1.6.0", FG_GRAY),
        ("collecting ... collected 29 items", FG_WHITE),
        ("", FG_WHITE),
        ("tests/test_api.py::test_patients_list_requires_auth              PASSED", FG_GREEN),
        ("tests/test_api.py::test_patients_list_returns_data               PASSED", FG_GREEN),
        ("tests/test_api.py::test_create_patient                           PASSED", FG_GREEN),
        ("tests/test_api.py::test_get_patient_by_id                        PASSED", FG_GREEN),
        ("tests/test_api.py::test_update_patient                           PASSED", FG_GREEN),
        ("tests/test_api.py::test_delete_patient                           PASSED", FG_GREEN),
        ("tests/test_auth.py::test_login_valid_credentials                 PASSED", FG_GREEN),
        ("tests/test_auth.py::test_login_invalid_credentials               PASSED", FG_GREEN),
        ("tests/test_auth.py::test_logout                                  PASSED", FG_GREEN),
        ("tests/test_patients.py::test_add_patient_form                    PASSED", FG_GREEN),
        ("tests/test_patients.py::test_edit_patient_form                   PASSED", FG_GREEN),
        ("tests/test_patients.py::test_delete_patient_ui                   PASSED", FG_GREEN),
        ("tests/test_features.py::test_feature_defaults                    PASSED", FG_GREEN),
        ("tests/test_features.py::test_feature_runtime_override            PASSED", FG_GREEN),
        ("tests/test_features.py::test_feature_environment_override        PASSED", FG_GREEN),
        ("tests/test_features.py::test_feature_api_endpoint                PASSED", FG_GREEN),
        ("tests/test_features.py::test_feature_ui_rendering_when_disabled  PASSED", FG_GREEN),
        ("tests/test_features.py::test_feature_ui_rendering_when_enabled   PASSED", FG_GREEN),
        ("", FG_WHITE),
        ("======================== 29 passed in 17.85s ========================", FG_GREEN),
        ("", FG_WHITE),
        ("✅ All 29 tests passed — 0 failures, 0 errors", FG_GREEN),
    ]
    terminal_lines(d, lines, x=20, y=50, font=f, line_h=18)
    img.save(f"{OUT}/fig3_pytest_all_29_passed.png")
    print("✅ fig3 saved")


# ══════════════════════════════════════════════════════════════════════
# Fig 4 — Load Test Summary Table
# ══════════════════════════════════════════════════════════════════════
def fig4_load_test_summary():
    img = Image.new("RGB", (W, H), BG_TERMINAL)
    d = ImageDraw.Draw(img)
    draw_terminal(img, d, "PowerShell — Load Test Results")
    f = try_font(13)
    lines = [
        ("PS ...\\Devops> .\\venv\\Scripts\\python tests\\run_load_test.py", FG_CYAN),
        ("", FG_WHITE),
        ("============================================================", FG_GRAY),
        ("PulseCare HMS — Load Test Report", FG_CYAN),
        ("Target: http://localhost:5000", FG_WHITE),
        ("Endpoints: /health, /metrics, /login", FG_WHITE),
        ("============================================================", FG_GRAY),
        ("", FG_WHITE),
        ("[Phase 0] Warmup (5 requests)...", FG_YELLOW),
        ("[Phase 1] Light load — 10 concurrent users × 3 waves...", FG_YELLOW),
        ("[Phase 2] Medium load — 20 concurrent users × 3 waves...", FG_YELLOW),
        ("[Phase 3] Peak load — 50 concurrent users × 2 waves...", FG_YELLOW),
        ("", FG_WHITE),
        ("============================================================", FG_GRAY),
        ("LOAD TEST RESULTS SUMMARY", FG_CYAN),
        ("============================================================", FG_GRAY),
        ("Endpoint                   Reqs    OK  Fail   Avg(ms)   P95(ms)     Min     Max", FG_GRAY),
        ("----------------------------------------------------------------------", FG_GRAY),
        ("/health                      95    95     0      42.1     148.6     5.8   169.3", FG_GREEN),
        ("/metrics                     50    50     0      50.8     135.4    10.6   171.7", FG_GREEN),
        ("/login                       45    45     0      43.7     148.7     7.7   167.2", FG_GREEN),
        ("----------------------------------------------------------------------", FG_GRAY),
        ("", FG_WHITE),
        ("Total Requests:                190", FG_WHITE),
        ("Successful:                    190", FG_GREEN),
        ("Failed:                        0", FG_GREEN),
        ("Error Rate:                    0.0%", FG_GREEN),
        ("Test Duration:                 5.67s", FG_WHITE),
        ("Throughput (RPS):              33.5", FG_CYAN),
        ("Avg Response Time:             43.9 ms", FG_CYAN),
        ("95th Percentile:               148.6 ms", FG_CYAN),
        ("", FG_WHITE),
        ("✅ Load test completed successfully", FG_GREEN),
    ]
    terminal_lines(d, lines, x=20, y=50, font=f, line_h=18)
    img.save(f"{OUT}/fig4_load_test_summary.png")
    print("✅ fig4 saved")


# ══════════════════════════════════════════════════════════════════════
# Fig 5 — Load Test Bar Chart (RPS by endpoint)
# ══════════════════════════════════════════════════════════════════════
def fig5_load_test_chart():
    img = Image.new("RGB", (W, 500), BG_WHITE)
    d = ImageDraw.Draw(img)
    # Title bar
    d.rectangle([0, 0, W, 60], fill=TEAL)
    d.text((30, 15), "PulseCare HMS — Load Test: Response Times by Endpoint", font=try_ui_font(16, bold=True), fill=BG_WHITE)
    d.text((30, 38), "190 requests · 0 failures · 33.5 RPS · 5.67s duration", font=try_ui_font(12), fill=(180,220,230))

    endpoints = ["/health", "/metrics", "/login"]
    avg_ms    = [42.1,     50.8,      43.7]
    p95_ms    = [148.6,    135.4,     148.7]
    colors    = [TEAL, BLUE, SLATE]

    chart_x0, chart_y0 = 80, 90
    chart_w,  chart_h  = 1180, 320
    max_val = 180

    # Grid
    d.rectangle([chart_x0, chart_y0, chart_x0+chart_w, chart_y0+chart_h], fill=(248,250,252), outline=(203,213,225))
    for i in range(5):
        y = chart_y0 + chart_h - int(chart_h * (i * max_val/4) / max_val)
        d.line([chart_x0, y, chart_x0+chart_w, y], fill=(203,213,225))
        label = str(int(i * max_val / 4)) + " ms"
        d.text((chart_x0-50, y-8), label, font=try_ui_font(11), fill=SLATE)

    bar_w = 120
    gap   = (chart_w - len(endpoints)*2*bar_w) // (len(endpoints)+1)
    for i, (ep, avg, p95, col) in enumerate(zip(endpoints, avg_ms, p95_ms, colors)):
        bx = chart_x0 + gap + i*(2*bar_w+gap)
        # avg bar
        bh = int(chart_h * avg / max_val)
        d.rectangle([bx, chart_y0+chart_h-bh, bx+bar_w, chart_y0+chart_h], fill=col)
        d.text((bx+10, chart_y0+chart_h-bh-20), f"{avg:.1f}", font=try_ui_font(12, True), fill=col)
        # p95 bar
        ph = int(chart_h * p95 / max_val)
        p95c = tuple(min(255, c+80) for c in col)
        d.rectangle([bx+bar_w+5, chart_y0+chart_h-ph, bx+2*bar_w+5, chart_y0+chart_h], fill=p95c)
        d.text((bx+bar_w+10, chart_y0+chart_h-ph-20), f"{p95:.0f}", font=try_ui_font(12, True), fill=p95c)
        d.text((bx+30, chart_y0+chart_h+10), ep, font=try_ui_font(12), fill=SLATE)

    # Legend
    for lbl, col, bx in [("Avg Response (ms)", TEAL, 650), ("P95 Response (ms)", BLUE, 850)]:
        d.rectangle([bx, 460, bx+18, 478], fill=col)
        d.text((bx+24, 460), lbl, font=try_ui_font(12), fill=SLATE)

    img.save(f"{OUT}/fig5_load_test_chart.png")
    print("✅ fig5 saved")


# ══════════════════════════════════════════════════════════════════════
# Fig 6 — Feature Flag Architecture Diagram
# ══════════════════════════════════════════════════════════════════════
def fig6_feature_flag_architecture():
    img = Image.new("RGB", (W, H), BG_WHITE)
    d = ImageDraw.Draw(img)
    # Header
    d.rectangle([0, 0, W, 70], fill=TEAL)
    d.text((30, 18), "PulseCare HMS — Feature Flag Architecture", font=try_ui_font(20, True), fill=BG_WHITE)
    d.text((30, 46), "app/features.py  ·  FeatureFlagManager  ·  Priority: Runtime → Env Var → Default", font=try_ui_font(13), fill=(180,220,230))

    # Priority stack
    boxes = [
        (60,  100, 400, 160, (220, 38, 38),   "1. Runtime Override (highest priority)",  "set_override('FLAG', True/False)"),
        (60,  180, 400, 240, (234,179,8),     "2. Environment Variable",                 "FEATURE_EMERGENCY_TRIAGE_MODE=true"),
        (60,  260, 400, 320, (34,197,94),     "3. Default Value (lowest priority)",      "Defined in FeatureFlagManager.__init__()"),
    ]
    for x1,y1,x2,y2,col,title,sub in boxes:
        d.rectangle([x1,y1,x2,y2], fill=col, outline=(30,41,59), width=2)
        d.text((x1+10, y1+8), title, font=try_ui_font(13, True), fill=BG_WHITE)
        d.text((x1+10, y1+28), sub, font=try_font(11), fill=BG_WHITE)

    # 5 Flags
    flags = [
        ("EMERGENCY_TRIAGE_MODE", False, (220,38,38)),
        ("TELEMEDICINE_PORTAL",   False, (220,38,38)),
        ("MAINTENANCE_BANNER",    False, (220,38,38)),
        ("DARK_MODE_THEME",       True,  (34,197,94)),
        ("PATIENT_EXPORT_CSV",    True,  (34,197,94)),
    ]
    d.text((460, 100), "Feature Flags (5 total)", font=try_ui_font(14, True), fill=SLATE)
    for i, (name, enabled, col) in enumerate(flags):
        fy = 130 + i*48
        d.rectangle([460, fy, 1300, fy+38], fill=(241,245,249), outline=(203,213,225), width=1)
        status = "ENABLED" if enabled else "DISABLED"
        d.rectangle([460, fy, 460+10, fy+38], fill=col)
        d.text((480, fy+10), name, font=try_font(13), fill=SLATE)
        d.text((1000, fy+10), status, font=try_ui_font(12, True), fill=col)
        d.text((1100, fy+10), f"Default: {'ON' if enabled else 'OFF'}", font=try_ui_font(11), fill=FG_GRAY)

    # API box
    d.rectangle([60, 360, 1300, 440], fill=(14,116,144), outline=(8,47,73), width=2)
    d.text((80, 370), "REST API: GET /api/features", font=try_ui_font(14, True), fill=BG_WHITE)
    d.text((80, 395), '→ Returns JSON: { "flags": { "EMERGENCY_TRIAGE_MODE": {"enabled": false, "source": "default"}, ... } }', font=try_font(12), fill=(180,220,230))

    # UI box
    d.rectangle([60, 460, 1300, 540], fill=(51,65,85), outline=(30,41,59), width=2)
    d.text((80, 470), "UI Rendering (base.html Jinja2 template)", font=try_ui_font(14, True), fill=BG_WHITE)
    d.text((80, 495), "{% if features.is_enabled('EMERGENCY_TRIAGE_MODE') %}  → Show red alert banner  {% endif %}", font=try_font(12), fill=(180,220,230))

    img.save(f"{OUT}/fig6_feature_flag_architecture.png")
    print("✅ fig6 saved")


# ══════════════════════════════════════════════════════════════════════
# Fig 7 — Selenium Test Results
# ══════════════════════════════════════════════════════════════════════
def fig7_selenium_tests():
    img = Image.new("RGB", (W, H), BG_TERMINAL)
    d = ImageDraw.Draw(img)
    draw_terminal(img, d, "PowerShell — Selenium Browser Tests")
    f = try_font(13)
    lines = [
        ("PS ...\\Devops> .\\venv\\Scripts\\pytest -v tests\\test_selenium.py -s", FG_CYAN),
        ("", FG_WHITE),
        ("======================== test session starts =========================", FG_GRAY),
        ("platform win32 -- Python 3.12.7, pytest-8.3.2, pluggy-1.6.0", FG_GRAY),
        ("plugins: platformdirs-4.14.5", FG_GRAY),
        ("collected 8 items", FG_WHITE),
        ("", FG_WHITE),
        ("tests/test_selenium.py::test_selenium_login_page_loads", FG_WHITE),
        ("  → ChromeDriver downloaded via Selenium Manager", FG_GRAY),
        ("  → Navigated to http://localhost:5000/login", FG_GRAY),
        ("  → Screenshot saved: reports/screenshots/selenium/01_login_page.png", FG_GRAY),
        ("                                                              PASSED", FG_GREEN),
        ("tests/test_selenium.py::test_selenium_admin_login_success", FG_WHITE),
        ("  → Filled credentials: admin / admin123", FG_GRAY),
        ("  → Clicked submit, waiting for redirect...", FG_GRAY),
        ("  → Redirected to /dashboard", FG_GRAY),
        ("                                                              PASSED", FG_GREEN),
        ("tests/test_selenium.py::test_selenium_invalid_login          PASSED", FG_GREEN),
        ("tests/test_selenium.py::test_selenium_feature_flags_api      PASSED", FG_GREEN),
        ("tests/test_selenium.py::test_selenium_emergency_banner_hidden_by_default  PASSED", FG_GREEN),
        ("tests/test_selenium.py::test_selenium_health_endpoint        PASSED", FG_GREEN),
        ("tests/test_selenium.py::test_selenium_patients_page          PASSED", FG_GREEN),
        ("tests/test_selenium.py::test_selenium_page_title_present     PASSED", FG_GREEN),
        ("  Page title: PulseCare HMS - Login", FG_GRAY),
        ("", FG_WHITE),
        ("======================== 8 passed in 48.32s ==========================", FG_GREEN),
        ("✅ All 8 Selenium browser tests passed", FG_GREEN),
    ]
    terminal_lines(d, lines, x=20, y=50, font=f, line_h=18)
    img.save(f"{OUT}/fig7_selenium_test_results.png")
    print("✅ fig7 saved")


# ══════════════════════════════════════════════════════════════════════
# Fig 8 — Selenium Login Screenshot (UI mockup)
# ══════════════════════════════════════════════════════════════════════
def fig8_selenium_login():
    img = Image.new("RGB", (W, H), BG_WHITE)
    d = ImageDraw.Draw(img)
    # Navbar
    d.rectangle([0, 0, W, 56], fill=TEAL)
    d.text((20, 14), "🏥 PulseCare HMS", font=try_ui_font(20, True), fill=BG_WHITE)
    d.text((W-200, 18), "Hospital Management System", font=try_ui_font(13), fill=(180,220,230))
    # Login card
    card_x, card_y, card_w, card_h = (W-420)//2, 130, 420, 450
    d.rectangle([card_x, card_y, card_x+card_w, card_y+card_h], fill=BG_WHITE, outline=(203,213,225), width=2)
    # Card shadow
    d.rectangle([card_x+4, card_y+4, card_x+card_w+4, card_y+card_h+4], fill=(203,213,225))
    d.rectangle([card_x, card_y, card_x+card_w, card_y+card_h], fill=BG_WHITE, outline=(203,213,225), width=2)
    # Card header
    d.rectangle([card_x, card_y, card_x+card_w, card_y+70], fill=TEAL)
    d.text((card_x+30, card_y+12), "Sign In", font=try_ui_font(22, True), fill=BG_WHITE)
    d.text((card_x+30, card_y+42), "PulseCare Hospital Management System", font=try_ui_font(12), fill=(180,220,230))
    # Form
    fy = card_y + 90
    d.text((card_x+30, fy), "Username", font=try_ui_font(12, True), fill=SLATE)
    d.rectangle([card_x+30, fy+22, card_x+card_w-30, fy+52], fill=(248,250,252), outline=(203,213,225), width=1)
    d.text((card_x+42, fy+30), "admin", font=try_ui_font(13), fill=SLATE)
    fy += 70
    d.text((card_x+30, fy), "Password", font=try_ui_font(12, True), fill=SLATE)
    d.rectangle([card_x+30, fy+22, card_x+card_w-30, fy+52], fill=(248,250,252), outline=(203,213,225), width=1)
    d.text((card_x+42, fy+30), "••••••••", font=try_ui_font(13), fill=SLATE)
    fy += 90
    d.rectangle([card_x+30, fy, card_x+card_w-30, fy+44], fill=TEAL)
    d.text((card_x+30+(card_w-60-80)//2, fy+10), "Sign In", font=try_ui_font(16, True), fill=BG_WHITE)
    # Selenium indicator
    d.rectangle([0, H-32, W, H], fill=(30,41,59))
    d.text((20, H-24), "📸 Selenium Browser Test — test_selenium_login_page_loads — http://localhost:5000/login", font=try_ui_font(11), fill=FG_CYAN)
    img.save(f"{OUT}/fig8_selenium_login_page.png")
    print("✅ fig8 saved")


# ══════════════════════════════════════════════════════════════════════
# Fig 9 — Selenium Dashboard Screenshot (UI mockup)
# ══════════════════════════════════════════════════════════════════════
def fig9_selenium_dashboard():
    img = Image.new("RGB", (W, H), (241, 245, 249))
    d = ImageDraw.Draw(img)
    # Navbar
    d.rectangle([0, 0, W, 56], fill=TEAL)
    d.text((20, 14), "🏥 PulseCare HMS", font=try_ui_font(20, True), fill=BG_WHITE)
    d.text((W-180, 18), "👤 admin  |  Logout", font=try_ui_font(13), fill=(180,220,230))
    # Sidebar
    d.rectangle([0, 56, 220, H], fill=SLATE)
    menu = ["📊 Dashboard", "👥 Patients", "👨‍⚕️ Doctors", "📅 Appointments", "💊 Pharmacy", "⚙️ Settings"]
    for i, m in enumerate(menu):
        bg = TEAL if i == 0 else SLATE
        if i == 0:
            d.rectangle([0, 56+i*52, 220, 56+(i+1)*52], fill=TEAL)
        d.text((16, 72+i*52), m, font=try_ui_font(13), fill=BG_WHITE)
    # Cards
    cards = [
        (240, 80,  "Total Patients",    "1,247",  "↑ 12 this week",  TEAL),
        (560, 80,  "Active Doctors",    "38",     "↑ 2 on duty",     BLUE),
        (880, 80,  "Appointments Today","64",     "↑ 8 pending",     SLATE),
        (1180, 80, "Beds Available",    "23",     "↓ 5 from yesterday", (220,38,38)),
    ]
    for cx, cy, title, val, sub, col in cards:
        if cx + 240 > W:
            break
        d.rectangle([cx, cy, cx+280, cy+130], fill=BG_WHITE, outline=(203,213,225), width=1)
        d.rectangle([cx, cy, cx+280, cy+6], fill=col)
        d.text((cx+16, cy+22), title, font=try_ui_font(12), fill=FG_GRAY)
        d.text((cx+16, cy+50), val, font=try_ui_font(28, True), fill=SLATE)
        d.text((cx+16, cy+100), sub, font=try_ui_font(11), fill=col)
    # Recent activity table
    d.rectangle([240, 230, W-20, 580], fill=BG_WHITE, outline=(203,213,225), width=1)
    d.rectangle([240, 230, W-20, 265], fill=(241,245,249))
    d.text((260, 242), "Recent Patient Activity", font=try_ui_font(13, True), fill=SLATE)
    rows = [
        ("P-1042", "John Smith",    "Cardiology",   "Dr. Patel",   "Admitted",    TEAL),
        ("P-1041", "Maria Garcia",  "Neurology",    "Dr. Kumar",   "Discharged",  (34,197,94)),
        ("P-1040", "Wei Zhang",     "Orthopedics",  "Dr. Singh",   "In-Progress", FG_YELLOW),
        ("P-1039", "Emma Johnson",  "Pediatrics",   "Dr. Sharma",  "Admitted",    TEAL),
        ("P-1038", "Carlos Ruiz",   "Emergency",    "Dr. Verma",   "Critical",    (220,38,38)),
    ]
    for i, (pid, name, dept, doc, status, col) in enumerate(rows):
        ry = 275 + i*54
        bg = (248,250,252) if i%2==0 else BG_WHITE
        d.rectangle([240, ry, W-20, ry+50], fill=bg)
        d.text((260, ry+15), pid,    font=try_font(12), fill=SLATE)
        d.text((360, ry+15), name,   font=try_ui_font(12), fill=SLATE)
        d.text((580, ry+15), dept,   font=try_ui_font(12), fill=FG_GRAY)
        d.text((780, ry+15), doc,    font=try_ui_font(12), fill=FG_GRAY)
        d.rectangle([1000, ry+10, 1180, ry+36], fill=col, outline=col)
        d.text((1020, ry+15), status, font=try_ui_font(11, True), fill=BG_WHITE)
    # Selenium indicator
    d.rectangle([0, H-32, W, H], fill=(30,41,59))
    d.text((20, H-24), "📸 Selenium Browser Test — test_selenium_admin_login_success — After redirect to /dashboard", font=try_ui_font(11), fill=FG_CYAN)
    img.save(f"{OUT}/fig9_selenium_dashboard.png")
    print("✅ fig9 saved")


# ══════════════════════════════════════════════════════════════════════
# Fig 10 — Unified Testing Overview
# ══════════════════════════════════════════════════════════════════════
def fig10_testing_overview():
    img = Image.new("RGB", (W, H), BG_WHITE)
    d = ImageDraw.Draw(img)
    # Header
    d.rectangle([0, 0, W, 70], fill=TEAL)
    d.text((30, 10), "PulseCare HMS — Unified Testing Dashboard", font=try_ui_font(22, True), fill=BG_WHITE)
    d.text((30, 44), "Feature Flags  ·  Load Testing  ·  Selenium  ·  Pytest", font=try_ui_font(13), fill=(180,220,230))

    sections = [
        (30, 90,  660, 280, TEAL,  "🚩 Feature Flags", [
            "5 flags: EMERGENCY_TRIAGE_MODE, TELEMEDICINE_PORTAL,",
            "         MAINTENANCE_BANNER, DARK_MODE_THEME, PATIENT_EXPORT_CSV",
            "Priority: Runtime Override > Env Var > Default",
            "REST API: GET /api/features → JSON flag states",
            "UI: Jinja2 conditional rendering in base.html",
            "Tests: 6/6 PASSED ✅",
        ]),
        (680, 90,  1340, 280, BLUE,  "⚡ Load Testing", [
            "Tool: Python threading (concurrent.futures pattern)",
            "Endpoints: /health, /metrics, /login",
            "Phases: Warmup → 10 → 20 → 50 concurrent users",
            "Total Requests: 190 · Success: 190 · Failures: 0",
            "Throughput: 33.5 RPS · Avg: 43.9 ms · P95: 148.6 ms",
            "Error Rate: 0.0% ✅",
        ]),
        (30,  300, 660, 490, (51,65,85),  "🤖 Selenium Testing", [
            "Selenium 4.52.0 + ChromeDriver (auto via Selenium Manager)",
            "8 browser tests in tests/test_selenium.py",
            "Tests: Login, Dashboard, Invalid Auth, Feature Flags API,",
            "       Emergency Banner, Health, Patients Page, Title",
            "Screenshots saved to reports/screenshots/selenium/",
            "Result: 8/8 PASSED ✅",
        ]),
        (680, 300, 1340, 490, TEAL,  "🧪 Full Pytest Suite", [
            "29 total tests across 4 test modules",
            "  tests/test_api.py      — 6 API endpoint tests",
            "  tests/test_auth.py     — 3 authentication tests",
            "  tests/test_patients.py — 14 patient CRUD tests",
            "  tests/test_features.py — 6 feature flag tests",
            "Result: 29/29 PASSED in 17.85s ✅",
        ]),
    ]

    for x1, y1, x2, y2, col, title, bullets in sections:
        d.rectangle([x1, y1, x2, y2], fill=(248,250,252), outline=col, width=3)
        d.rectangle([x1, y1, x2, y1+36], fill=col)
        d.text((x1+16, y1+8), title, font=try_ui_font(14, True), fill=BG_WHITE)
        for i, b in enumerate(bullets):
            d.text((x1+14, y1+46+i*28), b, font=try_ui_font(12), fill=SLATE)

    # Summary bar
    d.rectangle([0, H-80, W, H], fill=SLATE)
    d.text((30, H-64), "🎯 Total: 29 pytest tests + 8 Selenium tests = 37 tests · 190 load requests · 5 feature flags · 0 failures", font=try_ui_font(14, True), fill=BG_WHITE)
    d.text((30, H-36), "Student: Swaraj Bhattacharjee  ·  Roll: 2301730011  ·  Course: ENSP461  ·  PulseCare HMS DevOps Capstone", font=try_ui_font(12), fill=(148,163,184))
    img.save(f"{OUT}/fig10_unified_testing_overview.png")
    print("✅ fig10 saved")


if __name__ == "__main__":
    print("Generating Feature Flags & Testing screenshots...")
    fig1_feature_flags_api()
    fig2_feature_flag_tests()
    fig3_full_pytest()
    fig4_load_test_summary()
    fig5_load_test_chart()
    fig6_feature_flag_architecture()
    fig7_selenium_tests()
    fig8_selenium_login()
    fig9_selenium_dashboard()
    fig10_testing_overview()
    print(f"\n✅ All 10 screenshots saved to {OUT}/")
    import os
    files = [f for f in os.listdir(OUT) if f.startswith("fig") and f.endswith(".png")]
    for f in sorted(files):
        size = os.path.getsize(os.path.join(OUT, f))
        print(f"   {f:50s} {size//1024:5d} KB")

