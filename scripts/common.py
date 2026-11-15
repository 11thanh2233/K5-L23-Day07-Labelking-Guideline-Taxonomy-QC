"""Hàm dùng chung cho các script của lab (đọc taxonomy, đọc nhãn COCO của CVAT, IoU, ghép box...).

Học viên KHÔNG cần sửa file này. Nhóm chỉ sửa submission/taxonomy.json khi đổi lớp/thuộc tính.
"""
from __future__ import annotations

import csv
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
TAXONOMY_PATH = ROOT / "submission" / "taxonomy.json"
LABELS_DIR = ROOT / "submission" / "labels"
QC_DIR = ROOT / "submission" / "qc"
IMAGES_DIR = ROOT / "data" / "images"
WORK_DIR = ROOT / "work"
IMG_EXT = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

Box = Tuple[float, float, float, float]  # (x1, y1, x2, y2)


def die(msg: str, code: int = 2) -> None:
    print(f"\nLỖI: {msg}", file=sys.stderr)
    sys.exit(code)


# --------------------------------------------------------------------------- taxonomy
class Taxonomy:
    def __init__(self, d: dict):
        self.raw = d
        self.version = d.get("version", "?")
        self.classes: List[str] = [c["name"] for c in d["classes"]]
        self.attrs: Dict[str, dict] = {a["name"]: a for a in d.get("attributes", [])}
        self.rules: dict = d["rules"]
        self.ignore: str = d.get("ignore_class", "ignore_region")

    @property
    def object_classes(self) -> List[str]:
        return [c for c in self.classes if c != self.ignore]

    def default(self, name: str) -> str:
        return self.norm_attr(name, self.attrs[name].get("default"))

    def norm_attr(self, name: str, value) -> str:
        """Chuẩn hoá giá trị thuộc tính về chuỗi thường để so sánh được giữa các người gán."""
        a = self.attrs.get(name, {})
        vals = [str(v).lower() for v in a.get("values", [])]
        if a.get("type") == "checkbox":
            if value is None:
                return "false"
            return "true" if str(value).strip().lower() in ("true", "1", "yes", "on", "1.0") else "false"
        if value is None:
            value = a.get("default", "")
        if isinstance(value, bool):
            if "yes" in vals:
                return "yes" if value else "no"
            return "true" if value else "false"
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        s = str(value).strip().lower()
        if s in ("true", "false") and "yes" in vals:
            s = "yes" if s == "true" else "no"
        if s.endswith(".0") and s[:-2].isdigit():
            s = s[:-2]
        return s

    def valid(self, name: str, norm_value: str) -> bool:
        a = self.attrs[name]
        if a.get("type") == "checkbox":
            return norm_value in ("true", "false")
        return norm_value in [str(v).lower() for v in a.get("values", [])]

    def to_coco_value(self, name: str, norm_value: str):
        if self.attrs[name].get("type") == "checkbox":
            return norm_value == "true"
        return norm_value


def load_taxonomy() -> Taxonomy:
    if not TAXONOMY_PATH.exists():
        die(f"Không thấy {TAXONOMY_PATH.relative_to(ROOT)}. Hãy chạy script từ thư mục gốc của repo.")
    try:
        return Taxonomy(json.loads(TAXONOMY_PATH.read_text(encoding="utf8")))
    except (json.JSONDecodeError, KeyError) as e:
        die(f"taxonomy.json bị lỗi cú pháp/thiếu trường ({e}). Kiểm tra dấu phẩy, ngoặc kép.")
        raise


# --------------------------------------------------------------------------- hình học
def xywh_to_xyxy(b) -> Box:
    return (float(b[0]), float(b[1]), float(b[0]) + float(b[2]), float(b[1]) + float(b[3]))


def xyxy_to_xywh(b: Box) -> List[float]:
    return [round(b[0], 2), round(b[1], 2), round(b[2] - b[0], 2), round(b[3] - b[1], 2)]


def area(b: Box) -> float:
    return max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])


def inter_area(a: Box, b: Box) -> float:
    return max(0.0, min(a[2], b[2]) - max(a[0], b[0])) * max(0.0, min(a[3], b[3]) - max(a[1], b[1]))


def iou(a: Box, b: Box) -> float:
    inter = inter_area(a, b)
    u = area(a) + area(b) - inter
    return inter / u if u > 0 else 0.0


def covered_by(box: Box, regions: List[Box], frac: float = 0.5) -> bool:
    """True nếu >= frac diện tích box nằm trong một vùng ignore."""
    a = area(box)
    return a > 0 and any(inter_area(box, r) / a >= frac for r in regions)


def mean_box(boxes: List[Box]) -> Box:
    n = len(boxes)
    return tuple(sum(b[i] for b in boxes) / n for i in range(4))  # type: ignore


def iou_threshold(tax: Taxonomy, a: Box, b: Box) -> float:
    h = ((a[3] - a[1]) + (b[3] - b[1])) / 2
    r = tax.rules
    return r["iou_thr_large"] if h >= r["large_px"] else r["iou_thr_small"]


# --------------------------------------------------------------------------- đọc COCO
@dataclass
class Obj:
    id: int
    cls: str
    box: Box
    attrs: Dict[str, str]
    raw_attrs: dict = field(default_factory=dict)


@dataclass
class LabelFile:
    path: Path
    mshv: str
    name: str
    images: Dict[str, Tuple[int, int]]          # basename -> (w, h)
    objects: Dict[str, List[Obj]]               # basename -> objects (kể cả ignore_region)
    problems: List[str] = field(default_factory=list)


def mshv_of(path: Path) -> str:
    return path.stem.split("_", 1)[0]


def load_coco(path: Path, tax: Taxonomy) -> LabelFile:
    data = json.loads(Path(path).read_text(encoding="utf8"))
    cats = {c["id"]: c["name"] for c in data.get("categories", [])}
    imgs = {}
    lf = LabelFile(Path(path), mshv_of(Path(path)), Path(path).stem, {}, {})
    for im in data.get("images", []):
        base = Path(im["file_name"]).name
        if base in lf.images:
            lf.problems.append(f"ảnh {base} xuất hiện 2 lần trong file")
        imgs[im["id"]] = base
        lf.images[base] = (int(im.get("width", 0)), int(im.get("height", 0)))
        lf.objects.setdefault(base, [])
    for an in data.get("annotations", []):
        base = imgs.get(an.get("image_id"))
        if base is None:
            lf.problems.append(f"annotation {an.get('id')} trỏ tới image_id không có trong 'images'")
            continue
        cls = cats.get(an.get("category_id"), f"?category_id={an.get('category_id')}")
        raw = an.get("attributes", {}) or {}
        attrs = {n: tax.norm_attr(n, raw.get(n)) for n in tax.attrs}
        lf.objects[base].append(Obj(an.get("id", 0), cls, xywh_to_xyxy(an["bbox"]), attrs, raw))
    return lf


def list_label_files() -> List[Path]:
    return sorted(p for p in LABELS_DIR.glob("*.json"))


def load_all_labels(tax: Taxonomy) -> Dict[str, LabelFile]:
    files = list_label_files()
    if not files:
        die("Chưa có file nhãn nào trong submission/labels/. Mỗi thành viên export COCO 1.0 từ CVAT, "
            "đặt tên <MSHV>_<HoTen>.json rồi bỏ vào đó.")
    out: Dict[str, LabelFile] = {}
    for p in files:
        try:
            lf = load_coco(p, tax)
        except Exception as e:  # noqa
            die(f"Không đọc được {p.name}: {e}. Chạy `python scripts/validate_labels.py` để xem chi tiết.")
            raise
        out[lf.mshv] = lf
    return out


def load_assignment() -> Optional[Dict[str, List[str]]]:
    p = QC_DIR / "assignment.csv"
    if not p.exists():
        return None
    with p.open(encoding="utf8", newline="") as f:
        return {r["image"]: [x for x in r["annotators"].split("|") if x] for r in csv.DictReader(f)}


def list_images() -> List[str]:
    if not IMAGES_DIR.exists():
        return []
    return sorted(p.name for p in IMAGES_DIR.iterdir() if p.suffix.lower() in IMG_EXT)


def read_flagged() -> List[str]:
    p = QC_DIR / "flagged_images.txt"
    if not p.exists():
        return []
    return [l.strip() for l in p.read_text(encoding="utf8").splitlines() if l.strip()]


# --------------------------------------------------------------------------- ghép box
def match_boxes(A: List[Obj], B: List[Obj], thr: float):
    """Ghép 1-1 tham lam theo IoU giảm dần (không quan tâm lớp). Trả về (cặp, A chưa ghép, B chưa ghép)."""
    cands = []
    for i, a in enumerate(A):
        for j, b in enumerate(B):
            v = iou(a.box, b.box)
            if v >= thr:
                cands.append((v, i, j))
    cands.sort(key=lambda t: (-t[0], t[1], t[2]))
    ua, ub, pairs = set(), set(), []
    for v, i, j in cands:
        if i in ua or j in ub:
            continue
        ua.add(i)
        ub.add(j)
        pairs.append((A[i], B[j], v))
    return pairs, [a for i, a in enumerate(A) if i not in ua], [b for j, b in enumerate(B) if j not in ub]


def cluster_objects(per_ann: Dict[str, List[Obj]], thr: float) -> List[Dict[str, Obj]]:
    """Gom box của các người gán thành cụm (mỗi cụm tối đa 1 box/người). Class-agnostic."""
    clusters: List[Dict[str, Obj]] = []
    for m in sorted(per_ann):
        objs = per_ann[m]
        cands = []
        for oi, o in enumerate(objs):
            for ci, c in enumerate(clusters):
                v = iou(o.box, mean_box([x.box for x in c.values()]))
                if v >= thr:
                    cands.append((v, oi, ci))
        cands.sort(key=lambda t: (-t[0], t[1], t[2]))
        used_o, used_c = set(), set()
        for v, oi, ci in cands:
            if oi in used_o or ci in used_c:
                continue
            clusters[ci][m] = objs[oi]
            used_o.add(oi)
            used_c.add(ci)
        for oi, o in enumerate(objs):
            if oi not in used_o:
                clusters.append({m: o})
    return clusters


def annotators_of_image(files: Dict[str, LabelFile], img: str,
                        assignment: Optional[Dict[str, List[str]]]) -> List[str]:
    """Người đã gán ảnh img (có ảnh trong file của họ, và — nếu có assignment — được giao ảnh đó)."""
    if assignment is not None and img not in assignment:
        return []
    return [m for m in sorted(files)
            if img in files[m].objects and (assignment is None or m in assignment[img])]


# --------------------------------------------------------------------------- ghi COCO
def build_coco(tax: Taxonomy, images: List[dict], annotations: List[dict], info: Optional[dict] = None) -> dict:
    return {
        "info": info or {},
        "licenses": [],
        "categories": [{"id": i + 1, "name": n} for i, n in enumerate(tax.classes)],
        "images": images,
        "annotations": annotations,
    }


def make_ann(tax: Taxonomy, ann_id: int, image_id: int, cls: str, box: Box, attrs: Dict[str, str],
             extra: Optional[dict] = None) -> dict:
    xywh = xyxy_to_xywh(box)
    at = {n: tax.to_coco_value(n, attrs.get(n, tax.default(n))) for n in tax.attrs}
    at.update(extra or {})
    return {"id": ann_id, "image_id": image_id, "category_id": tax.classes.index(cls) + 1,
            "bbox": xywh, "area": round(xywh[2] * xywh[3], 2), "iscrowd": 0, "attributes": at}


def read_csv(path: Path) -> List[dict]:
    with path.open(encoding="utf8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, header: List[str], rows: List[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)
