"""Test script for CLI template management commands.

This validates that the template management CLI commands work correctly.

Author: Project Wizard Team
Created: 2025-11-28
"""

import subprocess
import sys


def run_command(cmd):
    """Run a CLI command and return result."""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr


def test_templates_help():
    """Test that templates command shows help."""
    returncode, stdout, stderr = run_command("project-wizard templates --help")
    assert returncode == 0, f"Command failed: {stderr}"
    assert "Manage document templates" in stdout
    assert "list" in stdout
    assert "show" in stdout
    assert "validate" in stdout
    print("✓ templates --help works")


def test_templates_list():
    """Test listing templates."""
    returncode, stdout, stderr = run_command("project-wizard templates list")
    assert returncode == 0, f"Command failed: {stderr}"
    assert "project_charter" in stdout
    assert "work_plan" in stdout
    assert "proposal" in stdout
    print("✓ templates list works")


def test_templates_list_verbose():
    """Test listing templates with verbose output."""
    returncode, stdout, stderr = run_command("project-wizard templates list -v")
    assert returncode == 0, f"Command failed: {stderr}"
    assert "v1.0.0" in stdout
    assert "Inputs:" in stdout
    assert "Sections:" in stdout
    assert "verification, rubric" in stdout
    print("✓ templates list -v works")


def test_templates_show():
    """Test showing template details."""
    returncode, stdout, stderr = run_command("project-wizard templates show project_charter")
    assert returncode == 0, f"Command failed: {stderr}"
    assert "Template: project_charter" in stdout
    assert "Inputs (" in stdout
    assert "Sections (" in stdout
    assert "Verification Questions" in stdout
    assert "Quality Rubric" in stdout
    print("✓ templates show project_charter works")


def test_templates_validate_all():
    """Test validating all templates."""
    returncode, stdout, stderr = run_command("project-wizard templates validate --all")
    assert returncode == 0, f"Command failed: {stderr}"
    assert "project_charter" in stdout
    assert "work_plan" in stdout
    assert "proposal" in stdout
    assert "All templates are valid" in stdout
    print("+ templates validate --all works")


def test_templates_validate_single():
    """Test validating a single template."""
    returncode, stdout, stderr = run_command("project-wizard templates validate proposal")
    assert returncode == 0, f"Command failed: {stderr}"
    assert "Blueprint JSON is valid" in stdout
    assert "Template file exists" in stdout
    assert "Template contains Jinja2 syntax" in stdout
    print("✓ templates validate proposal works")


def test_main_cli_still_works():
    """Test that main CLI commands are not broken."""
    returncode, stdout, stderr = run_command("project-wizard --help")
    assert returncode == 0, f"Command failed: {stderr}"
    assert "init" in stdout
    assert "plan" in stdout
    assert "status" in stdout
    assert "templates" in stdout
    print("✓ main CLI still works")


if __name__ == "__main__":
    print("=" * 60)
    print("TESTING CLI TEMPLATE COMMANDS")
    print("=" * 60)
    print()
    
    tests = [
        test_templates_help,
        test_templates_list,
        test_templates_list_verbose,
        test_templates_show,
        test_templates_validate_all,
        test_templates_validate_single,
        test_main_cli_still_works,
    ]
    
    failed = 0
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    if failed == 0:
        print("✅ ALL TESTS PASSED")
    else:
        print(f"❌ {failed} TESTS FAILED")
    print("=" * 60)
    
    sys.exit(1 if failed > 0 else 0)
