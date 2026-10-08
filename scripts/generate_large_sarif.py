#!/usr/bin/env python3
"""Generate a realistic SARIF (Trivy-style) security scan report padded to a target size.

Usage: generate_large_sarif.py <output_path> [target_size_bytes]
"""
import json
import os
import sys

TARGET_SIZE = int(sys.argv[2]) if len(sys.argv) > 2 else 50 * 1024 * 1024  # 50MB default
OUTPUT_PATH = sys.argv[1] if len(sys.argv) > 1 else "test/large-scan.sarif"

RULES = [
    {
        "id": "CVE-2023-44487",
        "name": "HTTP2RapidReset",
        "shortDescription": {"text": "HTTP/2 Rapid Reset Attack"},
        "fullDescription": {
            "text": "The HTTP/2 protocol allows a denial of service (server resource consumption) "
            "because request cancellation can reset many streams quickly."
        },
        "defaultConfiguration": {"level": "error"},
        "properties": {"precision": "very-high", "severity": "HIGH"},
    },
    {
        "id": "CVE-2024-0567",
        "name": "GnuTLSCertVerification",
        "shortDescription": {"text": "GnuTLS certificate verification bypass"},
        "fullDescription": {
            "text": "A vulnerability was found in GnuTLS where a cockpit web service may accept a "
            "certificate that is not yet valid or has been revoked."
        },
        "defaultConfiguration": {"level": "warning"},
        "properties": {"precision": "high", "severity": "MEDIUM"},
    },
]

RESULT_TEMPLATES = [
    {
        "ruleId": "CVE-2023-44487",
        "ruleIndex": 0,
        "level": "error",
        "message": {
            "text": "Package: golang.org/x/net\nInstalled Version: 0.15.0\nFixed Version: 0.17.0\n"
            "Vulnerability: HTTP/2 Rapid Reset Attack"
        },
        "locations": [
            {"physicalLocation": {"artifactLocation": {"uri": "go.sum"}, "region": {"startLine": 1}}}
        ],
    },
    {
        "ruleId": "CVE-2024-0567",
        "ruleIndex": 1,
        "level": "warning",
        "message": {
            "text": "Package: gnutls\nInstalled Version: 3.7.8\nFixed Version: 3.7.10\n"
            "Vulnerability: GnuTLS certificate verification bypass"
        },
        "locations": [
            {"physicalLocation": {"artifactLocation": {"uri": "Dockerfile"}, "region": {"startLine": 1}}}
        ],
    },
]


def build_report(results):
    return {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "trivy",
                        "version": "0.50.0",
                        "informationUri": "https://github.com/aquasecurity/trivy",
                        "rules": RULES,
                    }
                },
                "results": results,
            }
        ],
    }


# Measure the serialized size of one "round" of results to compute how many rounds are
# needed, instead of re-serializing the whole (growing) list on every iteration.
round_len = len(json.dumps(RESULT_TEMPLATES)) + 1  # +1 for the comma joining rounds
results = []
round_index = 0
while (round_index * round_len) < TARGET_SIZE - 4096:
    for template in RESULT_TEMPLATES:
        results.append(json.loads(json.dumps(template)))
    round_index += 1

# Trim off any overshoot (results don't grow with index here, so this should rarely
# trigger, but measure for real rather than assume the estimate above was exact).
num_templates = len(RESULT_TEMPLATES)
overshoot = len(json.dumps(build_report(results))) - (TARGET_SIZE - 4096)
if overshoot > 0:
    rounds_to_drop = overshoot // round_len + 1
    results = results[: len(results) - rounds_to_drop * num_templates]
    while results and len(json.dumps(build_report(results))) > TARGET_SIZE - 4096:
        del results[-num_templates:]

# Pad the last result's message text (a legitimate free-form string field) to hit the
# target size exactly, rather than adding an unrecognized top-level key to the SARIF doc.
report = build_report(results)
current_len = len(json.dumps(report))
pad_needed = max(0, TARGET_SIZE - current_len)
report["runs"][0]["results"][-1]["message"]["text"] += "\n" + ("a" * max(0, pad_needed - 1))

output_dir = os.path.dirname(OUTPUT_PATH)
if output_dir:
    os.makedirs(output_dir, exist_ok=True)

with open(OUTPUT_PATH, "w") as f:
    json.dump(report, f)

print("wrote", os.path.getsize(OUTPUT_PATH), "bytes to", OUTPUT_PATH)
