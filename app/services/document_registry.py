"""
Document Registry - Tracks documents within a project
"""

import json
from datetime import datetime
from pathlib import Path


class DocumentRegistry:
    """Manages document metadata and tracking within a project"""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.registry_file = project_path / ".project_metadata.json"
        self._load_registry()

    def _load_registry(self):
        """Load document registry from disk"""
        if self.registry_file.exists():
            try:
                data = json.loads(self.registry_file.read_text())
                self.documents = data.get("documents", {})
                self.project_version = data.get("version", "0.1.0")
            except:
                self.documents = {}
                self.project_version = "0.1.0"
        else:
            self.documents = {}
            self.project_version = "0.1.0"

    def _save_registry(self):
        """Save document registry to disk"""
        data = {
            "version": self.project_version,
            "last_updated": datetime.now().isoformat(),
            "documents": self.documents,
        }
        self.registry_file.write_text(json.dumps(data, indent=2))

    def register_document(
        self, doc_name: str, doc_type: str = "deliverable", version: str = "1.0.0"
    ) -> dict:
        """Register a new document"""
        doc_data = {
            "name": doc_name,
            "type": doc_type,  # "core", "charter", "deliverable"
            "version": version,
            "created_date": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat(),
            "word_count": 0,
            "critique_score": None,
            "status": "draft",  # draft, in_progress, complete
        }

        self.documents[doc_name] = doc_data
        self._save_registry()

        return doc_data

    def update_document(self, doc_name: str, **kwargs):
        """Update document metadata"""
        if doc_name in self.documents:
            self.documents[doc_name].update(kwargs)
            self.documents[doc_name]["last_modified"] = datetime.now().isoformat()
            self._save_registry()

    def set_word_count(self, doc_name: str, word_count: int):
        """Update document word count"""
        self.update_document(doc_name, word_count=word_count)

    def set_critique_score(self, doc_name: str, score: float):
        """Update document critique score (0-100)"""
        self.update_document(doc_name, critique_score=score)

    def set_version(self, doc_name: str, version: str):
        """Update document version"""
        self.update_document(doc_name, version=version)

    def get_document(self, doc_name: str) -> dict | None:
        """Get document metadata"""
        return self.documents.get(doc_name)

    def document_exists(self, doc_name: str) -> bool:
        """Check if document is registered"""
        return doc_name in self.documents

    def list_documents(self, doc_type: str | None = None, status: str | None = None) -> list[dict]:
        """List all documents, optionally filtered by type or status"""
        docs = list(self.documents.values())

        if doc_type:
            docs = [d for d in docs if d.get("type") == doc_type]

        if status:
            docs = [d for d in docs if d.get("status") == status]

        # Sort by last modified (most recent first)
        docs.sort(key=lambda x: x.get("last_modified", ""), reverse=True)

        return docs

    def get_project_version(self) -> str:
        """Get current project version"""
        return self.project_version

    def set_project_version(self, version: str):
        """Update project version"""
        self.project_version = version
        self._save_registry()

    def get_document_count(self, doc_type: str | None = None) -> int:
        """Get count of documents, optionally filtered by type"""
        if doc_type:
            return len([d for d in self.documents.values() if d.get("type") == doc_type])
        return len(self.documents)

    def remove_document(self, doc_name: str):
        """Remove document from registry (doesn't delete file)"""
        if doc_name in self.documents:
            del self.documents[doc_name]
            self._save_registry()

    def get_stats(self) -> dict:
        """Get project statistics"""
        docs = list(self.documents.values())

        total_words = sum(d.get("word_count", 0) for d in docs)
        avg_score = None

        scores = [d.get("critique_score") for d in docs if d.get("critique_score") is not None]
        if scores:
            avg_score = sum(scores) / len(scores)

        return {
            "total_documents": len(docs),
            "core_docs": len([d for d in docs if d.get("type") == "core"]),
            "deliverables": len([d for d in docs if d.get("type") == "deliverable"]),
            "total_words": total_words,
            "average_critique_score": avg_score,
            "project_version": self.project_version,
        }
