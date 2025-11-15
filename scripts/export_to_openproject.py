#!/usr/bin/env python3
"""
OpenProject Export Utility

Parses ISSUES.md (work plan) and exports to OpenProject via API.
Creates project structure with phases (parent work packages), tasks (child work packages), and milestones.

Usage:
    python scripts/export_to_openproject.py ISSUES.md --api-key YOUR_API_KEY --url http://10.69.1.86:8080
    
Or use environment variables:
    export OPENPROJECT_API_KEY="your_key"
    export OPENPROJECT_URL="http://10.69.1.86:8080"
    python scripts/export_to_openproject.py ISSUES.md
"""

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Optional
import requests


class OpenProjectExporter:
    """Export work plan to OpenProject via API"""
    
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        })
    
    def parse_issues_md(self, filepath: str) -> Dict:
        """Parse ISSUES.md and extract project structure"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        project_data = {
            'name': self._extract_project_name(content),
            'identifier': self._generate_identifier(),
            'description': '',
            'phases': [],
            'milestones': []
        }
        
        # Extract project metadata
        project_data.update(self._extract_project_metadata(content))
        
        # Extract phases and tasks
        project_data['phases'] = self._extract_phases(content)
        
        # Extract milestones
        project_data['milestones'] = self._extract_milestones(content)
        
        return project_data
    
    def _extract_project_name(self, content: str) -> str:
        """Extract project name from document"""
        match = re.search(r'\*\*Project:\*\*\s+(.+)', content)
        if match:
            return match.group(1).strip()
        
        # Fallback to first heading
        match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        
        return "Untitled Project"
    
    def _generate_identifier(self) -> str:
        """Generate project identifier"""
        # You might want to make this more sophisticated
        import random
        return f"project-{random.randint(1000, 9999)}"
    
    def _extract_project_metadata(self, content: str) -> Dict:
        """Extract start date, due date, priority from project structure table"""
        metadata = {}
        
        # Look for Project Structure section
        structure_section = re.search(
            r'##\s+🧭\s+Project Structure.*?\n(.*?)(?=\n##|\Z)',
            content,
            re.DOTALL
        )
        
        if structure_section:
            section_text = structure_section.group(1)
            
            # Extract dates
            start_match = re.search(r'\*\*Start Date\*\*.*?(\d{4}-\d{2}-\d{2})', section_text)
            if start_match:
                metadata['startDate'] = start_match.group(1)
            
            due_match = re.search(r'\*\*Due Date\*\*.*?(\d{4}-\d{2}-\d{2})', section_text)
            if due_match:
                metadata['dueDate'] = due_match.group(1)
            
            # Extract priority
            priority_match = re.search(r'\*\*Priority\*\*.*?(\w+)', section_text)
            if priority_match:
                metadata['priority'] = priority_match.group(1)
        
        return metadata
    
    def _extract_phases(self, content: str) -> List[Dict]:
        """Extract phases and their tasks from Work Packages section"""
        phases = []
        
        # Find the Work Packages section
        wp_section = re.search(
            r'##\s+📋\s+Work Packages.*?\n(.*?)(?=\n##|\Z)',
            content,
            re.DOTALL
        )
        
        if not wp_section:
            return phases
        
        section_text = wp_section.group(1)
        
        # Find all phase sections (### Phase N: Name)
        phase_pattern = r'###\s+Phase\s+\d+:\s+(.+?)\n(.*?)(?=###\s+Phase|\Z)'
        phase_matches = re.finditer(phase_pattern, section_text, re.DOTALL)
        
        for match in phase_matches:
            phase_name = match.group(1).strip()
            phase_content = match.group(2)
            
            # Extract phase description (text before the table)
            desc_match = re.search(r'^(.+?)(?=\|)', phase_content, re.DOTALL)
            description = desc_match.group(1).strip() if desc_match else ''
            
            # Extract tasks from markdown table
            tasks = self._extract_tasks_from_table(phase_content)
            
            phases.append({
                'name': phase_name,
                'description': description,
                'tasks': tasks
            })
        
        return phases
    
    def _extract_tasks_from_table(self, table_text: str) -> List[Dict]:
        """Extract tasks from markdown table"""
        tasks = []
        
        # Find table rows (skip header and separator)
        lines = table_text.split('\n')
        in_table = False
        
        for line in lines:
            if line.strip().startswith('|') and '---' not in line:
                if not in_table:
                    in_table = True
                    continue  # Skip header row
                
                # Parse table row
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                if len(cells) >= 5:
                    tasks.append({
                        'subject': cells[0],
                        'description': cells[1],
                        'assignee': cells[2],
                        'duration': cells[3],
                        'dependency': cells[4]
                    })
        
        return tasks
    
    def _extract_milestones(self, content: str) -> List[Dict]:
        """Extract milestones from Milestones section"""
        milestones = []
        
        # Find Milestones section
        ms_section = re.search(
            r'##\s+📈\s+Milestones.*?\n(.*?)(?=\n##|\Z)',
            content,
            re.DOTALL
        )
        
        if not ms_section:
            return milestones
        
        section_text = ms_section.group(1)
        
        # Extract from table
        lines = section_text.split('\n')
        in_table = False
        
        for line in lines:
            if line.strip().startswith('|') and '---' not in line:
                if not in_table:
                    in_table = True
                    continue  # Skip header
                
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                if len(cells) >= 3:
                    milestones.append({
                        'subject': cells[0],
                        'date': cells[1],
                        'description': cells[2]
                    })
        
        return milestones
    
    def create_project(self, project_data: Dict) -> Optional[str]:
        """Create project in OpenProject"""
        payload = {
            '_type': 'Project',
            'name': project_data['name'],
            'identifier': project_data['identifier'],
            'description': {
                'format': 'markdown',
                'raw': project_data.get('description', '')
            },
            'public': False
        }
        
        if 'startDate' in project_data:
            payload['startDate'] = project_data['startDate']
        if 'dueDate' in project_data:
            payload['dueDate'] = project_data['dueDate']
        
        try:
            response = self.session.post(
                f'{self.api_url}/api/v3/projects',
                json=payload
            )
            response.raise_for_status()
            project_id = response.json()['id']
            print(f"✓ Created project: {project_data['name']} (ID: {project_id})")
            return project_id
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to create project: {e}")
            if hasattr(e.response, 'text'):
                print(f"  Response: {e.response.text}")
            return None
    
    def create_work_packages(self, project_id: str, project_data: Dict):
        """Create work packages (phases and tasks) in OpenProject"""
        
        for phase in project_data['phases']:
            # Create parent work package for phase
            phase_id = self._create_phase_work_package(project_id, phase)
            
            if phase_id:
                # Create child work packages for tasks
                for task in phase['tasks']:
                    self._create_task_work_package(project_id, phase_id, task)
        
        # Create milestones
        for milestone in project_data['milestones']:
            self._create_milestone(project_id, milestone)
    
    def _create_phase_work_package(self, project_id: str, phase: Dict) -> Optional[str]:
        """Create a phase as a parent work package"""
        payload = {
            '_type': 'WorkPackage',
            'subject': phase['name'],
            'description': {
                'format': 'markdown',
                'raw': phase.get('description', '')
            },
            '_links': {
                'project': {'href': f'/api/v3/projects/{project_id}'},
                'type': {'href': '/api/v3/types/1'}  # Default type
            }
        }
        
        try:
            response = self.session.post(
                f'{self.api_url}/api/v3/work_packages',
                json=payload
            )
            response.raise_for_status()
            phase_id = response.json()['id']
            print(f"  ✓ Created phase: {phase['name']}")
            return phase_id
        except requests.exceptions.RequestException as e:
            print(f"  ✗ Failed to create phase {phase['name']}: {e}")
            return None
    
    def _create_task_work_package(self, project_id: str, parent_id: str, task: Dict):
        """Create a task as a child work package"""
        payload = {
            '_type': 'WorkPackage',
            'subject': task['subject'],
            'description': {
                'format': 'markdown',
                'raw': task.get('description', '')
            },
            '_links': {
                'project': {'href': f'/api/v3/projects/{project_id}'},
                'type': {'href': '/api/v3/types/1'},
                'parent': {'href': f'/api/v3/work_packages/{parent_id}'}
            }
        }
        
        # TODO: Handle duration, assignee, dependencies
        # These require additional API calls to get user IDs, parse durations, etc.
        
        try:
            response = self.session.post(
                f'{self.api_url}/api/v3/work_packages',
                json=payload
            )
            response.raise_for_status()
            print(f"    ✓ Created task: {task['subject']}")
        except requests.exceptions.RequestException as e:
            print(f"    ✗ Failed to create task {task['subject']}: {e}")
    
    def _create_milestone(self, project_id: str, milestone: Dict):
        """Create a milestone work package"""
        payload = {
            '_type': 'WorkPackage',
            'subject': milestone['subject'],
            'description': {
                'format': 'markdown',
                'raw': milestone.get('description', '')
            },
            '_links': {
                'project': {'href': f'/api/v3/projects/{project_id}'},
                'type': {'href': '/api/v3/types/2'}  # Milestone type (usually ID 2)
            }
        }
        
        if milestone.get('date'):
            payload['date'] = milestone['date']
        
        try:
            response = self.session.post(
                f'{self.api_url}/api/v3/work_packages',
                json=payload
            )
            response.raise_for_status()
            print(f"  ✓ Created milestone: {milestone['subject']}")
        except requests.exceptions.RequestException as e:
            print(f"  ✗ Failed to create milestone {milestone['subject']}: {e}")
    
    def export(self, issues_filepath: str):
        """Main export workflow"""
        print(f"Parsing {issues_filepath}...")
        project_data = self.parse_issues_md(issues_filepath)
        
        print(f"\nCreating project in OpenProject...")
        project_id = self.create_project(project_data)
        
        if not project_id:
            print("\n✗ Export failed: Could not create project")
            return False
        
        print(f"\nCreating work packages...")
        self.create_work_packages(project_id, project_data)
        
        print(f"\n✓ Export complete! View project at: {self.api_url}/projects/{project_data['identifier']}")
        return True


def main():
    parser = argparse.ArgumentParser(description='Export ISSUES.md to OpenProject')
    parser.add_argument('issues_file', help='Path to ISSUES.md file')
    parser.add_argument('--url', help='OpenProject URL (default: env OPENPROJECT_URL)')
    parser.add_argument('--api-key', help='OpenProject API key (default: env OPENPROJECT_API_KEY)')
    
    args = parser.parse_args()
    
    # Get configuration
    api_url = args.url or os.getenv('OPENPROJECT_URL', 'http://10.69.1.86:8080')
    api_key = args.api_key or os.getenv('OPENPROJECT_API_KEY')
    
    if not api_key:
        print("Error: OpenProject API key required. Set OPENPROJECT_API_KEY env var or use --api-key")
        sys.exit(1)
    
    if not os.path.exists(args.issues_file):
        print(f"Error: File not found: {args.issues_file}")
        sys.exit(1)
    
    # Export
    exporter = OpenProjectExporter(api_url, api_key)
    success = exporter.export(args.issues_file)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
