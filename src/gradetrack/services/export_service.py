import csv
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import yaml

from repositories import grade_repository
from services.auth_service import TEACHER, STUDENT, require_role

OUT_DIR = Path(__file__).resolve().parents[3] / "out"


def flatten(record, prefix=""):
    result = {}
    for key, value in record.items():
        name = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            result.update(flatten(value, name))
        elif isinstance(value, list):
            result[name] = json.dumps(value, ensure_ascii=False)
        else:
            result[name] = value
    return result


def fill_xml(element, value):
    if isinstance(value, dict):
        for key, item in value.items():
            fill_xml(ET.SubElement(element, key), item)
    elif isinstance(value, list):
        for item in value:
            fill_xml(ET.SubElement(element, "item"), item)
    elif value is not None:
        element.text = str(value)


def write_files(records, directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)

    with (directory / "data.json").open("w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=2)

    with (directory / "data.yaml").open("w", encoding="utf-8") as file:
        yaml.safe_dump(records, file, allow_unicode=True, sort_keys=False)

    rows = [flatten(record) for record in records]
    columns = list(dict.fromkeys(key for row in rows for key in row))
    with (directory / "data.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    root = ET.Element("records")
    for record in records:
        fill_xml(ET.SubElement(root, "record"), record)
    ET.indent(root, space="  ")
    ET.ElementTree(root).write(directory / "data.xml", encoding="utf-8", xml_declaration=True)


def export_grades(user):
    require_role(user, TEACHER, STUDENT)
    student_id = user.user_id if user.role_id == STUDENT else None
    records = grade_repository.get_for_export(student_id)
    write_files(records, OUT_DIR)
    return len(records), OUT_DIR
