import streamlit as st
import os
from embed import get_embedding_model
from weaviate_client import get_weaviate_client, setup_weaviate_schema
from load_file import load_file
from groq_api import get_reponse
from section_chunking import section_chunking
from prompting import zero_shot_template, context_injection_template
from vectorstore import get_context
from evaluation import evaluate_f1

st.set_page_config(page_title="Insurance Report Analyser", page_icon="🤖", layout="wide")

# --- SESSION STATE FOR CHAT ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- SIDEBAR ---
with st.sidebar:
    st.title("Insurance Report Analyser🤖")
    uploaded_file = st.file_uploader("Upload your insurance policy document", type=["pdf", "txt", "docx"])
    prompt_type = st.selectbox("Prompting Technique", ["Zero-shot", "Context-injection"])
    st.markdown("---")
    st.write("Ask questions about your insurance policy and get instant answers!")

# --- CHAT WINDOW STYLING ---
st.markdown(
    """
    <style>
    .chat-window {
        background: #f9f9f9;
        border-radius: 15px;
        padding: 20px;
        max-width: 800px;
        margin: auto;
        min-height: 400px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        overflow-y: auto;
    }
    .user-bubble {
        background-color: #e1eaff;
        border-radius: 10px;
        padding: 10px 16px;
        margin-bottom: 8px;
        width: fit-content;
        max-width: 70%;
        margin-left: auto;
        text-align: left;
    }
    .bot-bubble {
        background-color: #f4f4f4;
        border-radius: 10px;
        padding: 10px 16px;
        margin-bottom: 8px;
        width: fit-content;
        max-width: 70%;
        margin-right: auto;
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Insurance Policy Chat")

questions=["What are the main reasons for the decline in life insurance penetration in mature markets from 2007 to 2023?","How does customer dissatisfaction manifest in the life insurance industry, and what are the top CX pain points for policyholders?","What are the key transformation strategies recommended for life insurers to achieve customer centricity?","How are best-in-class life insurers using generative AI (Gen AI) to drive business results and enhance customer experience?","What are the challenges life insurers face in modernizing legacy technology systems, and how does this impact CX?","Describe the Capgemini blueprint for an efficient, seamless, and customer-centric transformation in life insurance.","What are the specific onboarding challenges for retail and group life insurance customers?","How can AI-powered tools improve self-service and claims processes in life insurance?","What benefits are reported by insurers that have implemented integrated data management and unified customer views?","What are the skills and talent gaps in the insurance industry’s drive toward greater customer centricity and AI adoption?"]

gold_answers=["The decline in life insurance penetration in mature markets—from 5.4% in 2007 to 3.6% in 2023—has multiple drivers: Flat Growth in Mature Markets: Growth has stalled over the past 16 years at -0.2%. Customer Asset Allocation Shift: Consumers are allocating more assets to equities (increasing from 15.9% to 23.4%) while reducing the share held in life insurance (7.5% down to 5.8%).Product Relevance: Life insurance is increasingly viewed as a “maybe” purchase rather than a “must-have,” especially among younger generations.Investment Appeal: The industry’s market capitalization also dropped (15% to 9%) relative to other financial services, reflecting declining investor confidence.Demand for Flexibility: There’s a trend toward simpler, more flexible, and transparent solutions, including unit-linked products in low interest environments","Customer dissatisfaction is evident in poor experiences throughout the policyholder journey: Lack of Pricing Transparency: 59% are dissatisfied with policy pricing, citing unclear premium calculations, lifestyle-based adjustments, and hidden fees.Multiple Dissatisfaction Touchpoints:Product Offerings (51%)Onboarding (51%)Service (48%)Claims/Surrender (55%)Perceived Rigidity & Complexity: Products are seen as complex, inflexible, and their value hard to quantify.Top CX Pain Points: Complex terms, long onboarding/application processes, slow or unclear underwriting and claims, lack of digital options, and confusion or lack of communication throughout the customer journey.","Recommended strategies for achieving true customer centricity: Optimize Onboarding: Streamline processes via data-driven distribution and rapid risk assessment.Enhance Self-Service: Integrate AI-powered tools and intelligent platforms for both customers and staff.Empathetic & Intelligent Claims: Enable easy digital claims, communication transparency, and empathetic support via AI copilots.Modernize Technology: Invest in advanced tech, cloud/data infrastructure, and digital platforms.Cultural Change: Foster a customer-first culture through talent development, incentive alignment, and continuous improvement.Partnerships & Ecosystem Integration: Collaborate with technology providers and ecosystem partners to accelerate innovation","Leading insurers leverage Gen AI for substantial business results:Process Automation: Use Gen AI for automated underwriting, claims assessment, and policy management.Enhanced Customer Experience: AI augments human interaction, delivers omnichannel engagement, and personalizes offerings.Cost & Productivity: Achieve higher NPS (38% above mainstream), lower expense ratios (11% below mainstream), and faster growth (6% above industry).Workforce Productivity: One skilled person enabled by Gen AI can replace several in operations or CX enhancement.Data & Insight Integration: AI extracts, cleans, and integrates data from legacy systems and boosts real-time insights","Aging Infrastructure: 52% of insurers cite legacy tech as a significant hurdle. Old systems weren’t designed for data sharing or customer engagement.Fragmented Data: Siloed operations hinder unified customer views and streamlined processes.Limited Digital Options: Leads to paperwork, delays, and poor personalization.Regulatory Barriers: Restrict automation and require nuanced, human-involved processes.Low Transformation Success Rate: Only 41% met/exceeded transformation goals, in part because of complexities and lack of skilled resources","The blueprint includes:Orchestrate the Transformation: Focus on both advanced tech (modernizing legacy, data management, enabling Gen AI) and people (talent and partnerships).Optimize Onboarding: Use data-driven strategies for quick, personalized onboarding.Enhance Self-Service: Deploy AI-powered portals and platforms.Empathetic, Intelligent Claims: Leverage AI copilots, real-time status, and digital processes.Infuse Intelligence Into Processes: Embed intelligence for ongoing engagement and operational efficiency.Business Benefits: Boost customer satisfaction, operational efficiency, and overall financial performance.","Retail Customers:Complex terms and conditions (35%) Lengthy and complicated application processes (27%) Delays in underwriting (25%) Group Customers: Unclear benefits and coverage (34%) Limited add-on options (25%) Lack of communication on enrollment deadlines (19%)","AI Self-Service: Provides faster, 24/7 access for policy changes and routine needs, reducing support wait times and increasing satisfaction.Intelligent Platforms: Analytics identify at-risk policyholders, power personalized recommendations, and automate administrative tasks for agents.AI in Claims: Digital portals, real-time status updates, and emotion-aware AI copilots deliver empathetic, efficient resolution—especially in sensitive situations.AI-Enhanced Call Centers: Proactively identify and assist vulnerable customers (e.g., Aviva, 97% accuracy rate).Unified Data Platforms: Enable cross-sell, upsell, lapse prevention, and segmentation use cases","Operational Efficiency: Faster, more accurate reporting and month-end processes (e.g., 40% faster implementation, 2+ days saved in reporting). Single “Source of Truth”: Delivers data reliability and enables targeted marketing, better customer service, and product innovation. Critical Business Insights: 360-degree views enable upselling, cross-selling, segmentation, and lapse prevention","In-Demand Skills: Behavioral scientists, experience designers, and AI prompt engineers are most needed. Talent Barriers: 34% of insurers list talent shortages as a top-three obstacle to customer experience improvement. Culture Change: Upskilling, incentive alignment, and partnerships are required to support end-to-end transformation and harness new tools"]

if uploaded_file:
    text, file_path = load_file(uploaded_file)
    chunks = section_chunking(text)
    embedder = get_embedding_model()
    embedder.embed_documents(chunks)

    client = get_weaviate_client()
    setup_weaviate_schema(client)
    predicted_answers = []
    scores=0
    for ques in questions:
        context = get_context(client, embedder, ques, chunks)
        context_injection_template_obj = context_injection_template()
        prompt = context_injection_template_obj.format(query=ques, context=context)
        predicted_answers.append(get_reponse(prompt))
    for gold, predicted in zip(gold_answers, predicted_answers):
        scores += evaluate_f1(gold, predicted)
    scores /= len(gold_answers)
    
with st.sidebar:
    st.markdown(f"### Evaluation Score\n- F1 Score: {scores}")

def handle_query(query):
    if query:
        
        query = query.strip()

        context = get_context(client, embedder, query, chunks)

        zero_shot_template_obj = zero_shot_template()
        context_injection_template_obj = context_injection_template()

        if prompt_type == "Zero-shot":
            prompt = zero_shot_template_obj.format(query=query)
        else:
            prompt = context_injection_template_obj.format(query=query, context=context)
        response = get_reponse(prompt)

        st.session_state.chat_history.append({"type": "human", "content": query})
        st.session_state.chat_history.append({"type": "ai", "content": response})
        os.unlink(file_path)



with st.container():
    if chatInput := st.chat_input("Type your question and press Enter...", key="chat_input"):
        handle_query(chatInput)
        for msg in st.session_state.chat_history[::-1]:
            if msg["type"] == "human":
                st.markdown(f'<div class="user-bubble">🧑 <b>You:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-bubble">🤖 <b>Bot:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)