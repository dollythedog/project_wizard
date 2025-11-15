"""
OpenProject Exporter Service
Exports WORK_PLAN.md to OpenProject via REST API
"""
import os
import re
import base64
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Task:
    """Represents a task from the work plan"""
    task_id: str
    description: str
    responsible: str
    duration: str
    dependency: str
    phase_name: str


class OpenProjectExporter:
    """Exports work plan tasks to OpenProject"""
    
    def __init__(self, base_url: str, api_key: str):
        """
        Initialize the OpenProject exporter.
        
        Args:
            base_url: OpenProject instance URL (e.g., http://10.69.1.86:8080)
            api_key: OpenProject API key
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        # OpenProject uses Basic auth with apikey:{API_KEY} base64 encoded
        credentials = f'apikey:{api_key}'
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def parse_project_start_date(self, work_plan_path: str):
        """Parse PROJECT_CHARTER.md to get project start date."""
        from pathlib import Path
        charter_path = Path(work_plan_path).parent / "PROJECT_CHARTER.md"
        
        if not charter_path.exists():
            print(f"⚠️  PROJECT_CHARTER.md not found, using today's date")
            return datetime.now().date()
        
        try:
            with open(charter_path, 'r', encoding='utf-8') as f:
                charter_content = f.read()
            
            timeline_match = re.search(
                r'\*\*Timeline:\*\*\s+(\w+\s+\d+,\s+\d{4})\s+to',
                charter_content
            )
            
            if timeline_match:
                date_str = timeline_match.group(1)
                start_date = datetime.strptime(date_str, '%B %d, %Y').date()
                print(f"📅 Using project start date from charter: {start_date}")
                return start_date
            else:
                print(f"⚠️  Start date not found in charter, using today's date")
                return datetime.now().date()
                
        except Exception as e:
            print(f"⚠️  Error parsing charter: {e}, using today's date")
            return datetime.now().date()

    def parse_work_plan(self, file_path: str) -> Tuple[Dict, List[Task]]:
        """
        Parse WORK_PLAN.md and extract project info and tasks.
        
        Args:
            file_path: Path to WORK_PLAN.md
            
        Returns:
            Tuple of (project_info dict, list of Task objects)
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract project metadata
        project_info = {}
        
        # Extract project name
        name_match = re.search(r'\*\*Project Name\*\*:\s*(.+)', content)
        if name_match:
            project_info['name'] = name_match.group(1).strip()
        
        # Extract project type
        type_match = re.search(r'\*\*Project Type\*\*:\s*(.+)', content)
        if type_match:
            project_info['type'] = type_match.group(1).strip()
        
        # Extract dates
        start_match = re.search(r'\*\*Start Date\*\*:\s*(.+)', content)
        if start_match:
            project_info['start_date'] = start_match.group(1).strip()
        
        end_match = re.search(r'\*\*End Date\*\*:\s*(.+)', content)
        if end_match:
            project_info['end_date'] = end_match.group(1).strip()
        
        # Extract phases and tasks
        tasks = []
        phase_pattern = r'### (Phase \d+: .+?)\n\*\*Objective\*\*: (.+?)\n\n\| Task \|'
        task_row_pattern = r'\| ([\d.]+) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|'
        
        phases = re.finditer(phase_pattern, content)
        
        for phase_match in phases:
            phase_name = phase_match.group(1).strip()
            phase_objective = phase_match.group(2).strip()
            
            # Find the table after this phase header
            phase_start = phase_match.end()
            next_phase = re.search(r'### Phase', content[phase_start:])
            phase_end = phase_start + next_phase.start() if next_phase else len(content)
            phase_content = content[phase_start:phase_end]
            
            # Extract tasks from the table
            task_rows = re.finditer(task_row_pattern, phase_content)
            for task_match in task_rows:
                task = Task(
                    task_id=task_match.group(1).strip(),
                    description=task_match.group(2).strip(),
                    responsible=task_match.group(3).strip(),
                    duration=task_match.group(4).strip(),
                    dependency=task_match.group(5).strip(),
                    phase_name=phase_name
                )
                tasks.append(task)
        
        return project_info, tasks
    
    def get_or_create_project(self, project_name: str) -> Optional[int]:
        """
        Get existing project by name or create new one.
        
        Args:
            project_name: Name of the project
            
        Returns:
            Project ID or None if failed
        """
        # Search for existing project
        response = self.session.get(
            f'{self.base_url}/api/v3/projects',
            params={'filters': f'[{{"name":{{"operator":"~","values":["{project_name}"]}}}}]'}
        )
        
        if response.status_code == 200:
            projects = response.json().get('_embedded', {}).get('elements', [])
            if projects:
                project_id = projects[0]['id']
                print(f"✓ Found existing project: {project_name} (ID: {project_id})")
                return project_id
        
        # Create new project
        project_data = {
            'name': project_name,
            'identifier': re.sub(r'[^a-z0-9-]', '-', project_name.lower())[:100],
            'description': {
                'format': 'markdown',
                'raw': f'Project imported from WORK_PLAN.md on {datetime.now().strftime("%Y-%m-%d")}'
            }
        }
        
        response = self.session.post(
            f'{self.base_url}/api/v3/projects',
            json=project_data
        )
        
        if response.status_code == 201:
            project_id = response.json()['id']
            print(f"✓ Created new project: {project_name} (ID: {project_id})")
            return project_id
        else:
            print(f"✗ Failed to create project: {response.status_code}")
            print(f"  Response: {response.text}")
            return None
    
    def get_work_package_type_id(self, project_id: int, type_name: str = 'Task') -> Optional[int]:
        """
        Get work package type ID by name.
        
        Args:
            project_id: OpenProject project ID
            type_name: Type name ('Phase', 'Milestone', 'Task', etc.)
            
        Returns:
            Type ID or None if not found
        """
        response = self.session.get(f'{self.base_url}/api/v3/projects/{project_id}')
        
        if response.status_code == 200:
            # Get available types for this project
            types_url = response.json().get('_links', {}).get('types', {}).get('href')
            if types_url:
                types_response = self.session.get(f'{self.base_url}{types_url}')
                if types_response.status_code == 200:
                    types = types_response.json().get('_embedded', {}).get('elements', [])
                    # Find the requested type
                    for t in types:
                        if t['name'].lower() == type_name.lower():
                            return t['id']
                    # Fallback: try 'Task' if requested type not found
                    if type_name.lower() != 'task':
                        for t in types:
                            if t['name'].lower() == 'task':
                                return t['id']
                    # Last resort: use first available
                    if types:
                        return types[0]['id']
        return None
    
    def create_work_package(self, project_id: int, task: Task, 
                          type_id: int, parent_id: Optional[int] = None,
                          start_date = None, finish_date = None) -> Optional[int]:
        """
        Create a work package in OpenProject.
        
        Args:
            project_id: OpenProject project ID
            task: Task object with task details
            type_id: Work package type ID
            parent_id: Parent work package ID (for subtasks)
            
        Returns:
            Work package ID or None if failed
        """
        # Parse duration to estimate effort
        duration_match = re.search(r'(\d+)\s*days?', task.duration, re.IGNORECASE)
        estimated_hours = int(duration_match.group(1)) * 8 if duration_match else None
        
        work_package_data = {
            'subject': f"{task.task_id}: {task.description}" if task.task_id else task.description,
            'description': {
                'format': 'markdown',
                'raw': f"**Responsible:** {task.responsible}\n"
                       f"**Duration:** {task.duration}\n"
                       f"**Dependency:** {task.dependency}\n"
                       f"**Phase:** {task.phase_name}"
            },
            '_links': {
                'type': {'href': f'/api/v3/types/{type_id}'},
                'project': {'href': f'/api/v3/projects/{project_id}'}
            }
        }
        
        if start_date:
            work_package_data['startDate'] = start_date.isoformat()
        if finish_date:
            work_package_data['dueDate'] = finish_date.isoformat()
        
        if estimated_hours:
            work_package_data['estimatedTime'] = f'PT{estimated_hours}H'
        
        if parent_id:
            work_package_data['_links']['parent'] = {'href': f'/api/v3/work_packages/{parent_id}'}
        
        response = self.session.post(
            f'{self.base_url}/api/v3/work_packages',
            json=work_package_data
        )
        
        if response.status_code == 201:
            wp_id = response.json()['id']
            print(f"  ✓ Created: {task.task_id} - {task.description[:50]}")
            return wp_id
        else:
            print(f"  ✗ Failed to create {task.task_id}: {response.status_code}")
            print(f"    Response: {response.text}")
            return None
    
    def export_work_plan(self, work_plan_path: str) -> bool:
        """
        Main method to export work plan to OpenProject.
        
        Args:
            work_plan_path: Path to WORK_PLAN.md file
            
        Returns:
            True if successful, False otherwise
        """
        print(f"\n📋 Parsing work plan: {work_plan_path}")
        project_info, tasks = self.parse_work_plan(work_plan_path)
        
        if not tasks:
            print("✗ No tasks found in work plan")
            return False
        
        print(f"✓ Found {len(tasks)} tasks across phases")
        
        # Get or create project
        print(f"\n🔧 Setting up OpenProject project...")
        project_id = self.get_or_create_project(project_info.get('name', 'Imported Project'))
        
        if not project_id:
            print("✗ Failed to get/create project")
            return False
        
        # Get work package type
        # Get work package type IDs
        phase_type_id = self.get_work_package_type_id(project_id, 'Phase')
        task_type_id = self.get_work_package_type_id(project_id, 'Task')
        
        if not phase_type_id or not task_type_id:
            print("✗ Failed to get work package types")
            return False
        
        # Get project start date from PROJECT_CHARTER.md
        project_start = self.parse_project_start_date(work_plan_path)
        current_date = project_start
        # Create work packages for each task with dates
        print(f"\n📦 Creating work packages...")
        print(f"  Using types: Phase (ID: {phase_type_id}), Task (ID: {task_type_id})")
        phase_parents = {}
        task_dates = {}
        
        for task in tasks:
            # Create phase parent if not exists
            if task.phase_name not in phase_parents:
                phase_task = Task(
                    task_id="",
                    description=task.phase_name,
                    responsible="",
                    duration="",
                    dependency="",
                    phase_name=task.phase_name
                )
                parent_id = self.create_work_package(project_id, phase_task, phase_type_id, None, None, None)
                if parent_id:
                    phase_parents[task.phase_name] = parent_id
            
            # Calculate dates based on dependencies
            start_date = current_date
            if task.dependency and task.dependency != "None":
                dep_id = task.dependency.strip()
                if dep_id in task_dates:
                    start_date = task_dates[dep_id]
            
            # Calculate duration
            duration_match = re.search(r'(\d+)\s*days?', task.duration, re.IGNORECASE)
            duration_days = int(duration_match.group(1)) if duration_match else 5
            finish_date = start_date + timedelta(days=duration_days)
            
            task_dates[task.task_id] = finish_date
            
            if not task.dependency or task.dependency == "None":
                current_date = finish_date
            
            # Create task with dates
            parent_id = phase_parents.get(task.phase_name)
            self.create_work_package(project_id, task, task_type_id, parent_id, start_date, finish_date)
        print(f"\n✅ Export complete! View at: {self.base_url}/projects/{project_id}/work_packages")
        return True


def main():
    """Main entry point for the exporter script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Export WORK_PLAN.md to OpenProject')
    parser.add_argument('work_plan', help='Path to WORK_PLAN.md file')
    parser.add_argument('--url', default='http://10.69.1.86:8080',
                       help='OpenProject URL (default: http://10.69.1.86:8080)')
    parser.add_argument('--api-key', help='OpenProject API key (or set OPENPROJECT_API_KEY env var)')
    
    args = parser.parse_args()
    
    # Get API key from args or environment
    api_key = args.api_key or os.getenv('OPENPROJECT_API_KEY')
    if not api_key:
        print("Error: API key required. Provide via --api-key or OPENPROJECT_API_KEY env var")
        return 1
    
    # Validate work plan file
    if not os.path.exists(args.work_plan):
        print(f"Error: Work plan file not found: {args.work_plan}")
        return 1
    
    # Export
    exporter = OpenProjectExporter(args.url, api_key)
    success = exporter.export_work_plan(args.work_plan)
    
    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
