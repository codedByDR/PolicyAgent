AI‑Assisted Flexible Work & Life Balance Request System 
As a woman employee, I want to request flexible work arrangements—such as working from home, 
shift changes, and caregiving support—with the assistance of AI. The AI should help me structure 
my request, track approval status, and monitor outcomes to ensure that work-life balance is 
promoted fairly and consistently across the organization. 
Expanded Details 
• Request Initiation: Employees can submit requests for flexible work arrangements through 
an intuitive interface. The AI guides users to specify their needs (e.g., WFH, shift changes, 
caregiving support) and captures relevant context such as timing, urgency, and supporting 
information. 
• AI-Generated Justification: The AI analyzes the employee’s informal reasoning, converting 
it into a professionally formatted justification. It suggests relevant request categories and 
references applicable company policies, ensuring the submission aligns with organizational 
guidelines. 
• Approval Workflow: Requests are routed automatically to designated approvers based on 
organizational hierarchy and type of request.  
• Policy Tagging: Each request is tagged with relevant company policies and procedures, 
helping both employees and managers understand the criteria for approval and ensuring 
compliance. 
• Outcome Monitoring: The system tracks outcomes of approved or denied requests, 
enabling employees to receive feedback and suggestions for future submissions. The AI 
provides analytics on the effectiveness of flexible arrangements and their impact on work
life balance. 
Functional Scope 
• Request Intake: Guided submission process for flexible work arrangements. 
• AI-Generated Justification: Intelligent conversion of informal reasoning to professional 
requests. 
• Approval Workflow: Automated routing, tracking, and follow-up of requests. 
• Policy Tagging: Linking requests to company policies for clarity and compliance. 
• Outcome Monitoring: Feedback and analytics on request outcomes. 
• Reporting dashboard

Functional Scope 
• Request Intake: Guided submission process for flexible work arrangements. 
• AI-Generated Justification: Intelligent conversion of informal reasoning to professional 
requests. 
• Approval Workflow: Automated routing, tracking, and follow-up of requests. 
• Policy Tagging: Linking requests to company policies for clarity and compliance. 
• Outcome Monitoring: Feedback and analytics on request outcomes. 
• Reporting dashboard 

#Requirement
Generate a policy guidelines document based on the given usecase
make sure policy document should be professional as a mnc company policy guideliness
policy document should open in browser
use RAG model to go through the policy document
there should be a button to explain about the policy guideliness
after clicking it, AI should explain clearly about the content in document and AI should also give a voice note of the document in the preferred language.

use below LLM
## LLM Configuration
Use the following snippet to create the LLM:

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import httpx

client = httpx.Client(verify=False)

llm = ChatOpenAI(
    base_url="https://genailab.tcs.in",
    model="gemini-2.5-pro",
    api_key='API_KEY', # Replace with your actual API key
    http_client=client
)

embedding_model = OpenAIEmbeddings(
    base_url="https://genailab.tcs.in", 
    model="azure/genailab-maas-gpt-4o",
    api_key='API_KEY', # Replace with your actual API key
    http_client=client
)
```

create a readme file with detailed view of code & how to execute it and see the output results.