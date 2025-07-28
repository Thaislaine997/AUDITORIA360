# Auditoria Automática dos Dados GCP

import os
import json
def audit_gcp_configs():
    report = []
    configs_dir = [
        'configs'
    ]
    keys = [
        'project_id', 'gcp_project_id', 'control_bq_dataset_id', 'processed_bq_dataset_id',
        'raw_bq_dataset_id', 'log_bq_dataset_id', 'log_bq_table_id', 'bucket', 'region', 'organization'
    ]
    for folder in configs_dir:
        for fname in os.listdir(folder):
            if fname.endswith('.json'):
                fpath = os.path.join(folder, fname)
                try:
                    with open(fpath) as f:
                        data = json.load(f)
                    found = {k: data.get(k) for k in keys if k in data}
                    report.append({'file': fpath, 'fields': found})
                except Exception as e:
                    report.append({'file': fpath, 'error': str(e)})
    with open('configs/auditoria_gcp_report.json', 'w') as out:
        json.dump(report, out, indent=2)
    print('Relatório de auditoria gerado em configs/auditoria_gcp_report.json')

if __name__ == '__main__':
    audit_gcp_configs()
