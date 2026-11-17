# SYNAPSE – Offline AI Voice Assistant

**SYNAPSE (Synthetic Neural Architecture for Perception, Speech & Embodied Intelligence)** is an offline AI voice assistant built with Python. It combines streaming speech recognition, a locally running language model, speech synthesis, conversational memory, and RAG-based knowledge retrieval.

The project is designed to provide private, locally processed voice interactions without depending on cloud-based AI APIs.

## Features

- **Speech-to-Text:** Streaming speech recognition using Sherpa-ONNX.
- **Local Language Model:** Runs SmolLM2 locally using llama.cpp.
- **Text-to-Speech:** Voice generation using Piper.
- **Voice Activity Detection:** Detects speech activity during audio input.
- **Conversational Memory:** Stores conversations and user facts using SQLite.
- **Knowledge Retrieval:** Searches local documents using BM25-based retrieval.
- **PDF and JSON Processing:** Loads and processes supported knowledge documents.
- **Offline Architecture:** Designed to operate without external AI inference APIs.

## Architecture

```text
         Microphone Input
                |
                v
       Voice Activity Detection
                |
                v
      Streaming Speech Recognition
          (Sherpa-ONNX)
                |
                v
        Local Language Model
          (SmolLM2 / llama.cpp)
                |
          +-----+------+
          |            |
          v            v
   SQLite Memory   Knowledge Retrieval
                    (BM25 / RAG)
          |            |
          +-----+------+
                |
                v
          Generated Response
                |
                v
          Text-to-Speech
              (Piper)
                |
                v
           Audio Output
```

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.10 |
| Speech Recognition | Sherpa-ONNX |
| Language Model | SmolLM2 |
| Local LLM Runtime | llama.cpp |
| Text-to-Speech | Piper |
| Audio Processing | NumPy, SoundDevice, SoundFile |
| Conversational Memory | SQLite |
| Document Processing | pypdf |
| Information Retrieval | rank-bm25 |

## Project Structure

```text
SYNAPSE/
│
├── src/
│   ├── audio/       # Audio input and processing
│   ├── cache/       # Caching utilities
│   ├── knowledge/   # Document processing and knowledge base
│   ├── llm/         # Local language model
│   ├── memory/      # SQLite conversational memory
│   ├── pipeline/    # Assistant pipeline
│   ├── retrieval/   # Information retrieval
│   ├── stt/         # Speech-to-text
│   ├── tts/         # Text-to-speech
│   └── vad/         # Voice activity detection
│
├── models/          # Local AI models (not included)
├── data/            # Local databases and knowledge data (not included)
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/DeepikaCPSTech/SYNAPSE_VOICE_MODEL.git
cd SYNAPSE_VOICE_MODEL
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

> Note: llama-cpp-python and audio-related packages may require platform-specific installation steps. The listed dependency versions reflect the development environment and may need adjustment on other hardware.

## Model Setup

SYNAPSE uses local model files that are not included in this repository.

You need to configure:

- A compatible Sherpa-ONNX streaming speech recognition model.
- A compatible SmolLM2 GGUF language model.
- A Piper voice model and its configuration file.

Place model files in the appropriate directories under `models/` and configure their paths in the project.

## Knowledge Base Setup

The knowledge assistant supports local PDF and JSON documents.

Place authorized documents in:

```text
data/knowledge/documents/
```

Run the document-processing and knowledge-base scripts provided in `src/knowledge/` to prepare the retrieval data.

## Privacy

SYNAPSE is designed for local processing. Its AI models and knowledge data are stored locally and are not included in this public repository.

Do not add passwords, API keys, private databases, personal student records, or other sensitive information to the repository.

## Development Status

SYNAPSE is under active development. Features, model configurations, and hardware support may evolve.

## License

No license has been specified yet. All rights are reserved unless a license is added to this repository.
