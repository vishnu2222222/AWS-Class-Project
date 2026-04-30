from __future__ import annotations

SITE_NAME = "Vishnu Gangula | CyberFolio"
SITE_DESCRIPTION = (
    "Cybersecurity portfolio focused on vulnerability management, AWS deployment, "
    "and operationally useful security work."
)
REDIRECTED_RESUME_FILENAME = "resume/vishnu-gangula-resume-redacted.pdf"

PROFILE = {
    "name": "Vishnu Gangula",
    "headline": "Cybersecurity student and information security intern",
    "subheadline": (
        "Focused on vulnerability management, cloud deployment, and documentation "
        "that helps teams respond faster and operate more clearly."
    ),
    "summary": (
        "I am a University of Texas at Dallas student building a portfolio around "
        "practical security work: vulnerability management, AWS-hosted projects, "
        "and communication that makes technical systems easier to defend."
    ),
    "availability": (
        "Interested in security operations, vulnerability management, cloud security, "
        "and project-based cybersecurity work."
    ),
    "location": "Dallas-Fort Worth, Texas",
    "education_short": "UT Dallas | BS in Computer Information Systems and Technology",
    "current_focus": [
        "Turning noisy security data into clear remediation signals",
        "Deploying database-backed web projects on AWS infrastructure",
        "Documenting operational workflows so teams can move with confidence",
    ],
}

SOCIAL_LINKS = [
    {
        "label": "GitHub",
        "url": "https://github.com/vishnu2222222",
        "display": "github.com/vishnu2222222",
    },
    {
        "label": "LinkedIn",
        "url": "https://linkedin.com/in/vishnugangula",
        "display": "linkedin.com/in/vishnugangula",
    },
]

HOME_METRICS = [
    {"value": "4M+", "label": "Vulnerabilities surfaced through dashboard reporting"},
    {"value": "32", "label": "Business units onboarded into Qualys workflows"},
    {"value": "600+", "label": "Devices added to authenticated scan coverage"},
]

ABOUT_SECTIONS = [
    {
        "title": "Security work that stays practical",
        "body": (
            "My best work sits where technical detail meets operational usefulness. "
            "I am interested in projects that reduce risk in measurable ways, whether "
            "that means cleaning up exposure data, improving scan coverage, or shipping "
            "infrastructure that is easy to understand and maintain."
        ),
    },
    {
        "title": "Cloud deployment with a real outcome",
        "body": (
            "I use web and AWS projects as a way to prove deployment fundamentals in "
            "public. This portfolio itself includes Flask, SQLite, Gunicorn, Nginx, "
            "and AWS Lightsail so the code is backed by an actual hosted environment."
        ),
    },
    {
        "title": "Documentation as a security skill",
        "body": (
            "I treat documentation, escalation notes, and workflow design as part of "
            "security engineering. Clear written guidance makes vulnerability "
            "management, support operations, and incident response easier to execute "
            "under pressure."
        ),
    },
]

EDUCATION = {
    "school": "The University of Texas at Dallas",
    "degree": (
        "Bachelor of Science in Computer Information Systems and Technology, "
        "Concentration in Cybersecurity Management"
    ),
    "dates": "Aug 2022 - May 2026",
}

EXPERIENCE = [
    {
        "role": "Information Security Intern",
        "company": "Cencora, Inc. (AmerisourceBergen)",
        "location": "Carrollton, TX",
        "dates": "Jun 2025 - Present",
        "summary": (
            "Support enterprise vulnerability management by improving visibility, "
            "scan coverage, remediation prioritization, and cross-team follow-through."
        ),
        "bullets": [
            (
                "Developed the organization's first automated endpoint vulnerability "
                "dashboard in Power BI, surfacing 4M+ vulnerabilities and tracking "
                "KPIs, KRIs, MTTR, and SLA thresholds."
            ),
            (
                "Onboarded 32 newly acquired business units into Qualys and expanded "
                "authenticated scan coverage to 600+ devices."
            ),
            (
                "Reduced unmonitored systems from 1,400+ to under 450 by analyzing "
                "coverage gaps and tuning scan policies."
            ),
            (
                "Restored visibility for 15,000+ endpoints affected by telemetry gaps "
                "and coordinated fixes with engineering teams."
            ),
            (
                "Performed weekly threat triage on emerging CVEs and zero-days using "
                "CVSS v3.1, EPSS, and DREAD-informed prioritization."
            ),
            (
                "Led remediation discussions across infrastructure, endpoint, and "
                "application teams to improve accountability and SLA adherence."
            ),
        ],
    },
    {
        "role": "IT Help Desk Analyst -> Technician -> Supervisor",
        "company": "UT Dallas Office of Information Technology",
        "location": "Richardson, TX",
        "dates": "Aug 2023 - May 2025",
        "summary": (
            "Worked across frontline IT support, escalations, team leadership, and "
            "knowledge-base improvements in a high-volume university environment."
        ),
        "bullets": [
            (
                "Provided multi-channel technical support through AWS Amazon Connect "
                "for hardware, software, network, and account-related issues."
            ),
            (
                "Logged, tracked, and prioritized work through TeamDynamix to speed "
                "resolution and route complex cases appropriately."
            ),
            (
                "Coordinated incident workflows for escalated issues requiring quick "
                "containment and cross-team communication."
            ),
            (
                "Trained and managed analysts and technicians while serving as a key "
                "escalation point for more complex problems."
            ),
            (
                "Updated knowledge-base documentation through testing, research, and "
                "written process improvement."
            ),
        ],
    },
]

SKILL_GROUPS = [
    {
        "title": "Security and Vulnerability Management",
        "items": [
            "Axonius",
            "Wiz",
            "Qualys",
            "Wireshark",
            "Ionix",
            "Seemplicity",
            "Zafran",
            "BlackKite",
        ],
    },
    {
        "title": "Programming and Automation",
        "items": ["Python", "Java", "C++", "Git", "GitHub"],
    },
    {
        "title": "Data and Reporting",
        "items": ["Power BI", "Excel", "SQL", "SQL Server Management Studio"],
    },
    {
        "title": "Cloud, Identity, and Operations",
        "items": [
            "AWS (Amazon Connect)",
            "Duo Security",
            "SailPoint IIQ",
            "Microsoft Identity Manager",
            "Azure",
            "ServiceNow",
            "TeamDynamix",
            "Jira",
            "Confluence",
        ],
    },
]

CERTIFICATIONS = [
    {
        "name": "Qualys Vulnerability Management, Detection & Response (VMDR)",
        "status": "Completed",
        "completed": True,
        "details": (
            "Hands-on vulnerability management certification aligned with the Qualys "
            "tooling used in enterprise exposure management workflows."
        ),
    },
    {
        "name": "CyberDefender Level 1 (CCDL1)",
        "status": "In Progress",
        "completed": False,
        "details": (
            "Completed hands-on SOC labs covering log analysis, packet inspection, "
            "and attack detection workflows across real-world scenarios."
        ),
    },
    {
        "name": "CompTIA Security+",
        "status": "In Progress",
        "completed": False,
        "details": (
            "Focused on foundational security operations, threat analysis, risk "
            "management, and network defense concepts."
        ),
    },
]

PROJECTS = [
    {
        "title": "ASA Log Sentinel",
        "kicker": "Python | Security Analytics | Log Parsing",
        "summary": (
            "Parses raw Cisco ASA firewall logs, sessionizes related activity, and "
            "produces structured JSONL evidence for attack-vector classification."
        ),
        "impact": (
            "Shows how security data engineering can turn noisy firewall events into "
            "clean model-ready evidence for analysts, rules, and LLM workflows."
        ),
        "repo_url": "https://github.com/vishnu2222222/ASA-Log-Sentinel",
        "tags": ["Python", "Cisco ASA", "JSONL", "LLM workflow"],
    },
    {
        "title": "Workout Tracker",
        "kicker": "React | TypeScript | Offline-First PWA",
        "summary": (
            "Modern progressive web app for tracking push and pull workouts with an "
            "exercise library, rest timer, workout history, and offline storage."
        ),
        "impact": (
            "Demonstrates front-end product thinking through typed React state, "
            "installable PWA behavior, and a polished offline user experience."
        ),
        "repo_url": "https://github.com/vishnu2222222/Workout-Tracker-",
        "tags": ["React 18", "TypeScript", "Tailwind CSS", "Dexie.js", "PWA"],
    },
    {
        "title": "AWS Class Project",
        "kicker": "Flask | AWS Lightsail | SQLite",
        "summary": (
            "Multi-page cybersecurity portfolio site with a database-backed contact "
            "form, protected admin dashboard, and production-style deployment using "
            "Gunicorn, Nginx, and AWS Lightsail."
        ),
        "impact": (
            "Demonstrates full-stack deployment fundamentals by taking a Flask app "
            "from local development to a public AWS-hosted environment."
        ),
        "repo_url": "https://github.com/vishnu2222222/AWS-Class-Project",
        "tags": ["Flask", "Gunicorn", "Nginx", "SQLite", "AWS Lightsail"],
    },
]

BLOG_POSTS = [
    {
        "title": "What a useful vulnerability dashboard should help teams do",
        "date": "April 2026",
        "excerpt": (
            "Good dashboards do more than count findings. They should help teams see "
            "coverage gaps, prioritize high-risk issues, and follow remediation work "
            "through to closure."
        ),
    },
    {
        "title": "What deploying Flask on AWS Lightsail taught me",
        "date": "April 2026",
        "excerpt": (
            "Shipping a small web app on AWS reinforced the basics that matter most: "
            "environment configuration, reverse proxy setup, service management, and "
            "verifying the app end to end."
        ),
    },
    {
        "title": "Why documentation matters during incident response",
        "date": "March 2026",
        "excerpt": (
            "Fast response depends on clear escalation paths, stable ownership, and "
            "simple written guidance. Documentation is not extra work when it lowers "
            "confusion during time-sensitive incidents."
        ),
    },
]

FOCUS_AREAS = [
    {
        "title": "Vulnerability Management",
        "description": (
            "I enjoy work that improves asset visibility, scan coverage, remediation "
            "prioritization, and the quality of security data teams rely on."
        ),
    },
    {
        "title": "Cloud Deployment Projects",
        "description": (
            "I build and deploy projects that prove practical cloud fundamentals, from "
            "Linux setup and reverse proxying to app configuration and database-backed "
            "functionality."
        ),
    },
    {
        "title": "Operational Documentation",
        "description": (
            "I like turning complex technical work into repeatable instructions, "
            "knowledge-base updates, and process notes that help teams move faster."
        ),
    },
]
