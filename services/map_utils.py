import re
import urllib.parse


def build_map_links(start_location: str, city: str, destination: str) -> dict:
    origin = start_location.strip() if start_location.strip() else f"{city}市中心"
    destination = destination.strip()
    query = urllib.parse.quote(f"{origin} 到 {destination}")

    return {
        "amap": f"https://www.amap.com/search?query={query}",
        "baidu": f"https://map.baidu.com/search/{query}",
    }


def extract_destination_from_answer(answer: str) -> str:
    patterns = [
        r"地点名称[:：]\s*(.+)",
        r"推荐地点[:：]\s*(.+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, answer)

        if match:
            name = match.group(1).strip()
            name = re.sub(r"[*#`]", "", name)
            name = name.split("\n")[0].strip()

            if 2 <= len(name) <= 40:
                return name

    return ""