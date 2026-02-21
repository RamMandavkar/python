# python
## Project Setup

1. init the repository: `git init`
2. Clone the repository: `git clone https://github.com/RamMandavkar/python.git`
3. Pull the latest changes: `git pull https://github.com/RamMandavkar/python.git jan2026ai`
4. To check git status: `git status`
5. To check git logs: `git log`

## Branch Management

* Created and switched to branch: `git checkout -b jan2026ai ` 
* Remote add branch: `git remote add origin https://github.com/RamMandavkar/python.git`

## Git Workflow

1. Add changes: `git add .`
2. Commit changes: `git commit -m 'updated'`
3. Push changes: `git push --set-upstream origin jan2026ai`

## Repository Management

* Added remote origin: `git remote add origin https://github.com/RamMandavkar/python.git`
* Verified remote origin: `git remote -v`
* git rebase: `git rebase -i 65e8374757015aa9cae016d0d9b7b64c57f5a48b`

## VS Code Setup

1. Reload VS Code: View -> Command Palette → Developer: Reload Window
2. Restart Python Language Server: View -> Command Palette → Python: Restart Language Server
3. Select Python Interpreter: Command Palette → Python: Select Interpreter → choose venv/conda/env

## Python Environment

* Check Python version: `python --version`
* Install/Upgrade Langchain: `pip install --upgrade langchain`
* Check Langchain version: `pip show langchain`

### Complete RAG(Retrieval-Augmented Generation) Architecture with Chunking
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

### Complete End-to-End RAG(Retrieval-Augmented Generation) Flow Diagram 
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