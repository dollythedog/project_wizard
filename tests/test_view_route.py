"""Debug script to test view_document route."""

from app.services.database import get_db_session
from app.models.database import DocumentRun, Project

session = next(get_db_session())

# Test with document ID 6
doc_id = 6
print(f"\n=== Testing view_document logic for doc_id={doc_id} ===\n")

document_run = session.get(DocumentRun, doc_id)
print(f"1. DocumentRun found: {document_run is not None}")
if document_run:
    print(f"   - ID: {document_run.id}")
    print(f"   - Project ID: {document_run.project_id}")
    print(f"   - Template: {document_run.template_name}")
    print(f"   - Status: {document_run.status}")
    print(f"   - Has initial_draft: {document_run.initial_draft is not None}")
    print(f"   - Draft length: {len(document_run.initial_draft) if document_run.initial_draft else 0}")

project = session.get(Project, document_run.project_id)
print(f"\n2. Project found: {project is not None}")
if project:
    print(f"   - ID: {project.id}")
    print(f"   - Title: {project.title}")
    print(f"   - Type: {project.project_type}")

# Test template rendering context
print(f"\n3. Template context would be:")
context = {
    "project": project,
    "template_name": document_run.template_name,
    "draft_content": document_run.initial_draft[:100] + "..." if document_run.initial_draft else None,
    "model_used": "Previously Generated",
    "tokens_used": 0,
    "step_back_summary": document_run.step_back_summary[:100] + "..." if document_run.step_back_summary else None,
    "document_run_id": document_run.id
}

for key, value in context.items():
    if key == "project":
        print(f"   - {key}: Project(id={value.id}, title={value.title})")
    else:
        print(f"   - {key}: {value}")

print("\n=== Test complete - no errors ===\n")
