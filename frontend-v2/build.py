import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
DIST = ROOT / "dist"
LEGACY = ROOT.parent / "frontend"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def render(template: str, context: dict[str, str]) -> str:
    output = template
    for key, value in context.items():
        output = output.replace(f"{{{{ {key} }}}}", value)
    return output


def load_locales() -> dict[str, dict[str, str]]:
    return json.loads(read_text(SRC / "data" / "locales.json"))


def copy_assets() -> None:
    DIST.mkdir(parents=True, exist_ok=True)

    for file_name in ["styles.css", "script.js", "script-en.js", "logo-pinnacle.png", "robots.txt", "sitemap.xml"]:
        source = LEGACY / file_name
        if source.exists():
            shutil.copy2(source, DIST / file_name)

    for directory_name in ["js", "img"]:
        source_dir = LEGACY / directory_name
        target_dir = DIST / directory_name
        if source_dir.exists():
            shutil.copytree(source_dir, target_dir, dirs_exist_ok=True)


def get_root_page_context(config: dict[str, str]) -> dict[str, str]:
    return {
        "lang": config["lang"],
        "title": config["title"],
        "meta_description": config["meta_description"],
        "canonical": config["canonical"],
        "hreflang_fr": config["hreflang_fr"],
        "hreflang_en": config["hreflang_en"],
        "hreflang_default": config["hreflang_default"],
        "stylesheet_path": config.get("stylesheet_path", "./styles.css"),
        "page_shell_class": config.get("page_shell_class", "page-shell"),
    }


def build_footer_links(links: list[tuple[str, str]]) -> str:
    return "\n      ".join(f'<a href="{href}">{label}</a>' for href, label in links)


def render_header(
    locale: dict[str, str],
    *,
    logo_path: str,
    home_path: str,
    about_href: str,
    expertises_href: str,
    approach_href: str,
    insights_href: str,
    contact_href: str,
    fr_href: str,
    en_href: str,
    is_fr: bool,
) -> str:
    return render(
        read_text(SRC / "partials" / "header.html"),
        {
            "logo_path": logo_path,
            "home_path": home_path,
            "about_href": about_href,
            "expertises_href": expertises_href,
            "approach_href": approach_href,
            "insights_href": insights_href,
            "contact_href": contact_href,
            "fr_href": fr_href,
            "en_href": en_href,
            "fr_class": "language-flag is-active" if is_fr else "language-flag",
            "en_class": "language-flag is-active" if not is_fr else "language-flag",
            "fr_aria_current": ' aria-current="page"' if is_fr else "",
            "en_aria_current": ' aria-current="page"' if not is_fr else "",
            **locale,
        },
    )


def render_footer(
    locale: dict[str, str],
    *,
    logo_path: str,
    footer_links: list[tuple[str, str]],
) -> str:
    return render(
        read_text(SRC / "partials" / "footer.html"),
        {
            "logo_path": logo_path,
            "footer_text": locale["footer_text"],
            "footer_copyright": locale["footer_copyright"],
            "footer_links": build_footer_links(footer_links),
        },
    )


def build_home_pages() -> None:
    base_template = read_text(SRC / "templates" / "base.html")
    home_template = read_text(SRC / "templates" / "home.html")
    gtm_head = read_text(SRC / "partials" / "gtm-head.html")
    gtm_body = read_text(SRC / "partials" / "gtm-body.html")
    configs = json.loads(read_text(SRC / "data" / "homepages.json"))
    locales = load_locales()

    for config in configs:
        is_fr = config["lang"] == "fr"
        locale = locales[config["lang"]]
        header = render_header(
            locale,
            logo_path="./logo-pinnacle.png",
            home_path="#top",
            about_href="#about",
            expertises_href="#expertises",
            approach_href="#approach",
            insights_href="#insights",
            contact_href="#contact",
            fr_href="./index.html",
            en_href="./index-en.html",
            is_fr=is_fr,
        )
        footer = render_footer(
            locale,
            logo_path="./logo-pinnacle.png",
            footer_links=[
                ("#about", locale["nav_about"]),
                ("#expertises", locale["nav_expertises"]),
                ("#insights", locale["nav_insights"]),
                ("#contact", locale["nav_contact"]),
            ],
        )

        html_output = render(
            base_template,
            {
                **get_root_page_context(config),
                "header": header,
                "main": render(home_template, {"home_sections": read_text(ROOT / config["content_path"]).strip()}),
                "footer": footer,
                "page_scripts": config["page_scripts"],
                "partial:gtm-head": gtm_head,
                "partial:gtm-body": gtm_body,
            },
        )

        (DIST / config["output"]).write_text(html_output, encoding="utf-8", newline="\n")


def build_internal_family(data_file_name: str) -> None:
    base_template = read_text(SRC / "templates" / "base.html")
    page_template = read_text(SRC / "templates" / "page.html")
    gtm_head = read_text(SRC / "partials" / "gtm-head.html")
    gtm_body = read_text(SRC / "partials" / "gtm-body.html")
    items = json.loads(read_text(SRC / "data" / data_file_name))
    locales = load_locales()

    for item in items:
        lang = item["lang"]
        is_fr = lang == "fr"
        locale = locales[lang]
        home_path = "../../index.html" if is_fr else "../../index-en.html"
        page_scripts = (
            '<button class="scroll-top-button" type="button" aria-label="Revenir en haut de la page">↑</button>\n<script src="../../js/page-enhancements.js"></script>'
            if is_fr
            else '<button class="scroll-top-button" type="button" aria-label="Back to top">↑</button>\n<script src="../../js/page-enhancements.js"></script>'
        )

        header = render_header(
            locale,
            logo_path="../../logo-pinnacle.png",
            home_path=home_path,
            about_href=f"{home_path}#about",
            expertises_href=f"{home_path}#expertises",
            approach_href=f"{home_path}#approach",
            insights_href=f"{home_path}#insights",
            contact_href=f"{home_path}#contact",
            fr_href=item["fr_href"],
            en_href=item["en_href"],
            is_fr=is_fr,
        )
        footer = render_footer(
            locale,
            logo_path="../../logo-pinnacle.png",
            footer_links=[
                (f"{home_path}#expertises", locale["nav_expertises"]),
                (f"{home_path}#approach", locale["nav_approach"]),
                (f"{home_path}#insights", locale["nav_insights"]),
                (f"{home_path}#contact", locale["nav_contact"]),
            ],
        )

        html_output = render(
            base_template,
            {
                **get_root_page_context(
                    {
                        **item,
                        "stylesheet_path": "../../styles.css",
                        "page_shell_class": item.get("page_shell_class", "page-shell"),
                    }
                ),
                "header": header,
                "main": render(
                    page_template,
                    {"page_content": read_text(ROOT / item["content_path"]).strip()},
                ),
                "footer": footer,
                "page_scripts": page_scripts,
                "partial:gtm-head": gtm_head,
                "partial:gtm-body": gtm_body,
            },
        )

        output_path = DIST / item["output_path"]
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html_output, encoding="utf-8", newline="\n")


def main() -> None:
    copy_assets()
    build_home_pages()
    build_internal_family("insights.json")
    build_internal_family("expertise.json")
    build_internal_family("perspective.json")
    print(f"frontend-v2 dist generated in {DIST}")


if __name__ == "__main__":
    main()
