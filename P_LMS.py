import os
import re
import streamlit as st
from openai import OpenAI

# 🔑 Use environment variable for API key
client = OpenAI(api_key=os.getenv("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"))

def defang_url(url):
    return url.replace('.', '[.]').replace(':', '[:]')

def sanitize_message(message):
    url_pattern = re.compile(r'(https?://[^\s]+)')
    return url_pattern.sub(lambda m: defang_url(m.group(0)), message)

def ask_openai_chat(prompt, topic):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful tutor. Use MathJax ($$equations$$) for math/science."},
            {"role": "user", "content": f"Topic: {topic}\n{prompt}"},
        ],
        max_tokens=250,
        temperature=0.7,
    )
    return response.choices[0].message.content

curriculum = {
    "Math": {
        "Algebra": {
            "lessons": [
                "### Algebra - Lesson 1\nLinear equations: $$ax+b=c$$.",
                "### Algebra - Lesson 2\nSolve $$2x+3=7$$ → $$x=2$$.",
                "### Algebra - Lesson 3\nQuadratic basics: $$ax^2+bx+c=0$$."
            ],
            "practice": {"question": "Solve for $x$: $$3x+2=11$$", "answer": "3"},
        },
        "Geometry": {
            "lessons": [
                "### Geometry - Lesson 1\nAngles in a triangle = $$180^\\circ$$.",
                "### Geometry - Lesson 2\nPythagoras theorem: $$a^2+b^2=c^2$$.",
                "### Geometry - Lesson 3\nArea of circle: $$A=\\pi r^2$$."
            ],
            "practice": {"question": "What is the sum of angles in a triangle?", "answer": "180"},
        },
        "Calculus": {
            "lessons": [
                "### Calculus - Lesson 1\nDifferentiation basics.",
                "### Calculus - Lesson 2\n$$\\frac{d}{dx}(x^n)=nx^{n-1}$$.",
                "### Calculus - Lesson 3\nIntegration basics: $$\\int x dx=\\frac{x^2}{2}+C$$."
            ],
            "practice": {"question": "Differentiate: $$f(x)=x^3$$", "answer": "3x^2"},
        }
    },
    "Physics": {
        "Kinematics": {
            "lessons": [
                "### Kinematics - Lesson 1\nEquation of motion: $$v=u+at$$.",
                "### Kinematics - Lesson 2\nDisplacement: $$s=ut+\\frac{1}{2}at^2$$.",
                "### Kinematics - Lesson 3\nGraphical motion analysis."
            ],
            "practice": {"question": "If $$u=0, a=2, t=5$$, find $$v$$", "answer": "10"},
        },
        "Work & Energy": {
            "lessons": [
                "### Work & Energy - Lesson 1\nWork = Force × Displacement.",
                "### Work & Energy - Lesson 2\nKinetic energy: $$KE=\\frac{1}{2}mv^2$$.",
                "### Work & Energy - Lesson 3\nPotential energy: $$PE=mgh$$."
            ],
            "practice": {"question": "If a 10N force moves an object 5m, how much work is done?", "answer": "50"},
        }
    },
    "Chemistry": {
        "Atomic Structure": {
            "lessons": [
                "### Atomic Structure - Lesson 1\nAtom = proton + neutron + electron.",
                "### Atomic Structure - Lesson 2\nElectron shells: K, L, M, N.",
                "### Atomic Structure - Lesson 3\nIsotopes: same protons, different neutrons."
            ],
            "practice": {"question": "What is the charge of an electron?", "answer": "-1"},
        },
        "Periodic Table": {
            "lessons": [
                "### Periodic Table - Lesson 1\nArranged by atomic number.",
                "### Periodic Table - Lesson 2\nGroups & periods show trends.",
                "### Periodic Table - Lesson 3\nNoble gases are inert."
            ],
            "practice": {"question": "Which element has atomic number 6?", "answer": "Carbon"},
        }
    },
    "History": {
        "World War II": {
            "lessons": [
                "### WWII - Lesson 1\nStarted in 1939 with invasion of Poland.",
                "### WWII - Lesson 2\nMajor powers: Allies vs Axis.",
                "### WWII - Lesson 3\nEnded in 1945 after atomic bombings."
            ],
            "practice": {"question": "In which year did WWII begin?", "answer": "1939"},
        },
        "Indian Independence": {
            "lessons": [
                "### Indian Independence - Lesson 1\nIndia was a British colony.",
                "### Indian Independence - Lesson 2\nKey leaders: Gandhi, Nehru, Patel.",
                "### Indian Independence - Lesson 3\nIndependence on 15th August 1947."
            ],
            "practice": {"question": "Who was the first Prime Minister of India?", "answer": "Jawaharlal Nehru"},
        }
    },
    "Computer Science": {
        "Programming Basics": {
            "lessons": [
                "### Programming Basics - Lesson 1\nPrograms = instructions for computers.",
                "### Programming Basics - Lesson 2\nPython uses `def` for functions.",
                "### Programming Basics - Lesson 3\nVariables store values."
            ],
            "practice": {"question": "Which keyword is used to define a function in Python?", "answer": "def"},
        },
        "Data Structures": {
            "lessons": [
                "### Data Structures - Lesson 1\nList = ordered collection.",
                "### Data Structures - Lesson 2\nStack works on LIFO.",
                "### Data Structures - Lesson 3\nQueue works on FIFO."
            ],
            "practice": {"question": "Which data structure works on FIFO?", "answer": "Queue"},
        },
        "Networking": {
            "lessons": [
                "### Networking - Lesson 1\nInternet uses TCP/IP.",
                "### Networking - Lesson 2\nIP = Internet Protocol.",
                "### Networking - Lesson 3\nHTTP is stateless."
            ],
            "practice": {"question": "What does IP stand for?", "answer": "Internet Protocol"},
        }
    }
}

st.set_page_config(page_title="P-LMS", layout="wide")

st.title("📘 Personalized LMS with E.C.H.O")

subject = st.selectbox("📚 Choose Subject:", list(curriculum.keys()))
topic = st.selectbox("📖 Choose Topic:", list(curriculum[subject].keys()))

st.header("📖 Lessons")
for i, lesson in enumerate(curriculum[subject][topic]["lessons"], start=1):
    with st.expander(f"Lesson {i}"):
        st.markdown(lesson)

st.header("📝 Practice Problem")
q = curriculum[subject][topic]["practice"]["question"]
a = curriculum[subject][topic]["practice"]["answer"]

st.markdown(q)
user_answer = st.text_input("Your Answer:")

if st.button("Submit Answer"):
    if user_answer.strip().lower() == a.lower():
        st.success("✅ Correct! Well done.")
    else:
        st.error(f"❌ Oops! The correct answer is {a}.")


st.sidebar.title("💬 E.C.H.O")

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [{"sender": "bot", "text": "Hi! Ask me anything."}]

for msg in st.session_state.chat_messages:
    if msg["sender"] == "user":
        st.sidebar.markdown(f"**You:** {msg['text']}")
    else:
        st.sidebar.markdown(f"**Tutor:** {msg['text']}")

user_input = st.sidebar.text_input("Type your question:")
if st.sidebar.button("Send"):
    if user_input.strip():
        sanitized = sanitize_message(user_input)
        st.session_state.chat_messages.append({"sender": "user", "text": sanitized})

        with st.spinner("Thinking..."):
            bot_response = ask_openai_chat(sanitized, topic)

        st.session_state.chat_messages.append({"sender": "bot", "text": bot_response})
        st.rerun()
