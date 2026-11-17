from pathlib import Path
from llama_cpp import Llama

# Find the main SYNAPSE project folder
BASE_DIR = Path(__file__).resolve().parents[2]

# Locate the downloaded GGUF model
MODEL_PATH = (
    BASE_DIR
    / "models"
    / "llm"
    / "SmolLM2-360M-Instruct.Q4_K_M.gguf"
)


def load_llm():

    if not MODEL_PATH.is_file():
        raise FileNotFoundError(
            f"LLM model not found: {MODEL_PATH}"
        )

    print("Loading SmolLM2...")

    llm = Llama(
        model_path=str(MODEL_PATH),
        n_ctx=2048,
        n_threads=4,
        verbose=False
    )

    print("SmolLM2 loaded successfully!")

    return llm


if __name__ == "__main__":

    model = load_llm()

    print("SYNAPSE LLM is ready!")