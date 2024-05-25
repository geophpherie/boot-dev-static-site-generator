from pathlib import Path
import shutil

from block_markdown import markdown_to_html_node
from htmlnode import HTMLNode


def extract_title(htmlnode: HTMLNode) -> str:
    elements = htmlnode.children
    if not elements or len(elements) < 1:
        raise Exception("Bad markdown")

    first_element = elements[0]

    if (
        first_element.tag != "h1"
        or not first_element.children
        or len(first_element.children) == 0
    ):
        raise Exception("Bad markdown")

    if first_element.children[0].value is None:
        raise Exception("Bad markdown")

    return first_element.children[0].value


def generate_page(from_path: Path, template_path: Path, dest_path: Path) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown = from_path.read_text()
    template = template_path.read_text()

    html = markdown_to_html_node(markdown)

    title = extract_title(html)

    template = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", html.to_html()
    )

    if not dest_path.parent.exists():
        dest_path.parent.mkdir()

    dest_path.write_text(template)


def copy_directory_recursive(src: Path, dst: Path) -> None:
    if not dst.exists():
        dst.mkdir()

    for f in src.iterdir():
        new_f = dst / f.name
        if f.is_dir():
            copy_directory_recursive(f, new_f)
        else:
            print(f"Copying {f} to {new_f}")
            shutil.copy(f, new_f)


def generate_pages_recursive(
    dir_path_content: Path, template_path: Path, dest_dir_path: Path
) -> None:
    if not dest_dir_path.exists():
        dest_dir_path.mkdir()

    for f in dir_path_content.iterdir():
        new_f = dest_dir_path / f.name
        if f.is_dir():
            generate_pages_recursive(f, template_path, new_f)
        else:
            if f.suffix.lower() == ".md":
                generate_page(f, template_path, new_f.with_suffix(".html"))
            else:
                print(f"Ignoring {f}")


def main():
    project_root = Path(__file__).parent.parent

    public_dir = project_root / "public"
    static_dir = project_root / "static"

    # remove before copying
    if public_dir.exists():
        shutil.rmtree(public_dir)

    copy_directory_recursive(static_dir, public_dir)

    from_path = project_root / "content"
    template_path = project_root / "template.html"
    dest_path = project_root / "public"

    generate_pages_recursive(from_path, template_path, dest_path)


if __name__ == "__main__":
    main()
