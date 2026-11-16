"""Kiểm bài nộp và đối chiếu quyết định với vòng QC của bản nhãn hiện tại."""
from __future__ import annotations

import argparse
import json
import re

from common import QC_DIR, ROOT, digest, load_all_labels, load_taxonomy, require_assignment
from qc_report import make_report
from review_evidence import LABELS_PATH, round_dir

SUB = ROOT / "submission"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--round", type=int, default=1, help="Vòng được dùng để ra quyết định cuối.")
    args = parser.parse_args()
    if args.round < 1:
        parser.error("--round phải là số nguyên dương.")
    assignment = require_assignment()
    members = {member for codes in assignment.values() for member in codes}
    errors = []
    for member in sorted(members):
        for path in (
            SUB / "guidelines" / "individual" / f"guideline_{member}.md",
            SUB / "labels" / f"{member}.json",
            SUB / "individual_notes" / f"{member}.md",
        ):
            if not path.is_file() or not path.read_text(encoding="utf-8").strip():
                errors.append(f"Thiếu hoặc trống: {path.relative_to(ROOT)}.")
    labels = load_all_labels(load_taxonomy())
    if set(labels) != members:
        errors.append("Danh sách file nhãn phải khớp mã thành viên trong assignment.csv.")
    starter = ROOT / "guideline" / "guideline_v0_starter.md"
    for member in sorted(members):
        draft = SUB / "guidelines" / "individual" / f"guideline_{member}.md"
        if draft.is_file() and digest(draft) == digest(starter):
            errors.append(f"Guideline {member} giống nguyên bản v0.")
    report = QC_DIR / "QC_REPORT.md"
    try:
        text = report.read_text(encoding="utf-8")
        if "<<" in text or "TODO" in text:
            errors.append("QC_REPORT.md còn nội dung mẫu.")
        decision_line = re.search(r"^- Quyết định: (Release|Hold|Rework)\s*$", text, re.M)
        round_line = re.search(r"^- Vòng QC: ([0-9]+)\s*$", text, re.M)
        if not round_line or int(round_line[1]) != args.round:
            errors.append("QC_REPORT.md cần ghi số vòng QC đang nộp.")
        directory = round_dir(args.round)
        result = json.loads((directory / "qc_result.json").read_text(encoding="utf-8"))
        if (
            result["round"] != args.round or result["labels_sha256"] != digest(LABELS_PATH)
            or result["review_sha256"] != digest(directory / "qc_review.csv")
        ):
            errors.append("qc_result.json lệch phiếu hoặc bản nhãn. Chạy qc_report.py với đúng vòng.")
        review_args = argparse.Namespace(round=args.round, **result["reviewer_inputs"])
        computed, _ = make_report(directory, review_args)
        if computed != result["decision"] or not decision_line or computed != decision_line[1].upper():
            errors.append(f"Quyết định trong bài nộp cần khớp vòng QC hiện tại ({computed}).")
    except (OSError, ValueError, KeyError, TypeError, SystemExit) as exc:
        errors.append(f"Chưa đủ bằng chứng bàn giao: {exc}.")
    if not (ROOT / "TEAM.md").is_file():
        errors.append("Thiếu TEAM.md.")
    for error in errors:
        print(f"LỖI: {error}")
    print(f"Tổng kết: {len(errors)} lỗi. Reviewer vẫn cần kiểm nội dung và mở thử gói bàn giao.")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
