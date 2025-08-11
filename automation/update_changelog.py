#!/usr/bin/env python3
"""
AUDITORIA360 - Automated Changelog Generator
Integrates with git history to maintain comprehensive changelog
"""

import os
import re
import subprocess
from datetime import datetime
from typing import List, Dict, Any
import json

class ChangelogGenerator:
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
        self.changelog_file = os.path.join(repo_path, "CHANGELOG.md")
        
    def get_git_commits_since_tag(self, tag: str = None) -> List[Dict[str, Any]]:
        """Get git commits since last tag"""
        
        if tag:
            cmd = f"git log {tag}..HEAD --pretty=format:'%H|%s|%an|%ad|%b' --date=iso"
        else:
            # Get commits since last tag
            try:
                last_tag = subprocess.check_output(
                    ["git", "describe", "--tags", "--abbrev=0"], 
                    cwd=self.repo_path
                ).decode().strip()
                cmd = f"git log {last_tag}..HEAD --pretty=format='%H|%s|%an|%ad|%b' --date=iso"
            except subprocess.CalledProcessError:
                # No tags found, get all commits
                cmd = "git log --pretty=format='%H|%s|%an|%ad|%b' --date=iso"
        
        try:
            result = subprocess.check_output(cmd, shell=True, cwd=self.repo_path)
            lines = result.decode().strip().split('\n')
            
            commits = []
            for line in lines:
                if '|' in line:
                    parts = line.split('|', 4)
                    if len(parts) >= 4:
                        commits.append({
                            'hash': parts[0],
                            'subject': parts[1],
                            'author': parts[2],
                            'date': parts[3],
                            'body': parts[4] if len(parts) > 4 else ''
                        })
            return commits
        except subprocess.CalledProcessError:
            return []
    
    def categorize_commit(self, commit: Dict[str, Any]) -> str:
        """Categorize commit based on conventional commits format"""
        
        subject = commit['subject'].lower()
        
        if subject.startswith('feat'):
            return 'features'
        elif subject.startswith('fix'):
            return 'fixes'
        elif subject.startswith('docs'):
            return 'documentation'
        elif subject.startswith('test'):
            return 'testing'
        elif subject.startswith('refactor'):
            return 'refactoring'
        elif subject.startswith('perf'):
            return 'performance'
        elif subject.startswith('ci'):
            return 'ci'
        elif subject.startswith('chore'):
            return 'maintenance'
        elif subject.startswith('style'):
            return 'style'
        elif subject.startswith('build'):
            return 'build'
        elif 'security' in subject:
            return 'security'
        elif 'breaking' in subject or 'major' in subject:
            return 'breaking'
        else:
            return 'other'
    
    def generate_version_section(self, version: str, commits: List[Dict[str, Any]]) -> str:
        """Generate changelog section for a version"""
        
        # Categorize commits
        categories = {
            'breaking': [],
            'security': [],
            'features': [],
            'fixes': [],
            'performance': [],
            'refactoring': [],
            'documentation': [],
            'testing': [],
            'ci': [],
            'build': [],
            'style': [],
            'maintenance': [],
            'other': []
        }
        
        for commit in commits:
            category = self.categorize_commit(commit)
            categories[category].append(commit)
        
        # Generate markdown
        date = datetime.now().strftime("%Y-%m-%d")
        section = f"\n## [{version}] - {date}\n\n"
        
        # Category mapping with emojis
        category_titles = {
            'breaking': '💥 Breaking Changes',
            'security': '🔒 Security',
            'features': '✨ New Features',
            'fixes': '🐛 Bug Fixes',
            'performance': '⚡ Performance',
            'refactoring': '♻️  Refactoring',
            'documentation': '📚 Documentation',
            'testing': '🧪 Testing',
            'ci': '👷 CI/CD',
            'build': '📦 Build',
            'style': '🎨 Style',
            'maintenance': '🔧 Maintenance',
            'other': '📝 Other'
        }
        
        for category, commits_in_category in categories.items():
            if commits_in_category:
                section += f"### {category_titles[category]}\n\n"
                for commit in commits_in_category:
                    # Format commit message
                    subject = commit['subject']
                    # Remove conventional commit prefix
                    subject = re.sub(r'^(feat|fix|docs|test|refactor|perf|ci|chore|style|build)(\(.+?\))?\s*:\s*', '', subject)
                    
                    section += f"- {subject}"
                    
                    # Add hash for reference
                    short_hash = commit['hash'][:7]
                    section += f" ([{short_hash}](https://github.com/Thaislaine997/AUDITORIA360/commit/{commit['hash']}))"
                    
                    # Add body if significant
                    body = commit.get('body', '').strip()
                    if body and len(body) > 10:
                        # Get first line of body
                        first_line = body.split('\n')[0].strip()
                        if first_line:
                            section += f"\n  - {first_line}"
                    
                    section += "\n"
                
                section += "\n"
        
        return section
    
    def get_current_version(self) -> str:
        """Get current version from git tags or generate one"""
        
        try:
            # Get latest tag
            result = subprocess.check_output(
                ["git", "describe", "--tags", "--abbrev=0"],
                cwd=self.repo_path
            )
            latest_tag = result.decode().strip()
            
            # Parse version and increment patch
            if re.match(r'v?\d+\.\d+\.\d+', latest_tag):
                version_match = re.search(r'(\d+)\.(\d+)\.(\d+)', latest_tag)
                if version_match:
                    major, minor, patch = map(int, version_match.groups())
                    return f"v{major}.{minor}.{patch + 1}"
            
            return "v1.0.1"
            
        except subprocess.CalledProcessError:
            # No tags found
            return "v1.0.0"
    
    def read_existing_changelog(self) -> str:
        """Read existing changelog content"""
        
        if os.path.exists(self.changelog_file):
            with open(self.changelog_file, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return self.create_initial_changelog()
    
    def create_initial_changelog(self) -> str:
        """Create initial changelog structure"""
        
        return """# Changelog

Todas as mudanças importantes neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## Tipos de Mudanças

- 💥 **Breaking Changes**: Mudanças que quebram compatibilidade
- 🔒 **Security**: Correções e melhorias de segurança  
- ✨ **New Features**: Novas funcionalidades
- 🐛 **Bug Fixes**: Correções de bugs
- ⚡ **Performance**: Melhorias de performance
- ♻️ **Refactoring**: Refatorações de código
- 📚 **Documentation**: Mudanças na documentação
- 🧪 **Testing**: Adição ou correção de testes
- 👷 **CI/CD**: Mudanças em CI/CD
- 📦 **Build**: Mudanças no sistema de build
- 🎨 **Style**: Mudanças de formatação/estilo
- 🔧 **Maintenance**: Manutenção geral
- 📝 **Other**: Outras mudanças

"""
    
    def update_changelog(self, version: str = None, commits: List[Dict[str, Any]] = None):
        """Update changelog with new version"""
        
        if version is None:
            version = self.get_current_version()
        
        if commits is None:
            commits = self.get_git_commits_since_tag()
        
        if not commits:
            print("ℹ️  No new commits found since last tag")
            return
        
        # Read existing changelog
        existing_content = self.read_existing_changelog()
        
        # Generate new version section
        new_section = self.generate_version_section(version, commits)
        
        # Find where to insert new section (after the header)
        lines = existing_content.split('\n')
        insert_index = len(lines)
        
        # Look for first version section or end of header
        for i, line in enumerate(lines):
            if line.startswith('## [') or (line.startswith('##') and 'Unreleased' not in line):
                insert_index = i
                break
        
        # Insert new section
        lines.insert(insert_index, new_section)
        
        # Write updated changelog
        updated_content = '\n'.join(lines)
        with open(self.changelog_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ Updated {self.changelog_file} with version {version}")
        print(f"📝 Added {len(commits)} commits to changelog")
    
    def generate_release_notes(self, version: str = None) -> str:
        """Generate release notes for GitHub releases"""
        
        if version is None:
            version = self.get_current_version()
        
        commits = self.get_git_commits_since_tag()
        if not commits:
            return f"## {version}\n\nNo significant changes in this release."
        
        # Generate simplified release notes
        section = self.generate_version_section(version, commits)
        
        # Remove version header for release notes
        lines = section.strip().split('\n')
        if lines and lines[0].startswith('## ['):
            lines = lines[2:]  # Remove version line and empty line
        
        return '\n'.join(lines)

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AUDITORIA360 Changelog Generator')
    parser.add_argument('--version', help='Version to generate changelog for')
    parser.add_argument('--release-notes', action='store_true', help='Generate release notes instead of updating changelog')
    parser.add_argument('--since-tag', help='Generate changelog since specific tag')
    args = parser.parse_args()
    
    print("📋 AUDITORIA360 Changelog Generator")
    print("=" * 40)
    
    generator = ChangelogGenerator()
    
    if args.release_notes:
        # Generate release notes
        notes = generator.generate_release_notes(args.version)
        print("🚀 Release Notes:")
        print(notes)
        
        # Save to file for CI/CD
        with open('release_notes.md', 'w', encoding='utf-8') as f:
            f.write(notes)
        print("✅ Saved release notes to release_notes.md")
        
    else:
        # Update changelog
        commits = generator.get_git_commits_since_tag(args.since_tag) if args.since_tag else None
        generator.update_changelog(args.version, commits)

if __name__ == "__main__":
    main()