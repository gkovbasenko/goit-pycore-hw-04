def get_cats_info(path_to_file):
    cats_info = []
    with open(path_to_file, "r", encoding="utf-8") as file:
        for lineno, raw in enumerate(file, start=1):
            line = raw.strip()
            if not line:
                continue

            parts = line.split(",")
            if len(parts) != 3:
                raise ValueError(f"Line {lineno}: expected 'id,name,age' — {line!r}")
           
            id, name, age_part = parts[0].strip(), parts[1].strip(), parts[2].strip()
            if not id:
                raise ValueError(f"Line {lineno}: empty id")
            if not name:
                raise ValueError(f"Line {lineno}: empty name")            
            if not age_part:
                raise ValueError(f"Line {lineno}: empty age")

            try:
                age = int(age_part)
            except ValueError:
                raise ValueError(f"Line {lineno}: invalid age {age_part!r}") from None

            if age < 0:
                raise ValueError(f"Line {lineno}: negative age {age}")

            cats_info.append({"id": id, "name": name, "age": age})

    return cats_info



# cats_info = get_cats_info("cats_file.txt")
# print(cats_info)