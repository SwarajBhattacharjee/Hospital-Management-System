import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import os

def create_report():
    doc = docx.Document()
    
    # 1. Page Margins (0.8 inches / 57.6 pt)
    for s in doc.sections:
        s.top_margin = Pt(57.6)
        s.bottom_margin = Pt(57.6)
        s.left_margin = Pt(57.6)
        s.right_margin = Pt(57.6)
        
    def add_title(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(22)
        run.bold = True
        run.font.color.rgb = RGBColor(15, 23, 42)
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(14)
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(71, 85, 105)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(14)
        run.bold = True
        run.font.color.rgb = RGBColor(14, 116, 144) # 0E7490
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(11.5)
        run.bold = True
        run.font.color.rgb = RGBColor(51, 65, 85) # 334155
        return p

    def add_body(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(51, 65, 85)
        return p

    def style_code_cell(cell, fill_hex="F8F9FA", left_border_hex="0284C7"):
        tcPr = cell._tc.get_or_add_tcPr()
        
        # Shading
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), fill_hex)
        tcPr.append(shd)
        
        # Borders
        tcBorders = OxmlElement('w:tcBorders')
        top = OxmlElement('w:top')
        top.set(qn('w:val'), 'single')
        top.set(qn('w:sz'), '6')
        top.set(qn('w:color'), 'E2E8F0')
        tcBorders.append(top)
        
        left = OxmlElement('w:left')
        left.set(qn('w:val'), 'single')
        left.set(qn('w:sz'), '24')
        left.set(qn('w:color'), left_border_hex)
        tcBorders.append(left)
        
        bottom = OxmlElement('w:bottom')
        bottom.set(qn('w:val'), 'single')
        bottom.set(qn('w:sz'), '6')
        bottom.set(qn('w:color'), 'E2E8F0')
        tcBorders.append(bottom)
        
        right = OxmlElement('w:right')
        right.set(qn('w:val'), 'single')
        right.set(qn('w:sz'), '6')
        right.set(qn('w:color'), 'E2E8F0')
        tcBorders.append(right)
        tcPr.append(tcBorders)
        
        # Margins
        tcMar = OxmlElement('w:tcMar')
        for side, width in [('top', '100'), ('bottom', '100'), ('left', '150'), ('right', '150')]:
            node = OxmlElement(f'w:{side}')
            node.set(qn('w:w'), width)
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    def add_code_block(code_text):
        t = doc.add_table(rows=1, cols=1)
        t.autofit = False
        t.columns[0].width = Inches(6.8)
        cell = t.rows[0].cells[0]
        style_code_cell(cell, fill_hex="F8F9FA", left_border_hex="0284C7")
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.05
        
        lines = code_text.strip().split('\n')
        for i, line in enumerate(lines):
            run = p.add_run(line + ('\n' if i < len(lines)-1 else ''))
            run.font.name = 'Consolas'
            run.font.size = Pt(8.5)
            run.font.color.rgb = RGBColor(30, 41, 59) # 1E293B

    def add_callout(quote_text):
        t = doc.add_table(rows=1, cols=1)
        t.autofit = False
        t.columns[0].width = Inches(6.8)
        cell = t.rows[0].cells[0]
        style_code_cell(cell, fill_hex="F0FDF4", left_border_hex="10B981") # Soft green
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(quote_text)
        run.font.name = 'Arial'
        run.font.size = Pt(10)
        run.bold = True
        run.font.color.rgb = RGBColor(14, 116, 144)

    def add_image_box(img_path, caption_text):
        if not os.path.exists(img_path):
            return
        t = doc.add_table(rows=1, cols=1)
        t.autofit = False
        t.columns[0].width = Inches(6.8)
        cell = t.rows[0].cells[0]
        style_code_cell(cell, fill_hex="FFFFFF", left_border_hex="CBD5E1")
        
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run()
        run.add_picture(img_path, width=Inches(6.4))
        
        cap_p = doc.add_paragraph()
        cap_p.paragraph_format.space_before = Pt(2)
        cap_p.paragraph_format.space_after = Pt(10)
        cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap_run = cap_p.add_run(caption_text)
        cap_run.font.name = 'Arial'
        cap_run.font.size = Pt(9)
        cap_run.italic = True
        cap_run.font.color.rgb = RGBColor(100, 116, 139)

    # ================= DOCUMENT CONTENT =================
    add_title("Centralized Logging & Telemetry Report")
    add_subtitle("Log Collection, Structured Parsing, and Real-Time Visualization using the ELK Stack")
    
    # Table 0: Metadata Table
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.autofit = False
    meta_table.columns[0].width = Inches(1.8)
    meta_table.columns[1].width = Inches(5.0)
    
    meta_data = [
        ("Student Name:", "Swaraj Bhattacharjee"),
        ("Roll Number:", "2301730011"),
        ("Course / Lab:", "DevOps & Automation Lab Capstone (ENSP461)"),
        ("Deliverable:", "Rubric Deliverable: Centralized Logging using ELK Stack (5 Marks)")
    ]
    for row_idx, (k, v) in enumerate(meta_data):
        r = meta_table.rows[row_idx]
        
        # Key cell
        c0 = r.cells[0]
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(2)
        p0.paragraph_format.space_after = Pt(2)
        run0 = p0.add_run(k)
        run0.font.name = 'Arial'
        run0.font.size = Pt(10)
        run0.bold = True
        run0.font.color.rgb = RGBColor(15, 23, 42)
        
        # Value cell
        c1 = r.cells[1]
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(2)
        p1.paragraph_format.space_after = Pt(2)
        run1 = p1.add_run(v)
        run1.font.name = 'Arial'
        run1.font.size = Pt(10)
        run1.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Section 1
    add_h1("1. Task Description & Rubric Objective")
    add_callout("Rubric Specification (5 Marks):\n“Implement centralized logging using the ELK stack and demonstrate log collection, parsing, and visualization in Kibana.”")
    
    add_body("This deliverable demonstrates the end-to-end design, implementation, and verification of a production-grade centralized logging and log analytics stack for the PulseCare Hospital Management System. Traditional decentralized logging—where application logs reside exclusively inside container writable layers or on disparate host filesystems—severely degrades incident resolution speed, prevents correlated troubleshooting across services, and introduces compliance liabilities. By shifting to the ELK (Elasticsearch, Logstash, Kibana) + Filebeat architecture, all system and application events are continuously harvested at the edge, structured into dimensional schemas via regular expression filters, indexed into a distributed search engine, and visualized in real time on Kibana dashboards.")

    # Section 2
    add_h1("2. Observability Architecture & Pipeline Design")
    add_h2("2.1 Telemetry Flow & Decoupled Log Processing Topology")
    add_body("The centralized logging pipeline implements a four-stage decoupled architecture ensuring minimal edge memory consumption, robust schema parsing, and sub-second analytical querying:")
    add_body("1. Lightweight Edge Harvester (Filebeat:8.11.3): Deployed as a micro-daemon with volume mounts to the application log directory ('/var/log/hospital_app'). Filebeat runs with an internal state registry, tracking read byte offsets to guarantee at-least-once delivery while respecting downstream backpressure signals over TCP port 5044.\n"
             "2. Stream Parsing & Enrichment Engine (Logstash:8.11.3): Ingests the raw Beats stream, executes custom Grok pattern extraction to parse unstructured text into typed fields ('log_timestamp', 'log_level', 'service_name', 'log_details', 'http_status'), normalizes the event timestamp into '@timestamp', and outputs structured JSON documents.\n"
             "3. Distributed Search & Analytics Storage (Elasticsearch:8.11.3): Serves as the persistence and inverted-index search engine. Ingested documents are partitioned across daily time-series indices ('hospital-logs-YYYY.MM.dd') for optimal lifecycle retention and query performance.\n"
             "4. Visualization & Log Investigation (Kibana:8.11.3): Connects to Elasticsearch over port 9200, provides a unified Data View ('hospital-logs-*'), and exposes Discover search tools alongside custom operational dashboards.")

    add_h2("2.2 Tracked Log Attributes & Schema Enforcement")
    add_body("The Logstash Grok filter enforces strict type mapping on all ingested telemetry:")
    add_body("• @timestamp (Date): Canonical UTC event time parsed from the application log line.\n"
             "• log_level (Keyword): Normalized uppercase severity classification ('INFO', 'WARN', 'ERROR').\n"
             "• service_name (Keyword): The emitting hospital microservice ('AuthService', 'PatientService', 'DatabaseService', 'LabService', etc.).\n"
             "• http_status (Integer): Numeric HTTP response code enabling numeric range filtering (e.g. 'http_status >= 500').\n"
             "• log_details (Text): High-cardinality descriptive event message with full-text search capability.")

    # Section 3
    add_h1("3. Configuration & Declarative Pipeline Specifications")
    add_body("All infrastructure, shipper configurations, and log-parsing rules were declared modularly under the 'logging/' directory:")

    add_h2("3.1 File: logging/docker-compose.logging.yml (Multi-Container ELK Orchestration)")
    compose_code = """services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.3
    container_name: elk_elasticsearch
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    healthcheck:
      test: ["CMD-SHELL", "curl -s http://localhost:9200/_cat/health | grep -q 'green\\\\|yellow'"]
      interval: 10s
      retries: 15
    networks:
      - elk-net

  logstash:
    image: docker.elastic.co/logstash/logstash:8.11.3
    container_name: elk_logstash
    volumes:
      - ./logstash/pipeline/logstash.conf:/usr/share/logstash/pipeline/logstash.conf:ro
    ports:
      - "5044:5044"
    networks:
      - elk-net
    depends_on:
      elasticsearch:
        condition: service_healthy

  filebeat:
    image: docker.elastic.co/beats/filebeat:8.11.3
    container_name: elk_filebeat
    user: root
    volumes:
      - ./filebeat/filebeat.yml:/usr/share/filebeat/filebeat.yml:ro
      - ./logs:/var/log/hospital_app:ro
    command: ["filebeat", "-e", "--strict.perms=false"]
    networks:
      - elk-net
    depends_on:
      - logstash

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.3
    container_name: elk_kibana
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    networks:
      - elk-net
    depends_on:
      elasticsearch:
        condition: service_healthy"""
    add_code_block(compose_code)

    add_h2("3.2 File: logging/logstash/pipeline/logstash.conf (Grok Parser & Output Mapping)")
    logstash_code = """input {
  beats {
    port => 5044
  }
}

filter {
  grok {
    match => {
      "message" => "^%{TIMESTAMP_ISO8601:log_timestamp} \\\\[%{WORD:log_level}\\\\] \\\\[%{WORD:service_name}\\\\] %{GREEDYDATA:log_details}(?: - Status %{NUMBER:http_status:int})?$"
    }
  }

  date {
    match => [ "log_timestamp", "yyyy-MM-dd HH:mm:ss" ]
    target => "@timestamp"
    timezone => "UTC"
  }

  mutate {
    uppercase => [ "log_level" ]
  }
}

output {
  elasticsearch {
    hosts => ["http://elasticsearch:9200"]
    index => "hospital-logs-%{+YYYY.MM.dd}"
  }
  
  stdout {
    codec => rubydebug
  }
}"""
    add_code_block(logstash_code)

    add_h2("3.3 File: logging/filebeat/filebeat.yml (Log Shipper Definition)")
    filebeat_code = """filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /var/log/hospital_app/*.log
    scan_frequency: 2s
    close_inactive: 5m

output.logstash:
  hosts: ["logstash:5044"]

logging.level: info
logging.to_files: false"""
    add_code_block(filebeat_code)

    # Section 4
    add_h1("4. Verification Evidence & Terminal Execution Logs")
    add_body("The centralized logging pipeline was launched, verified, and stress-tested using authentic CLI commands. The unedited execution logs and health inspection outputs are presented below:")

    add_h2("4.1 Multi-Container Stack Deployment (docker compose up -d)")
    add_image_box("reports/screenshots/logging/fig1_docker_compose_up.png", "Figure 1: Orchestrating the ELK Stack and Filebeat services via Docker Compose")

    add_h2("4.2 Container Runtime Status Verification (docker ps)")
    add_body("Running 'docker ps' confirms that all four ELK services along with the primary 'hms-application' container are active and healthy:")
    add_image_box("reports/screenshots/logging/fig2_containers_running.png", "Figure 2: Active container status confirming healthy states on bridge network logging_elk-net")

    add_h2("4.3 Elasticsearch Cluster Health Verification (curl.exe http://localhost:9200/_cluster/health)")
    add_body("Querying the Elasticsearch native cluster health API confirms primary shard allocations and active indexing capability:")
    add_image_box("reports/screenshots/logging/fig3_elasticsearch_health.png", "Figure 3: Elasticsearch cluster health endpoint confirming status 'yellow' on single-node cluster")

    add_h2("4.4 Logstash Real-Time Grok Ingestion & Rubydebug Output")
    add_body("Inspecting the Logstash container stream proves that raw filebeat entries are successfully decomposed into typed JSON fields:")
    add_image_box("reports/screenshots/logging/fig4_logstash_ingestion.png", "Figure 4: Logstash stdout logs showing successful Grok regex field extraction and date parsing")

    add_h2("4.5 Elasticsearch Daily Index Catalog Verification")
    add_body("Querying '_cat/indices' verifies that index 'hospital-logs-2026.11.13' was automatically created with 12 documents successfully stored:")
    add_image_box("reports/screenshots/logging/fig5_elasticsearch_indices.png", "Figure 5: Elasticsearch index catalog confirming document count and daily shard creation")

    # Section 5
    add_h1("5. Kibana Visualization & Operational Dashboards")
    add_body("With log records actively indexed in Elasticsearch, Kibana was configured to provide real-time search, filtering, and graphical dashboards.")

    add_h2("5.1 Kibana Data View Configuration (hospital-logs-*)")
    add_body("A Data View matching 'hospital-logs-*' with primary timestamp field '@timestamp' was registered:")
    add_image_box("reports/screenshots/logging/fig6_kibana_data_view.png", "Figure 6: Kibana Data View registration binding the daily index pattern to '@timestamp'")

    add_h2("5.2 Log Discovery & Filtering (Kibana Discover)")
    add_body("Navigating to Discover allows filtering by log levels, microservice names, and HTTP status codes using Kibana Query Language (KQL):")
    add_image_box("reports/screenshots/logging/fig7_kibana_discover_parsed.png", "Figure 7: Kibana Discover tab demonstrating parsed field columns and filtered ERROR logs")

    add_h2("5.3 Visual Analytics: Log Level Severity Distribution (Donut Chart)")
    add_body("Using Kibana Lens, a Donut Chart was constructed aggregating logs by 'log_level.keyword'. The visualization highlights that 58.3% of traffic is normal (INFO), 16.7% reflects operational warnings (WARN), and 25.0% surfaces critical failures (ERROR):")
    add_image_box("reports/screenshots/logging/fig8_kibana_visualization_loglevel.png", "Figure 8: Donut chart visualization in Kibana Lens depicting log volume across severity classifications")

    add_h2("5.4 Visual Analytics: Ingestion Timeline by Microservice (Histogram)")
    add_body("A stacked histogram charts log generation volume over 10-minute buckets broken down by emitting microservice ('service_name.keyword'):")
    add_image_box("reports/screenshots/logging/fig9_kibana_visualization_timeline.png", "Figure 9: Ingestion volume over time grouped by hospital microservice")

    add_h2("5.5 Centralized Logging Operations Dashboard")
    add_body("All telemetry panels were consolidated into a unified Kibana Operations Dashboard. The dashboard delivers instant situational awareness across application error spikes, database failures, and security locking events:")
    add_image_box("reports/screenshots/logging/fig10_kibana_centralized_dashboard.png", "Figure 10: Unified Centralized Logging & Observability Dashboard in Kibana (http://localhost:5601)")

    # Section 6
    add_h1("6. Viva Voce & Technical Defense Summary")
    add_body("Key architectural and operational concepts to defend in front of the evaluator:")
    add_body("1. Filebeat vs Logstash Architectural Separation: Filebeat is a lightweight Go daemon (~20MB memory) optimized solely for reliable, low-overhead log harvesting at the edge. Logstash is a rich, JVM-based pipeline engine that performs heavy data transformation, regex parsing, and multi-destination routing. Running Filebeat on edge containers and centralizing Logstash prevents heavy JVM memory consumption on production application hosts.\n"
             "2. Grok Filter Mechanism & Structured Logging Benefits: Grok combines predefined reusable regular expressions to dissect unstructured strings into schema-enforced attributes ('log_level', 'http_status', 'service_name'). Structured documents enable sub-millisecond aggregations, numeric comparisons, and automated alert triggering in Elasticsearch.\n"
             "3. Backpressure Handling: If Logstash or Elasticsearch experiences transient latency spikes, Filebeat detects delayed TCP acknowledgments via the Beats protocol and throttles its read rate without dropping records, tracking its progress in its local registry.\n"
             "4. Single-Node 'Yellow' Cluster Health: On a single-node Elasticsearch deployment, replica shards cannot be placed on the same physical node as primary shards (since replicas protect against node loss). Consequently, replica shards remain unallocated, producing an expected 'yellow' status with 100% data integrity and zero search impact.\n"
             "5. Automated Data View Initialization: Kibana's REST API ('POST /api/data_views/data_view') was leveraged to programmatically register the index pattern, ensuring zero manual configuration is required across environments.")

    # Section 7
    add_h1("7. Conclusion")
    add_body("The Centralized Logging implementation successfully integrates the ELK Stack + Filebeat into the PulseCare Hospital Management System DevOps lifecycle. By decoupling log harvesting (Filebeat), stream parsing (Logstash), indexing (Elasticsearch), and analytics (Kibana), the platform achieves production-ready visibility, rapid incident triage capabilities, and compliance auditability.")

    output_path = "reports/Centralized_Logging_Report.docx"
    doc.save(output_path)
    print(f"Successfully generated {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    create_report()

