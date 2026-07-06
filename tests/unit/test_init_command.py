from argparse import Namespace

from travel_film_maker_cli.commands.init import handle


def test_init_creates_external_project_structure(tmp_path):
    project_dir = tmp_path / "Europe2026"

    exit_code = handle(Namespace(directory=project_dir, title="Europe 2026", id=None, timezone="UTC"))

    assert exit_code == 0
    assert (project_dir / "project.yaml").exists()
    assert (project_dir / "style.yaml").exists()
    assert (project_dir / "assets").is_dir()
    assert (project_dir / "gps").is_dir()
    assert (project_dir / "music").is_dir()
    assert (project_dir / "output").is_dir()

    gitignore = (project_dir / ".gitignore").read_text(encoding="utf-8")
    assert "assets/" in gitignore
    assert "output/" in gitignore
    assert "CacheClip/" in gitignore
    assert "earth-studio-cache/" in gitignore
