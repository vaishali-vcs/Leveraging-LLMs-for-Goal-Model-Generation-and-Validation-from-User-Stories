# Use test_env
# code for chatbot without criteria
# to execute use streamlit run chatbot.py
# Background of GRL is taken from https://www.cs.toronto.edu/km/GRL/grl_syntax.html
# changes - LLM used is gpt-4. With a textual one-shot example
import streamlit as st
from xml_builder import build_XML

import numpy as np
from openai import OpenAI
from utils import load_userstories
import traceback

exampleuserstorytext_1 = f""" The objective of Traffic Simulator is to generate cars and the simulator should also focus on 
the following quality attributes: ease of use, realistic simulation and simple design. In order to generate cars, 
the simulation can either create new cars or keep the same cars. In order to run the simulation the system depends on 
resources are car objects.  The task of creating new cars contributes towards the following goals: Realistic 
simulation and Simple design"""



delimiter = "####"
format_text = f"""
<?xml version='1.0' encoding='ISO-8859-1'?>
<grl-catalog catalog-name="URNspec" description="" author="vaish">
    <element-def>
        <intentional-element id="72" name="Car objects" description="" type="Ressource" decompositiontype="And"/>
        <intentional-element id="80" name="Easy to use" description="" type="Softgoal" decompositiontype="And"/>
        <intentional-element id="82" name="Realistic simulation" description="" type="Softgoal" decompositiontype="And"/>
        <intentional-element id="84" name="Simple design" description="" type="Softgoal" decompositiontype="And"/>
        <intentional-element id="88" name="Generate cars" description="" type="Goal" decompositiontype="And"/>
        <intentional-element id="96" name="Create new cars" description="" type="Task" decompositiontype="And"/>
        <intentional-element id="98" name="Keep same cars" description="" type="Task" decompositiontype="And"/>
    </element-def>
    <link-def>
        <contribution name="Contribution105" description="" srcid="96" destid="82" contributiontype="Unknown" quantitativeContribution="0" correlation="false"/>
        <contribution name="Contribution106" description="" srcid="96" destid="84" contributiontype="Unknown" quantitativeContribution="0" correlation="false"/>
        <decomposition name="Decomposition111" description="" srcid="96" destid="88"/>
        <decomposition name="Decomposition114" description="" srcid="98" destid="88"/>
        <dependency name="Dependency116" description="" dependerid="88" dependeeid="72"/>
    </link-def>
    <actor-def>
        <actor id="11" name="Traffic Simulator" description=""/>
    </actor-def>
    <actor-IE-link-def>
        <actorContIE actor="11" ie="72"/>
        <actorContIE actor="11" ie="80"/>
        <actorContIE actor="11" ie="82"/>
        <actorContIE actor="11" ie="84"/>
        <actorContIE actor="11" ie="88"/>
        <actorContIE actor="11" ie="96"/>
        <actorContIE actor="11" ie="98"/>
    </actor-IE-link-def>
</grl-catalog>
"""

context = f"""
You are a requirements engineer with with an eagle eye for understanding what stakeholders' requirements are and how they can be fulfilled . You "
                   "carefully analyse user stories with great detail and extract important elements from them. User stories are semi-structured pieces of text that express stakeholders' intention, role, and rationale for their need. A user story template takes the following form: as a [WHO], I want/need [WHAT], so that [RATIONALE].
                   
                   Goal Modelling is employed to organize the user stories, and reveal how they are related to each other. 
                   A background of GRL (Goal-oriented Requirement Language) is provided below. 
GRL is a modeling language for specifying intentions, business goals, and non-functional requirements of multiple stakeholders. 
GRL can be used to specify alternatives that have to be considered, decisions that have been made, and rationales for making decisions. 
A GRL model is a connected graph of intentional elements. The model shows softgoals, goals, tasks and the relationship between the different intentional elements in the model. 
Here is a small description of intentional elements. 
'Actors':  An actor represents a stakeholder of a system or the system itself. Actors are holders of intentions; they are the active entities in the system or its environment who want goals to be achieved, 
tasks to be performed, resources to be available, and softgoals to be satisfied. 
'Goals': A goal is defined as something that the stakeholders hope to achieve as a result of the development of a software product. 
'SoftGoals': A softgoal is a condition or state of affairs in the world that the actor would like to achieve, but unlike in the concept of (hard) goal, there are no clear-cut criteria for whether the condition is achieved, and it is up to subjective judgement and interpretation of the developer to judge whether a particular state of affairs in fact achieves sufficiently the stated softgoal.
Softgoals are often related to non-functional requirements, whereas goals are related to functional requirements. Along with the SoftGoals mentioned in the user story you must include a set of specifications that describe the system’s operation capabilities and constraints and attempt to improve its 
functionality. These are basically the requirements that outline how well it will operate including things like speed, security, reliability, data integrity,etc. 
'Tasks': Tasks represent solutions to (or operationalizations of) goals and softgoals. Note tasks can be decomposed into subtasks that must be performed.
Different relationships or links connect the elements in a GRL model. 
The Contribution relationships statement describes how softgoals, task, believes, or links contribute to the satisficing of another intentional element. 
The five categories of Contribution Links are as follows.  
MAKE : The contribution of the contributing element is positive and sufficient.  BREAK : The contribution of the contributing element is negative and sufficient.  HELP : The contribution of the contributing element is positive but not sufficient.  HURT : The contribution of the contributing element is negative but not sufficient. EQUAL : There is equal contribution in both directions.
Contribution links describe how softgoals, task, believes, or links contribute to others. Graphically, a contribution link describes how one intentional element contributes to the satisficing of another intentional element. A Contribution relationships can be of one of the following kinds-AND, OR, EQUAL, HURT, and HELP.  
The Dependency relationships describe an intentional relationship between two actors, i.e., one actor (the Depender) depends on another actor (the Dependee) on something (the Dependum).  Note that the dependum is optional. 
DECOMPOSITON relationships provide the ability to define what other elements need to be achieved or available in order for a task to perform. Note that only Task and Goal can be decomposed into goal, task, resource, and softgoal. A Task Decomposition Structure shows the essential components of a task, which include subtasks that must be performed, subgoals that must be achieved, resources that must be accessible, and softgoals that must be satisfied. Similarly, a Goal Decomposition Structure connects a goal with its sub-goals directly, which is a short hand form of one Goal Means_Ends Structure and the related Task Decomposition Structure. The three categories of Decomposition Links are as follows.  
AND DECOMPOSITON: The relations between the dependent elements are “AND”. Each of the sub-components are necessary.  OR DECOMPOSITON : The relations between the contributing elements are “OR”. Any of the sub-components is sufficient. XOR DECOMPOSITON: The relations between the contributing elements
"""



st.header('Goal Modeling using ChatGPT', divider='rainbow')
# st.title("Goal Modeling using ChatGPT")

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo-1106"
from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

with st.sidebar:
    st.title('Parameters')
    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key provided', icon='✅')

    chosen_temp = st.slider("Select Temperature",
                            0.0, 2.0, 1.00)
    st.write("Selected Temperature", chosen_temp)
    st.write("Selected LLM: gpt-4")


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo-1106"

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.intentional_elements = {}
    st.session_state.index_key = 0

for message in st.session_state.messages[1:]:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    # create a markdown-formatted message that asks GPT to explain the function, formatted as a bullet list
    explain_system_message = {
        "role": "system",
        "content": context,
    }
    st.session_state.messages.append(explain_system_message)

    # print(explain_system_message)

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            temperature=chosen_temp,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
        # print(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
