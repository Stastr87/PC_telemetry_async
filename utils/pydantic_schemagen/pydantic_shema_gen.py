"""Generate pydantic schemas"""
import os
from re import search
from typing import Any

from utils.common_utils import load_json_from_file, write_lines_to_file


def create_json_file_from_dict(value: dict, file_name: str) -> None:
    """create json file"""

    new_lines = ["{"]
    for k, v in value.items():
        if str(v).isdecimal():
            new_lines.append(f'"{k}": {v},')
        elif str(v).startswith("["):
            new_lines.append(
                f'"{k}": {v},'.replace("'", '"')
                .replace("True", '"True"')
                .replace("False", '"False"')
            )
        else:
            new_lines.append(f'"{k}": "{v}",')
    last_str = new_lines[-1].replace(",", "")
    new_lines = new_lines[:-1] + [last_str] + ["}"]
    write_lines_to_file(file_name, new_lines)


def define_class_name(method_name: str) -> str:
    """Define name for schema class"""
    class_str = method_name[0].upper()
    is_upper = False
    for ch in method_name[1:]:
        if is_upper:
            class_str += ch.upper()
            is_upper = False
        elif ch != "_":
            class_str += ch
        elif ch == "_":
            is_upper = True

    return class_str


def define_type(value: Any) -> str:
    """Define type"""

    str_type = ""
    value_type = search("'.*'", str(type(value)))
    if value_type:
        str_type = value_type.group(0).replace("'", "")

    return str_type


def schema_gen(
    file_path: str, method_name: str, method_type: str, reqursion: bool = False
):  # pylint: disable=R0914
    """Generate code for pydantic schemas"""

    json_data = load_json_from_file(file_path)

    lines = []
    fields = ['"""Field names"""\n\n']
    fields_dict = {}

    class_str = define_class_name(method_name)

    for field, value in (
        json_data.items() if isinstance(json_data, dict) else json_data[3].items()
    ):

        str_type = define_type(value)
        field_value = str_type
        field_dict_value: Any = '""'

        if str_type == "dict":
            file_name = os.path.join('output', field + file_path)
            create_json_file_from_dict(value, field + file_path)
            schema_gen(file_name, field, "", True)
            field_value = f"{define_class_name(field)}Schema"
            field_dict_value = {}

        elif str_type == "list":
            if len(value) > 0 and isinstance(value[0], dict):
                file_name = os.path.join('output', field + file_path)
                create_json_file_from_dict(value[0], field + file_path)
                schema_gen(file_name, field, "", True)
                field_value = f"List[{define_class_name(field)}Schema]"
                field_dict_value = [{}]
            elif len(value) > 0:
                field_value = f"List[{define_type(value[0])}]"
            else:
                field_value = "List[]"

        elif str_type == "int":
            field_dict_value = 0

        lines.append(f"""    {field}: {field_value}\n""")
        field_name = f"{method_name.upper()}_{str(field).upper()}_FIELD"
        fields.append(f'{field_name} = "{field}"\n')
        fields_dict[field_name] = field_dict_value

    class_str += "" if lines else method_type[0].upper() + method_type[1:]
    if lines:
        lines.append("\n\n\n")

    lines = (
        [
            f'"""{method_name} {method_type} method schema"""\n'
            "from clients.api_inspector.base_schema import BaseSchema\n\n"
        ]
        + [f"\nclass {class_str}Schema(BaseSchema):\n"]
        + [f'    """{method_name} {method_type} method schema"""\n\n']
        + lines
    )
    write_lines_to_file(os.path.join('output', f"{method_name}_{method_type}.py"), lines)
    write_lines_to_file(os.path.join('output',f"field_names{method_name if reqursion else ""}.py"), fields)

    print("Dictionary template with field names: ")
    print("{")
    for key, value in fields_dict.items():
        print(f"{key}: {value},")
    print("}\n")


schema_gen(
    file_path="model.json",
    method_name="return_hw_data",
    method_type="post",
)
