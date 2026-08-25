USER_KB = Path(r"backend\knowledge_base\user_kb")


def save_if_new(data):
    USER_KB.mkdir(parents=True, exist_ok=True)


    text = "\n".join(
        page["text"]
        for page in data["pages"]
    )


    doc_hash = hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()



    for file in USER_KB.glob("*.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                existing = json.load(f)

            if existing.get("doc_hash") == doc_hash:
                print("Already exists in user_kb.")
                return False

        except (json.JSONDecodeError, OSError):
            continue


    data["doc_hash"] = doc_hash

    filename = Path(data["source"]).stem + ".json"
    output_path = USER_KB / filename

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(f"Added to user_kb: {output_path}")
    return True