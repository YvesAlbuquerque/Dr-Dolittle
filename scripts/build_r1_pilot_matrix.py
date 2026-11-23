#!/usr/bin/env python3
"""Build an explicitly provisional capability-by-sampling-group source-coverage matrix.

Not a heatmap of biological presence or absence. No entries are independently reviewed.
Usage: python scripts/build_r1_pilot_matrix.py --root .
"""
import argparse
import csv
import html
from collections import defaultdict
from pathlib import Path


def read(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def build(root):
    root = Path(root)
    evidence = root / "data" / "evidence"
    ontology = root / "data" / "ontology"
    assertions = read(evidence / "assertions.csv")
    if not assertions or any(r["review_status"] != "draft_unreviewed" for r in assertions):
        raise ValueError("R1 draft matrix requires nonempty all-draft assertions")
    groups = {r["assertion_id"]: r["sampling_group"] for r in read(evidence / "assertion_sampling_scope.csv")}
    names = {r["capability_id"]: r["label"] for r in read(ontology / "capabilities.csv")}
    refs = defaultdict(set)
    for r in read(evidence / "assertion_sources.csv"):
        refs[r["assertion_id"]].add(r["reference_id"])
    coverage = defaultdict(set)
    for link in read(evidence / "assertion_capabilities.csv"):
        aid = link["assertion_id"]
        if aid not in groups or link["capability_id"] not in names:
            raise ValueError(f"invalid coverage relation: {link}")
        coverage[(link["capability_id"], groups[aid])].update(refs[aid])
    caps = sorted(names, key=lambda item: names[item].lower())
    group_labels = {
        "birds": "Birds", "cephalopods": "Cephalopods", "cetaceans": "Cetaceans",
        "eusocial_insects": "Social insects", "fishes": "Fishes",
        "group_living_insects": "Other group insects", "primates": "Primates",
        "rodents": "Rodents", "terrestrial_mammals": "Other mammals",
    }
    cols = sorted(set(groups.values()), key=lambda item: group_labels.get(item, item).lower())
    rows = [{"capability_id": cap, "capability_label": names[cap],
             "sampling_group": group, "source_count_draft": len(coverage[(cap, group)]),
             "interpretation": "draft_sources_only" if coverage[(cap, group)] else "not_covered_by_pilot"}
            for cap in caps for group in cols]
    generated = root / "docs" / "figures"
    generated.mkdir(parents=True, exist_ok=True)
    with (generated / "r1-draft-coverage.csv").open("w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fieldnames=rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    # Static SVG, with accessible text and no inference from missing pilot sources.
    left, top, cell_w, cell_h = 278, 184, 102, 46
    width, height = left + len(cols)*cell_w + 22, top + len(caps)*cell_h + 78
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="ttl desc">',
           '<title id="ttl">R1 pilot draft source coverage by candidate capability and animal sampling group</title>',
           '<desc id="desc">Not evidence of presence or absence. Cells show count of unique linked papers in a curated fifteen-study draft pilot. Blank cells mean not covered by this pilot.</desc>',
           f'<rect width="{width}" height="{height}" fill="#fffdf9"/>',
           '<text x="20" y="35" font-family="Arial,sans-serif" font-size="20" font-weight="700" fill="#18272e">R1 • Draft source coverage</text>',
           '<text x="20" y="61" font-family="Arial,sans-serif" font-size="14" fill="#4a6069">15 selected studies · candidate tags · unreviewed extractions</text>',
           '<text x="20" y="83" font-family="Arial,sans-serif" font-size="14" fill="#9a481d">NOT a map of biological ability, absence, prevalence, or verified science</text>',
           '<text x="20" y="113" font-family="Arial,sans-serif" font-size="13" fill="#415861">Cell values = distinct linked draft papers · dash = not sampled in this pilot</text>']
    for j, group in enumerate(cols):
        name = html.escape(group_labels.get(group, group))
        x = left + j * cell_w + cell_w / 2
        # Vertical header text supports compact labels without overlap.
        svg.append(f'<text x="{x:.1f}" y="{top-7}" text-anchor="start" transform="rotate(-48 {x:.1f} {top-7})" font-family="Arial,sans-serif" font-size="11" fill="#243d47">{name}</text>')
    for i, cap in enumerate(caps):
        y = top + i * cell_h
        label = html.escape(names[cap])
        svg.append(f'<text x="20" y="{y+28}" font-family="Arial,sans-serif" font-size="13" fill="#203842">{label}</text>')
        for j, group in enumerate(cols):
            n = len(coverage[(cap, group)])
            x = left+j*cell_w
            fill = "#e1eef2" if n else "#f2f3f2"
            label = str(n) if n else "–"
            svg.append(f'<rect x="{x+3}" y="{y+4}" width="{cell_w-6}" height="{cell_h-8}" rx="5" fill="{fill}" stroke="#dbe2e1"/>')
            svg.append(f'<text x="{x+cell_w/2:.1f}" y="{y+30}" text-anchor="middle" font-family="Arial,sans-serif" font-size="15" font-weight="600" fill="#315a68">{label}</text>')
    svg.append(f'<text x="20" y="{height-25}" font-family="Arial,sans-serif" font-size="12" fill="#586b70">Source: data/evidence/*.csv · generated by scripts/build_r1_pilot_matrix.py · 2026-11-23</text>')
    svg.append('</svg>')
    (generated / "r1-draft-coverage.svg").write_text("\n".join(svg)+"\n", encoding="utf-8")
    return {"studies": len(assertions), "capabilities": len(caps), "groups": len(cols), "cells": len(rows)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    opts = parser.parse_args()
    print(build(opts.root))


if __name__ == "__main__":
    main()
