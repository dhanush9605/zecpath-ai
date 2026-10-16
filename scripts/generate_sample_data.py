"""Generate sample raw resumes/JDs and their validated structured JSON counterparts.

Creates 10 diverse multi-domain resumes and 4 job descriptions (tech & non-tech),
validating each structured instance against Pydantic AI data models.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure repository root is on sys.path
repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from parsers.models import (
    CandidateMetadata,
    CandidateProfile,
    CertificationObject,
    ContactInfo,
    DegreeLevel,
    EducationObject,
    EmploymentType,
    ExperienceObject,
    JobProfile,
    JobRequirements,
    LanguageProficiencyObject,
    LocationObject,
    PayPeriod,
    ProjectObject,
    RoleType,
    SalaryRange,
    SeniorityLevel,
    SkillCategory,
    SkillObject,
    SkillProficiency,
    WorkplaceType,
)


def get_raw_and_structured_resumes() -> list[tuple[str, str, CandidateProfile]]:
    """Return pairs of (raw_filename, raw_text, structured_profile) for 10 domains."""
    resumes = []

    # 1. Backend Engineer
    raw_01 = """ALEX CHEN
Email: alex.chen.dev@example.com | Phone: +1-415-555-0192 | Location: San Francisco, CA
LinkedIn: linkedin.com/in/alexchen-backend | GitHub: github.com/alexchen-cloud

PROFESSIONAL SUMMARY
Senior Backend Engineer with 7+ years of experience designing high-throughput, fault-tolerant distributed systems. Specialized in Go, Python, gRPC microservices, and event-driven architectures processing 50M+ events daily.

SKILLS
- Languages: Go, Python, SQL, C++
- Distributed Systems: Kafka, gRPC, RabbitMQ, Redis, Elasticsearch
- Cloud & DevOps: Docker, Kubernetes, AWS (EKS, RDS, S3), Terraform
- Databases: PostgreSQL, MongoDB, DynamoDB

PROFESSIONAL EXPERIENCE
Staff Distributed Systems Engineer | CloudScale Inc. | San Francisco, CA (Hybrid)
March 2021 - Present
- Architected an event-driven payment reconciliation service in Go processing $40M daily volume.
- Reduced API p99 latency from 320ms to 45ms by introducing Redis caching clusters and connection pooling.
- Mentored a pod of 5 backend engineers in concurrency patterns, unit testing, and observability.

Backend Software Engineer | DataStream Labs | San Jose, CA
July 2017 - February 2021
- Built asynchronous ingestion pipelines using Python, FastAPI, and Apache Kafka.
- Designed schema migration strategies for PostgreSQL databases with 200M+ rows with zero downtime.

EDUCATION
Bachelor of Science in Computer Science | University of California, Berkeley (2013 - 2017)
GPA: 3.8 / 4.0

CERTIFICATIONS
- AWS Certified Solutions Architect - Associate (Amazon Web Services, 2022)
- Certified Kubernetes Administrator (Linux Foundation, 2023)

PROJECTS
- Distributed Raft Key-Value Store: Open-source implementation of Raft consensus algorithm in Go.
"""
    profile_01 = CandidateProfile(
        candidate_id="cand-001-backend",
        contact_info=ContactInfo(
            full_name="Alex Chen",
            email="alex.chen.dev@example.com",
            phone="+1-415-555-0192",
            location=LocationObject(
                city="San Francisco", state_or_province="CA", country="USA", is_remote=False
            ),
            linkedin_url="https://linkedin.com/in/alexchen-backend",
            github_url="https://github.com/alexchen-cloud",
        ),
        headline="Senior Backend & Distributed Systems Engineer",
        professional_summary="Senior Backend Engineer with 7+ years of experience designing high-throughput, fault-tolerant distributed systems. Specialized in Go, Python, gRPC microservices, and event-driven architectures processing 50M+ events daily.",
        target_role="Staff Distributed Systems Engineer",
        domain="Backend Software Engineering",
        total_experience_years=7.5,
        skills=[
            SkillObject(
                name="Go",
                category=SkillCategory.TECHNICAL,
                proficiency=SkillProficiency.EXPERT,
                years_of_experience=6.0,
                last_used_year=2024,
            ),
            SkillObject(
                name="Python",
                category=SkillCategory.TECHNICAL,
                proficiency=SkillProficiency.ADVANCED,
                years_of_experience=7.5,
                last_used_year=2024,
            ),
            SkillObject(
                name="Apache Kafka",
                category=SkillCategory.TOOL,
                proficiency=SkillProficiency.ADVANCED,
                years_of_experience=5.0,
                last_used_year=2024,
            ),
            SkillObject(
                name="Kubernetes",
                category=SkillCategory.CLOUD_DEVOPS,
                proficiency=SkillProficiency.ADVANCED,
                years_of_experience=4.5,
                last_used_year=2024,
            ),
            SkillObject(
                name="PostgreSQL",
                category=SkillCategory.DATABASE,
                proficiency=SkillProficiency.EXPERT,
                years_of_experience=7.0,
                last_used_year=2024,
            ),
            SkillObject(
                name="gRPC",
                category=SkillCategory.FRAMEWORK,
                proficiency=SkillProficiency.ADVANCED,
                years_of_experience=4.0,
                last_used_year=2024,
            ),
        ],
        experience=[
            ExperienceObject(
                company_name="CloudScale Inc.",
                designation="Staff Distributed Systems Engineer",
                standardized_title="Staff Backend Engineer",
                seniority=SeniorityLevel.LEAD,
                employment_type=EmploymentType.FULL_TIME,
                location=LocationObject(
                    city="San Francisco", state_or_province="CA", country="USA", is_remote=False
                ),
                start_date="2021-03",
                end_date=None,
                is_current=True,
                duration_in_months=42,
                description="Core platform infrastructure engineering.",
                responsibilities=[
                    "Architect event-driven microservices architecture.",
                    "Lead technical design reviews across 3 engineering squads.",
                ],
                achievements=[
                    "Architected an event-driven payment reconciliation service in Go processing $40M daily volume.",
                    "Reduced API p99 latency from 320ms to 45ms by introducing Redis caching clusters.",
                ],
                technologies_used=["Go", "Kafka", "PostgreSQL", "AWS", "Kubernetes", "Redis"],
            ),
            ExperienceObject(
                company_name="DataStream Labs",
                designation="Backend Software Engineer",
                standardized_title="Backend Software Engineer",
                seniority=SeniorityLevel.MID,
                employment_type=EmploymentType.FULL_TIME,
                location=LocationObject(
                    city="San Jose", state_or_province="CA", country="USA", is_remote=False
                ),
                start_date="2017-07",
                end_date="2021-02",
                is_current=False,
                duration_in_months=44,
                responsibilities=[
                    "Developed asynchronous ingestion pipelines in FastAPI.",
                    "Maintained relational database clusters and query optimizations.",
                ],
                achievements=[
                    "Designed zero-downtime schema migration strategies for PostgreSQL tables with 200M+ records."
                ],
                technologies_used=["Python", "FastAPI", "PostgreSQL", "Docker"],
            ),
        ],
        education=[
            EducationObject(
                institution_name="University of California, Berkeley",
                degree="Bachelor of Science in Computer Science",
                degree_level=DegreeLevel.BACHELOR,
                field_of_study="Computer Science",
                start_year=2013,
                end_year=2017,
                grade_or_gpa="3.8/4.0",
            )
        ],
        certifications=[
            CertificationObject(
                name="AWS Certified Solutions Architect - Associate",
                issuing_organization="Amazon Web Services",
                issue_date="2022-04",
                credential_id="AWS-SAA-839201",
            )
        ],
        projects=[
            ProjectObject(
                title="Distributed Raft Key-Value Store",
                role="Creator / Maintainer",
                description="Fault-tolerant, linearizable KV store implementing Raft consensus in Go.",
                technologies=["Go", "Raft", "gRPC"],
                outcomes=["Achieved 12,000 writes/sec with automated leader election."],
            )
        ],
        languages=[
            LanguageProficiencyObject(language="English", proficiency="NATIVE"),
            LanguageProficiencyObject(language="Mandarin", proficiency="CONVERSATIONAL"),
        ],
        metadata=CandidateMetadata(
            source_file_name="resume_01_backend.txt",
            parser_version="0.1.0",
            extracted_at="2026-10-15T10:00:00Z",
            confidence_score=0.98,
        ),
    )
    resumes.append(("resume_01_backend.txt", raw_01, profile_01))

    # 2. Frontend / Full-Stack Engineer
    raw_02 = """PRIYA SHARMA
Email: priya.sharma.tech@example.com | Phone: +1-206-555-0144 | Location: Seattle, WA
LinkedIn: linkedin.com/in/priyasharma-web | Portfolio: priyasharma.dev

SUMMARY
Lead Frontend Engineer with 6+ years driving design systems, accessible UI/UX, and high-performance Web applications using React, TypeScript, Next.js, and GraphQL.

SKILLS
- Core Web: TypeScript, JavaScript (ESNext), HTML5, CSS3, Web Components
- Frameworks: React, Next.js, Vue.js, Tailwind CSS, Redux Toolkit, Zustand
- Tooling: Webpack, Vite, Jest, Playwright, Storybook, Figma

EXPERIENCE
Lead Frontend Engineer | PixelCraft Media | Seattle, WA
January 2022 - Present
- Led a team of 6 engineers revamping customer dashboard in Next.js 14, improving Core Web Vitals (LCP improved by 65%).
- Created an enterprise accessible component library across 4 consumer products reaching WCAG 2.1 AA compliance.

Frontend Developer | InnovateWeb | Austin, TX
August 2018 - December 2021
- Built responsive client portal utilizing React and TypeScript integrated with GraphQL APIs.
- Cut client-side bundle size by 42% through code-splitting and dynamic imports.

EDUCATION
Bachelor of Engineering in Information Technology | University of Washington (2014 - 2018)
First Class Honors

CERTIFICATIONS
- Meta Certified Front-End Developer (Meta, 2021)
"""
    profile_02 = CandidateProfile(
        candidate_id="cand-002-frontend",
        contact_info=ContactInfo(
            full_name="Priya Sharma",
            email="priya.sharma.tech@example.com",
            phone="+1-206-555-0144",
            location=LocationObject(
                city="Seattle", state_or_province="WA", country="USA", is_remote=False
            ),
            linkedin_url="https://linkedin.com/in/priyasharma-web",
            portfolio_url="https://priyasharma.dev",
        ),
        headline="Lead Frontend & UI Platform Engineer",
        professional_summary="Lead Frontend Engineer with 6+ years driving design systems, accessible UI/UX, and high-performance Web applications using React, TypeScript, Next.js, and GraphQL.",
        target_role="Lead Frontend Engineer",
        domain="Frontend / Full-Stack Engineering",
        total_experience_years=6.2,
        skills=[
            SkillObject(
                name="React",
                category=SkillCategory.FRAMEWORK,
                proficiency=SkillProficiency.EXPERT,
                years_of_experience=6.0,
                last_used_year=2024,
            ),
            SkillObject(
                name="TypeScript",
                category=SkillCategory.TECHNICAL,
                proficiency=SkillProficiency.EXPERT,
                years_of_experience=5.5,
                last_used_year=2024,
            ),
            SkillObject(
                name="Next.js",
                category=SkillCategory.FRAMEWORK,
                proficiency=SkillProficiency.ADVANCED,
                years_of_experience=4.0,
                last_used_year=2024,
            ),
            SkillObject(
                name="GraphQL",
                category=SkillCategory.TECHNICAL,
                proficiency=SkillProficiency.INTERMEDIATE,
                years_of_experience=3.0,
                last_used_year=2024,
            ),
        ],
        experience=[
            ExperienceObject(
                company_name="PixelCraft Media",
                designation="Lead Frontend Engineer",
                standardized_title="Lead Frontend Engineer",
                seniority=SeniorityLevel.LEAD,
                employment_type=EmploymentType.FULL_TIME,
                location=LocationObject(city="Seattle", state_or_province="WA", country="USA"),
                start_date="2022-01",
                end_date=None,
                is_current=True,
                duration_in_months=33,
                responsibilities=[
                    "Oversee UI engineering standards",
                    "Maintain component design system",
                ],
                achievements=[
                    "Improved Largest Contentful Paint (LCP) by 65% across primary web portals."
                ],
                technologies_used=["Next.js", "React", "TypeScript", "Tailwind CSS", "Storybook"],
            )
        ],
        education=[
            EducationObject(
                institution_name="University of Washington",
                degree="Bachelor of Engineering in Information Technology",
                degree_level=DegreeLevel.BACHELOR,
                field_of_study="Information Technology",
                start_year=2014,
                end_year=2018,
                grade_or_gpa="First Class Honors",
            )
        ],
        certifications=[
            CertificationObject(
                name="Meta Certified Front-End Developer",
                issuing_organization="Meta",
                issue_date="2021-08",
            )
        ],
        languages=[LanguageProficiencyObject(language="English", proficiency="NATIVE")],
        metadata=CandidateMetadata(
            source_file_name="resume_02_frontend.txt",
            parser_version="0.1.0",
            extracted_at="2026-10-15T10:00:00Z",
            confidence_score=0.99,
        ),
    )
    resumes.append(("resume_02_frontend.txt", raw_02, profile_02))

    # 3. Data Science & Machine Learning
    raw_03 = """DR. MARCUS VANCE
Email: marcus.vance.ai@example.com | Phone: +1-617-555-0188 | Location: Boston, MA
LinkedIn: linkedin.com/in/marcus-vance-ai | Google Scholar: scholar.google.com/citations?user=mvance

SUMMARY
Senior AI/ML Research Scientist with a Ph.D. in Computer Science and 5+ years building deep learning systems, Large Language Model (LLM) fine-tuning pipelines, and retrieval-augmented generation (RAG) architectures.

SKILLS
- Machine Learning & DL: PyTorch, TensorFlow, Hugging Face, Scikit-learn, LangChain, LlamaIndex
- MLOps & Vector DBs: MLflow, Kubeflow, Pinecone, Milvus, Triton Inference Server
- Mathematics: Bayesian Inference, Optimization, Linear Algebra, Statistical Hypothesis Testing

EXPERIENCE
Senior AI Research Scientist | DeepThought Systems | Boston, MA
September 2021 - Present
- Spearheaded fine-tuning of domain-specific 13B LLMs for enterprise contract synthesis using LoRA and QLoRA.
- Built low-latency RAG pipeline with hybrid search (dense embeddings + BM25), boosting response relevance by 34%.

Machine Learning Engineer | BioAnalytics AI | Cambridge, MA
June 2019 - August 2021
- Trained convolutional neural networks for biomolecular image classification with 94.2% AUC.

EDUCATION
Ph.D. in Computer Science (Machine Learning) | Massachusetts Institute of Technology (2015 - 2019)
Bachelor of Science in Mathematics & CS | Carnegie Mellon University (2011 - 2015)
"""
    profile_03 = CandidateProfile(
        candidate_id="cand-003-aiml",
        contact_info=ContactInfo(
            full_name="Dr. Marcus Vance",
            email="marcus.vance.ai@example.com",
            phone="+1-617-555-0188",
            location=LocationObject(city="Boston", state_or_province="MA", country="USA"),
            linkedin_url="https://linkedin.com/in/marcus-vance-ai",
        ),
        headline="Senior AI/ML Research Scientist (LLMs & RAG)",
        professional_summary="Senior AI/ML Research Scientist with a Ph.D. in Computer Science and 5+ years building deep learning systems, Large Language Model (LLM) fine-tuning pipelines, and retrieval-augmented generation (RAG) architectures.",
        target_role="Staff Machine Learning Engineer",
        domain="Data Science & Machine Learning",
        total_experience_years=5.3,
        skills=[
            SkillObject(
                name="PyTorch",
                category=SkillCategory.FRAMEWORK,
                proficiency=SkillProficiency.EXPERT,
                years_of_experience=5.0,
                last_used_year=2024,
            ),
            SkillObject(
                name="Large Language Models (LLMs)",
                category=SkillCategory.TECHNICAL,
                proficiency=SkillProficiency.EXPERT,
                years_of_experience=3.0,
                last_used_year=2024,
            ),
            SkillObject(
                name="Vector Databases",
                category=SkillCategory.DATABASE,
                proficiency=SkillProficiency.ADVANCED,
                years_of_experience=3.0,
                last_used_year=2024,
            ),
            SkillObject(
                name="MLOps",
                category=SkillCategory.CLOUD_DEVOPS,
                proficiency=SkillProficiency.ADVANCED,
                years_of_experience=4.0,
                last_used_year=2024,
            ),
        ],
        experience=[
            ExperienceObject(
                company_name="DeepThought Systems",
                designation="Senior AI Research Scientist",
                standardized_title="Senior Machine Learning Scientist",
                seniority=SeniorityLevel.SENIOR,
                employment_type=EmploymentType.FULL_TIME,
                location=LocationObject(city="Boston", state_or_province="MA", country="USA"),
                start_date="2021-09",
                end_date=None,
                is_current=True,
                achievements=[
                    "Boosted RAG response relevance by 34% deploying hybrid dense-sparse vector indexing."
                ],
                technologies_used=["PyTorch", "Hugging Face", "Pinecone", "Triton", "Kubeflow"],
            )
        ],
        education=[
            EducationObject(
                institution_name="Massachusetts Institute of Technology",
                degree="Ph.D. in Computer Science (Machine Learning)",
                degree_level=DegreeLevel.DOCTORATE,
                field_of_study="Computer Science & Artificial Intelligence",
                start_year=2015,
                end_year=2019,
            )
        ],
        certifications=[],
        languages=[LanguageProficiencyObject(language="English", proficiency="NATIVE")],
        metadata=CandidateMetadata(
            source_file_name="resume_03_ai_ml.txt",
            parser_version="0.1.0",
            extracted_at="2026-10-15T10:00:00Z",
            confidence_score=0.97,
        ),
    )
    resumes.append(("resume_03_ai_ml.txt", raw_03, profile_03))

    # 4. DevOps & Cloud Platform
    raw_04 = """ELENA ROSTOVA
Email: elena.rostova.ops@example.com | Phone: +1-312-555-0177 | Location: Chicago, IL
LinkedIn: linkedin.com/in/elena-rostova-cloud

SUMMARY
Principal DevOps & Cloud Platform Architect with 8+ years designing zero-trust cloud infrastructure on AWS and GCP. Expert in Kubernetes cluster lifecycle, Infrastructure as Code with Terraform, and DevSecOps compliance.

SKILLS
- Cloud Providers: AWS (ECS, EKS, IAM, VPC), Google Cloud Platform (GKE)
- Orchestration & IaC: Kubernetes, Terraform, Helm, Ansible, Docker
- Observability: Prometheus, Grafana, Datadog, OpenTelemetry
- CI/CD & Security: GitHub Actions, ArgoCD, SonarQube, Vault

EXPERIENCE
Principal Cloud Architect | FinTech Cloudworks | Chicago, IL
April 2020 - Present
- Designed multi-region active-active EKS clusters handling 12,000 req/sec with 99.999% SLA.
- Standardized Terraform modules across 15 engineering squads, cutting infrastructure provisioning time by 80%.

DevOps Engineer | MetroNet Telecom | Chicago, IL
June 2016 - March 2020
- Automated CI/CD pipelines via GitHub Actions and Docker, reducing deployment cycle from 4 days to 15 minutes.

EDUCATION
Bachelor of Science in Electrical & Computer Engineering | University of Illinois Urbana-Champaign (2012 - 2016)

CERTIFICATIONS
- AWS Certified Solutions Architect - Professional (AWS, 2023)
- HashiCorp Certified: Terraform Associate (HashiCorp, 2022)
"""
    profile_04 = CandidateProfile(
        candidate_id="cand-004-devops",
        contact_info=ContactInfo(
            full_name="Elena Rostova",
            email="elena.rostova.ops@example.com",
            phone="+1-312-555-0177",
            location=LocationObject(city="Chicago", state_or_province="IL", country="USA"),
            linkedin_url="https://linkedin.com/in/elena-rostova-cloud",
        ),
        headline="Principal DevOps & Cloud Infrastructure Architect",
        professional_summary="Principal DevOps & Cloud Platform Architect with 8+ years designing zero-trust cloud infrastructure on AWS and GCP. Expert in Kubernetes cluster lifecycle, Infrastructure as Code with Terraform, and DevSecOps compliance.",
        target_role="Principal Cloud Platform Architect",
        domain="DevOps & Cloud Infrastructure",
        total_experience_years=8.3,
        skills=[
            SkillObject(
                name="AWS",
                category=SkillCategory.CLOUD_DEVOPS,
                proficiency=SkillProficiency.EXPERT,
                years_of_experience=8.0,
                last_used_year=2024,
            ),
            SkillObject(
                name="Kubernetes",
                category=SkillCategory.CLOUD_DEVOPS,
                proficiency=SkillProficiency.EXPERT,
                years_of_experience=6.5,
                last_used_year=2024,
            ),
            SkillObject(
                name="Terraform",
                category=SkillCategory.TOOL,
                proficiency=SkillProficiency.EXPERT,
                years_of_experience=6.0,
                last_used_year=2024,
            ),
            SkillObject(
                name="ArgoCD",
                category=SkillCategory.TOOL,
                proficiency=SkillProficiency.ADVANCED,
                years_of_experience=4.0,
                last_used_year=2024,
            ),
        ],
        experience=[
            ExperienceObject(
                company_name="FinTech Cloudworks",
                designation="Principal Cloud Architect",
                standardized_title="Principal DevOps Architect",
                seniority=SeniorityLevel.PRINCIPAL,
                employment_type=EmploymentType.FULL_TIME,
                location=LocationObject(city="Chicago", state_or_province="IL", country="USA"),
                start_date="2020-04",
                end_date=None,
                is_current=True,
                achievements=[
                    "Designed multi-region EKS clusters achieving 99.999% SLA and reduced provisioning time by 80%."
                ],
                technologies_used=["AWS", "Terraform", "Kubernetes", "Datadog", "ArgoCD"],
            )
        ],
        education=[
            EducationObject(
                institution_name="University of Illinois Urbana-Champaign",
                degree="Bachelor of Science in Electrical & Computer Engineering",
                degree_level=DegreeLevel.BACHELOR,
                field_of_study="Electrical & Computer Engineering",
                start_year=2012,
                end_year=2016,
            )
        ],
        certifications=[
            CertificationObject(
                name="AWS Certified Solutions Architect - Professional",
                issuing_organization="Amazon Web Services",
                issue_date="2023-01",
                credential_id="AWS-SAP-998811",
            )
        ],
        languages=[
            LanguageProficiencyObject(language="English", proficiency="NATIVE"),
            LanguageProficiencyObject(language="Russian", proficiency="NATIVE"),
        ],
        metadata=CandidateMetadata(
            source_file_name="resume_04_devops.txt",
            parser_version="0.1.0",
            extracted_at="2026-10-15T10:00:00Z",
            confidence_score=0.98,
        ),
    )
    resumes.append(("resume_04_devops.txt", raw_04, profile_04))

    # 5. Cybersecurity & Threat Analysis
    raw_05 = """DAVID OKAFOR
Email: david.okafor.sec@example.com | Phone: +1-202-555-0133 | Location: Washington, DC
LinkedIn: linkedin.com/in/david-okafor-sec

SUMMARY
Senior Cybersecurity & SOC Incident Response Lead with 6+ years protecting critical financial and defense digital assets. Certified Information Systems Security Professional (CISSP).

SKILLS
- Security Operations: SIEM (Splunk, Sentinel), EDR (CrowdStrike), Wireshark, Zeek
- Threat Intel & Frameworks: MITRE ATT&CK, NIST CSF, ISO 27001, SOC 2 Type II
- Vulnerability Mgmt: Tenable Nessus, Qualys, Burp Suite, Python Security Scripting

EXPERIENCE
Senior Information Security Analyst | Apex Defense Systems | Washington, DC
July 2020 - Present
- Led tier-3 incident response investigations mitigating 140+ targeted phishing and ransomware campaigns.
- Developed automated threat hunting playbooks in Splunk Phantom reducing mean-time-to-remediate (MTTR) by 45%.

SOC Analyst | Capital Guard Financial | McLean, VA
June 2018 - June 2020
- Monitored real-time intrusion alerts and triaged network telemetry across 15,000 corporate endpoints.

EDUCATION
Master of Science in Cybersecurity | Johns Hopkins University (2018 - 2020)
Bachelor of Science in Information Technology | George Mason University (2014 - 2018)

CERTIFICATIONS
- Certified Information Systems Security Professional (CISSP) | (ISC)², 2022
- CompTIA Security+ (CompTIA, 2018)
"""
    profile_05 = CandidateProfile(
        candidate_id="cand-005-cybersec",
        contact_info=ContactInfo(
            full_name="David Okafor",
            email="david.okafor.sec@example.com",
            phone="+1-202-555-0133",
            location=LocationObject(city="Washington", state_or_province="DC", country="USA"),
            linkedin_url="https://linkedin.com/in/david-okafor-sec",
        ),
        headline="Senior Cyber Security & SOC Incident Response Lead (CISSP)",
        professional_summary="Senior Cybersecurity & SOC Incident Response Lead with 6+ years protecting critical financial and defense digital assets. Certified Information Systems Security Professional (CISSP).",
        target_role="Lead Information Security Officer",
        domain="Cybersecurity & Threat Analysis",
        total_experience_years=6.3,
        skills=[
            SkillObject(
                name="SIEM / Splunk",
                category=SkillCategory.TOOL,
                proficiency=SkillProficiency.EXPERT,
                years_of_experience=6.0,
                last_used_year=2024,
            ),
            SkillObject(
                name="CrowdStrike EDR",
                category=SkillCategory.TOOL,
                proficiency=SkillProficiency.ADVANCED,
                years_of_experience=4.5,
                last_used_year=2024,
            ),
            SkillObject(
                name="Incident Response",
                category=SkillCategory.TECHNICAL,
                proficiency=SkillProficiency.EXPERT,
                years_of_experience=6.0,
                last_used_year=2024,
            ),
            SkillObject(
                name="NIST Cybersecurity Framework",
                category=SkillCategory.DOMAIN,
                proficiency=SkillProficiency.ADVANCED,
                years_of_experience=5.0,
                last_used_year=2024,
            ),
        ],
        experience=[
            ExperienceObject(
                company_name="Apex Defense Systems",
                designation="Senior Information Security Analyst",
                standardized_title="Senior Cyber Security Analyst",
                seniority=SeniorityLevel.SENIOR,
                employment_type=EmploymentType.FULL_TIME,
                location=LocationObject(city="Washington", state_or_province="DC", country="USA"),
                start_date="2020-07",
                end_date=None,
                is_current=True,
                achievements=[
                    "Developed automated threat hunting playbooks reducing incident MTTR by 45%."
                ],
                technologies_used=["Splunk", "CrowdStrike", "Python", "Zeek"],
            )
        ],
        education=[
            EducationObject(
                institution_name="Johns Hopkins University",
                degree="Master of Science in Cybersecurity",
                degree_level=DegreeLevel.MASTER,
                field_of_study="Cybersecurity",
                start_year=2018,
                end_year=2020,
            )
        ],
        certifications=[
            CertificationObject(
                name="Certified Information Systems Security Professional (CISSP)",
                issuing_organization="(ISC)²",
                issue_date="2022-03",
                credential_id="CISSP-774411",
            )
        ],
        languages=[LanguageProficiencyObject(language="English", proficiency="NATIVE")],
        metadata=CandidateMetadata(
            source_file_name="resume_05_cybersecurity.txt",
            parser_version="0.1.0",
            extracted_at="2026-10-15T10:00:00Z",
            confidence_score=0.98,
        ),
    )
    resumes.append(("resume_05_cybersecurity.txt", raw_05, profile_05))

    # 6. Technical Product Manager
    raw_06 = """RACHEL KIM
Email: rachel.kim.pm@example.com | Phone: +1-212-555-0155 | Location: New York, NY
LinkedIn: linkedin.com/in/rachel-kim-pm

SUMMARY
Senior Technical Product Manager with 7+ years scaling B2B SaaS and fintech platforms. Track record of driving $18M ARR growth through user discovery, data-informed roadmaps, and agile execution.

SKILLS
- Product Strategy: Roadmap Planning, PRD Authoring, OKRs, User Journey Mapping
- Methodologies: Agile Scrum, Kanban, Design Thinking, Continuous Discovery
- Analytics & Tools: Mixpanel, Amplitude, Jira, SQL, Tableau, Figma

EXPERIENCE
Senior Product Manager | PayFlow Commerce | New York, NY
August 2021 - Present
- Owned end-to-end checkout product roadmap, boosting conversion rates by 19% across 2.4M monthly checkouts.
- Partnered with 12 engineers and 2 UX designers using two-week sprints and clear acceptance criteria.

Product Manager | Omnia Analytics | New York, NY
June 2017 - July 2021
- Launched self-service data exploration tool that scaled from 0 to $6M ARR within 18 months.

EDUCATION
Bachelor of Science in Industrial Engineering & Economics | Columbia University (2013 - 2017)
Magna Cum Laude

CERTIFICATIONS
- Certified Scrum Product Owner (CSPO) | Scrum Alliance, 2020
- Pragmatic Institute Certified (PMC-III), 2021
"""
    profile_06 = CandidateProfile(
        candidate_id="cand-006-prodmgr",
        contact_info=ContactInfo(
            full_name="Rachel Kim",
            email="rachel.kim.pm@example.com",
            phone="+1-212-555-0155",
            location=LocationObject(city="New York", state_or_province="NY", country="USA"),
            linkedin_url="https://linkedin.com/in/rachel-kim-pm",
        ),
        headline="Senior Technical Product Manager (B2B SaaS & FinTech)",
        professional_summary="Senior Technical Product Manager with 7+ years scaling B2B SaaS and fintech platforms. Track record of driving $18M ARR growth through user discovery, data-informed roadmaps, and agile execution.",
        target_role="Group Product Manager",
        domain="Product Management",
        total_experience_years=7.3,
        skills=[
            SkillObject(
                name="Product Strategy",
                category=SkillCategory.DOMAIN,
                proficiency=SkillProficiency.EXPERT,
                years_of_experience=7.0,
                last_used_year=2024,
            ),
            SkillObject(
                name="Agile / Scrum",
                category=SkillCategory.METHODOLOGY,
                proficiency=SkillProficiency.EXPERT,
                years_of_experience=7.0,
                last_used_year=2024,
            ),
            SkillObject(
                name="SQL & Analytics",
                category=SkillCategory.TECHNICAL,
                proficiency=SkillProficiency.ADVANCED,
                years_of_experience=6.0,
                last_used_year=2024,
            ),
            SkillObject(
                name="Amplitude / Mixpanel",
                category=SkillCategory.TOOL,
                proficiency=SkillProficiency.ADVANCED,
                years_of_experience=5.0,
                last_used_year=2024,
            ),
        ],
        experience=[
            ExperienceObject(
                company_name="PayFlow Commerce",
                designation="Senior Product Manager",
                standardized_title="Senior Product Manager",
                seniority=SeniorityLevel.SENIOR,
                employment_type=EmploymentType.FULL_TIME,
                location=LocationObject(city="New York", state_or_province="NY", country="USA"),
                start_date="2021-08",
                end_date=None,
                is_current=True,
                achievements=[
                    "Increased checkout conversion rates by 19% across 2.4M monthly checkouts."
                ],
                technologies_used=["Jira", "Mixpanel", "SQL", "Figma"],
            )
        ],
        education=[
            EducationObject(
                institution_name="Columbia University",
                degree="Bachelor of Science in Industrial Engineering & Economics",
                degree_level=DegreeLevel.BACHELOR,
                field_of_study="Industrial Engineering",
                start_year=2013,
                end_year=2017,
                grade_or_gpa="Magna Cum Laude",
            )
        ],
        certifications=[
            CertificationObject(
                name="Certified Scrum Product Owner (CSPO)",
                issuing_organization="Scrum Alliance",
                issue_date="2020-05",
            )
        ],
        languages=[
            LanguageProficiencyObject(language="English", proficiency="NATIVE"),
            LanguageProficiencyObject(language="Korean", proficiency="FLUENT"),
        ],
        metadata=CandidateMetadata(
            source_file_name="resume_06_product_manager.txt",
            parser_version="0.1.0",
            extracted_at="2026-10-15T10:00:00Z",
            confidence_score=0.99,
        ),
    )
    resumes.append(("resume_06_product_manager.txt", raw_06, profile_06))

    # 7. UI/UX Design & Research
    raw_07 = """MATEO SILVA
Email: mateo.silva.ux@example.com | Phone: +1-305-555-0162 | Location: Miami, FL
LinkedIn: linkedin.com/in/mateo-silva-ux | Portfolio: mateosilva.design

SUMMARY
Principal Product Designer & UX Architect with 8+ years crafting intuitive consumer and enterprise experiences. Expert in Figma component tokens, accessibility compliance, and quantitative user testing.

SKILLS
- Design Systems: Figma (Variables, Auto-layout), Tokens Studio, Zeroheight
- UX Methodologies: User Journey Mapping, Rapid Prototyping, Usability Benchmarking
- Front-End Knowledge: HTML5, CSS/SCSS, React Basics

EXPERIENCE
Principal Product Designer | NextEra Digital | Miami, FL
February 2021 - Present
- Created and maintained the unified design system adopted by 40+ designers and 120 front-end engineers.
- Redesigned mobile app onboarding flow, lifting 30-day user retention from 28% to 47%.

Lead UX Designer | CreativeSphere Agency | Austin, TX
March 2016 - January 2021
- Led user research sprints for Fortune 500 retail clients, facilitating 100+ customer interview sessions.

EDUCATION
Bachelor of Fine Arts in Interaction Design | Savannah College of Art and Design (SCAD) (2012 - 2016)
Summa Cum Laude

CERTIFICATIONS
- Nielsen Norman Group UX Master Certified (NN/g, 2021)
"""
    profile_07 = CandidateProfile(
        candidate_id="cand-007-uiux",
        contact_info=ContactInfo(
            full_name="Mateo Silva",
            email="mateo.silva.ux@example.com",
            phone="+1-305-555-0162",
            location=LocationObject(city="Miami", state_or_province="FL", country="USA"),
            linkedin_url="https://linkedin.com/in/mateo-silva-ux",
            portfolio_url="https://mateosilva.design",
        ),
        headline="Principal Product Designer & UX Design Systems Architect",
        professional_summary="Principal Product Designer & UX Architect with 8+ years crafting intuitive consumer and enterprise experiences. Expert in Figma component tokens, accessibility compliance, and quantitative user testing.",
        target_role="Director of Product Design",
        domain="UI/UX Product Design",
        total_experience_years=8.5,
        skills=[
            SkillObject(
                name="Figma",
                category=SkillCategory.TOOL,
                proficiency=SkillProficiency.EXPERT,
                years_of_experience=8.0,
                last_used_year=2024,
            ),
            SkillObject(
                name="Design Systems",
                category=SkillCategory.DOMAIN,
                proficiency=SkillProficiency.EXPERT,
                years_of_experience=7.0,
                last_used_year=2024,
            ),
            SkillObject(
                name="User Research",
                category=SkillCategory.METHODOLOGY,
                proficiency=SkillProficiency.EXPERT,
                years_of_experience=8.0,
                last_used_year=2024,
            ),
            SkillObject(
                name="Interaction Design",
                category=SkillCategory.DOMAIN,
                proficiency=SkillProficiency.EXPERT,
                years_of_experience=8.0,
                last_used_year=2024,
            ),
        ],
        experience=[
            ExperienceObject(
                company_name="NextEra Digital",
                designation="Principal Product Designer",
                standardized_title="Principal Product Designer",
                seniority=SeniorityLevel.PRINCIPAL,
                employment_type=EmploymentType.FULL_TIME,
                location=LocationObject(city="Miami", state_or_province="FL", country="USA"),
                start_date="2021-02",
                end_date=None,
                is_current=True,
                achievements=[
                    "Llifted 30-day user retention from 28% to 47% via redesigned onboarding."
                ],
                technologies_used=["Figma", "Design Tokens", "UserTesting.com", "Miro"],
            )
        ],
        education=[
            EducationObject(
                institution_name="Savannah College of Art and Design (SCAD)",
                degree="Bachelor of Fine Arts in Interaction Design",
                degree_level=DegreeLevel.BACHELOR,
                field_of_study="Interaction Design",
                start_year=2012,
                end_year=2016,
                grade_or_gpa="Summa Cum Laude",
            )
        ],
        certifications=[
            CertificationObject(
                name="Nielsen Norman Group UX Master Certified",
                issuing_organization="Nielsen Norman Group",
                issue_date="2021-11",
                credential_id="NNG-UXM-9021",
            )
        ],
        languages=[
            LanguageProficiencyObject(language="English", proficiency="NATIVE"),
            LanguageProficiencyObject(language="Spanish", proficiency="NATIVE"),
        ],
        metadata=CandidateMetadata(
            source_file_name="resume_07_ui_ux.txt",
            parser_version="0.1.0",
            extracted_at="2026-10-15T10:00:00Z",
            confidence_score=0.99,
        ),
    )
    resumes.append(("resume_07_ui_ux.txt", raw_07, profile_07))

    # 8. HR & Technical Talent Acquisition
    raw_08 = """SARAH JENKINS
Email: sarah.jenkins.hr@example.com | Phone: +1-404-555-0121 | Location: Atlanta, GA
LinkedIn: linkedin.com/in/sarah-jenkins-talent

SUMMARY
Senior Technical Talent Acquisition Partner with 6+ years partnering with engineering leadership to hire world-class software, infrastructure, and AI engineering talent. Closed 180+ technical hires.

SKILLS
- Recruiting & Sourcing: Full Lifecycle Recruiting, Executive Search, Diversity Sourcing (DEI)
- Tools & ATS: Greenhouse, Lever, Ashby, LinkedIn Recruiter, Gem, Workday
- Metrics: Time-to-Fill, Offer Acceptance Rate, Cost-per-Hire, Candidate Experience NPS

EXPERIENCE
Senior Technical Recruiter | HyperScale AI | Atlanta, GA (Remote)
January 2021 - Present
- Sourced and closed 75+ software engineers across distributed systems and machine learning within 24 months.
- Maintained a 91% offer acceptance rate and reduced average time-to-fill from 62 days to 38 days.

Technical Recruiter | Apex Staffing Solutions | Atlanta, GA
September 2018 - December 2020
- Built candidate pipelines for hyper-growth venture-backed SaaS startups.

EDUCATION
Bachelor of Arts in Human Resources Management | University of Georgia (2014 - 2018)
Dean's List

CERTIFICATIONS
- SHRM Certified Professional (SHRM-CP) | SHRM, 2021
- AIRS Certified Internet Recruiter (CIR), 2019
"""
    profile_08 = CandidateProfile(
        candidate_id="cand-008-talent",
        contact_info=ContactInfo(
            full_name="Sarah Jenkins",
            email="sarah.jenkins.hr@example.com",
            phone="+1-404-555-0121",
            location=LocationObject(
                city="Atlanta", state_or_province="GA", country="USA", is_remote=True
            ),
            linkedin_url="https://linkedin.com/in/sarah-jenkins-talent",
        ),
        headline="Senior Technical Talent Acquisition Partner",
        professional_summary="Senior Technical Talent Acquisition Partner with 6+ years partnering with engineering leadership to hire world-class software, infrastructure, and AI engineering talent. Closed 180+ technical hires.",
        target_role="Lead Technical Talent Partner",
        domain="HR & Talent Acquisition",
        total_experience_years=6.1,
        skills=[
            SkillObject(
                name="Technical Sourcing",
                category=SkillCategory.DOMAIN,
                proficiency=SkillProficiency.EXPERT,
                years_of_experience=6.0,
                last_used_year=2024,
            ),
            SkillObject(
                name="Applicant Tracking Systems (Greenhouse / Ashby)",
                category=SkillCategory.TOOL,
                proficiency=SkillProficiency.EXPERT,
                years_of_experience=6.0,
                last_used_year=2024,
            ),
            SkillObject(
                name="Diversity & Inclusion Recruiting",
                category=SkillCategory.DOMAIN,
                proficiency=SkillProficiency.ADVANCED,
                years_of_experience=5.0,
                last_used_year=2024,
            ),
        ],
        experience=[
            ExperienceObject(
                company_name="HyperScale AI",
                designation="Senior Technical Recruiter",
                standardized_title="Senior Technical Recruiter",
                seniority=SeniorityLevel.SENIOR,
                employment_type=EmploymentType.FULL_TIME,
                location=LocationObject(
                    city="Atlanta", state_or_province="GA", country="USA", is_remote=True
                ),
                start_date="2021-01",
                end_date=None,
                is_current=True,
                achievements=[
                    "Maintained a 91% offer acceptance rate and reduced time-to-fill from 62 to 38 days."
                ],
                technologies_used=["Greenhouse", "LinkedIn Recruiter", "Gem", "Slack"],
            )
        ],
        education=[
            EducationObject(
                institution_name="University of Georgia",
                degree="Bachelor of Arts in Human Resources Management",
                degree_level=DegreeLevel.BACHELOR,
                field_of_study="Human Resources Management",
                start_year=2014,
                end_year=2018,
            )
        ],
        certifications=[
            CertificationObject(
                name="SHRM Certified Professional (SHRM-CP)",
                issuing_organization="Society for Human Resource Management",
                issue_date="2021-06",
                credential_id="SHRM-CP-55221",
            )
        ],
        languages=[LanguageProficiencyObject(language="English", proficiency="NATIVE")],
        metadata=CandidateMetadata(
            source_file_name="resume_08_hr_talent.txt",
            parser_version="0.1.0",
            extracted_at="2026-10-15T10:00:00Z",
            confidence_score=0.99,
        ),
    )
    resumes.append(("resume_08_hr_talent.txt", raw_08, profile_08))

    # 9. Financial Analysis & Modeling
    raw_09 = """VIKRAM PATEL
Email: vikram.patel.cfa@example.com | Phone: +1-704-555-0199 | Location: Charlotte, NC
LinkedIn: linkedin.com/in/vikram-patel-cfa

SUMMARY
Senior Financial Analyst (FP&A) and CFA Charterholder with 5+ years building dynamic 3-statement financial models, discounted cash flow (DCF) valuations, and corporate budget forecasting for multi-entity enterprises.

SKILLS
- Financial Modeling: 3-Statement Modeling, DCF, LBO, Scenario Sensitivity Analysis
- Analytics & ERP: Advanced Excel/VBA, Power BI, Oracle NetSuite, SAP ERP, SQL
- Accounting & Standards: US GAAP, IFRS, Revenue Recognition (ASC 606), Variance Analysis

EXPERIENCE
Senior FP&A Analyst | Pinnacle Financial Holdings | Charlotte, NC
July 2021 - Present
- Built annual operating budget models forecasting $320M in revenue with 98.4% variance accuracy.
- Prepared board-level quarterly financial decks analyzing SaaS unit economics (CAC, LTV, Net Retention).

Financial Analyst | Crestview Capital Partners | Charlotte, NC
August 2019 - June 2021
- Conducted financial due diligence and cash flow sensitivity models for 12 M&A acquisitions.

EDUCATION
Master of Science in Finance | Vanderbilt University (2018 - 2019)
Bachelor of Science in Accounting & Economics | University of North Carolina at Chapel Hill (2014 - 2018)

CERTIFICATIONS
- Chartered Financial Analyst (CFA) | CFA Institute, 2022
"""
    profile_09 = CandidateProfile(
        candidate_id="cand-009-finance",
        contact_info=ContactInfo(
            full_name="Vikram Patel",
            email="vikram.patel.cfa@example.com",
            phone="+1-704-555-0199",
            location=LocationObject(city="Charlotte", state_or_province="NC", country="USA"),
            linkedin_url="https://linkedin.com/in/vikram-patel-cfa",
        ),
        headline="Senior Financial Analyst (FP&A & Valuation, CFA)",
        professional_summary="Senior Financial Analyst (FP&A) and CFA Charterholder with 5+ years building dynamic 3-statement financial models, discounted cash flow (DCF) valuations, and corporate budget forecasting for multi-entity enterprises.",
        target_role="Lead FP&A Manager",
        domain="Financial Analysis & Modeling",
        total_experience_years=5.2,
        skills=[
            SkillObject(
                name="Financial Modeling & DCF",
                category=SkillCategory.TECHNICAL,
                proficiency=SkillProficiency.EXPERT,
                years_of_experience=5.0,
                last_used_year=2024,
            ),
            SkillObject(
                name="Advanced Excel & VBA",
                category=SkillCategory.TOOL,
                proficiency=SkillProficiency.EXPERT,
                years_of_experience=6.0,
                last_used_year=2024,
            ),
            SkillObject(
                name="US GAAP & ASC 606",
                category=SkillCategory.DOMAIN,
                proficiency=SkillProficiency.ADVANCED,
                years_of_experience=5.0,
                last_used_year=2024,
            ),
            SkillObject(
                name="Power BI & SQL",
                category=SkillCategory.TECHNICAL,
                proficiency=SkillProficiency.ADVANCED,
                years_of_experience=4.0,
                last_used_year=2024,
            ),
        ],
        experience=[
            ExperienceObject(
                company_name="Pinnacle Financial Holdings",
                designation="Senior FP&A Analyst",
                standardized_title="Senior Financial Analyst",
                seniority=SeniorityLevel.SENIOR,
                employment_type=EmploymentType.FULL_TIME,
                location=LocationObject(city="Charlotte", state_or_province="NC", country="USA"),
                start_date="2021-07",
                end_date=None,
                is_current=True,
                achievements=["Budgeted $320M in operating revenue with 98.4% variance accuracy."],
                technologies_used=["Excel", "Power BI", "NetSuite", "SQL"],
            )
        ],
        education=[
            EducationObject(
                institution_name="Vanderbilt University",
                degree="Master of Science in Finance",
                degree_level=DegreeLevel.MASTER,
                field_of_study="Finance",
                start_year=2018,
                end_year=2019,
            )
        ],
        certifications=[
            CertificationObject(
                name="Chartered Financial Analyst (CFA)",
                issuing_organization="CFA Institute",
                issue_date="2022-09",
                credential_id="CFA-99120",
            )
        ],
        languages=[
            LanguageProficiencyObject(language="English", proficiency="NATIVE"),
            LanguageProficiencyObject(language="Hindi", proficiency="FLUENT"),
        ],
        metadata=CandidateMetadata(
            source_file_name="resume_09_finance.txt",
            parser_version="0.1.0",
            extracted_at="2026-10-15T10:00:00Z",
            confidence_score=0.98,
        ),
    )
    resumes.append(("resume_09_finance.txt", raw_09, profile_09))

    # 10. Digital Growth & Marketing Lead
    raw_10 = """CHLOE DUPONT
Email: chloe.dupont.growth@example.com | Phone: +1-512-555-0105 | Location: Austin, TX
LinkedIn: linkedin.com/in/chloe-dupont-growth

SUMMARY
Growth Marketing Lead with 6+ years executing performance marketing, conversion rate optimization (CRO), and multichannel customer acquisition strategies generating $22M+ in pipeline revenue.

SKILLS
- Growth Channels: Paid Search (Google Ads), Paid Social (Meta, LinkedIn Ads), SEO
- MarTech & Tools: HubSpot, Google Analytics 4 (GA4), Segment, Optimizely, Webflow
- Data Skills: A/B Testing, Cohort Retention Analysis, SQL, Attribution Modeling

EXPERIENCE
Growth Marketing Lead | ScaleUp SaaS | Austin, TX
May 2021 - Present
- Scaled qualified inbound lead generation by 145% year-over-year while dropping customer acquisition cost (CAC) by 26%.
- Managed $3.5M annual marketing budget across programmatic display, search, and paid social.

Digital Marketing Specialist | GrowthWave Media | Denver, CO
July 2018 - April 2021
- Ran 200+ landing page A/B tests via Optimizely lifting visitor-to-demo conversion rates from 3.1% to 6.8%.

EDUCATION
Bachelor of Science in Marketing & Communications | University of Texas at Austin (2014 - 2018)

CERTIFICATIONS
- Google Ads Search Professional (Google, 2023)
- HubSpot Inbound Marketing Certified (HubSpot, 2022)
"""
    profile_10 = CandidateProfile(
        candidate_id="cand-010-marketing",
        contact_info=ContactInfo(
            full_name="Chloe Dupont",
            email="chloe.dupont.growth@example.com",
            phone="+1-512-555-0105",
            location=LocationObject(city="Austin", state_or_province="TX", country="USA"),
            linkedin_url="https://linkedin.com/in/chloe-dupont-growth",
        ),
        headline="Growth Marketing & Performance Acquisition Lead",
        professional_summary="Growth Marketing Lead with 6+ years executing performance marketing, conversion rate optimization (CRO), and multichannel customer acquisition strategies generating $22M+ in pipeline revenue.",
        target_role="Director of Growth Marketing",
        domain="Digital Growth & Marketing",
        total_experience_years=6.3,
        skills=[
            SkillObject(
                name="Performance Marketing & Paid Ads",
                category=SkillCategory.TECHNICAL,
                proficiency=SkillProficiency.EXPERT,
                years_of_experience=6.0,
                last_used_year=2024,
            ),
            SkillObject(
                name="Conversion Rate Optimization (CRO)",
                category=SkillCategory.METHODOLOGY,
                proficiency=SkillProficiency.EXPERT,
                years_of_experience=5.0,
                last_used_year=2024,
            ),
            SkillObject(
                name="Google Analytics 4 / GA4",
                category=SkillCategory.TOOL,
                proficiency=SkillProficiency.ADVANCED,
                years_of_experience=4.0,
                last_used_year=2024,
            ),
            SkillObject(
                name="Attribution Modeling & SQL",
                category=SkillCategory.TECHNICAL,
                proficiency=SkillProficiency.ADVANCED,
                years_of_experience=4.5,
                last_used_year=2024,
            ),
        ],
        experience=[
            ExperienceObject(
                company_name="ScaleUp SaaS",
                designation="Growth Marketing Lead",
                standardized_title="Growth Marketing Lead",
                seniority=SeniorityLevel.LEAD,
                employment_type=EmploymentType.FULL_TIME,
                location=LocationObject(city="Austin", state_or_province="TX", country="USA"),
                start_date="2021-05",
                end_date=None,
                is_current=True,
                achievements=[
                    "Scaled inbound pipeline by 145% YoY and cut customer acquisition costs by 26%."
                ],
                technologies_used=["Google Ads", "HubSpot", "GA4", "Optimizely"],
            )
        ],
        education=[
            EducationObject(
                institution_name="University of Texas at Austin",
                degree="Bachelor of Science in Marketing & Communications",
                degree_level=DegreeLevel.BACHELOR,
                field_of_study="Marketing & Communications",
                start_year=2014,
                end_year=2018,
            )
        ],
        certifications=[
            CertificationObject(
                name="Google Ads Search Professional",
                issuing_organization="Google",
                issue_date="2023-02",
            )
        ],
        languages=[
            LanguageProficiencyObject(language="English", proficiency="NATIVE"),
            LanguageProficiencyObject(language="French", proficiency="PROFICIENT"),
        ],
        metadata=CandidateMetadata(
            source_file_name="resume_10_marketing.txt",
            parser_version="0.1.0",
            extracted_at="2026-10-15T10:00:00Z",
            confidence_score=0.99,
        ),
    )
    resumes.append(("resume_10_marketing.txt", raw_10, profile_10))

    return resumes


def get_raw_and_structured_jobs() -> list[tuple[str, str, JobProfile]]:
    """Return pairs of (raw_filename, raw_text, structured_job) for 4 technical & non-tech JDs."""
    jobs = []

    # 1. Senior Backend Distributed Systems Engineer (Technical)
    raw_jd_01 = """JOB REQUISITION: Senior Backend Distributed Systems Engineer
Company: CloudScale Infrastructure Inc.
Location: San Francisco, CA (Hybrid)
Role Type: Technical | Employment Type: Full-time

ABOUT THE ROLE:
CloudScale is looking for an experienced Senior Backend Distributed Systems Engineer to scale our transactional core engine processing over 50M API transactions daily.

RESPONSIBILITIES:
- Architect, build, and deploy low-latency, event-driven microservices in Go and Python.
- Maintain mission-critical PostgreSQL and Kafka clustering with zero downtime guarantees.
- Mentor mid-level and junior engineers on distributed consensus, testing, and production telemetry.

REQUIREMENTS:
- Minimum 5+ years of production experience in backend or systems engineering.
- Expertise in Go or Python with deep knowledge of concurrency, garbage collection, and profiling.
- Strong hands-on experience with Kafka, PostgreSQL, Docker, and Kubernetes.
- Bachelor's degree in Computer Science or equivalent practical experience.

COMPENSATION & BENEFITS:
- $165,000 - $210,000 base annual salary + equity
- Comprehensive health, dental, and 401(k) matching
"""
    job_01 = JobProfile(
        job_id="job-001-backend-dist",
        title="Senior Backend Distributed Systems Engineer",
        company_name="CloudScale Infrastructure Inc.",
        department="Core Engineering",
        role_type=RoleType.TECHNICAL,
        seniority_level=SeniorityLevel.SENIOR,
        employment_type=EmploymentType.FULL_TIME,
        workplace_type=WorkplaceType.HYBRID,
        location=LocationObject(
            city="San Francisco", state_or_province="CA", country="USA", is_remote=False
        ),
        salary_range=SalaryRange(
            currency="USD", min_amount=165000.0, max_amount=210000.0, pay_period=PayPeriod.ANNUAL
        ),
        summary="CloudScale is seeking a Senior Backend Distributed Systems Engineer to scale high-throughput core financial and telemetry microservices.",
        responsibilities=[
            "Architect, build, and deploy low-latency, event-driven microservices in Go and Python.",
            "Maintain mission-critical PostgreSQL and Kafka clustering with zero downtime guarantees.",
            "Mentor mid-level and junior engineers on distributed consensus, testing, and production telemetry.",
        ],
        requirements=JobRequirements(
            minimum_experience_years=5.0,
            required_skills=[
                SkillObject(
                    name="Go",
                    category=SkillCategory.TECHNICAL,
                    proficiency=SkillProficiency.ADVANCED,
                ),
                SkillObject(
                    name="Distributed Systems",
                    category=SkillCategory.TECHNICAL,
                    proficiency=SkillProficiency.ADVANCED,
                ),
                SkillObject(
                    name="PostgreSQL",
                    category=SkillCategory.DATABASE,
                    proficiency=SkillProficiency.ADVANCED,
                ),
                SkillObject(
                    name="Apache Kafka",
                    category=SkillCategory.TOOL,
                    proficiency=SkillProficiency.INTERMEDIATE,
                ),
            ],
            preferred_skills=[
                SkillObject(
                    name="Kubernetes",
                    category=SkillCategory.CLOUD_DEVOPS,
                    proficiency=SkillProficiency.INTERMEDIATE,
                ),
                SkillObject(
                    name="gRPC",
                    category=SkillCategory.FRAMEWORK,
                    proficiency=SkillProficiency.INTERMEDIATE,
                ),
            ],
            minimum_education_level=DegreeLevel.BACHELOR,
            required_certifications=[],
        ),
        benefits=["Comprehensive health, dental, vision", "401(k) matching", "Equity grant"],
        created_at="2026-10-01",
        is_active=True,
    )
    jobs.append(("jd_01_senior_backend.txt", raw_jd_01, job_01))

    # 2. Staff Machine Learning & AI Engineer (Technical)
    raw_jd_02 = """JOB REQUISITION: Staff Machine Learning & Generative AI Engineer
Company: DeepThought Systems
Location: Boston, MA (Hybrid or Remote)
Role Type: Technical | Employment Type: Full-time

ABOUT THE ROLE:
DeepThought Systems is hiring a Staff ML Engineer to build production foundation model workflows, agentic orchestration, and advanced RAG architectures.

RESPONSIBILITIES:
- Lead the architecture and implementation of enterprise LLM fine-tuning and inference pipelines.
- Integrate vector databases, semantic caching, and guardrail validation into real-time APIs.
- Collaborate with product managers and researchers to turn cutting-edge model research into reliable products.

REQUIREMENTS:
- Minimum 6+ years of machine learning engineering experience in production.
- Deep expertise in PyTorch, Hugging Face, vector retrieval (Milvus/Pinecone), and MLOps pipelines.
- Master's or Ph.D. in Computer Science, AI, or related quantitative field preferred.

COMPENSATION:
- $190,000 - $240,000 base annual salary + competitive equity
"""
    job_02 = JobProfile(
        job_id="job-002-staff-ml",
        title="Staff Machine Learning & Generative AI Engineer",
        company_name="DeepThought Systems",
        department="AI Research & Engineering",
        role_type=RoleType.TECHNICAL,
        seniority_level=SeniorityLevel.LEAD,
        employment_type=EmploymentType.FULL_TIME,
        workplace_type=WorkplaceType.HYBRID,
        location=LocationObject(
            city="Boston", state_or_province="MA", country="USA", is_remote=True
        ),
        salary_range=SalaryRange(
            currency="USD", min_amount=190000.0, max_amount=240000.0, pay_period=PayPeriod.ANNUAL
        ),
        summary="Leading enterprise foundation model fine-tuning, RAG indexing, and low-latency inference pipelines.",
        responsibilities=[
            "Lead architecture and implementation of enterprise LLM fine-tuning pipelines.",
            "Integrate vector databases and semantic caching into production APIs.",
            "Establish automated evaluation benchmarks and safety guardrails.",
        ],
        requirements=JobRequirements(
            minimum_experience_years=6.0,
            required_skills=[
                SkillObject(
                    name="PyTorch",
                    category=SkillCategory.FRAMEWORK,
                    proficiency=SkillProficiency.EXPERT,
                ),
                SkillObject(
                    name="Large Language Models (LLMs)",
                    category=SkillCategory.TECHNICAL,
                    proficiency=SkillProficiency.ADVANCED,
                ),
                SkillObject(
                    name="Vector Databases",
                    category=SkillCategory.DATABASE,
                    proficiency=SkillProficiency.ADVANCED,
                ),
            ],
            preferred_skills=[
                SkillObject(
                    name="Triton Inference Server",
                    category=SkillCategory.TOOL,
                    proficiency=SkillProficiency.INTERMEDIATE,
                ),
                SkillObject(
                    name="Kubeflow",
                    category=SkillCategory.CLOUD_DEVOPS,
                    proficiency=SkillProficiency.INTERMEDIATE,
                ),
            ],
            minimum_education_level=DegreeLevel.MASTER,
            required_certifications=[],
        ),
        benefits=[
            "Health, dental, and life coverage",
            "Home office stipend",
            "Generous equity grant",
        ],
        created_at="2026-10-05",
        is_active=True,
    )
    jobs.append(("jd_02_ml_engineer.txt", raw_jd_02, job_02))

    # 3. Senior Talent Acquisition Partner (Non-Technical)
    raw_jd_03 = """JOB REQUISITION: Senior Talent Acquisition Partner
Company: HyperScale AI
Location: Atlanta, GA (Remote)
Role Type: Non-Technical | Employment Type: Full-time

ABOUT THE ROLE:
HyperScale AI is scaling its global talent operations. We are seeking a consultative Senior Talent Partner to lead full-lifecycle technical and non-technical hiring across our product and engineering departments.

RESPONSIBILITIES:
- Partner directly with VP of Engineering and Department Heads to define headcount requirements.
- Drive active sourcing, boolean search, and outreach campaigns to attract high-caliber passive candidates.
- Ensure fair, objective candidate evaluation and deliver an NPS-leading candidate experience.

REQUIREMENTS:
- 5+ years of full-lifecycle recruiting experience, preferably in high-growth technology or AI startups.
- Expert-level proficiency with modern ATS platforms (Greenhouse, Ashby, or Lever).
- Excellent verbal communication, negotiation skills, and commitment to DEI hiring.
- Bachelor's degree in HR, Business, or related discipline.

COMPENSATION:
- $110,000 - $140,000 base annual salary + quarterly performance bonus
"""
    job_03 = JobProfile(
        job_id="job-003-senior-talent",
        title="Senior Talent Acquisition Partner",
        company_name="HyperScale AI",
        department="People & Talent Operations",
        role_type=RoleType.NON_TECHNICAL,
        seniority_level=SeniorityLevel.SENIOR,
        employment_type=EmploymentType.FULL_TIME,
        workplace_type=WorkplaceType.REMOTE,
        location=LocationObject(
            city="Atlanta", state_or_province="GA", country="USA", is_remote=True
        ),
        salary_range=SalaryRange(
            currency="USD", min_amount=110000.0, max_amount=140000.0, pay_period=PayPeriod.ANNUAL
        ),
        summary="Partnering with executive leadership to run full-lifecycle hiring across engineering, product, and business units.",
        responsibilities=[
            "Partner directly with VP of Engineering and Department Heads to define headcount requirements.",
            "Drive active sourcing, boolean search, and outreach campaigns to attract top passive talent.",
            "Manage candidate offer generation, closing negotiations, and onboarding handoffs.",
        ],
        requirements=JobRequirements(
            minimum_experience_years=5.0,
            required_skills=[
                SkillObject(
                    name="Technical Recruiting",
                    category=SkillCategory.DOMAIN,
                    proficiency=SkillProficiency.ADVANCED,
                ),
                SkillObject(
                    name="Greenhouse ATS",
                    category=SkillCategory.TOOL,
                    proficiency=SkillProficiency.ADVANCED,
                ),
                SkillObject(
                    name="Candidate Sourcing & Outreach",
                    category=SkillCategory.DOMAIN,
                    proficiency=SkillProficiency.ADVANCED,
                ),
            ],
            preferred_skills=[
                SkillObject(
                    name="DEI Strategy",
                    category=SkillCategory.DOMAIN,
                    proficiency=SkillProficiency.INTERMEDIATE,
                ),
            ],
            minimum_education_level=DegreeLevel.BACHELOR,
            required_certifications=[],
        ),
        benefits=["100% remote flexibility", "Annual wellness stipend", "Performance bonus"],
        created_at="2026-10-08",
        is_active=True,
    )
    jobs.append(("jd_03_talent_acquisition.txt", raw_jd_03, job_03))

    # 4. Lead Financial Planning & Analysis (FP&A) Analyst (Non-Technical)
    raw_jd_04 = """JOB REQUISITION: Lead Financial Planning & Analysis (FP&A) Analyst
Company: Pinnacle Financial Holdings
Location: Charlotte, NC (Onsite / Hybrid)
Role Type: Non-Technical | Employment Type: Full-time

ABOUT THE ROLE:
Pinnacle Financial is looking for a Lead FP&A Analyst to direct corporate budgeting, financial modeling, and strategic revenue variance analysis.

RESPONSIBILITIES:
- Build and maintain multi-year 3-statement integrated financial models.
- Lead quarterly business reviews (QBRs) and deliver board deck presentations on departmental spending.
- Partner with product and sales operations on price elasticity and customer unit economics.

REQUIREMENTS:
- 5+ years of progressive corporate finance, investment banking, or FP&A experience.
- Mastery of financial statement modeling, DCF, and sensitivity analysis.
- Advanced proficiency in Excel, Power BI, SQL, and enterprise ERP systems (NetSuite/SAP).
- Bachelor's degree in Finance, Accounting, or Economics; CFA or CPA strongly preferred.

COMPENSATION:
- $135,000 - $165,000 base annual salary + 15% annual bonus
"""
    job_04 = JobProfile(
        job_id="job-004-lead-fpa",
        title="Lead Financial Planning & Analysis (FP&A) Analyst",
        company_name="Pinnacle Financial Holdings",
        department="Corporate Finance",
        role_type=RoleType.NON_TECHNICAL,
        seniority_level=SeniorityLevel.LEAD,
        employment_type=EmploymentType.FULL_TIME,
        workplace_type=WorkplaceType.HYBRID,
        location=LocationObject(
            city="Charlotte", state_or_province="NC", country="USA", is_remote=False
        ),
        salary_range=SalaryRange(
            currency="USD", min_amount=135000.0, max_amount=165000.0, pay_period=PayPeriod.ANNUAL
        ),
        summary="Leading corporate budgeting, 3-statement modeling, and SaaS unit economics evaluation for executive stakeholders.",
        responsibilities=[
            "Build and maintain multi-year 3-statement integrated financial models.",
            "Lead quarterly business reviews (QBRs) and deliver board deck presentations.",
            "Analyze customer cohort retention and price elasticity with sales operations.",
        ],
        requirements=JobRequirements(
            minimum_experience_years=5.0,
            required_skills=[
                SkillObject(
                    name="Financial Modeling",
                    category=SkillCategory.TECHNICAL,
                    proficiency=SkillProficiency.EXPERT,
                ),
                SkillObject(
                    name="Corporate Budgeting & FP&A",
                    category=SkillCategory.DOMAIN,
                    proficiency=SkillProficiency.EXPERT,
                ),
                SkillObject(
                    name="Advanced Excel",
                    category=SkillCategory.TOOL,
                    proficiency=SkillProficiency.EXPERT,
                ),
            ],
            preferred_skills=[
                SkillObject(
                    name="Power BI",
                    category=SkillCategory.TOOL,
                    proficiency=SkillProficiency.ADVANCED,
                ),
                SkillObject(
                    name="SQL",
                    category=SkillCategory.TECHNICAL,
                    proficiency=SkillProficiency.INTERMEDIATE,
                ),
            ],
            minimum_education_level=DegreeLevel.BACHELOR,
            required_certifications=["CFA or CPA preferred"],
        ),
        benefits=[
            "401(k) with 6% company match",
            "Comprehensive health insurance",
            "Tuition reimbursement",
        ],
        created_at="2026-10-10",
        is_active=True,
    )
    jobs.append(("jd_04_financial_analyst.txt", raw_jd_04, job_04))

    return jobs


def main() -> None:
    """Create directory hierarchy and populate all sample datasets."""
    base_data = repo_root / "data"
    raw_resumes_dir = base_data / "raw" / "resumes"
    raw_jds_dir = base_data / "raw" / "job_descriptions"
    struct_resumes_dir = base_data / "structured" / "resumes"
    struct_jds_dir = base_data / "structured" / "job_descriptions"

    for directory in [raw_resumes_dir, raw_jds_dir, struct_resumes_dir, struct_jds_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    print("Generating 10 multi-domain resumes...")
    for filename, raw_text, profile in get_raw_and_structured_resumes():
        # Save raw text
        raw_path = raw_resumes_dir / filename
        raw_path.write_text(raw_text.strip(), encoding="utf-8")

        # Save structured JSON
        json_filename = filename.replace(".txt", ".json")
        json_path = struct_resumes_dir / json_filename
        json_path.write_text(profile.model_dump_json(indent=2), encoding="utf-8")
        print(
            f"  [Resume] Saved {raw_path.name} -> {json_path.name} (Valid: {profile.candidate_id})"
        )

    print("\nGenerating 4 technical & non-technical job descriptions...")
    for filename, raw_text, job in get_raw_and_structured_jobs():
        # Save raw text
        raw_path = raw_jds_dir / filename
        raw_path.write_text(raw_text.strip(), encoding="utf-8")

        # Save structured JSON
        json_filename = filename.replace(".txt", ".json")
        json_path = struct_jds_dir / json_filename
        json_path.write_text(job.model_dump_json(indent=2), encoding="utf-8")
        print(f"  [JD] Saved {raw_path.name} -> {json_path.name} (Valid: {job.job_id})")

    print("\nAll sample datasets generated successfully!")


if __name__ == "__main__":
    main()
