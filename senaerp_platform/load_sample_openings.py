#!/usr/bin/env python3
"""
Script to create sample job openings for Opening doctype
Run: bench --site senatest2.localhost execute sentra_core.load_sample_openings.load_sample_openings
"""

import frappe


def load_sample_openings():
    """Create sample job openings with comprehensive descriptions"""

    sample_openings = [
        {
            "title": "Fullstack Engineer",
            "department": "Engineering",
            "positions_open": 3,
            "experience_required": "2-5 years",
            "job_description": """<div class="ql-editor read-mode">
<h3>About the Role</h3>
<p>We're looking for talented Fullstack Engineers to join our engineering team and help build the future of business software. You'll be working on Sena, our AI-first ERP platform, touching everything from frontend React components to backend Python services. This is a unique opportunity to work with cutting-edge AI technology while solving real-world business problems.</p>

<h3>What You'll Do</h3>
<ul>
<li>Design and implement new features across the full stack (React/Next.js frontend, Python/Frappe backend)</li>
<li>Build responsive and intuitive user interfaces that delight users</li>
<li>Develop robust backend APIs and integrate with AI services (OpenAI, Anthropic)</li>
<li>Collaborate closely with product, design, and AI teams to deliver exceptional experiences</li>
<li>Write clean, maintainable, well-tested code following best practices</li>
<li>Participate in code reviews and contribute to technical architecture decisions</li>
<li>Optimize application performance and scalability</li>
<li>Debug production issues and implement monitoring solutions</li>
</ul>

<h3>What We're Looking For</h3>
<ul>
<li>2-5 years of professional software development experience</li>
<li>Strong proficiency in JavaScript/TypeScript and modern frontend frameworks (React, Next.js, Vue)</li>
<li>Solid backend experience with Python and API development</li>
<li>Experience with RESTful APIs, database design (PostgreSQL, MySQL), and ORM frameworks</li>
<li>Understanding of web performance optimization and security best practices</li>
<li>Excellent problem-solving and debugging skills</li>
<li>Strong communication and collaboration abilities</li>
<li>Self-motivated with ability to work independently in a remote environment</li>
</ul>

<h3>Nice to Have</h3>
<ul>
<li>Experience with Frappe Framework or ERPNext</li>
<li>Knowledge of AI/ML integration in web applications</li>
<li>Experience with cloud platforms (AWS, GCP, Azure)</li>
<li>Familiarity with Docker, Kubernetes, and CI/CD pipelines</li>
<li>Contributions to open-source projects</li>
<li>Experience in B2B SaaS or enterprise software</li>
</ul>

<h3>What We Offer</h3>
<ul>
<li>Competitive salary and equity package</li>
<li>Remote-friendly work environment with flexible hours</li>
<li>Health, dental, and vision insurance</li>
<li>Learning and development budget</li>
<li>Latest hardware and software tools</li>
<li>Opportunity to work on cutting-edge AI technology</li>
<li>Collaborative and inclusive team culture</li>
</ul>
</div>""",
            "is_active": 1
        },
        {
            "title": "UI/UX Designer",
            "department": "Design",
            "positions_open": 2,
            "experience_required": "3-5 years",
            "job_description": """<div class="ql-editor read-mode">
<h3>About the Role</h3>
<p>Join our design team as a UI/UX Designer and help shape the user experience of Sena, our next-generation AI-powered ERP platform. You'll be responsible for creating beautiful, intuitive interfaces that make complex business workflows feel effortless. This role is perfect for someone who is passionate about user-centered design and wants to make a real impact on how businesses operate.</p>

<h3>What You'll Do</h3>
<ul>
<li>Design elegant and intuitive user interfaces for web applications</li>
<li>Conduct user research, interviews, and usability testing to understand user needs</li>
<li>Create user flows, wireframes, prototypes, and high-fidelity mockups</li>
<li>Develop and maintain our design system and component library</li>
<li>Collaborate with product managers and engineers to bring designs to life</li>
<li>Design AI-powered features and conversational interfaces</li>
<li>Iterate on designs based on user feedback and analytics data</li>
<li>Ensure consistency and accessibility across all touchpoints</li>
<li>Stay current with design trends and best practices</li>
</ul>

<h3>What We're Looking For</h3>
<ul>
<li>3-5 years of experience in UI/UX design, preferably in B2B SaaS or enterprise software</li>
<li>Strong portfolio demonstrating excellent visual design and UX thinking</li>
<li>Expert proficiency in Figma (our primary design tool)</li>
<li>Deep understanding of user-centered design principles and methodologies</li>
<li>Experience with design systems and component-based design</li>
<li>Knowledge of web technologies (HTML, CSS) and design constraints</li>
<li>Excellent communication and presentation skills</li>
<li>Ability to give and receive constructive feedback</li>
<li>Detail-oriented with strong organizational skills</li>
</ul>

<h3>Nice to Have</h3>
<ul>
<li>Experience designing for AI-powered products or conversational interfaces</li>
<li>Knowledge of accessibility standards (WCAG)</li>
<li>Experience with motion design and micro-interactions</li>
<li>Familiarity with front-end development (React, CSS)</li>
<li>Background in graphic design or illustration</li>
<li>Experience conducting design workshops and design sprints</li>
<li>Knowledge of ERP systems or business software</li>
</ul>

<h3>What We Offer</h3>
<ul>
<li>Competitive salary and equity package</li>
<li>Remote-friendly work environment with flexible hours</li>
<li>Comprehensive health benefits</li>
<li>Professional development budget for conferences and courses</li>
<li>Latest design tools and hardware (MacBook Pro, external monitors)</li>
<li>Collaborative design team that values creativity and innovation</li>
<li>Opportunity to shape the design direction of the company</li>
</ul>
</div>""",
            "is_active": 1
        },
        {
            "title": "Marketing Intern",
            "department": "Marketing",
            "positions_open": 2,
            "experience_required": "0-1 years",
            "job_description": """<div class="ql-editor read-mode">
<h3>About the Role</h3>
<p>We're seeking creative and motivated Marketing Interns to join our growing marketing team. This is a fantastic opportunity for students or recent graduates to gain hands-on experience in B2B SaaS marketing, content creation, and growth strategies. You'll work on real projects that directly impact our business and learn from experienced marketers.</p>

<h3>What You'll Do</h3>
<ul>
<li>Create engaging content for our blog, social media channels, and email campaigns</li>
<li>Assist with market research and competitive analysis</li>
<li>Help manage our social media presence (Twitter, LinkedIn, Instagram)</li>
<li>Support the execution of marketing campaigns and product launches</li>
<li>Analyze marketing metrics and prepare performance reports</li>
<li>Assist with SEO optimization and keyword research</li>
<li>Help create marketing materials (presentations, one-pagers, case studies)</li>
<li>Coordinate with design team on visual content</li>
<li>Participate in brainstorming sessions and contribute creative ideas</li>
<li>Stay up-to-date with marketing trends and best practices</li>
</ul>

<h3>What We're Looking For</h3>
<ul>
<li>Currently pursuing or recently completed a degree in Marketing, Communications, Business, or related field</li>
<li>Strong writing and communication skills with attention to detail</li>
<li>Passion for marketing, technology, and learning</li>
<li>Basic understanding of digital marketing concepts (social media, SEO, email marketing)</li>
<li>Familiarity with social media platforms and trends</li>
<li>Creative mindset with ability to generate fresh ideas</li>
<li>Proficiency in Google Workspace (Docs, Sheets, Slides)</li>
<li>Self-starter who can work independently and take initiative</li>
<li>Excellent organizational and time management skills</li>
</ul>

<h3>Nice to Have</h3>
<ul>
<li>Experience with Canva, Adobe Creative Suite, or other design tools</li>
<li>Basic knowledge of analytics tools (Google Analytics, social media insights)</li>
<li>Understanding of AI/ML technologies and trends</li>
<li>Experience managing social media accounts (personal or professional)</li>
<li>Video editing skills</li>
<li>Previous internship experience in marketing or related field</li>
</ul>

<h3>What We Offer</h3>
<ul>
<li>Competitive internship stipend</li>
<li>Flexible remote work arrangement (part-time or full-time)</li>
<li>Mentorship from experienced marketing professionals</li>
<li>Opportunity to work on real projects with measurable impact</li>
<li>Learn about B2B SaaS marketing and growth strategies</li>
<li>Networking opportunities within the tech industry</li>
<li>Potential for full-time employment based on performance</li>
<li>Professional development and skill-building opportunities</li>
</ul>

<p><strong>Duration:</strong> 3-6 months with possibility of extension</p>
</div>""",
            "is_active": 1
        },
        {
            "title": "Engineering Intern",
            "department": "Engineering",
            "positions_open": 3,
            "experience_required": "0-1 years",
            "job_description": """<div class="ql-editor read-mode">
<h3>About the Role</h3>
<p>Join our engineering team as an Engineering Intern and get hands-on experience building real-world applications with modern web technologies and AI. You'll work alongside experienced engineers on Sena, our AI-first ERP platform, contributing to features that impact businesses worldwide. This internship is perfect for students or recent graduates passionate about software development and eager to learn.</p>

<h3>What You'll Do</h3>
<ul>
<li>Work on real features and bug fixes for our web application</li>
<li>Write clean, well-documented code in JavaScript/TypeScript and Python</li>
<li>Collaborate with senior engineers through pair programming and code reviews</li>
<li>Build responsive UI components using React and Next.js</li>
<li>Develop backend APIs and integrate with AI services</li>
<li>Write unit tests and participate in quality assurance</li>
<li>Learn about system architecture, database design, and API development</li>
<li>Participate in agile development processes (sprint planning, standups, retros)</li>
<li>Debug issues and implement fixes</li>
<li>Contribute to technical documentation</li>
</ul>

<h3>What We're Looking For</h3>
<ul>
<li>Currently pursuing or recently completed a degree in Computer Science, Software Engineering, or related field</li>
<li>Solid understanding of programming fundamentals (data structures, algorithms, OOP)</li>
<li>Experience with at least one programming language (JavaScript, Python, Java, or similar)</li>
<li>Basic knowledge of web development (HTML, CSS, JavaScript)</li>
<li>Familiarity with Git and version control</li>
<li>Strong problem-solving skills and logical thinking</li>
<li>Eager to learn new technologies and best practices</li>
<li>Good communication and teamwork abilities</li>
<li>Self-motivated and able to work independently with guidance</li>
</ul>

<h3>Nice to Have</h3>
<ul>
<li>Experience with React, Vue, or other modern JavaScript frameworks</li>
<li>Knowledge of Python web frameworks (Flask, Django, FastAPI)</li>
<li>Understanding of RESTful APIs and HTTP protocols</li>
<li>Familiarity with SQL databases (PostgreSQL, MySQL)</li>
<li>Experience with AI/ML concepts or APIs (OpenAI, Hugging Face)</li>
<li>Previous internship or project experience</li>
<li>Contributions to open-source projects or personal GitHub projects</li>
<li>Knowledge of Docker, cloud platforms, or DevOps concepts</li>
</ul>

<h3>What You'll Learn</h3>
<ul>
<li>Full-stack web development with modern technologies (React, Next.js, Python)</li>
<li>Building and deploying production applications</li>
<li>Working with AI APIs and implementing AI-powered features</li>
<li>Software engineering best practices (testing, code review, documentation)</li>
<li>Agile development methodologies</li>
<li>Collaboration and communication in a remote team</li>
</ul>

<h3>What We Offer</h3>
<ul>
<li>Competitive internship compensation</li>
<li>Flexible remote work with flexible hours</li>
<li>Mentorship from experienced senior engineers</li>
<li>Real-world project experience for your portfolio</li>
<li>Learning and development resources</li>
<li>Access to modern development tools and technologies</li>
<li>Opportunity to work on cutting-edge AI technology</li>
<li>Potential for full-time employment based on performance</li>
<li>Collaborative and supportive team environment</li>
</ul>

<p><strong>Duration:</strong> 3-6 months with possibility of extension or full-time conversion</p>
</div>""",
            "is_active": 1
        },
        {
            "title": "Product Manager",
            "department": "Product",
            "positions_open": 1,
            "experience_required": "4-6 years",
            "job_description": """<div class="ql-editor read-mode">
<h3>About the Role</h3>
<p>We're looking for an experienced Product Manager to drive the vision and execution of Sena, our AI-first ERP platform. You'll work at the intersection of AI, business software, and user experience, defining what we build and why. This is a high-impact role where you'll shape product strategy, work closely with customers, and lead cross-functional teams to deliver innovative solutions.</p>

<h3>What You'll Do</h3>
<ul>
<li>Define and own the product roadmap for key product areas</li>
<li>Conduct user research and gather customer feedback to inform product decisions</li>
<li>Write detailed product requirements and specifications</li>
<li>Work closely with engineering, design, and AI teams to deliver features</li>
<li>Define success metrics and analyze product performance</li>
<li>Prioritize features based on business impact, user value, and technical feasibility</li>
<li>Conduct competitive analysis and market research</li>
<li>Collaborate with sales and customer success on go-to-market strategy</li>
<li>Run beta programs and gather feedback from early adopters</li>
<li>Make data-driven decisions to optimize product-market fit</li>
<li>Communicate product vision and updates to stakeholders</li>
</ul>

<h3>What We're Looking For</h3>
<ul>
<li>4-6 years of product management experience, preferably in B2B SaaS or enterprise software</li>
<li>Proven track record of shipping successful products from 0 to 1 or scaling existing products</li>
<li>Strong analytical skills with experience using data to drive decisions</li>
<li>Excellent communication and stakeholder management abilities</li>
<li>Deep empathy for users and passion for solving customer problems</li>
<li>Technical background or strong technical fluency to work effectively with engineers</li>
<li>Experience with agile development methodologies</li>
<li>Strategic thinker who can also execute on tactical details</li>
<li>Self-starter who thrives in fast-paced, ambiguous environments</li>
</ul>

<h3>Nice to Have</h3>
<ul>
<li>Experience with AI/ML products or working with AI teams</li>
<li>Knowledge of ERP systems, business workflows, or enterprise software</li>
<li>Background in software engineering or technical degree</li>
<li>Experience with product analytics tools (Mixpanel, Amplitude, Heap)</li>
<li>Familiarity with design tools (Figma) and ability to create mockups</li>
<li>Experience conducting user interviews and usability testing</li>
<li>MBA or advanced degree in a relevant field</li>
<li>Experience in a high-growth startup environment</li>
</ul>

<h3>What We Offer</h3>
<ul>
<li>Competitive salary and significant equity package</li>
<li>Remote-friendly work environment with flexible hours</li>
<li>Comprehensive health, dental, and vision insurance</li>
<li>Professional development budget</li>
<li>Opportunity to shape the product direction of a growing company</li>
<li>Work on cutting-edge AI technology with real business impact</li>
<li>Collaborative and transparent company culture</li>
<li>Direct access to founders and leadership team</li>
<li>Influence over company strategy and direction</li>
</ul>
</div>""",
            "is_active": 1
        },
    ]

    created = 0
    updated = 0
    for opening_data in sample_openings:
        try:
            # Check if opening already exists
            if frappe.db.exists("Job Opening", opening_data["title"]):
                # Update existing opening
                opening = frappe.get_doc("Job Opening", opening_data["title"])
                for key, value in opening_data.items():
                    if key != "title":  # Don't update the title (it's the primary key)
                        opening.set(key, value)
                opening.save()
                frappe.db.commit()
                updated += 1
                print(f"↻ Updated opening: {opening_data['title']}")
            else:
                # Create new opening
                opening = frappe.get_doc({
                    "doctype": "Job Opening",
                    **opening_data
                })
                opening.insert()
                frappe.db.commit()
                created += 1
                print(f"✓ Created opening: {opening_data['title']}")

        except Exception as e:
            print(f"✗ Error processing opening '{opening_data['title']}': {str(e)}")
            frappe.db.rollback()

    print(f"\n{'='*50}")
    print(f"Created {created} new job openings")
    print(f"Updated {updated} existing job openings")
    print(f"{'='*50}")
