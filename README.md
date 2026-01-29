# AI-Medical-Chatbot
### A Medical Question-Answering Chatbot using RAG, LangChain, Pinecone, Flask & AWS

This project implements an **AI-powered Medical Chatbot** that answers user questions based on **medical textbooks** using a **Retrieval-Augmented Generation (RAG)** pipeline.  
The chatbot retrieves relevant medical context from indexed documents and generates concise, textbook-style answers.

---

## 📚 Data Sources (Medical Books)

This chatbot uses **two medical reference books (PDF format)** as its knowledge base:

- 📘 **Medical Book 1** – Core medical concepts (definitions, pathophysiology, causes)
- 📗 **Medical Book 2** – Clinical features, complications, disease explanations

The books are:
- Stored in the `data/` directory
- Loaded using `PyPDFLoader`
- Split into semantic chunks
- Embedded using HuggingFace embeddings
- Indexed and queried from Pinecone

---

## 🧠 How the RAG System Works

1. **PDF Ingestion**
   - Medical PDFs are loaded from the `data/` folder
   - Only minimal metadata is retained

2. **Text Chunking**
   - Documents are split into overlapping chunks for better retrieval

3. **Embeddings**
   - Model used:  
     `sentence-transformers/all-MiniLM-L6-v2`

4. **Vector Database**
   - All embeddings are stored in **Pinecone**

5. **Retrieval**
   - Top-k relevant chunks are retrieved using similarity search

6. **Answer Generation**
   - The LLM generates answers **strictly from retrieved context**
   - If context is missing, the model responds that it does not know

---

## 🚀 LLM Used

- **Groq LLM**
  - Model: `llama-3.1-8b-instant`
  - Integrated via LangChain
  - Fast and suitable for RAG-based applications

---

## 🖥️ Frontend

- Built using **Flask**
- Simple chat-based UI
- User queries are sent to the RAG pipeline
- Responses are rendered in real time

---

## 🛠️ Tech Stack

- Python
- LangChain
- Flask
- HuggingFace Embeddings
- Pinecone
- Groq LLM
- Docker
- AWS (EC2, ECR, IAM)
- GitHub Actions (CI/CD)

---

## ⚙️ How to Run Locally

### STEP 1: Clone the Repository

```bash
git clone https://github.com/shahkhushi28k/AI-Medical-Chatbot.git
cd AI-Medical-Chatbot

### STEP 2: Create Virtual Environment

python3 -m venv venv
source venv/bin/activate

### STEP 3: Install Dependencies
pip install -r requirements.txt

### STEP 4: Create .env File

Create a .env file in the root directory:

PINECONE_API_KEY=your_pinecone_api_key
GROQ_API_KEY=your_groq_api_key

### STEP 5: Store Embeddings in Pinecone

python store_index.py

This step:

Reads both medical books

Generates embeddings

Stores them in Pinecone

### STEP 6: Run the Application

python app.py

Open your browser:

http://localhost:8080

☁️ AWS CI/CD Deployment with GitHub Actions

This project is deployed on AWS EC2 using Docker and GitHub Actions.

🔐 AWS Setup
    1. Login to AWS Console
    2. Create IAM User (for CI/CD)

        Permissions attached:

        AmazonEC2ContainerRegistryFullAccess

        AmazonEC2FullAccess

        Used by GitHub Actions to:

        Build Docker images

        Push images to Amazon ECR

    3. Create ECR Repository

        Save the ECR URI:

        747088593584.dkr.ecr.us-east-2.amazonaws.com/medicalbot

    4. Create EC2 Instance

        OS: Ubuntu

        Acts as Docker host and deployment server

    5. Install Docker on EC2
    
        sudo apt update -y
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker ubuntu
        newgrp docker

    6. Configure EC2 as Self-Hosted Runner

            From GitHub:

            Repository → Settings → Actions → Runners → New self-hosted runner


            Run the provided commands on EC2.

    7. Attach IAM Role to EC2 (IMPORTANT)

            Attach an IAM Role with:

            AmazonEC2ContainerRegistryReadOnly

            This allows EC2 to pull images from ECR without access keys.

    8. GitHub Secrets Configuration

            Add the following secrets:

            AWS_ACCESS_KEY_ID
            AWS_SECRET_ACCESS_KEY
            AWS_DEFAULT_REGION
            ECR_REPO
            PINECONE_API_KEY
            GROQ_API_KEY

🐳 Dockerized Deployment Flow

    GitHub Actions builds Docker image

    Image is pushed to Amazon ECR

    EC2 pulls the latest image

    Docker container runs on port 8080

    Flask app serves users publicly

🌐 Access Deployed Application

http://<EC2_PUBLIC_IP>:8080

⚠️ Safety & Limitations

    Answers are strictly based on the provided medical books

    No diagnosis or treatment advice is provided

    If context is unavailable, the chatbot responds:

        "I do not know based on the provided context."

✅ Future Improvements

    Add source citations

    Improve UI/UX

    Add more medical textbooks

    Enable HTTPS with Nginx

    Add authentication

📌 Conclusion

    This project demonstrates a production-ready Medical RAG chatbot using:

    Trusted medical literature

    Vector search with Pinecone

    Fast LLM inference

    Cloud-native AWS deployment