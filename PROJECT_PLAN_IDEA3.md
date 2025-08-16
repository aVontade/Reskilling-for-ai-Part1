# Project Plan: AI Insight Generator (Idea 3)

## 1. Introduction

This document outlines the project plan and technical specification for building the "AI Insight Generator." This project aims to transform the static content of the "Reskilling for the AI Economy" book into a live, continuously updated, and interactive digital platform.

The core value proposition is to provide users—such as researchers, journalists, and strategists—with a dynamic resource that leverages generative AI to create visualizations on-the-fly, integrates real-time data from external sources, and allows for deep, conversational exploration of the content.

This plan details the core components, technology stack, feature specifications, and a development roadmap for building the Minimum Viable Product (MVP).

---

## 2. Core Architectural Components

This platform is data-intensive and relies on a robust set of interconnected services to function.

*   **Data Ingestion Layer:** An automated pipeline responsible for collecting, cleaning, and updating data. It will use scheduled connectors (managed by Apache Airflow) to pull data from public APIs and scrape key websites.
*   **Knowledge Base:** A multi-modal data store serving as the single source of truth.
    *   **Relational Database (PostgreSQL):** For storing structured data like statistics, report metadata, and user information.
    *   **Vector Database (Pinecone):** For storing text embeddings to power the AI-powered Q&A feature.
    *   **Data Lake (Amazon S3):** For storing raw, unprocessed documents and files from ingestion pipelines.
*   **Backend (API Server):** A GraphQL API designed for efficient data retrieval for a content-rich frontend. It will serve content, visualization specs, and Q&A results.
*   **AI/ML Service Layer:** A set of specialized microservices that form the core intelligence of the platform.
    *   **Generative Visualization Engine:** A service that uses an LLM to generate interactive chart specifications (Vega-Lite) based on descriptions in the text and live data.
    *   **Q&A Engine (RAG Pipeline):** A Retrieval-Augmented Generation system that provides cited, synthesized answers to user questions.
*   **Frontend (Web Application):** A dynamic, responsive user interface for displaying content, rendering live visualizations, and interacting with the Q&A engine.

---

## 3. Proposed Technology Stack

The tech stack is chosen to support complex data pipelines, high-performance AI services, and a rich, interactive user experience.

*   **Data Ingestion:**
    *   **Orchestration:** **Apache Airflow** (using Amazon MWAA) to manage and schedule data workflows.
    *   **Scraping/Automation:** **Scrapy**, **Beautiful Soup**, and **Playwright** (within Python).
*   **Backend:**
    *   **Language/Framework:** **Python with FastAPI**.
    *   **API:** **GraphQL** (using the **Strawberry** library) to allow for efficient and precise data fetching by the frontend.
*   **Databases:**
    *   **Relational:** **PostgreSQL** (using Amazon RDS).
    *   **Vector:** **Pinecone**.
    *   **Data Lake:** **Amazon S3**.
*   **AI/ML:**
    *   **RAG Framework:** **LlamaIndex** or **LangChain**.
    *   **LLM Provider:** **OpenAI (GPT-4 / GPT-4o)** or **Anthropic (Claude 3 Opus)**.
    *   **Visualization Generation:** An LLM generating **Vega-Lite** JSON specifications.
*   **Frontend:**
    *   **Framework:** **React (Next.js)**.
    *   **GraphQL Client:** **Apollo Client**.
    *   **Chart Rendering:** **Vega-Embed**.
*   **Deployment & Infrastructure:**
    *   **Cloud Provider:** **Amazon Web Services (AWS)**.
    *   **Containerization:** **Docker**.
    *   **Orchestration:** **AWS ECS** for services.
    *   **CI/CD:** **GitHub Actions**.

---

## 4. Key Feature Specifications

### 4.1. Generative Visualization Engine
*   **Objective:** Dynamically replace static image placeholders in the text with interactive, data-driven visualizations.
*   **User Flow:** As a user scrolls to a section with a chart, the platform sends the placeholder description to the backend. The AI engine generates a Vega-Lite chart spec using the most current data from the knowledge base. The frontend then renders this spec as a fully interactive chart.
*   **Implementation:** A backend service will use a prompted LLM to generate Vega-Lite JSON. The frontend will use the `vega-embed` library to render these specifications. Results will be cached to improve performance and reduce costs.

### 4.2. AI-Powered Q&A
*   **Objective:** Allow users to ask natural language questions about the content and receive synthesized, cited answers.
*   **User Flow:** The user types a question into a chat interface. The system uses a RAG pipeline to search the knowledge base for relevant text chunks, then feeds this context to an LLM to generate a comprehensive answer, complete with links to the source sections.
*   **Implementation:** A RAG pipeline built with LlamaIndex, using a vector database (Pinecone) for retrieval.

### 4.3. Real-Time Data Integration
*   **Objective:** Ensure that key statistics and data points within the text are always up-to-date.
*   **User Flow:** This is largely a backend process. Users experience this by seeing "live" data in the text, often with a small icon or tooltip indicating the data source and the last refresh date.
*   **Implementation:** Apache Airflow will manage scheduled jobs that run data connectors, pull new data, and update the PostgreSQL database.

### 4.4. Personalized Report Builder (Post-MVP)
*   **Objective:** Enable users to create their own custom reports using content and data from the platform.
*   **User Flow:** Users can select chapters, sections, and specific visualizations and arrange them in a custom report, which can then be exported as a PDF.
*   **Implementation:** A drag-and-drop UI on the frontend, with a backend service to handle the saving and rendering of the final report.

---

## 5. MVP Development Roadmap

The MVP will be built in approximately 16 weeks, focusing on the foundational data pipeline and the two core AI features.

*   **Phase 1: Data Foundation & Knowledge Base Setup (~6 weeks)**
    *   **Focus:** Build the data ingestion pipeline (Airflow), parse the book content, connect one external data source, and populate both PostgreSQL and Pinecone databases.
    *   **Outcome:** An automated data pipeline feeding a populated, multi-modal knowledge base.

*   **Phase 2: Backend API & AI Q&A Engine (~4 weeks)**
    *   **Focus:** Build the GraphQL API and the RAG pipeline for the Q&A feature.
    *   **Outcome:** A functional API and a basic chat interface for asking cited questions.

*   **Phase 3: The Generative Visualization Engine (~4 weeks)**
    *   **Focus:** Heavy R&D on LLM prompting to generate Vega-Lite specs and build the frontend to render them.
    *   **Outcome:** A polished content viewer with interactive, AI-generated charts.

*   **Phase 4: MVP Polish & Beta Launch (~2 weeks)**
    *   **Focus:** E2E testing, UI/UX refinement, and adding more data sources.
    *   **Outcome:** A stable MVP ready for a curated beta launch.

### Post-MVP Plan
*   **V1.1:** Expand data sources and build the "Explore the Data" feature.
*   **V1.2:** Implement the Personalized Report Builder.
*   **V2.0:** Introduce a subscription model and team-based features.
