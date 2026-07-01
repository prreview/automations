#!/usr/bin/env python3
"""Generate company.md files for all startups with hiring=true."""

import json
import os
import re

OUTPUT_DIR = os.path.expanduser("~/automations/goal/100-company")
INPUT_FILE = os.path.join(OUTPUT_DIR, "startups_data.json")

def slugify(name):
    """Convert company name to slug: lowercase, hyphens."""
    s = name.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = s.strip('-')
    return s

def format_founders(founders):
    if not founders:
        return "Not found"
    if len(founders) == 1:
        return founders[0]
    if len(founders) == 2:
        return f"{founders[0]}, {founders[1]}"
    return ", ".join(founders)

def format_roles(roles):
    if not roles:
        return "Engineering roles (see careers page)"
    return ", ".join(roles)

def format_job_urls(job_urls, source):
    if job_urls:
        lines = [f"  - {u}" for u in job_urls]
        return "\n".join(lines)
    else:
        return f"  - {source}"

def classify_role(roles_text):
    """Classify the role type for tailored outreach."""
    roles_lower = roles_text.lower()
    if any(k in roles_lower for k in ['founding', 'founder']):
        return 'founding'
    if any(k in roles_lower for k in ['frontend', 'front-end', 'front end', 'ui', 'react']):
        # Check if also fullstack
        if any(k in roles_lower for k in ['full stack', 'fullstack', 'full-stack']):
            return 'fullstack'
        return 'frontend'
    if any(k in roles_lower for k in ['full stack', 'fullstack', 'full-stack']):
        return 'fullstack'
    if any(k in roles_lower for k in ['backend', 'back-end', 'back end', 'sde', 'software engineer', 'systems engineer', 'senior sw', 'senior software', 'architect', 'lead', 'staff', 'devrel', 'distributed']):
        return 'backend'
    if any(k in roles_lower for k in ['ai', 'ml', 'applied ai', 'agentic', 'genai']):
        return 'ai'
    if any(k in roles_lower for k in ['smart contract', 'blockchain', 'web3']):
        return 'web3'
    if any(k in roles_lower for k in ['engineering manager', 'manager']):
        return 'manager'
    return 'fullstack'  # default

def get_cold_email(company_name, description, roles, role_type):
    """Generate a personalized cold email."""
    roles_str = format_roles(roles)
    
    # Subject lines
    subjects = {
        'fullstack': f"built a codegen transpiler + rag pipelines — fit for {roles_str.split(',')[0].strip()}?",
        'frontend': f"react performance + microfrontends — fit for {roles_str.split(',')[0].strip()}?",
        'founding': f"founding engineer at rava.ai + repo-aware ai at trevyn",
        'backend': f"backend ownership at rava.ai + codegen at wavemaker",
        'ai': f"built llm workflows at rava.ai — fit for {roles_str.split(',')[0].strip()}?",
        'web3': f"smart contracts + fullstack — interested in {company_name}",
        'manager': f"led engineering at rava.ai + trevyn — interested in {company_name}",
    }
    subject = subjects.get(role_type, subjects['fullstack'])
    
    # Body intros based on role type
    if role_type == 'founding':
        body = f"saw {company_name} is hiring a founding engineer. i was the founding engineer at rava.ai where i built llm workflows and rag pipelines from scratch — owned the entire backend. before that i built a code generation transpiler at wavemaker that turns visual designs into react/next.js code.\n\nat trevyn (my current project), i built a repo-aware ai pr review system that reads git diffs and suggests fixes. {description[:80]} feels like something i'd want to build on."
    elif role_type == 'frontend':
        body = f"looking at the {roles_str.split(',')[0].strip()} role at {company_name}. i spent 2+ years at wavemaker building a code generation transpiler — turns visual component trees into production react/next.js. handled microfrontend architecture and react performance tuning at scale.\n\nalso built the frontend for rava.ai's llm workflow builder. {description[:80]} — the ui work there looks like something i'd enjoy."
    elif role_type == 'backend':
        body = f"interested in the {roles_str.split(',')[0].strip()} role at {company_name}. at rava.ai i owned the entire backend — api design, llm orchestration, rag pipelines, vector stores. before that i built a code generation transpiler at wavemaker (react/next.js codegen from visual input).\n\ncurrently building trevyn, a repo-aware ai pr review tool. {description[:80]} is the kind of problem i want to work on."
    elif role_type == 'ai':
        body = f"saw the {roles_str.split(',')[0].strip()} opening at {company_name}. at rava.ai i built llm workflows end-to-end — prompt chaining, rag pipelines, vector search, evaluation harnesses. owned the full stack from api to inference.\n\nat trevyn i'm building repo-aware ai that reads git diffs and reviews prs. {description[:80]} — i've been in the trenches with exactly this kind of stack."
    elif role_type == 'web3':
        body = f"interested in the {roles_str.split(',')[0].strip()} role at {company_name}. i'm a fullstack engineer with 2.5+ years building production systems — codegen transpiler at wavemaker, llm workflows at rava.ai, and currently repo-aware ai at trevyn.\n\ni've been writing solidity on the side and want to move into web3 full-time. {description[:80]} looks like a great place to do that."
    elif role_type == 'manager':
        body = f"interested in the engineering manager role at {company_name}. i've led engineering at two startups — rava.ai (llm workflows, rag) and trevyn (repo-aware ai pr review). before that i was a senior ic at wavemaker building a code generation transpiler.\n\n{description[:80]} — happy to talk about how i'd approach building and scaling the team."
    else:  # fullstack
        body = f"looking at the {roles_str.split(',')[0].strip()} role at {company_name}. at wavemaker i built a code generation transpiler — turns visual designs into react/next.js code. at rava.ai i owned the full stack: llm workflows, rag pipelines, api design, frontend.\n\ncurrently building trevyn — a repo-aware ai pr review system. {description[:80]} feels like a good fit for the kind of systems i build."
    
    closing = "happy to jump on a call.\n\nRaj\nyagyaraj.com | trevyn.dev"
    
    return f"Subject: {subject}\n\n{body}\n\n{closing}"

def get_linkedin_message(company_name, description, roles, role_type):
    """Generate a short LinkedIn / InMail message."""
    roles_str = format_roles(roles)
    first_role = roles_str.split(',')[0].strip()
    
    messages = {
        'founding': f"saw the founding engineer role at {company_name}. i was founding eng at rava.ai — built llm workflows + rag from scratch. also built a codegen transpiler at wavemaker. currently building trevyn (repo-aware ai pr review). would love to chat.",
        'frontend': f"interested in the {first_role} role at {company_name}. 2+ years building react/next.js at wavemaker — codegen transpiler, microfrontends, performance work. also built frontend for rava.ai's llm workflow builder. would love to talk.",
        'fullstack': f"interested in the {first_role} role at {company_name}. built a codegen transpiler at wavemaker (react/next.js) + owned full stack at rava.ai (llm workflows, rag). currently building trevyn. would love to chat.",
        'backend': f"interested in the {first_role} role at {company_name}. owned the entire backend at rava.ai — apis, llm orchestration, rag. built a codegen transpiler at wavemaker. currently building trevyn. would love to chat.",
        'ai': f"saw the {first_role} role at {company_name}. built llm workflows + rag pipelines at rava.ai, and now building repo-aware ai at trevyn. {description[:60]} — looks like my kind of problem. let's talk?",
        'web3': f"interested in the {first_role} role at {company_name}. fullstack engineer (wavemaker codegen, rava.ai llm workflows, trevyn repo-aware ai). writing solidity on the side, want to go web3 full-time. would love to chat.",
        'manager': f"interested in the eng manager role at {company_name}. led engineering at rava.ai (llm workflows) and trevyn (repo-aware ai). senior ic before that at wavemaker. would love to talk team-building and tech.",
    }
    
    return messages.get(role_type, messages['fullstack']) + "\n\nRaj\nyagyaraj.com | trevyn.dev"

def get_twitter_dm(company_name, roles, role_type):
    """Generate a very short Twitter DM."""
    first_role = format_roles(roles).split(',')[0].strip()
    
    dms = {
        'founding': f"founding eng role at {company_name}? i was founding eng at rava.ai (llm/rag) + built codegen at wavemaker. let's talk?",
        'frontend': f"{first_role} at {company_name}? 2+ yrs react/next.js at wavemaker (codegen transpiler, microfrontends). interested — let's chat?",
        'fullstack': f"{first_role} at {company_name}? built codegen at wavemaker + owned full stack at rava.ai (llm/rag). interested — let's chat?",
        'backend': f"{first_role} at {company_name}? owned backend at rava.ai (llm/rag) + built codegen at wavemaker. would love to talk.",
        'ai': f"{first_role} at {company_name}? built llm workflows + rag at rava.ai, now building repo-aware ai at trevyn. let's talk?",
        'web3': f"{first_role} at {company_name}? fullstack eng looking to go web3. built codegen + llm systems. interested — let's chat?",
        'manager': f"eng manager at {company_name}? led eng at rava.ai + trevyn. would love to talk.",
    }
    
    return dms.get(role_type, dms['fullstack'])

def generate_file(company):
    """Generate the full markdown content for a company."""
    name = company['name']
    slug = slugify(name)
    
    founders = format_founders(company.get('founders', []))
    roles = company.get('roles', [])
    roles_str = format_roles(roles)
    job_urls = company.get('job_urls', [])
    source = company.get('source', 'Unknown')
    website = company.get('website', '')
    description = company.get('description', '')
    
    role_type = classify_role(roles_str)
    
    hiring_sources = format_job_urls(job_urls, source)
    
    cold_email = get_cold_email(name, description, roles, role_type)
    linkedin_msg = get_linkedin_message(name, description, roles, role_type)
    twitter_dm = get_twitter_dm(name, roles, role_type)
    
    content = f"""# Company: {name}
- **Description**: {description}
- **Website**: {website}
- **Founders/CTO**: {founders}
- **Founder Email**: Not found
- **Founder LinkedIn**: Not found
- **Hiring Signal**: true
- **Hiring sources**: {source}

## Hiring Signal Analysis
- **Open Roles Found**: {roles_str}
- **Hiring Sources**:
{hiring_sources}
- **Ways to Apply**: Cold Email / Cold Message on LinkedIn / Apply via job posting

## Draft Outreach

### Cold Email
{cold_email}

### Cold Message (LinkedIn / InMail)
{linkedin_msg}

### Twitter DM
{twitter_dm}
"""
    
    return slug, content

def main():
    with open(INPUT_FILE, 'r') as f:
        companies = json.load(f)
    
    hiring_companies = [c for c in companies if c.get('hiring', False)]
    
    print(f"Total companies: {len(companies)}")
    print(f"Hiring companies: {len(hiring_companies)}")
    
    created = 0
    for company in hiring_companies:
        slug, content = generate_file(company)
        filepath = os.path.join(OUTPUT_DIR, f"{slug}.md")
        with open(filepath, 'w') as f:
            f.write(content)
        created += 1
        print(f"  Created: {slug}.md")
    
    print(f"\nDone! Created {created} company.md files in {OUTPUT_DIR}")

if __name__ == '__main__':
    main()
