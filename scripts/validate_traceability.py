import re
from pathlib import Path


def find_markers():
    test_files = list(Path("api_tests").glob("test_*.py"))

    for file in test_files:
        content = file.read_text()
        if "@pytest.mark.TC_API" in content:
            marker = re.search(r'@pytest\.mark\.(TC_API_\d+)', content)
            if marker:
                print(f"✅ {marker.group(1):15} → {file.name}")
        else:
            print(f"❌ Sin marker      → {file.name}")


if __name__ == "__main__":
    print("\n🔍 Validando trazabilidad...\n")
    find_markers()
