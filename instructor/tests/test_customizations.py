import ast
from pathlib import Path
import re

import pytest

from scripts.export_materials import ROOT, STAGES, export_stage

CUSTOMIZATIONS = (
    "AGENTS.md",
    ".github/copilot-instructions.md",
    ".github/agents/postal-reviewer.agent.md",
    ".github/agents/postal-rpa-diagnostician.agent.md",
    ".github/instructions/tests.instructions.md",
    ".github/skills/postal-test-design/SKILL.md",
    ".github/skills/postal-test-design/test-matrix.md",
    ".github/skills/postal-rpa-diagnosis/SKILL.md",
    ".github/skills/postal-rpa-diagnosis/evidence-template.md",
    ".github/prompts/postal-review.prompt.md",
    ".github/prompts/postal-test-plan.prompt.md",
    ".github/prompts/postal-rpa.prompt.md",
    "docs/optional-customization.md",
)


def header_field(path: Path, field: str) -> str:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), path
    header = text.split("---", 2)[1]
    match = re.search(rf"^{re.escape(field)}: (.+)$", header, re.MULTILINE)
    assert match, f"{path}: missing {field}"
    return match.group(1)


@pytest.mark.parametrize("stage", STAGES)
def test_all_packages_include_customizations_without_instructor_files(tmp_path, stage):
    destination = tmp_path / stage
    export_stage(stage, destination)
    for relative in CUSTOMIZATIONS:
        assert (destination / relative).read_bytes() == (ROOT / relative).read_bytes()
    assert not (destination / "instructor").exists()
    assert not (destination / ".github" / "workflows").exists()
    assert not (destination / "scripts" / "export_materials.py").exists()
    for relative in CUSTOMIZATIONS:
        if relative.startswith("docs/"):
            continue
        path = destination / relative
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if not target.startswith(("https://", "http://", "#")):
                assert (path.parent / target.split("#")[0]).is_file(), (relative, target)


def test_agents_are_manual_read_only_roles():
    agents = list((ROOT / ".github" / "agents").glob("*.agent.md"))
    assert len(agents) == 2
    for path in agents:
        assert header_field(path, "name") == path.name.removesuffix(".agent.md")
        assert header_field(path, "description")
        assert header_field(path, "target") == "vscode"
        assert header_field(path, "disable-model-invocation") == "true"
        assert ast.literal_eval(header_field(path, "tools")) == ["read", "search"]
        assert not re.search(r"^model:", path.read_text(encoding="utf-8"), re.MULTILINE)


def test_skills_and_prompts_have_distinct_names_and_valid_references():
    skills = list((ROOT / ".github" / "skills").glob("*/SKILL.md"))
    prompts = list((ROOT / ".github" / "prompts").glob("*.prompt.md"))
    assert len(skills) == 2
    assert len(prompts) == 3
    names = []
    for path in skills:
        name = header_field(path, "name")
        assert name == path.parent.name
        assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)
        assert len(name) <= 64
        assert 0 < len(header_field(path, "description")) <= 1024
        assert header_field(path, "disable-model-invocation") == "true"
        names.append(name)
    agent_names = {
        header_field(path, "name")
        for path in (ROOT / ".github" / "agents").glob("*.agent.md")
    }
    for path in prompts:
        name = header_field(path, "name")
        assert name == path.name.removesuffix(".prompt.md")
        assert header_field(path, "agent") in agent_names | {"ask"}
        assert header_field(path, "description")
        assert not re.search(r"^(tools|model):", path.read_text(encoding="utf-8"), re.MULTILINE)
        names.append(name)
    assert len(names) == len(set(names))


def test_timing_is_only_on_main_lab_headings():
    for relative in ("README.md", "docs/labs.md", "instructor/guide.md"):
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert not re.search(r"^### .*(分鐘|\d{2}:\d{2})", text, re.MULTILINE)
        for number, duration in ((1, 45), (2, 15), (3, 18)):
            assert re.search(rf"^## Lab {number}.*（{duration} 分鐘）$", text, re.MULTILINE)
    instructions = ROOT / ".github" / "instructions" / "tests.instructions.md"
    assert header_field(instructions, "applyTo") == '"tests/**/*.py"'
