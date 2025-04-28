# modules/job_parser.py

def clean_and_chunk_text(text, chunk_size=2000):
    """
    Cleans the input text and splits it into a list of chunks,
    each approximately chunk_size characters, cutting only at word boundaries.
    """
    # Step 1: Clean the input text
    lines = text.splitlines()

    full_input = ""
    for line in lines:
        line = line.strip()
        if line:
            if not line.endswith(('.', '!', '?')):
                full_input += line + ' '
            else:
                full_input += line + ' '

    # Replace multiple spaces with a single space
    full_input = ' '.join(full_input.split())

    # Step 2: Split into chunks
    chunks = []
    start = 0

    while start < len(full_input):
        end = min(start + chunk_size, len(full_input))
        if end < len(full_input):
            # Look backwards for a space
            while end > start and full_input[end] != ' ':
                end -= 1
            if end == start:
                # Couldn't find a space, force hard cut
                end = min(start + chunk_size, len(full_input))
        chunk = full_input[start:end].strip()
        chunks.append(chunk)
        start = end + 1  # move past the space

    return chunks
