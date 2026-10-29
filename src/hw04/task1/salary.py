def calculate_average(total, count):
    return total / count if count > 0 else 0

def total_salary(path_to_file):
    total = 0
    count = 0
    with open(path_to_file, "r", encoding="utf-8") as file:
        for lineno, raw in enumerate(file, start=1):
            line = raw.strip()
            if not line:
                continue

            parts = line.split(",")
            if len(parts) != 2:
                raise ValueError(f"Line {lineno}: expected 'name,salary' — {line!r}")

            name, salary_part = parts[0].strip(), parts[1].strip()
            if not name:
                raise ValueError(f"Line {lineno}: empty name")

            try:
                salary = int(salary_part)
            except ValueError:
                raise ValueError(f"Line {lineno}: invalid salary {salary_part!r}") from None

            if salary < 0:
                raise ValueError(f"Line {lineno}: negative salary {salary}")

            total += salary
            count += 1

    return total, calculate_average(total, count)



# total, average = total_salary("salary_file.txt")
# print(f"Total salary: {total}, Average salary: {average}")