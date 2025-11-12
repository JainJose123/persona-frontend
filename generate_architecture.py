# ----------------------------------------------------------
# Persona ADHD Dashboard — Architecture Diagram Generator
# ----------------------------------------------------------
# Generates a visual diagram (architecture.png)
# using Graphviz showing the data flow between:
#   Frontend <-> Flask Backend <-> OpenRouter API
#   + Memory/History Store
# ----------------------------------------------------------

from graphviz import Digraph

# Create directed graph
dot = Digraph("Persona_Architecture", format="png")
dot.attr(bgcolor="white", rankdir="TB", fontname="Helvetica")

# ----------------------------
# Node Style Templates
# ----------------------------
frontend_style = {"shape": "box", "style": "filled,rounded", "color": "#00BFFF", "fillcolor": "#E0F7FF"}
backend_style  = {"shape": "box3d", "style": "filled,rounded", "color": "#FF7F50", "fillcolor": "#FFF1E6"}
api_style      = {"shape": "component", "style": "filled,rounded", "color": "#6A5ACD", "fillcolor": "#E6E0FF"}
memory_style   = {"shape": "cylinder", "style": "filled", "color": "#32CD32", "fillcolor": "#E9FFE9"}

# ----------------------------
# Nodes
# ----------------------------
dot.node("Frontend", "🎨 Frontend (HTML/CSS/JS)\n• ADHD-Dopamine UI\n• Chat, Tasks, XP, Email\n• Sidebar History", **frontend_style)
dot.node("Backend", "⚙️ Flask Backend (Python)\n• REST APIs\n• /api/ask, /api/tasks, /api/xp\n• /api/draft-email, /api/history", **backend_style)
dot.node("OpenRouter", "🧠 OpenRouter API\n• LLM Gateway\n• Llama-3 / Mistral / Gemma models", **api_style)
dot.node("Memory", "💾 In-Memory Store\n• XP\n• Last Chats\n• Last Tasks\n• History (Chats/Tasks/Emails)", **memory_style)

# ----------------------------
# Relationships
# ----------------------------
dot.edge("Frontend", "Backend", label="User Actions (Fetch API)\nChat / Task / XP / Email requests", color="#333333", fontsize="10")
dot.edge("Backend", "OpenRouter", label="LLM Prompt Calls\n(JSON via HTTPS)", color="#555555", fontsize="10")
dot.edge("Backend", "Memory", label="Update XP + Save History", color="#228B22", fontsize="10")
dot.edge("Memory", "Backend", label="Fetch Data / Stats", color="#228B22", fontsize="10")
dot.edge("Backend", "Frontend", label="AI Responses\n+ XP / History Updates", color="#333333", fontsize="10")

# ----------------------------
# Optional Cluster View
# ----------------------------
with dot.subgraph(name="cluster_user") as c:
    c.attr(label="👤 User Interface Layer", color="lightblue")
    c.node("Frontend")

with dot.subgraph(name="cluster_backend") as c:
    c.attr(label="🧩 Application Layer", color="coral")
    c.node("Backend")
    c.node("Memory")

with dot.subgraph(name="cluster_api") as c:
    c.attr(label="☁️ AI Model Layer", color="plum")
    c.node("OpenRouter")

# ----------------------------
# Render
# ----------------------------
output_path = dot.render("architecture")
print("✅ Architecture diagram generated → architecture.png")
