def conllish_to_iob2(conllish_data):
    iob2_data = []

    current_entity = None
    for line in conllish_data:
        if line.strip() == "":
            iob2_data.append("")  # Add empty line for sentence break
            current_entity = None
            continue

        parts = line.strip().split()
        token = parts[0]
        entity_tag = parts[-1]  # Assuming last column contains entity tags

        if entity_tag == "O":
            iob2_data.append(f"{token} O")
            current_entity = None
        else:
            tag, entity = entity_tag.split("-", 1)
            if tag == "B":
                iob2_data.append(f"{token} B-{entity}")
                current_entity = entity
            elif tag == "I" and entity == current_entity:
                iob2_data.append(f"{token} I-{entity}")
            else:
                # If tag is I but it's not continuing the current entity, treat it as O
                iob2_data.append(f"{token} O")
                current_entity = None

    return iob2_data

# Read CoNLL-ish data from file
def read_conllish_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.readlines()

# Write IOB2 data to file
def write_iob2_file(iob2_data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        for line in iob2_data:
            file.write(line + "\n")

# Example usage:
conllish_filename = "C:\\Users\\appuv\\backend1\\datasets\\devel.tsv"
iob2_filename = "iob2_devel.tsv"

conllish_data = read_conllish_file(conllish_filename)
iob2_data = conllish_to_iob2(conllish_data)
write_iob2_file(iob2_data, iob2_filename)
