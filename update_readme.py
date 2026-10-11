#!/usr/bin/env python3
"""
update_readme.py
Automatically regenerates the Progress stats and Solutions Index table
in README.md based on problem directories present in the repository.
"""

import os
import re

# Curated topic mappings for common problems (fallback is inferred or 'Algorithms')
KNOWN_TOPICS = {
    1: "Array, Hash Table",
    2: "Linked List, Math",
    3: "Hash Table, String, Sliding Window",
    4: "Array, Binary Search, Divide & Conquer",
    5: "String, Dynamic Programming",
    7: "Math",
    9: "Math",
    11: "Array, Two Pointers, Greedy",
    13: "Hash Table, Math, String",
    14: "String, Trie",
    15: "Array, Two Pointers, Sorting",
    19: "Linked List, Two Pointers",
    20: "String, Stack",
    21: "Linked List, Recursion",
    22: "String, Dynamic Programming, Backtracking",
    23: "Linked List, Divide & Conquer, Heap",
    26: "Array, Two Pointers",
    27: "Array, Two Pointers",
    33: "Array, Binary Search",
    35: "Array, Binary Search",
    42: "Array, Two Pointers, Dynamic Programming, Stack",
    46: "Array, Backtracking",
    48: "Array, Math, Matrix",
    49: "Array, Hash Table, String, Sorting",
    53: "Array, Divide & Conquer, Dynamic Programming",
    54: "Array, Matrix, Simulation",
    55: "Array, Dynamic Programming, Greedy",
    56: "Array, Sorting",
    70: "Math, Dynamic Programming, Memoization",
    74: "Array, Binary Search, Matrix",
    75: "Array, Two Pointers, Sorting",
    76: "Hash Table, String, Sliding Window",
    78: "Array, Backtracking, Bit Manipulation",
    79: "Array, String, Backtracking, Matrix",
    98: "Tree, Depth-First Search, Binary Search Tree",
    100: "Tree, Depth-First Search, Breadth-First Search",
    102: "Tree, Breadth-First Search, Binary Tree",
    104: "Tree, Depth-First Search, Breadth-First Search",
    121: "Array, Dynamic Programming",
    125: "Two Pointers, String",
    128: "Array, Hash Table, Union Find",
    136: "Array, Bit Manipulation",
    138: "Hash Table, Linked List",
    141: "Hash Table, Linked List, Two Pointers",
    143: "Linked List, Two Pointers, Stack",
    150: "Array, Math, Stack",
    153: "Array, Binary Search",
    155: "Stack, Design",
    167: "Array, Two Pointers, Binary Search",
    198: "Array, Dynamic Programming",
    200: "Array, Depth-First Search, Breadth-First Search, Union Find",
    206: "Linked List, Recursion",
    207: "Depth-First Search, Breadth-First Search, Graph, Topological Sort",
    208: "Hash Table, String, Design, Trie",
    217: "Array, Hash Table",
    226: "Tree, Depth-First Search, Breadth-First Search, Binary Tree",
    230: "Tree, Depth-First Search, Binary Search Tree",
    235: "Tree, Depth-First Search, Binary Search Tree",
    238: "Array, Prefix Sum",
    242: "Hash Table, String, Sorting",
    283: "Array, Two Pointers",
    300: "Array, Binary Search, Dynamic Programming",
    322: "Array, Dynamic Programming, Breadth-First Search",
    347: "Array, Hash Table, Divide & Conquer, Sorting, Heap",
    424: "Hash Table, String, Sliding Window",
    704: "Array, Binary Search",
}

DIFFICULTY_BADGES = {
    "Easy": "🟢 Easy",
    "Medium": "🟡 Medium",
    "Hard": "🔴 Hard",
}


def get_problem_number(folder_name: str) -> int:
    m = re.match(r"^(\d+)-", folder_name)
    return int(m.group(1)) if m else 999999


def parse_problems(base_dir: str):
    dirs = [
        d for d in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, d)) and not d.startswith(".") and re.match(r"^\d+-", d)
    ]
    dirs.sort(key=get_problem_number)

    problems = []
    counts = {"Easy": 0, "Medium": 0, "Hard": 0}

    for folder in dirs:
        num = get_problem_number(folder)
        readme_path = os.path.join(base_dir, folder, "README.md")
        raw_slug = folder.split("-", 1)[1] if "-" in folder else folder
        title = raw_slug.replace("-", " ").title()
        url = f"https://leetcode.com/problems/{raw_slug}/"
        diff = "Easy"

        if os.path.exists(readme_path):
            with open(readme_path, "r", encoding="utf-8") as rf:
                content = rf.read()
                m_title = re.search(r'<h2><a href="([^"]+)">([^<]+)</a></h2>', content)
                if m_title:
                    url = m_title.group(1).strip()
                    title = m_title.group(2).strip()
                m_diff = re.search(r"Difficulty-([A-Za-z]+)", content)
                if m_diff:
                    diff = m_diff.group(1).capitalize()

        if diff not in counts:
            counts[diff] = 0
        counts[diff] += 1

        py_files = [f for f in os.listdir(os.path.join(base_dir, folder)) if f.endswith(".py")]
        py_file = py_files[0] if py_files else ""
        topic = KNOWN_TOPICS.get(num, "Algorithms")

        problems.append({
            "num": num,
            "folder": folder,
            "title": title,
            "url": url,
            "diff": diff,
            "topic": topic,
            "py_file": py_file,
        })

    return problems, counts


def build_markdown_table(problems):
    lines = [
        "| # | Problem | Difficulty | Topic | Solution |",
        "| :-: | :-- | :-: | :-- | :-: |",
    ]
    for p in problems:
        num_str = f"{p['num']:04d}"
        prob_link = f"[{p['title']}]({p['folder']})"
        diff_str = DIFFICULTY_BADGES.get(p["diff"], p["diff"])
        topic_str = p["topic"]
        sol_link = f"[Python](./{p['folder']}/{p['py_file']})" if p["py_file"] else "—"
        lines.append(f"| {num_str} | {prob_link} | {diff_str} | {topic_str} | {sol_link} |")
    return "\n".join(lines)


def build_stats_table(counts, total):
    lines = [
        "| Metric | Count |",
        "| :--- | :---: |",
        f"| 🟢 **Easy** | `{counts.get('Easy', 0)}` |",
        f"| 🟡 **Medium** | `{counts.get('Medium', 0)}` |",
        f"| 🔴 **Hard** | `{counts.get('Hard', 0)}` |",
        f"| **Total Solved** | **`{total}`** |",
    ]
    return "\n".join(lines)


def update_readme():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    readme_path = os.path.join(base_dir, "README.md")

    if not os.path.exists(readme_path):
        print("README.md not found in repository root.")
        return

    problems, counts = parse_problems(base_dir)
    total = len(problems)

    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()

    # Update Badge Solved Count
    badge_pattern = r"(<!-- BADGE_SOLVED_START -->\s*\[!\[Problems Solved\]\(https://img\.shields\.io/badge/Solved-)[^-\)]+(-10B981\?style=flat-square\)\(\s*https://github\.com/abhaydasarathy/dsamaxxing\s*\)\s*<!-- BADGE_SOLVED_END -->)"
    replacement_badge = f"<!-- BADGE_SOLVED_START -->\n[![Problems Solved](https://img.shields.io/badge/Solved-{total}-10B981?style=flat-square)](https://github.com/abhaydasarathy/dsamaxxing)\n<!-- BADGE_SOLVED_END -->"
    readme_content = re.sub(
        r"<!-- BADGE_SOLVED_START -->.*?<!-- BADGE_SOLVED_END -->",
        replacement_badge,
        readme_content,
        flags=re.DOTALL,
    )

    # Update Stats Table
    stats_table = build_stats_table(counts, total)
    readme_content = re.sub(
        r"<!-- STATS_START -->.*?<!-- STATS_END -->",
        f"<!-- STATS_START -->\n{stats_table}\n<!-- STATS_END -->",
        readme_content,
        flags=re.DOTALL,
    )

    # Update Problems Table
    problems_table = build_markdown_table(problems)
    readme_content = re.sub(
        r"<!-- PROBLEMS_START -->.*?<!-- PROBLEMS_END -->",
        f"<!-- PROBLEMS_START -->\n{problems_table}\n<!-- PROBLEMS_END -->",
        readme_content,
        flags=re.DOTALL,
    )

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"Successfully updated README.md: {total} problems indexed (Easy: {counts.get('Easy', 0)}, Medium: {counts.get('Medium', 0)}, Hard: {counts.get('Hard', 0)}).")


if __name__ == "__main__":
    update_readme()
