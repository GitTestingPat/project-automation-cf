import re
from pathlib import Path


def find_markers():
    test_files = list(Path("api_tests").glob("test_*.py"))

    results = []
    for file in test_files:
        content = file.read_text()
        if "@pytest.mark.TC_API" in content:
            marker = re.search(r'@pytest\.mark\.(TC_API_\d+)', content)
            if marker:
                results.append((marker.group(1), file.name, True))
        else:
            results.append(("Sin marker", file.name, False))

    # Ordenar por ID
    results.sort(key=lambda x: (not x[2], x[0]))

    for marker, filename, has_marker in results:
        icon = "✅" if has_marker else "❌"
        print(f"{icon} {marker:15} → {filename}")


if __name__ == "__main__":
    print("\n🔍 Validando trazabilidad...\n")
    find_markers()
