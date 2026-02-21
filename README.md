# python
python test checkin

# git init -- Not required
# git clone https://github.com/RamMandavkar/python.git -- Not required

# git pull https://github.com/RamMandavkar/python.git jan2026ai
# git status
# git checkout -b jan2026ai  -- Not required
# git add .
# git remote add origin https://github.com/RamMandavkar/python.git
# git commit -m 'updated'
# git push --set-upstream origin jan2026ai
# git log
# git status
# git branch -m jan2026ai
# git remote set-url origin https://github.com/RamMandavkar/python.git
# git remote -v
# git rebase -i 65e8374757015aa9cae016d0d9b7b64c57f5a48b
#

# View -> Command Palette → Developer: Reload Window
# View -> Command Palette → Python: Restart Language Server

# Ensure VS Code is using that interpreter: 
# Command Palette → Python: Select Interpreter → # choose #your venv/conda/env.

# python --version
# pip show langchain
# pip install --upgrade langchain

# Complete RAG Architecture with Chunking
            Raw Documents
                ↓
            Chunking
                ↓
            Embeddings (vectorize chunks)
                ↓
            Vector Database (store vectors)
                ↓
            User Query
                ↓
            Query Embedding
                ↓
            Similarity Search (cosine similarity)
                ↓
            Top K relevant chunks
                ↓
            LLM + Context
                ↓
            Final Answer

# Complete End-to-End Flow Diagram
                ┌──────────────────────┐
                │   External Data      │
                └──────────┬───────────┘
                           ↓
                ┌──────────────────────┐
                │  Loader + Splitter   │
                └──────────┬───────────┘
                           ↓
                ┌──────────────────────┐
                │   Embedding Model    │
                └──────────┬───────────┘
                           ↓
                ┌──────────────────────┐
                │    Vector Store      │
                └──────────┬───────────┘
                           ↓
User Query → Query Embedding
                           ↓
                ┌──────────────────────┐
                │  Similarity Search   │
                └──────────┬───────────┘
                           ↓
                Retrieved Context
                           ↓
                ┌──────────────────────┐
                │       LLM            │
                └──────────┬───────────┘
                           ↓
                     Final Answer