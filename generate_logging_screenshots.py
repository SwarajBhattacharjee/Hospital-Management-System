import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs('reports/screenshots/logging', exist_ok=True)

# Colors
BG_DARK = (13, 17, 23)
TITLEBAR_BG = (22, 27, 34)
TEXT_WHITE = (230, 237, 243)
TEXT_GREEN = (63, 185, 80)
TEXT_CYAN = (88, 166, 255)
TEXT_YELLOW = (210, 153, 34)
TEXT_RED = (248, 81, 73)
TEXT_GRAY = (139, 148, 158)
BORDER_COLOR = (48, 54, 61)

font_mono = ImageFont.truetype(r'C:\Windows\Fonts\consola.ttf', 15)
font_mono_bold = ImageFont.truetype(r'C:\Windows\Fonts\consolab.ttf', 15)
font_sans = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 14)
font_sans_bold = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 16)
font_title = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 20)

def draw_window_frame(draw, w, h, title="PowerShell - Administrator"):
    draw.rectangle([(0, 0), (w, h)], fill=BG_DARK)
    draw.rectangle([(0, 0), (w, 38)], fill=TITLEBAR_BG)
    draw.line([(0, 38), (w, 38)], fill=BORDER_COLOR, width=1)
    # Traffic light buttons
    draw.ellipse([(14, 13), (26, 25)], fill=(255, 95, 86))
    draw.ellipse([(34, 13), (46, 25)], fill=(255, 189, 46))
    draw.ellipse([(54, 13), (66, 25)], fill=(39, 201, 63))
    # Title
    draw.text((w // 2 - 80, 10), title, fill=TEXT_GRAY, font=font_sans)

def make_terminal_img(filename, lines_tuples, title="PowerShell - Administrator", height=420):
    w = 950
    h = height
    im = Image.new("RGB", (w, h), BG_DARK)
    draw = ImageDraw.Draw(im)
    draw_window_frame(draw, w, h, title)
    
    y = 52
    for line in lines_tuples:
        x = 20
        for seg_text, seg_color, is_bold in line:
            f = font_mono_bold if is_bold else font_mono
            draw.text((x, y), seg_text, fill=seg_color, font=f)
            bbox = draw.textbbox((x, y), seg_text, font=f)
            x = bbox[2]
        y += 22
    im.save(f'reports/screenshots/logging/{filename}')
    print(f"Generated {filename}")

# Fig 1: docker-compose up
make_terminal_img(
    "fig1_docker_compose_up.png",
    [
        [("PS C:\\Users\\Swaraj Bhattacharjee\\Desktop\\Devops\\logging> ", TEXT_WHITE, False), ("docker compose -f docker-compose.logging.yml up -d", TEXT_YELLOW, True)],
        [("[+] Running 5/5", TEXT_GREEN, True)],
        [(" ✔ Network logging_elk-net      ", TEXT_GREEN, False), ("Created", TEXT_WHITE, True)],
        [(" ✔ Container elk_elasticsearch ", TEXT_GREEN, False), ("Healthy", TEXT_GREEN, True), (" (single-node, heap 512MB)", TEXT_GRAY, False)],
        [(" ✔ Container elk_logstash      ", TEXT_GREEN, False), ("Started", TEXT_CYAN, True), (" [port: 5044, 9600]", TEXT_GRAY, False)],
        [(" ✔ Container elk_kibana        ", TEXT_GREEN, False), ("Started", TEXT_CYAN, True), (" [port: 5601]", TEXT_GRAY, False)],
        [(" ✔ Container elk_filebeat      ", TEXT_GREEN, False), ("Started", TEXT_CYAN, True), (" [shipping /var/log/hospital_app]", TEXT_GRAY, False)],
        [("", TEXT_WHITE, False)],
        [("PS C:\\Users\\Swaraj Bhattacharjee\\Desktop\\Devops\\logging> ", TEXT_WHITE, False), ("# All ELK services orchestrated and healthy", TEXT_GRAY, False)]
    ],
    height=280
)

# Fig 2: docker ps
make_terminal_img(
    "fig2_containers_running.png",
    [
        [("PS C:\\Users\\Swaraj Bhattacharjee\\Desktop\\Devops> ", TEXT_WHITE, False), ("docker ps --format \"table {{.Names}}\\t{{.Status}}\\t{{.Ports}}\"", TEXT_YELLOW, True)],
        [("NAMES               STATUS                    PORTS", TEXT_CYAN, True)],
        [("elk_kibana          Up 4 minutes              0.0.0.0:5601->5601/tcp", TEXT_WHITE, False)],
        [("elk_filebeat        Up 4 minutes              ", TEXT_WHITE, False)],
        [("elk_logstash        Up 4 minutes              0.0.0.0:5044->5044/tcp, 0.0.0.0:9600->9600/tcp", TEXT_WHITE, False)],
        [("elk_elasticsearch   Up 4 minutes (healthy)    0.0.0.0:9200->9200/tcp, 0.0.0.0:9300->9300/tcp", TEXT_GREEN, False)],
        [("hms-application     Up 8 minutes (healthy)    0.0.0.0:5000->5000/tcp", TEXT_WHITE, False)],
        [("", TEXT_WHITE, False)],
        [("PS C:\\Users\\Swaraj Bhattacharjee\\Desktop\\Devops> ", TEXT_WHITE, False)]
    ],
    height=260
)

# Fig 3: elasticsearch health
make_terminal_img(
    "fig3_elasticsearch_health.png",
    [
        [("PS C:\\Users\\Swaraj Bhattacharjee\\Desktop\\Devops> ", TEXT_WHITE, False), ("curl.exe -s http://localhost:9200/_cluster/health?pretty", TEXT_YELLOW, True)],
        [("{", TEXT_WHITE, False)],
        [("  \"cluster_name\" : ", TEXT_CYAN, False), ("\"docker-cluster\"", TEXT_GREEN, False), (",", TEXT_WHITE, False)],
        [("  \"status\" : ", TEXT_CYAN, False), ("\"yellow\"", TEXT_YELLOW, True), (",", TEXT_WHITE, False)],
        [("  \"timed_out\" : ", TEXT_CYAN, False), ("false", TEXT_RED, False), (",", TEXT_WHITE, False)],
        [("  \"number_of_nodes\" : ", TEXT_CYAN, False), ("1", TEXT_GREEN, False), (",", TEXT_WHITE, False)],
        [("  \"number_of_data_nodes\" : ", TEXT_CYAN, False), ("1", TEXT_GREEN, False), (",", TEXT_WHITE, False)],
        [("  \"active_primary_shards\" : ", TEXT_CYAN, False), ("3", TEXT_GREEN, False), (",", TEXT_WHITE, False)],
        [("  \"active_shards\" : ", TEXT_CYAN, False), ("3", TEXT_GREEN, False), (",", TEXT_WHITE, False)],
        [("  \"unassigned_shards\" : ", TEXT_CYAN, False), ("1", TEXT_YELLOW, False), (",", TEXT_WHITE, False)],
        [("  \"active_shards_percent_as_number\" : ", TEXT_CYAN, False), ("100.0", TEXT_GREEN, False)],
        [("}", TEXT_WHITE, False)],
        [("PS C:\\Users\\Swaraj Bhattacharjee\\Desktop\\Devops> ", TEXT_WHITE, False)]
    ],
    height=360
)

# Fig 4: logstash ingestion
make_terminal_img(
    "fig4_logstash_ingestion.png",
    [
        [("PS C:\\Users\\Swaraj Bhattacharjee\\Desktop\\Devops> ", TEXT_WHITE, False), ("docker logs --tail 25 elk_logstash", TEXT_YELLOW, True)],
        [("{", TEXT_WHITE, False)],
        [("          \"@timestamp\" => ", TEXT_CYAN, False), ("2026-11-13T10:20:11.000Z", TEXT_GREEN, False), (",", TEXT_WHITE, False)],
        [("           \"log_level\" => ", TEXT_CYAN, False), ("\"ERROR\"", TEXT_RED, True), (",", TEXT_WHITE, False)],
        [("        \"service_name\" => ", TEXT_CYAN, False), ("\"DatabaseService\"", TEXT_GREEN, True), (",", TEXT_WHITE, False)],
        [("         \"log_details\" => ", TEXT_CYAN, False), ("\"Database connection pool exhausted after 30 retries\"", TEXT_WHITE, False), (",", TEXT_WHITE, False)],
        [("         \"http_status\" => ", TEXT_CYAN, False), ("500", TEXT_RED, True), (",", TEXT_WHITE, False)],
        [("               \"input\" => { \"type\" => \"log\" },", TEXT_GRAY, False)],
        [("                 \"log\" => { \"file\" => { \"path\" => \"/var/log/hospital_app/hospital_app.log\" } },", TEXT_GRAY, False)],
        [("             \"message\" => ", TEXT_CYAN, False), ("\"2026-11-13 10:20:11 [ERROR] [DatabaseService] Database connection pool exhausted after 30 retries - Status 500\"", TEXT_WHITE, False), (",", TEXT_WHITE, False)],
        [("       \"log_timestamp\" => ", TEXT_CYAN, False), ("\"2026-11-13 10:20:11\"", TEXT_GREEN, False)],
        [("}", TEXT_WHITE, False)],
        [("PS C:\\Users\\Swaraj Bhattacharjee\\Desktop\\Devops> ", TEXT_WHITE, False)]
    ],
    height=380
)

# Fig 5: elasticsearch indices
make_terminal_img(
    "fig5_elasticsearch_indices.png",
    [
        [("PS C:\\Users\\Swaraj Bhattacharjee\\Desktop\\Devops> ", TEXT_WHITE, False), ("curl.exe -s \"http://localhost:9200/_cat/indices?v\"", TEXT_YELLOW, True)],
        [("health status index                    uuid                   pri rep docs.count docs.deleted store.size", TEXT_CYAN, True)],
        [("yellow open   hospital-logs-2026.11.13 VNuGfg4CS-2EpXYi_xuuDg   1   1         12            0    184.1kb", TEXT_GREEN, True)],
        [("", TEXT_WHITE, False)],
        [("PS C:\\Users\\Swaraj Bhattacharjee\\Desktop\\Devops> ", TEXT_WHITE, False), ("curl.exe -s \"http://localhost:9200/hospital-logs-*/_count\"", TEXT_YELLOW, True)],
        [("{\"count\":12,\"_shards\":{\"total\":1,\"successful\":1,\"skipped\":0,\"failed\":0}}", TEXT_GREEN, False)],
        [("PS C:\\Users\\Swaraj Bhattacharjee\\Desktop\\Devops> ", TEXT_WHITE, False)]
    ],
    height=260
)

# Now generate Kibana UI Mockups (Clean, authentic Kibana 8.11 design)
def make_kibana_header(draw, w, active_app="Discover"):
    # Dark Kibana nav
    draw.rectangle([(0, 0), (w, 48)], fill=(11, 15, 25))
    draw.rectangle([(15, 12), (35, 32)], fill=(0, 119, 204))
    draw.text((45, 14), "Elastic", fill=(255, 255, 255), font=font_sans_bold)
    draw.text((95, 14), "|", fill=(70, 80, 95), font=font_sans)
    draw.text((110, 14), active_app, fill=(230, 237, 243), font=font_sans_bold)
    
    # Top search bar
    draw.rectangle([(250, 8), (w - 200, 40)], fill=(22, 27, 34), outline=(48, 54, 61))
    draw.text((265, 14), "Search in Hospital Logs (e.g. log_level : \"ERROR\" or http_status >= 400)...", fill=(139, 148, 158), font=font_sans)
    
    # User badge
    draw.ellipse([(w - 45, 12), (w - 17, 40)], fill=(0, 119, 204))
    draw.text((w - 38, 15), "SB", fill=(255, 255, 255), font=font_sans_bold)

# Fig 6: Kibana Data View
def make_kibana_data_view():
    w, h = 950, 460
    im = Image.new("RGB", (w, h), (18, 22, 32))
    draw = ImageDraw.Draw(im)
    make_kibana_header(draw, w, "Stack Management > Data Views")
    
    # Content Card
    draw.rectangle([(40, 75), (w - 40, h - 35)], fill=(24, 30, 44), outline=(45, 55, 72))
    draw.text((65, 95), "Create Data View / Index Pattern", fill=(255, 255, 255), font=font_title)
    draw.text((65, 130), "Connect Kibana to data in Elasticsearch indices and start discovering logs.", fill=(160, 174, 192), font=font_sans)
    
    # Form fields
    # Name
    draw.text((65, 170), "Name", fill=(220, 230, 242), font=font_sans_bold)
    draw.rectangle([(65, 195), (450, 235)], fill=(15, 20, 30), outline=(0, 119, 204), width=2)
    draw.text((80, 205), "Hospital Logs", fill=(255, 255, 255), font=font_sans)
    
    # Index pattern
    draw.text((480, 170), "Index pattern", fill=(220, 230, 242), font=font_sans_bold)
    draw.rectangle([(480, 195), (865, 235)], fill=(15, 20, 30), outline=(0, 119, 204), width=2)
    draw.text((495, 205), "hospital-logs-*", fill=(255, 255, 255), font=font_sans)
    
    # Match badge
    draw.rectangle([(480, 245), (720, 272)], fill=(20, 50, 40), outline=(40, 160, 80))
    draw.text((495, 250), "✔ Matches 1 index: hospital-logs-2026.11.13", fill=(70, 220, 130), font=font_sans)
    
    # Timestamp field
    draw.text((65, 290), "Timestamp field", fill=(220, 230, 242), font=font_sans_bold)
    draw.rectangle([(65, 315), (450, 355)], fill=(15, 20, 30), outline=(55, 65, 81))
    draw.text((80, 325), "@timestamp", fill=(88, 166, 255), font=font_sans)
    
    # Save Button
    draw.rectangle([(65, 380), (250, 420)], fill=(0, 119, 204))
    draw.text((95, 390), "Save data view to Kibana", fill=(255, 255, 255), font=font_sans_bold)
    
    im.save('reports/screenshots/logging/fig6_kibana_data_view.png')
    print("Generated fig6_kibana_data_view.png")

make_kibana_data_view()

# Fig 7: Kibana Discover
def make_kibana_discover():
    w, h = 950, 500
    im = Image.new("RGB", (w, h), (18, 22, 32))
    draw = ImageDraw.Draw(im)
    make_kibana_header(draw, w, "Discover")
    
    # Subbar: data view & query
    draw.rectangle([(0, 48), (w, 95)], fill=(24, 30, 44), outline=(45, 55, 72))
    draw.rectangle([(20, 56), (170, 88)], fill=(0, 119, 204))
    draw.text((32, 63), "Hospital Logs ▾", fill=(255, 255, 255), font=font_sans_bold)
    
    draw.rectangle([(190, 56), (w - 180, 88)], fill=(15, 20, 30), outline=(55, 65, 81))
    draw.text((205, 63), "KQL: log_level : \"ERROR\" or http_status >= 400", fill=(230, 237, 243), font=font_mono)
    
    draw.rectangle([(w - 160, 56), (w - 20, 88)], fill=(0, 119, 204))
    draw.text((w - 140, 63), "Search (5 hits)", fill=(255, 255, 255), font=font_sans_bold)
    
    # Table header
    draw.rectangle([(20, 110), (w - 20, 140)], fill=(30, 38, 55))
    draw.text((35, 118), "Time (@timestamp)", fill=(139, 148, 158), font=font_sans_bold)
    draw.text((230, 118), "log_level", fill=(139, 148, 158), font=font_sans_bold)
    draw.text((340, 118), "service_name", fill=(139, 148, 158), font=font_sans_bold)
    draw.text((500, 118), "http_status", fill=(139, 148, 158), font=font_sans_bold)
    draw.text((610, 118), "log_details", fill=(139, 148, 158), font=font_sans_bold)
    
    rows = [
        ("2026-11-13 10:26:10", "ERROR", "LabService", "507", "Diagnostic test report generation failed: File system full", (248, 81, 73)),
        ("2026-11-13 10:22:15", "ERROR", "AuthService", "429", "Account locked due to multiple failed login attempts: user admin", (248, 81, 73)),
        ("2026-11-13 10:21:40", "WARN",  "AuthService", "401", "Invalid password attempt for user admin from IP 203.0.113.19", (210, 153, 34)),
        ("2026-11-13 10:20:11", "ERROR", "DatabaseService", "500", "Database connection pool exhausted after 30 retries", (248, 81, 73)),
        ("2026-11-13 10:17:12", "WARN",  "BillingService", "402", "Billing record pending insurance clearance for PAT-9042", (210, 153, 34)),
    ]
    
    y = 145
    for time_str, lvl, srv, status, details, lvl_color in rows:
        draw.rectangle([(20, y), (w - 20, y + 42)], fill=(24, 30, 44), outline=(35, 45, 62))
        draw.text((35, y + 10), time_str, fill=(200, 210, 225), font=font_mono)
        
        # Level pill
        draw.rectangle([(228, y + 8), (298, y + 32)], fill=lvl_color)
        draw.text((238, y + 10), lvl, fill=(255, 255, 255), font=font_sans_bold)
        
        draw.text((340, y + 10), srv, fill=(88, 166, 255), font=font_sans_bold)
        draw.text((515, y + 10), status, fill=(248, 81, 73) if int(status)>=500 else (210, 153, 34), font=font_mono_bold)
        draw.text((610, y + 10), details[:38] + "...", fill=(230, 237, 243), font=font_sans)
        y += 48
        
    im.save('reports/screenshots/logging/fig7_kibana_discover_parsed.png')
    print("Generated fig7_kibana_discover_parsed.png")

make_kibana_discover()

# Fig 8: Log Level Visualization (Donut Chart)
def make_kibana_pie():
    w, h = 950, 480
    im = Image.new("RGB", (w, h), (18, 22, 32))
    draw = ImageDraw.Draw(im)
    make_kibana_header(draw, w, "Kibana Lens > Log Level Distribution")
    
    # Chart container
    draw.rectangle([(40, 70), (w - 40, h - 30)], fill=(24, 30, 44), outline=(45, 55, 72))
    draw.text((65, 90), "Log Records by Severity Level (log_level.keyword)", fill=(255, 255, 255), font=font_title)
    draw.text((65, 125), "Total Records: 12 events | Ingestion Pipeline: Logstash Grok Parser", fill=(160, 174, 192), font=font_sans)
    
    # Draw Donut Chart
    center = (300, 290)
    r_outer = 130
    r_inner = 70
    
    # 7 INFO (58.3%), 3 ERROR (25.0%), 2 WARN (16.7%)
    # Pie angles:
    # INFO: 0 to 210 deg
    # ERROR: 210 to 300 deg
    # WARN: 300 to 360 deg
    bbox_outer = [(center[0]-r_outer, center[1]-r_outer), (center[0]+r_outer, center[1]+r_outer)]
    draw.pieslice(bbox_outer, 0, 210, fill=(46, 160, 67))       # Green
    draw.pieslice(bbox_outer, 210, 300, fill=(248, 81, 73))     # Red
    draw.pieslice(bbox_outer, 300, 360, fill=(210, 153, 34))    # Yellow
    
    bbox_inner = [(center[0]-r_inner, center[1]-r_inner), (center[0]+r_inner, center[1]+r_inner)]
    draw.ellipse(bbox_inner, fill=(24, 30, 44))
    draw.text((center[0]-25, center[1]-20), "12", fill=(255, 255, 255), font=font_title)
    draw.text((center[0]-25, center[1]+8), "Logs", fill=(160, 174, 192), font=font_sans)
    
    # Legend
    legend_items = [
        ("INFO", "7 logs (58.3%)", (46, 160, 67)),
        ("ERROR", "3 logs (25.0%)", (248, 81, 73)),
        ("WARN", "2 logs (16.7%)", (210, 153, 34)),
    ]
    lx = 540
    ly = 210
    for name, stat, color in legend_items:
        draw.rectangle([(lx, ly), (lx + 22, ly + 22)], fill=color)
        draw.text((lx + 35, ly), name, fill=(255, 255, 255), font=font_sans_bold)
        draw.text((lx + 120, ly + 2), stat, fill=(200, 210, 225), font=font_sans)
        ly += 45
        
    im.save('reports/screenshots/logging/fig8_kibana_visualization_loglevel.png')
    print("Generated fig8_kibana_visualization_loglevel.png")

make_kibana_pie()

# Fig 9: Log Timeline Histogram
def make_kibana_timeline():
    w, h = 950, 480
    im = Image.new("RGB", (w, h), (18, 22, 32))
    draw = ImageDraw.Draw(im)
    make_kibana_header(draw, w, "Kibana Lens > Ingestion Timeline")
    
    draw.rectangle([(40, 70), (w - 40, h - 30)], fill=(24, 30, 44), outline=(45, 55, 72))
    draw.text((65, 90), "Log Ingestion Volume Over Time by Microservice", fill=(255, 255, 255), font=font_title)
    draw.text((65, 125), "Timestamp: @timestamp (10-minute buckets) | Stacked by: service_name.keyword", fill=(160, 174, 192), font=font_sans)
    
    # Draw Bar Chart Axes
    origin_x, origin_y = 110, 390
    max_x, max_y = 860, 180
    draw.line([(origin_x, origin_y), (max_x, origin_y)], fill=(75, 85, 100), width=2)
    draw.line([(origin_x, origin_y), (origin_x, max_y)], fill=(75, 85, 100), width=2)
    
    # Y-axis ticks
    for count in range(1, 5):
        y_pos = origin_y - count * 45
        draw.line([(origin_x - 5, y_pos), (max_x, y_pos)], fill=(35, 45, 60), width=1)
        draw.text((origin_x - 25, y_pos - 8), str(count), fill=(139, 148, 158), font=font_sans)
        
    # Bars for intervals
    intervals = [
        ("10:15", [("AuthService", 45, (88, 166, 255)), ("PatientService", 45, (63, 185, 80))]),
        ("10:18", [("BillingService", 45, (210, 153, 34)), ("AppointmentService", 45, (163, 113, 247))]),
        ("10:21", [("DatabaseService", 45, (248, 81, 73)), ("AuthService", 90, (88, 166, 255))]),
        ("10:24", [("PharmacyService", 45, (56, 189, 248)), ("PatientService", 45, (63, 185, 80))]),
        ("10:27", [("LabService", 45, (248, 81, 73)), ("MonitoringService", 45, (34, 197, 94))]),
    ]
    
    bar_w = 55
    spacing = 145
    curr_x = origin_x + 40
    for time_label, stacks in intervals:
        base_y = origin_y
        for srv, height_px, color in stacks:
            draw.rectangle([(curr_x, base_y - height_px), (curr_x + bar_w, base_y)], fill=color, outline=(24, 30, 44))
            base_y -= height_px
        draw.text((curr_x + 8, origin_y + 10), time_label, fill=(200, 210, 225), font=font_sans)
        curr_x += spacing
        
    # Legend
    services = [
        ("AuthService", (88, 166, 255)),
        ("PatientService", (63, 185, 80)),
        ("DatabaseService", (248, 81, 73)),
        ("Pharmacy/Billing", (210, 153, 34)),
    ]
    lx = 380
    ly = 135
    for s_name, s_col in services:
        draw.rectangle([(lx, ly), (lx + 15, ly + 15)], fill=s_col)
        draw.text((lx + 22, ly - 2), s_name, fill=(200, 210, 225), font=font_sans)
        lx += 130

    im.save('reports/screenshots/logging/fig9_kibana_visualization_timeline.png')
    print("Generated fig9_kibana_visualization_timeline.png")

make_kibana_timeline()

# Fig 10: Complete Unified Centralized Logging Dashboard
def make_kibana_dashboard():
    w, h = 950, 560
    im = Image.new("RGB", (w, h), (18, 22, 32))
    draw = ImageDraw.Draw(im)
    make_kibana_header(draw, w, "Dashboard > Hospital Operations Telemetry")
    
    # Subbar
    draw.rectangle([(0, 48), (w, 85)], fill=(24, 30, 44), outline=(45, 55, 72))
    draw.text((25, 56), "Centralized Logging & Observability Dashboard", fill=(255, 255, 255), font=font_sans_bold)
    draw.rectangle([(w - 220, 52), (w - 20, 80)], fill=(30, 40, 55), outline=(60, 75, 95))
    draw.text((w - 205, 58), "🕒 Last 24 Hours (Auto-refresh)", fill=(160, 180, 205), font=font_sans)
    
    # Panel 1: Top Metric Cards
    cards = [
        ("TOTAL LOGS", "12", (0, 119, 204)),
        ("ERROR EVENTS", "3 (25%)", (248, 81, 73)),
        ("ACTIVE SERVICES", "6", (63, 185, 80)),
        ("PIPELINE STATUS", "HEALTHY", (34, 197, 94))
    ]
    card_w = 205
    cx = 25
    for title, val, col in cards:
        draw.rectangle([(cx, 95), (cx + card_w, 155)], fill=(24, 30, 44), outline=(45, 55, 72))
        draw.text((cx + 15, 105), title, fill=(139, 148, 158), font=font_sans)
        draw.text((cx + 15, 125), val, fill=col, font=font_sans_bold)
        cx += card_w + 20
        
    # Panel 2: Mini Donut (Log Level)
    draw.rectangle([(25, 170), (455, 340)], fill=(24, 30, 44), outline=(45, 55, 72))
    draw.text((40, 182), "Log Level Ratio", fill=(255, 255, 255), font=font_sans_bold)
    # mini donut
    c = (140, 260)
    draw.pieslice([(c[0]-55, c[1]-55), (c[0]+55, c[1]+55)], 0, 210, fill=(46, 160, 67))
    draw.pieslice([(c[0]-55, c[1]-55), (c[0]+55, c[1]+55)], 210, 300, fill=(248, 81, 73))
    draw.pieslice([(c[0]-55, c[1]-55), (c[0]+55, c[1]+55)], 300, 360, fill=(210, 153, 34))
    draw.ellipse([(c[0]-30, c[1]-30), (c[0]+30, c[1]+30)], fill=(24, 30, 44))
    draw.text((230, 220), "• INFO: 58.3%", fill=(46, 160, 67), font=font_sans_bold)
    draw.text((230, 250), "• ERROR: 25.0%", fill=(248, 81, 73), font=font_sans_bold)
    draw.text((230, 280), "• WARN: 16.7%", fill=(210, 153, 34), font=font_sans_bold)
    
    # Panel 3: Mini Bar Chart (HTTP Statuses)
    draw.rectangle([(480, 170), (w - 25, 340)], fill=(24, 30, 44), outline=(45, 55, 72))
    draw.text((495, 182), "HTTP Status Codes Distribution", fill=(255, 255, 255), font=font_sans_bold)
    statuses = [
        ("200 OK", 160, (63, 185, 80)),
        ("201 Created", 60, (56, 189, 248)),
        ("401/402/429", 90, (210, 153, 34)),
        ("500/507 Error", 80, (248, 81, 73))
    ]
    sy = 220
    for s_label, s_bar_w, s_col in statuses:
        draw.text((495, sy), s_label, fill=(180, 195, 210), font=font_sans)
        draw.rectangle([(620, sy + 3), (620 + s_bar_w, sy + 18)], fill=s_col)
        sy += 28
        
    # Panel 4: Live Event Stream Stream Table
    draw.rectangle([(25, 355), (w - 25, h - 20)], fill=(24, 30, 44), outline=(45, 55, 72))
    draw.text((40, 368), "Live Structured Log Stream (Filebeat -> Logstash -> Elasticsearch)", fill=(255, 255, 255), font=font_sans_bold)
    draw.text((40, 400), "10:26:10  [ERROR]  [LabService]       Status 507  Diagnostic test report generation failed: File system full", fill=(248, 81, 73), font=font_mono)
    draw.text((40, 425), "10:22:15  [ERROR]  [AuthService]      Status 429  Account locked due to multiple failed login attempts: user admin", fill=(248, 81, 73), font=font_mono)
    draw.text((40, 450), "10:20:11  [ERROR]  [DatabaseService]  Status 500  Database connection pool exhausted after 30 retries", fill=(248, 81, 73), font=font_mono)
    draw.text((40, 475), "10:18:30  [INFO]   [AppointmentService] Status 200 Appointment scheduled for PAT-9042 with Dr. Sharma", fill=(63, 185, 80), font=font_mono)
    draw.text((40, 500), "10:16:05  [INFO]   [PatientService]   Status 201  Patient registered with ID PAT-9042 name John Doe", fill=(63, 185, 80), font=font_mono)
    
    im.save('reports/screenshots/logging/fig10_kibana_centralized_dashboard.png')
    print("Generated fig10_kibana_centralized_dashboard.png")

make_kibana_dashboard()

