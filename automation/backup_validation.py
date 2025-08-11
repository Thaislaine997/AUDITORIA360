#!/usr/bin/env python3
"""
AUDITORIA360 - Enhanced Backup Validation System
Automated backup creation, validation and recovery testing
"""

import os
import json
import subprocess
import psycopg2
import logging
import schedule
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
import hashlib
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BackupValidationSystem:
    """Enhanced backup validation system for AUDITORIA360"""
    
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
        self.backup_dir = os.getenv('BACKUP_DIR', '/tmp/auditoria360_backups')
        self.retention_days = int(os.getenv('BACKUP_RETENTION_DAYS', '30'))
        self.validation_db_name = 'auditoria360_validation_test'
        
        # Create backup directory if it doesn't exist
        os.makedirs(self.backup_dir, exist_ok=True)
        
    def create_database_backup(self) -> Dict[str, Any]:
        """Create database backup with validation"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(self.backup_dir, f'auditoria360_backup_{timestamp}.sql')
        
        try:
            logger.info("Starting database backup...")
            
            # Create backup using pg_dump
            cmd = [
                'pg_dump', 
                '--verbose',
                '--clean',
                '--if-exists',
                '--format=plain',
                '--file', backup_file,
                self.database_url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                raise Exception(f"pg_dump failed: {result.stderr}")
            
            # Calculate file hash for integrity verification
            file_hash = self._calculate_file_hash(backup_file)
            file_size = os.path.getsize(backup_file)
            
            backup_info = {
                'timestamp': timestamp,
                'file_path': backup_file,
                'file_size': file_size,
                'file_hash': file_hash,
                'created_at': datetime.now().isoformat(),
                'status': 'created'
            }
            
            logger.info(f"Database backup created successfully: {backup_file}")
            logger.info(f"Backup size: {file_size / 1024 / 1024:.2f} MB")
            
            return backup_info
            
        except Exception as e:
            logger.error(f"Failed to create database backup: {str(e)}")
            return {
                'timestamp': timestamp,
                'status': 'failed',
                'error': str(e),
                'created_at': datetime.now().isoformat()
            }
    
    def validate_backup(self, backup_info: Dict[str, Any]) -> Dict[str, Any]:
        """Validate backup by attempting restore to test database"""
        if backup_info.get('status') != 'created':
            return {'status': 'skipped', 'reason': 'Backup not created successfully'}
        
        backup_file = backup_info['file_path']
        
        try:
            logger.info("Starting backup validation...")
            
            # Verify file integrity
            current_hash = self._calculate_file_hash(backup_file)
            if current_hash != backup_info['file_hash']:
                raise Exception("Backup file integrity check failed")
            
            # Create test database for validation
            test_db_created = self._create_test_database()
            if not test_db_created:
                raise Exception("Failed to create test database")
            
            # Restore backup to test database
            restore_success = self._restore_backup_to_test_db(backup_file)
            if not restore_success:
                raise Exception("Failed to restore backup to test database")
            
            # Validate restored data
            validation_results = self._validate_restored_data()
            
            # Cleanup test database
            self._cleanup_test_database()
            
            validation_info = {
                'status': 'validated',
                'validated_at': datetime.now().isoformat(),
                'integrity_check': 'passed',
                'restore_test': 'passed',
                'data_validation': validation_results
            }
            
            logger.info("Backup validation completed successfully")
            return validation_info
            
        except Exception as e:
            logger.error(f"Backup validation failed: {str(e)}")
            self._cleanup_test_database()  # Cleanup on error
            
            return {
                'status': 'validation_failed',
                'error': str(e),
                'validated_at': datetime.now().isoformat()
            }
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA256 hash of file"""
        sha256_hash = hashlib.sha256()
        
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        
        return sha256_hash.hexdigest()
    
    def _create_test_database(self) -> bool:
        """Create test database for validation"""
        try:
            # Connect to postgres database to create test db
            conn = psycopg2.connect(self.database_url.replace('/auditoria360', '/postgres'))
            conn.autocommit = True
            cur = conn.cursor()
            
            # Drop if exists and create test database
            cur.execute(f'DROP DATABASE IF EXISTS {self.validation_db_name}')
            cur.execute(f'CREATE DATABASE {self.validation_db_name}')
            
            cur.close()
            conn.close()
            
            logger.info(f"Test database '{self.validation_db_name}' created")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create test database: {str(e)}")
            return False
    
    def _restore_backup_to_test_db(self, backup_file: str) -> bool:
        """Restore backup to test database"""
        try:
            test_db_url = self.database_url.replace('/auditoria360', f'/{self.validation_db_name}')
            
            cmd = [
                'psql',
                '--quiet',
                '--file', backup_file,
                test_db_url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            
            if result.returncode != 0:
                logger.error(f"Restore failed: {result.stderr}")
                return False
            
            logger.info("Backup restored to test database successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to restore backup: {str(e)}")
            return False
    
    def _validate_restored_data(self) -> Dict[str, Any]:
        """Validate restored data integrity"""
        try:
            test_db_url = self.database_url.replace('/auditoria360', f'/{self.validation_db_name}')
            conn = psycopg2.connect(test_db_url)
            cur = conn.cursor()
            
            validation_results = {}
            
            # Check key tables exist
            cur.execute("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
            """)
            tables = [row[0] for row in cur.fetchall()]
            validation_results['tables_count'] = len(tables)
            
            # Check for critical tables
            critical_tables = ['users', 'contabilidades', 'auditorias', 'clientes']
            missing_tables = [table for table in critical_tables if table not in tables]
            validation_results['missing_critical_tables'] = missing_tables
            
            # Count records in key tables
            record_counts = {}
            for table in ['users', 'contabilidades']:
                try:
                    cur.execute(f'SELECT COUNT(*) FROM {table}')
                    record_counts[table] = cur.fetchone()[0]
                except:
                    record_counts[table] = 0
            
            validation_results['record_counts'] = record_counts
            
            cur.close()
            conn.close()
            
            # Determine if validation passed
            validation_passed = (
                len(missing_tables) == 0 and
                validation_results['tables_count'] > 0 and
                sum(record_counts.values()) > 0
            )
            
            validation_results['validation_passed'] = validation_passed
            
            return validation_results
            
        except Exception as e:
            logger.error(f"Data validation failed: {str(e)}")
            return {'validation_passed': False, 'error': str(e)}
    
    def _cleanup_test_database(self) -> bool:
        """Cleanup test database"""
        try:
            conn = psycopg2.connect(self.database_url.replace('/auditoria360', '/postgres'))
            conn.autocommit = True
            cur = conn.cursor()
            
            cur.execute(f'DROP DATABASE IF EXISTS {self.validation_db_name}')
            
            cur.close()
            conn.close()
            
            logger.info(f"Test database '{self.validation_db_name}' cleaned up")
            return True
            
        except Exception as e:
            logger.warning(f"Failed to cleanup test database: {str(e)}")
            return False
    
    def backup_application_files(self) -> Dict[str, Any]:
        """Backup critical application files"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(self.backup_dir, f'auditoria360_files_{timestamp}.tar.gz')
        
        try:
            logger.info("Starting application files backup...")
            
            # Define critical directories and files to backup
            backup_paths = [
                'api/',
                'src/',
                'automation/',
                'docs/',
                '.env.example',
                'requirements.txt',
                'Makefile'
            ]
            
            # Create tar.gz backup
            cmd = ['tar', '-czf', backup_file] + backup_paths
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode != 0:
                raise Exception(f"File backup failed: {result.stderr}")
            
            file_size = os.path.getsize(backup_file)
            file_hash = self._calculate_file_hash(backup_file)
            
            backup_info = {
                'timestamp': timestamp,
                'file_path': backup_file,
                'file_size': file_size,
                'file_hash': file_hash,
                'created_at': datetime.now().isoformat(),
                'status': 'created',
                'type': 'application_files'
            }
            
            logger.info(f"Application files backup created: {backup_file}")
            logger.info(f"Backup size: {file_size / 1024 / 1024:.2f} MB")
            
            return backup_info
            
        except Exception as e:
            logger.error(f"Failed to backup application files: {str(e)}")
            return {
                'timestamp': timestamp,
                'status': 'failed',
                'error': str(e),
                'type': 'application_files',
                'created_at': datetime.now().isoformat()
            }
    
    def cleanup_old_backups(self):
        """Remove backups older than retention period"""
        try:
            cutoff_date = datetime.now() - timedelta(days=self.retention_days)
            removed_count = 0
            
            for filename in os.listdir(self.backup_dir):
                file_path = os.path.join(self.backup_dir, filename)
                
                if os.path.isfile(file_path):
                    file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                    
                    if file_mtime < cutoff_date:
                        os.remove(file_path)
                        removed_count += 1
                        logger.info(f"Removed old backup: {filename}")
            
            logger.info(f"Cleanup completed: {removed_count} old backups removed")
            
        except Exception as e:
            logger.error(f"Failed to cleanup old backups: {str(e)}")
    
    def generate_backup_report(self, db_backup_info: Dict[str, Any], 
                             db_validation_info: Dict[str, Any],
                             files_backup_info: Dict[str, Any]) -> str:
        """Generate backup report"""
        
        report = f"""# Backup Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Database Backup
- **Status**: {db_backup_info.get('status', 'unknown')}
- **Timestamp**: {db_backup_info.get('timestamp', 'unknown')}
- **File Size**: {db_backup_info.get('file_size', 0) / 1024 / 1024:.2f} MB
- **File Path**: {db_backup_info.get('file_path', 'unknown')}

## Database Validation
- **Status**: {db_validation_info.get('status', 'unknown')}
- **Integrity Check**: {db_validation_info.get('integrity_check', 'unknown')}
- **Restore Test**: {db_validation_info.get('restore_test', 'unknown')}

## Application Files Backup
- **Status**: {files_backup_info.get('status', 'unknown')}
- **Timestamp**: {files_backup_info.get('timestamp', 'unknown')}
- **File Size**: {files_backup_info.get('file_size', 0) / 1024 / 1024:.2f} MB

## Summary
- **Overall Status**: {'✅ SUCCESS' if all(info.get('status') in ['created', 'validated'] for info in [db_backup_info, files_backup_info]) else '❌ FAILURE'}
- **Next Scheduled Backup**: {(datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')}

---
*Report generated by AUDITORIA360 Backup Validation System*
"""
        
        return report
    
    def run_full_backup_cycle(self) -> Dict[str, Any]:
        """Run complete backup and validation cycle"""
        logger.info("Starting full backup cycle...")
        
        # Database backup
        db_backup_info = self.create_database_backup()
        
        # Database validation
        db_validation_info = self.validate_backup(db_backup_info)
        
        # Application files backup
        files_backup_info = self.backup_application_files()
        
        # Cleanup old backups
        self.cleanup_old_backups()
        
        # Generate report
        report = self.generate_backup_report(db_backup_info, db_validation_info, files_backup_info)
        
        # Save report
        report_file = os.path.join(self.backup_dir, f'backup_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md')
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"Backup cycle completed. Report saved: {report_file}")
        
        return {
            'database_backup': db_backup_info,
            'database_validation': db_validation_info,
            'files_backup': files_backup_info,
            'report_file': report_file
        }

def main():
    """Main function for backup validation system"""
    logger.info("Starting AUDITORIA360 backup validation system...")
    
    backup_system = BackupValidationSystem()
    
    # Schedule daily backups at 2 AM
    schedule.every().day.at("02:00").do(backup_system.run_full_backup_cycle)
    
    # For immediate execution during development/testing
    if os.getenv('RUN_IMMEDIATE', 'false').lower() == 'true':
        logger.info("Running immediate backup cycle...")
        results = backup_system.run_full_backup_cycle()
        
        # Print summary
        db_status = results['database_backup'].get('status')
        validation_status = results['database_validation'].get('status')
        files_status = results['files_backup'].get('status')
        
        logger.info(f"Backup cycle results:")
        logger.info(f"- Database backup: {db_status}")
        logger.info(f"- Database validation: {validation_status}")
        logger.info(f"- Files backup: {files_status}")
        
        return 0 if all(status in ['created', 'validated'] for status in [db_status, files_status]) else 1
    
    # Keep the service running
    logger.info("Backup validation system is running. Daily backups scheduled for 2:00 AM.")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    exit(main())