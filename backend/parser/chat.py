from retrieve import retrieve
from generate import generate_answer
from speech import speak

while True:
    q = input("\nAsk: ")

    if q.lower() in ["exit", "quit"]:
        break

    chunks = retrieve(q)

    answer = generate_answer(q, chunks)

    print("\nAnswer:\n")
    print(answer)

    lang = "ta" if any("\u0B80" <= c <= "\u0BFF" for c in answer) else "en"

    speak(answer, lang)